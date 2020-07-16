import codecs
import os.path
import setuptools

def read(rel_path):
    here = os.path.abspath(os.path.dirname(__file__))
    with codecs.open(os.path.join(here, rel_path), 'r') as fp:
        return fp.read()

def get_version(rel_path):
    for line in read(rel_path).splitlines():
        if line.startswith('__version__'):
            delim = '"' if '"' in line else "'"
            return line.split(delim)[1]
    else:
        raise RuntimeError("Unable to find version string.")


pkg_name = "neuropixels_data_sep_2020"

setuptools.setup(
    name=pkg_name,
    version=get_version(pkg_name + "/__init__.py"),
    author="Jeremy Magland",
    author_email="jmagland@flatironinstitute.org",
    description="Example neuropixels datasets for purposes of developing spike sorting algorithms",
    url="https://github.com/flatironinstitute/neuropixels-data-sep-2020",
    packages=setuptools.find_packages(),
    include_package_data=True,
    scripts=[
    ],
    install_requires=[
        "kachery_p2p>=0.2.0"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ]
)
