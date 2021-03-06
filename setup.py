
from setuptools import setup, find_packages
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
)
