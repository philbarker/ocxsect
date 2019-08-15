from setuptools import setup

setup(
    name="ocxsect",
    version="0.1.4",
    py_modules=["ocxsect"],
    install_requires=["setuptools>=40.6"],
    author="Phil Barker",
    author_email="phil.barker@pjjk.co.uk",
    url="https://github.com/philbarker/ocxmd",
    description="A python markdown extension that allows you to add semantic HTML5 sectioning elements into the generated html.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    license="Apache2",
    classifiers=[
        "Development Status :: 4 - Beta",
        "License :: OSI Approved :: Apache Software License",
        "Topic :: Text Processing :: Markup :: HTML",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
    ],
)
