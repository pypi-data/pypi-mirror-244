import os
import sys
import ants
import torch
import argparse
import numpy as np
import pandas as pd
import torch.nn as nn
import SimpleITK as sitk
from tqdm import tqdm
from IPython import embed
from skimage import measure
from itertools import product
import torch.nn.functional as F
from scipy import ndimage

from MIDP.utils import _ants_img_info, _seg_to_label, _select_top_k_region
from MIDP.utils import _normalize_to_standard, calculate_patch_index, _ants_registration

dir_test = os.path.split(os.path.split(os.path.realpath(__file__))[0])[0]

atlas_img_path = os.path.join(dir_test, 'data', 'MNI152_T1.nii.gz')
atlas_seg_path = os.path.join(dir_test, 'data', 'MNI152_mask.nii.gz')

device = 'cuda'
crop_size = (160, 160, 160)
overlap_ratio = 0.75
num_classes = 1

class IBN(nn.Module):
    r"""Instance-Batch Normalization layer from
    `"Two at Once: Enhancing Learning and Generalization Capacities via IBN-Net"
    <https://arxiv.org/pdf/1807.09441.pdf>`
    Args:
        planes (int): Number of channels for the input tensor
        ratio (float): Ratio of instance normalization in the IBN layer
    """
    def __init__(self, planes, ratio=0.5):
        super(IBN, self).__init__()
        self.half = int(planes * ratio)
        self.IN = nn.InstanceNorm3d(self.half, affine=True)
        self.BN = nn.BatchNorm3d(planes - self.half)

    def forward(self, x):
        split = torch.split(x, self.half, 1)
        out1 = self.IN(split[0].contiguous())
        out2 = self.BN(split[1].contiguous())
        out = torch.cat((out1, out2), 1)
        return out


class BasicBlock(nn.Module):
    # TODO: basic convolutional block, conv -> batchnorm -> activate
    def __init__(self, in_channels, out_channels, kernel_size, padding, activate=True, norm='IBNa', act='LeakyReLU'):
        super(BasicBlock, self).__init__()
        self.conv = nn.Conv3d(in_channels=in_channels, out_channels=out_channels, kernel_size=kernel_size,
                              padding=padding, bias=True)

        if norm == 'IBNa':
            self.bn = IBN(out_channels)
        else:
            self.bn = nn.BatchNorm3d(out_channels)

        if act == 'ReLU':
            self.activate = nn.ReLU(inplace=True)
        elif act == 'LeakyReLU':
            self.activate = nn.LeakyReLU(0.2)

        self.en_activate = activate

    def forward(self, x):
        if self.en_activate:
            return self.activate(self.bn(self.conv(x)))
        else:
            return self.bn(self.conv(x))


class ResidualBlock(nn.Module):
    # TODO: basic residual block established by BasicBlock
    def __init__(self, in_channels, out_channels, kernel_size, padding, nums, norm='IBNa',act='LeakyReLU'):
        '''
        TODO: initial parameters for basic residual network
        :param in_channels: input channel numbers
        :param out_channels: output channel numbers
        :param kernel_size: convoluition kernel size
        :param padding: padding size
        :param nums: number of basic convolutional layer
        '''
        super(ResidualBlock, self).__init__()

        layers = list()

        self.norm = norm

        for _ in range(nums):
            if _ != nums - 1:
                layers.append(BasicBlock(in_channels, out_channels, kernel_size, padding, True, norm, act))
            else:
                layers.append(BasicBlock(in_channels, out_channels, kernel_size, padding, False, None, act))

        self.do = nn.Sequential(*layers)

        if act == 'ReLU':
            self.activate = nn.ReLU(inplace=True)
        elif act == 'LeakyReLU':
            self.activate = nn.LeakyReLU(0.2)

        self.IN = nn.InstanceNorm3d(out_channels, affine=True) if norm == 'IBNb' else None

    def forward(self, x):
        output = self.do(x)
        if self.IN is not None:
            return self.activate(self.IN(output + x))
        else:
            return self.activate(output + x)


class InputTransition(nn.Module):
    # TODO: input transition convert image to feature space
    def __init__(self, in_channels, out_channels, norm=None):
        '''
        TODO: initial parameter for input transition <input size equals to output feature size>
        :param in_channels: input image channels
        :param out_channels: output feature channles
        '''
        super(InputTransition, self).__init__()
        self.norm = norm
        self.trans = BasicBlock(in_channels, out_channels, 3, 1, True, norm, 'LeakyReLU')

    def forward(self, x):
        out = self.trans(x)
        return out


