[![Build Status](https://travis-ci.org/philbarker/ocxsect.svg?branch=master)](https://travis-ci.org/philbarker/ocxsect)
[![Coverage](https://codecov.io/gh/philbarker/ocxsect/branch/master/graph/badge.svg)](https://codecov.io/gh/philbarker/ocxsect/)

# Sectioning in markdown
An extension to [python markdown](https://python-markdown.github.io/) that allows you to add semantic HTML5 sectioning elements into the generated html by putting strings such as `~~S~~` at the start of a section and `~~/S~~` at the end. Sectioning elements supported are `<section>`, `<chapter>`, `<header>`, `<footer>`, `<nav>`, `<div>`, and `<article>`. These can be given identifiers by adding text after the sectioning element letter, e.g. `~~S section1~~` to give `<section id="section1">`. A schematic representation of the structure (useful for debugging) is also generated and stored as the markdown.Markdown.tree_diagram property of the markdown object.

## Requirements & dependencies
Python 3 (tested on Python 3.6 and 3.7)

Designed for use with [MkDocs](https://www.mkdocs.org/#installation)

Uses python packages [Python-Markdown](https://python-markdown.github.io/install/), [Python re](https://docs.python.org/3/library/re.html), [xml.etree.ElementTree](https://docs.python.org/3.7/library/xml.etree.elementtree.html) and [re - Regular expression operations](https://docs.python.org/3/library/re.html)

Installation from github source with setup.py requires [setuptools](https://setuptools.readthedocs.io/en/latest/setuptools.html#installing-setuptools)

Doesn't play nicely with other python markdown extensions that use `~~~` to delineate markup, notably it can lead to text being shown as struck through.

## Installation
__Warning:__  The xml.etree.ElementTree module is not secure against maliciously constructed data. If you need to parse untrusted or unauthenticated data see [XML vulnerabilities](https://docs.python.org/3.7/library/xml.html#xml-vulnerabilities).

__Warning:__ exercise caution this early release software with no warranty, test this first in a virtual environment!

Install from pypi:
```
(venv)$ pip install ocxsect
```

Or install from github:
```
(venv)$ git clone https://github.com/philbarker/ocxsect.git
(venv)$ cd ocxsect
(venv)$ python setup.py test
(venv)$ python setup.py install
(venv)$ python test.py
```

## Usage
To create a new section put `~~X~~` on a line by itself, where X represents the type of HTML5 sectioning element you want to create. Sectioning elements supported are `section` (S), `chapter` (C) `header` (H) `footer` (F) `nav` (N) `div` (D) and `article` (A). These can be given identifiers by add text after the sectioning element letter, e.g. `~~S lesson1~~`. In order to avoid non-URL safe characters in the identifier any character not in the set A-Z, a-z, 0-9, !$-()+ is removed. So `~~A #activity 1~~` becomes `<article id="activity1">`.  

## Usage in MkDocs
After installation, add `ocxsect` to your extensions block in mkdocs.yml:
```
markdown_extensions:
  - ocxsect
```

## Example

### Markdown input

```
~~C lesson1~~

~~H~~
#Markdown structure test
This is in the header section of a chapter. The chapter has id #lesson1. The header has no id.

~~/H~~

~~S section 1~~
#Activity 1
This is in a regular section (id #section1) of a chapter

~~/S~~

~~F~~

This is in the footer of the chapter

~~/F~~

~~/C~~
```

### Schematic representation of structure

```
|--chapter{'id': 'lesson1'}
    |--header
        |--h1
        |--p
    |--section{'id': 'section1'}
        |--h1
        |--p
    |--footer
        |--p
|--p
```

### HTML output

```
<chapter id="lesson1">
  <header>
    <h1>Markdown structure test</h1>
    <p>This is in the header section of a chapter. The chapter has id #lesson1. The header has no id.</p>
  </header>
  <section id="section1">
    <h1>Activity 1</h1>
    <p>This is in a regular section (id #section1) of a chapter</p>
  </section>
  <footer>
    <p>This is in the footer of the chapter</p>
  </footer>
</chapter>
<p>This is after the chapter</p>
```

See test.py for a fully working example embedded in markdown.
