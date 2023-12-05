from setuptools import find_packages, setup
import os
import fedfair

base_dir = os.path.dirname(os.path.abspath(__file__))
__version__ = fedfair.__version__


setup(
    name="fedfair",
    version=__version__,
    keywords=["configuration", "config"],
    description="FedFair: A Fairness-aware Federated Learning Framework",
    long_description=open(os.path.join(base_dir, "README.md")).read(),
    long_description_content_type="text/markdown",
    author="Bingjie Yan",
    author_email="bj.yan.pa@qq.com",
    url="http://github.com/beiyuouo/fedfair",
    license="Apache-2.0 License",
    packages=find_packages(include=["fedfair", "fedfair.*", "LICENSE", "README.md"]),
    install_requires=["ezkfg"],
    python_requires=">=3.6",
)