class OutputTransition(nn.Module):
    # TODO: feature map convert to predict results
    def __init__(self, in_channels, out_channels, act='sigmoid'):
        '''
        TODO: initial for output transition
        :param in_channels: input feature channels
        :param out_channels: output results channels
        :param act: final activate layer sigmoid or softmax
        '''
        super(OutputTransition, self).__init__()
        assert act == 'sigmoid' or act =='softmax', \
            'final activate layer should be sigmoid or softmax, current activate is :{}'.format(act)
        self.conv1 = nn.Conv3d(in_channels=in_channels, out_channels=out_channels, kernel_size=3, padding=1)
        self.bn1 = nn.BatchNorm3d(out_channels)
        self.activate1 = nn.ReLU(inplace=True)
        self.conv2 = nn.Conv3d(in_channels=out_channels, out_channels=out_channels, kernel_size=1)

        self.softmax = nn.Softmax(dim=1)
        self.sigmoid = nn.Sigmoid()

        self.act = act

    def forward(self, x):
        out = self.activate1(self.bn1(self.conv1(x)))
        out = self.conv2(out)
        if self.act == 'sigmoid':
            return self.sigmoid(out)
        elif self.act == 'softmax':
            return self.softmax(out)


class DownTransition(nn.Module):
    # TODO: fundamental down-sample layer <inchannel -> 2*inchannel>
    def __init__(self, in_channels, nums, norm=None, act='LeakyReLU'):
        '''
        TODO: intial for down-sample
        :param in_channels: inpuit channels
        :param nums: number of reisidual block
        '''
        super(DownTransition, self).__init__()

        out_channels = in_channels * 2
        self.down = nn.Conv3d(in_channels, out_channels, kernel_size=2, stride=2, groups=1)
        self.bn1 = nn.BatchNorm3d(out_channels)
        self.activate1 = nn.ReLU(inplace=True)
        self.residual = ResidualBlock(out_channels, out_channels, 3, 1, nums, norm, act)

    def forward(self, x):
        out = self.activate1(self.bn1(self.down(x)))
        out = self.residual(out)
        return out


