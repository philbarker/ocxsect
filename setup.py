from setuptools import setup

setup(
    name="ocxsect",
    version="0.1",
    py_modules=["ocxsect"],
    install_requires=["markdown>=3.0"],
    author="Phil Barker",
    author_email="phil.barker@pjjk.co.uk",
    url="https://github.com/philbarker/ocxmd",
    description="A python markdown extension that allows you to add semantic HTML5 sectioning elements into the generated html.",
    license="Apache2",
)
