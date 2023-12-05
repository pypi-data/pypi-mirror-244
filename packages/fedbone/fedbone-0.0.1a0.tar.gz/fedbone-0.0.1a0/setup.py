from setuptools import find_packages, setup
import os
import fedbone

base_dir = os.path.dirname(os.path.abspath(__file__))
__version__ = fedbone.__version__


setup(
    name="fedbone",
    version=__version__,
    keywords=["configuration", "config"],
    description="FedBone: A PyTorch-based Federated Learning Framework",
    long_description=open(os.path.join(base_dir, "README.md")).read(),
    long_description_content_type="text/markdown",
    author="Bingjie Yan",
    author_email="bj.yan.pa@qq.com",
    url="http://github.com/beiyuouo/FedLLM",
    license="Apache-2.0 License",
    packages=find_packages(include=["fedbone", "fedbone.*", "LICENSE", "README.md"]),
    install_requires=["ezkfg"],
    python_requires=">=3.6",
)