class UpTransition(nn.Module):
    # TODO: fundamental up-sample layer (inchannels -> inchannels/2)
    def __init__(self, in_channels, out_channels, nums):
        '''
        TODO: initial for up-sample
        :param in_channels: input channels
        :param out_channels: output channels
        :param nums: number of residual block
        '''
        super(UpTransition, self).__init__()
        self.up = nn.Upsample(scale_factor=2, mode='trilinear', align_corners=True)
        self.conv1 = nn.Conv3d(in_channels, out_channels//2, kernel_size=3, padding=1)
        self.bn = nn.BatchNorm3d(out_channels//2)
        self.activate = nn.ReLU(inplace=True)
        self.residual = ResidualBlock(out_channels, out_channels, 3, 1, nums)

    def forward(self, x, skip_x):
        out = self.up(x)
        out = self.activate(self.bn(self.conv1(out)))
        out = torch.cat((out,skip_x), 1)
        out = self.residual(out)

        return out


class SegNetMultiScale(nn.Module):
    # TODO: fundamental segmentation framework
    # Multi-Scale strategy using different crop size and normalize to same size
    def __init__(self, in_channels, out_channels, norm=None):
        super().__init__()
        self.in_tr_s = InputTransition(in_channels, 16, norm=None)
        self.in_tr_b = InputTransition(in_channels, 16, norm=None)

        self.down_32_s = DownTransition(16, 1, norm=norm)
        self.down_32_b = DownTransition(16, 1, norm=norm)
        self.fusion_32 = BasicBlock(in_channels=64, out_channels=32, kernel_size=3, padding=1)

        self.down_64_s = DownTransition(32, 1, norm=norm)
        self.down_64_b = DownTransition(32, 1, norm=norm)
        self.fusion_64 = BasicBlock(in_channels=128, out_channels=64, kernel_size=3, padding=1)

        self.down_128_s = DownTransition(64, 2)
        self.down_128_b = DownTransition(64, 2)
        self.fusion_128 = BasicBlock(in_channels=256, out_channels=128, kernel_size=3, padding=1)

        self.down_256_s = DownTransition(128, 2)
        self.down_256_b = DownTransition(128, 2)
        self.fusion_256 = BasicBlock(in_channels=512, out_channels=256, kernel_size=3, padding=1)

        self.up_256_s = UpTransition(256, 256, 2)
        self.up_256_b = UpTransition(256, 256, 2)
        self.fusion_up_256 = BasicBlock(in_channels=512, out_channels=256, kernel_size=3, padding=1)

        self.up_128_s = UpTransition(256, 128, 2)
        self.up_128_b = UpTransition(256, 128, 2)
        self.fusion_up_128 = BasicBlock(in_channels=256, out_channels=128, kernel_size=3, padding=1)

        self.up_64_s = UpTransition(128, 64, 1)
        self.up_64_b = UpTransition(128, 64, 1)
        self.fusion_up_64 = BasicBlock(in_channels=128, out_channels=64, kernel_size=3, padding=1)

        self.up_32_s = UpTransition(64, 32, 1)
        self.up_32_b = UpTransition(64, 32, 1)
        self.fusion_up_32 = BasicBlock(in_channels=64, out_channels=32, kernel_size=3, padding=1)

        self.out_tr_s = OutputTransition(32, out_channels, 'softmax')
        self.out_tr_b = OutputTransition(32, out_channels, 'softmax')

    def forward(self, x):
        B, C, W, H, D = x.shape
        B_s, C_s, W_s, H_s, D_s = B, C, W - 32, H - 32, D - 32

        x_s = x[:, :, 16:W - 16, 16:H - 16, 16:D - 16]
        x_b = F.interpolate(x, size=[W_s, H_s, D_s], mode='trilinear')

        out_16_s = self.in_tr_s(x_s)
        out_16_b = self.in_tr_b(x_b)

        out_32_s = self.down_32_s(out_16_s)
        out_32_b = self.down_32_b(out_16_b)

        out_32_s = torch.cat([out_32_s, F.interpolate(out_32_b[:, :, 7:57, 7:57, 7:57], size=[64, 64, 64], mode='trilinear')], dim=1)
        out_32_s = self.fusion_32(out_32_s)

        out_64_s = self.down_64_s(out_32_s)
        out_64_b = self.down_64_b(out_32_b)

        out_64_s = torch.cat([out_64_s, F.interpolate(out_64_b[:, :, 4:28, 4:28, 4:28], size=[32, 32, 32], mode='trilinear')], dim=1)
        out_64_s = self.fusion_64(out_64_s)

        out_128_s = self.down_128_s(out_64_s)
        out_128_b = self.down_128_b(out_64_b)

        out_128_s = torch.cat([out_128_s, F.interpolate(out_128_b[:, :, 2:14, 2:14, 2:14], size=[16, 16, 16], mode='trilinear')], dim=1)
        out_128_s = self.fusion_128(out_128_s)

        out_256_s = self.down_256_s(out_128_s)
        out_256_b = self.down_256_b(out_128_b)

        out_256_s = torch.cat([out_256_s, F.interpolate(out_256_b[:, :, 1:7, 1:7, 1:7], size=[8, 8, 8], mode='trilinear')], dim=1)
        out_256_s = self.fusion_256(out_256_s)

        out_s = self.up_256_s(out_256_s, out_128_s)
        out_b = self.up_256_b(out_256_b, out_128_b)

        out_s = torch.cat([out_s, F.interpolate(out_b[:, :, 2:14, 2:14, 2:14], size=[16, 16, 16], mode='trilinear')], dim=1)
        out_s = self.fusion_up_256(out_s)

        out_s = self.up_128_s(out_s, out_64_s)
        out_b = self.up_128_b(out_b, out_64_b)

        out_s = torch.cat([out_s, F.interpolate(out_b[:, :, 4:28, 4:28, 4:28], size=[32, 32, 32], mode='trilinear')], dim=1)
        out_s = self.fusion_up_128(out_s)

        out_s = self.up_64_s(out_s, out_32_s)
        out_b = self.up_64_b(out_b, out_32_b)

        out_s = torch.cat([out_s, F.interpolate(out_b[:, :, 7:57, 7:57, 7:57], size=[64, 64, 64], mode='trilinear')], dim=1)
        out_s = self.fusion_up_64(out_s)

        out_s = self.up_32_s(out_s, out_16_s)
        out_b = self.up_32_b(out_b, out_16_b)

        out_s = torch.cat([out_s, F.interpolate(out_b[:, :, 13:115, 13:115, 13:115], size=[128, 128, 128], mode='trilinear')], dim=1)
        out_s = self.fusion_up_32(out_s)

        out_s = self.out_tr_s(out_s)
        out_b = self.out_tr_b(out_b)

        return out_s, out_b


def _model_init(model_path):

    # initialize model and load pretrained model parameters
    model = SegNetMultiScale(1, 2, norm='IBNa')
    model = torch.nn.DataParallel(model)
    model = model.to(device)
    model.load_state_dict(torch.load(model_path))
    model.eval()
    return model


def _get_pred(model, img):
    if len(img.shape) == 4:
        img = torch.unsqueeze(img, dim=0)
    m = nn.ConstantPad3d(16, 0)
    B, C, W, H, D = img.shape
    pos = calculate_patch_index((W, H, D), crop_size, overlap_ratio)

    pred_rec_s = torch.zeros((num_classes+1, W, H, D))
    freq_rec = torch.zeros((num_classes+1, W, H, D))

    for start_pos in pos:
        patch = img[:,:,start_pos[0]:start_pos[0]+crop_size[0], start_pos[1]:start_pos[1]+crop_size[1], start_pos[2]:start_pos[2]+crop_size[2]]

        model_out_s, model_out_b = model(patch)
        model_out_s = m(model_out_s)
        model_out_s = model_out_s.cpu().detach()

        pred_rec_s[:, start_pos[0]:start_pos[0]+crop_size[0], start_pos[1]:start_pos[1]+crop_size[1], start_pos[2]:start_pos[2]+crop_size[2]] += model_out_s[0,:,:,:,:]
        freq_rec[:, start_pos[0]:start_pos[0]+crop_size[0], start_pos[1]:start_pos[1]+crop_size[1], start_pos[2]:start_pos[2]+crop_size[2]] += 1

    pred_rec_s = pred_rec_s / freq_rec
    pred_rec_s = pred_rec_s[:, 16:W-16, 16:H-16, 16:D-16]

    return pred_rec_s


def get_pred(model, img_path):
    origin, spacing, direction, img = _ants_img_info(img_path)
    img = _normalize_to_standard(img)
    img = np.pad(img, ((16, 16), (16, 16), (16, 16)), 'constant')
    img = torch.from_numpy(img).type(torch.float32)
    img = img.to(device)
    img = img.unsqueeze(0)

    pred = _get_pred(model, img)
    pred = pred.argmax(0)
    pred = pred.numpy().astype(np.float32)

    pred = _select_top_k_region(pred, 1)
    pred = pred.astype(np.float32)

    ants_img_pred_seg = ants.from_numpy(pred, origin, spacing, direction)

    return ants_img_pred_seg


def Auto_BET(source_img_path, target_img_path, target_seg_path, model=None):
    print('Start process:')
    folder, file_name = os.path.split(source_img_path)
    file_name = file_name.split('.')[0]
    print('Step 1')
    persudo_brain_path = os.path.join(folder, file_name+'_persudo_brain.nii.gz')
    warped_mni_img, warped_mni_mask = _ants_registration(moving_img_path=atlas_img_path,
                                                         moving_seg_path=atlas_seg_path,
                                                         fixed_img_path=source_img_path,
                                                         type_of_transform='SyN')
    print('Step 2')
    origin, spacing, direction, img = _ants_img_info(source_img_path)
    persudo_mask = warped_mni_mask.numpy()
    persudo_mask = ndimage.binary_dilation(persudo_mask, iterations=5)
    persudo_mask = persudo_mask.astype(np.float32)

    persudo_brain = img * persudo_mask
    persudo_brain = ants.from_numpy(persudo_brain, origin, spacing, direction)
    ants.image_write(persudo_brain, persudo_brain_path)

    print('Step 3')

    pred = get_pred(model, persudo_brain_path)
    pred = pred.numpy()
    origin, spacing, direction, img = _ants_img_info(source_img_path)

    pred_brain = img * pred
    pred_brain = ants.from_numpy(pred_brain, origin, spacing, direction)
    ants.image_write(pred_brain, target_img_path)

    pred = ants.from_numpy(pred, origin, spacing, direction)
    ants.image_write(pred, target_seg_path)
    os.system('rm {}'.format(persudo_brain_path))
    print('Done')