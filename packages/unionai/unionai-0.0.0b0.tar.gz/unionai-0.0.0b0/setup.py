from setuptools import find_packages, setup  # noqa

from setuptools import setup

plugin_requires = [
    "googleapis-common-protos>=1.57",
    "grpcio",
    "grpcio-status",
    "importlib-metadata",
    "fsspec>=2023.3.0,<=2023.9.2",
    "aiofiles>=23.2.1",
]

__version__ = "0.0.0b0"

setup(
    name="unionai",
    version=__version__,
    author="unionai",
    author_email="oss@union.ai",
    description="Adds Union Cloud specific functionality to Flytekit",
    url="https://github.com/unionai-oss/unionai",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    packages=find_packages(include=[f"unionai*"]),
    include_package_data=True,
    install_requires=plugin_requires,
    extras_require={},
    license="apache2",
    python_requires=">=3.8",
    entry_points={
        'fsspec.specs': [
            'unionmeta=unionai.unionmetafs:AsyncUnionMetaFS',
            'union=unionai.unionfs:AsyncUnionFS',
        ],
    },
    classifiers=[
        "Intended Audience :: Science/Research",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Topic :: Scientific/Engineering",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Software Development",
        "Topic :: Software Development :: Libraries",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
)
