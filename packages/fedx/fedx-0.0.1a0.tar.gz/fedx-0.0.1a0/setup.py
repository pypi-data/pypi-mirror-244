from setuptools import find_packages, setup
import os
import fedx

base_dir = os.path.dirname(os.path.abspath(__file__))
__version__ = fedx.__version__


setup(
    name="fedx",
    version=__version__,
    keywords=["configuration", "config"],
    description="FedX: A federated learning framework based on PyTorch",
    long_description=open(os.path.join(base_dir, "README.md")).read(),
    long_description_content_type="text/markdown",
    author="Bingjie Yan",
    author_email="bj.yan.pa@qq.com",
    url="http://github.com/beiyuouo/fedx",
    license="Apache-2.0 License",
    packages=find_packages(include=["fedx", "fedx.*", "LICENSE", "README.md"]),
    install_requires=["ezkfg"],
    python_requires=">=3.6",
)
