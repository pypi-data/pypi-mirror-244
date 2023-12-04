from setuptools import find_packages, setup
import os
import fedllm

base_dir = os.path.dirname(os.path.abspath(__file__))
__version__ = "0.0.1a0"


setup(
    name="fedllm",
    version=__version__,
    keywords=["configuration", "config"],
    description="FedLLM: A Federated Learning Library for Large Language Models.",
    long_description=open(os.path.join(base_dir, "README.md")).read(),
    long_description_content_type="text/markdown",
    author="Bingjie Yan",
    author_email="bj.yan.pa@qq.com",
    url="http://github.com/beiyuouo/FedLLM",
    license="Apache-2.0 License",
    packages=find_packages(include=["fedllm", "fedllm.*", "LICENSE", "README.md"]),
    install_requires=["torch>=1.6.0"],
    python_requires=">=3.6",
)
