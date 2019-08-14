import markdown, pytest
from ocxsect import OCXMetadata

# test input with various potential issues
# - lower case and upper case tags
# - no blank lines around section tags
# - section tag on first line
# - section id with space in it
# - section id with a # in it
# - section id with a " in it
TESTINPUT = """~~C "lesson1">~~
~~h~~
# Markdown structure test
This is in the header section of a chapter. The chapter has id #lesson1. The header has no id.
~~/h~~
~~S section #1~~
# Activity 1
This is in a regular section (id #section1) of a chapter. The id has ilegal chars in it.
~~D~~
This is a division of a section.
~~/D~~
~~/S~~
~~F~~
This is in the footer of the chapter
~~N~~
this is navigation, opened in UC, closed in lc
~~/n~~
~~/F~~
~~/C~~
This is after the chapter
~~A~~
An article after the chapter
~~/A~~
"""
HTMLEXPECTED = """<chapter id="lesson1"><header><h1>Markdown structure test</h1><p>This is in the header section of a chapter. The chapter has id #lesson1. The header has no id.</p></header><section id="section1"><h1>Activity 1</h1><p>This is in a regular section (id #section1) of a chapter. The id has ilegal chars in it.</p><div><p>This is a division of a section.</p></div></section><footer><p>This is in the footer of the chapter</p><nav><p>this is navigation, opened in UC, closed in lc</p></nav></footer></chapter><p>This is after the chapter</p>
<article>
<p>An article after the chapter</p>
</article>"""
#one day i will understand why the article has line breaks but others don't

STRUCTUREEXPECTED = """\n    |--chapter{'id': 'lesson1'}\n        |--header\n            |--h1\n            |--p\n        |--section{'id': 'section1'}\n            |--h1\n            |--p\n            |--div\n                |--p\n        |--footer\n            |--p\n            |--nav\n                |--p\n    |--p\n    |--article\n        |--p"""

md = markdown.Markdown(extensions=["ocxsect"])
html = md.convert(TESTINPUT)


def test_html():
    print(html)
    assert html == HTMLEXPECTED


def test_struct():
    assert md.tree_diagram == STRUCTUREEXPECTED
