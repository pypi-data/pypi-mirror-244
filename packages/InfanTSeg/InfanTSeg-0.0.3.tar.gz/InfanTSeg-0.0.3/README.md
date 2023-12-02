# Repo for Infant Brain Tissue Segmentation Tools
```shell
Copyright IDEA Lab, School of Biomedical Engineering, ShanghaiTech University.

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the “Software”), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

Repo for Automatic Brain Extraction Tools (AutoBET)

Contact: JiamengLiu.PRC@gmail.com
```

## Install
`pip install InfanTSeg`

### GPU
Currently, our infant brain tissue segmentation tools works on GPU with at least 14G GPU memories. We are working on reduce the GPU capacity and will release it in the next version.

Due to the size limitation of PYPI we cannot include our model with the released InfanTSeg, please feel free to contact us to obtain our pretrained model (JiamengLiu.PRC@gmail.com)

## Usase

```python
from InfanTSeg.InfanTSeg import Infant_Seg, _model_init

source_img_path = '/path/to/your/T1/data'
target_img_path = '/path/to/your/skull/stripped/data'
target_seg_path = '/path/to/your/brain/mask'

model_path = '/path/to/pretrained/model'

model = _model_init(model_path)
Infant_Seg(source_img_path, target_seg_path, model)
```