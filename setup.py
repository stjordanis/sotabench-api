from setuptools import setup

PACKAGE_NAME = "sotabench"
LICENSE = "Apache 2.0"
AUTHOR = "Atlas ML"
EMAIL = "ross@atlasml.io"
URL = "https://www.atlas.ml"
DESCRIPTION = "Benchmarking open source deep learning models"


setup(
    name=PACKAGE_NAME,
    maintainer=AUTHOR,
    version='0.001',
    packages=[PACKAGE_NAME,
              'sotabench.datasets',
              'sotabench.vision',
              'sotabench.vision.image_classification'],
    include_package_data=True,
    license=LICENSE,
    description=DESCRIPTION,
    long_description=DESCRIPTION,
    url=URL,
    install_requires=['torch', 'torchvision'],
)