
from distutils.core import setup

setup(

    name = "XSTAF",
    packages = ["XSTAF", "XSTAF.core", "XSTAF.ui", "XSTAF.tools", "XSTAF.tools.report_generator"],
    package_data = {"XSTAF.ui": "icons/*"},
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
    long_description = ''' '''
    
)
