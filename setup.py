
from distutils.core import setup
import py2exe

setup(

    name = "XSTAF",
    packages = ["XSTAF", "XSTAF.core", "XSTAF.ui", "XSTAF.tools", "XSTAF.tools.report_generator", "XSTAF.tools.report_generator.html"],
    package_data = {"XSTAF.ui": ["icons/*"], 
                    "XSTAF.tools.report_generator.html": ["templates/*"]},
    version = "0.0.1",
    description = "distribute auto execution framework basing on STAF",
    author = "xcgspring",
    author_email = "xcgspring@163.com",
    license = "Apache Licence Version 2.0",
    url = "https://github.com/xcgspring/XSTAF",
    download_url = "",
    keywords = ["XSTAF", "auto"],
    classifiers = [
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
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
    windows=['XSTAF/main.py'],
    zipfile="Libs/libs.zip",
    options={"py2exe": {"skip_archive": True}},
)
