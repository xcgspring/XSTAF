
from setuptools import setup, find_packages

import py2exe
import os
import glob

def find_data_files(source,target,patterns):
    """Locates the specified data-files and returns the matches
    in a data_files compatible format.

    source is the root of the source data tree.
        Use '' or '.' for current directory.
    target is the root of the target data tree.
        Use '' or '.' for the distribution directory.
    patterns is a sequence of glob-patterns for the
        files you want to copy.
    """
    if glob.has_magic(source) or glob.has_magic(target):
        raise ValueError("Magic not allowed in src, target")
    ret = {}
    for pattern in patterns:
        pattern = os.path.join(source,pattern)
        for filename in glob.glob(pattern):
            if os.path.isfile(filename):
                targetpath = os.path.join(target,os.path.relpath(filename,source))
                path = os.path.dirname(targetpath)
                ret.setdefault(path,[]).append(filename)
    return sorted(ret.items())

setup(

    name = "XSTAF",
    packages = find_packages(),
    package_data = {"XSTAF.ui": ["icons/*"], 
                    "XSTAF.tools.report_generator.ui" : ["icons/*"],
                    "XSTAF.tools.report_generator.html": ["templates/*"],
                    "XSTAF.tools.testsuite_generator.ui" : ["icons/*"],
                    "XSTAF.tools.workspace_merger.ui" : ["icons/*"],
                    "XSTAF.tools.workspace_spliter.ui" : ["icons/*"],},
    version = "0.1.0",
    description = "distribute auto execution framework basing on STAF",
    author = "xcgspring",
    author_email = "xcgspring@163.com",
    license = "Apache Licence Version 2.0",
    url = "https://github.com/xcgspring/XSTAF",
    download_url = "",
    keywords = ["XSTAF", "auto", "distribute", "execution framework"],
    classifiers = [
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Development Status :: 2 - Pre-Alpha",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Software Development :: Quality Assurance",
        "Topic :: Software Development :: Testing",
        ],
    long_description = ''' ''',
    
    data_files = find_data_files("XSTAF", "Libs/XSTAF",["tools/report_generator/html/templates/*"]),
    windows=['XSTAF/main.py'],
    zipfile="Libs/libs.zip",
    options={"py2exe": {"packages": ['jinja2', 'XSTAF.tools'],
                        "skip_archive": True, 
                        "includes": ["sip"],}},
)
