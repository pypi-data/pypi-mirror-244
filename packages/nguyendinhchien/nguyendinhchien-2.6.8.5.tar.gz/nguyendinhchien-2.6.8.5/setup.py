from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))
 
with codecs.open(os.path.join(here, "README.md"),encoding="utf-8") as fh:
    ChienPc_description = "\n" + fh.read()
     
DESCRIPTION = "Python By ChienPc"

setup(
    name="nguyendinhchien",
    version="2.6.8.5",
    author="Nguyen Đinh Chien",
    author_email="<dinhchien2k7@gmail.com>",
    url="https://nguyendinhchien.io.vn",
    description=DESCRIPTION,
    ChienPC_content_type ="text/markdown",
    packages=find_packages(),
    install_requires = ["PySimpleGUI", "yagmail","pandas","openpyxl","requests"],
    keywords=["ChienPC","Python","Excel","Python Excel"],
    classifiers=[
        "Intended Audience :: Developers",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows"
    ] 
)
