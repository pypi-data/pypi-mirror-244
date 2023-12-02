import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="InfanTSeg",
    version="0.0.3",
    author="Jiameng Liu",
    author_email="JiamengLiu.PRC@gmail.com",
    description="Infant Brain Tissue Segmentation Tools",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/SaberPRC/Auto-BET",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        # exapmle
        'antspyx',
        'numpy',
        'pandas',
        'torch',
        'SimpleITK',
        'MIDP',
        'tqdm',
        # 'Django >= 1.11, != 1.11.1, <= 2',
    ],
    include_package_data=True,
)