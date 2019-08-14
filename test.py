import markdown, pytest
from ocxsect import OCXMetadata

# test input with various potential issues
# - lower case and upper case tags
# - no blank lines around section tags
# - section tag on first line
# - section id with space in it
# - section id with a # in it
# - section id with a " in it
TESTINPUT = """
~~C "lesson1"~~
~~h~~
# Markdown structure test
This is in the header section of a chapter. The chapter has id #lesson1. The header has no id.
~~/h~~
~~S section #1 >~~
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
"""

TESTINPUT2 ="""
here is some text before the first division

~~A~~
This would be an article
~~/A~~

here is some text after the first division
"""

HTMLEXPECTED = """<chapter id="lesson1"><header><h1>Markdown structure test</h1><p>This is in the header section of a chapter. The chapter has id #lesson1. The header has no id.</p></header><section id="section1"><h1>Activity 1</h1><p>This is in a regular section (id #section1) of a chapter. The id has ilegal chars in it.</p><div><p>This is a division of a section.</p></div></section><footer><p>This is in the footer of the chapter</p><nav><p>this is navigation, opened in UC, closed in lc</p></nav></footer></chapter><p>This is after the chapter</p>"""

HTMLEXPECTED2 = """<p>here is some text before the first division</p>
<article>
<p>This would be an article</p>
</article>
<p>here is some text after the first division</p>"""
# one day i will understand why this has line breaks but other doesn't

STRUCTUREEXPECTED = """
    |--chapter{'id': 'lesson1'}
        |--header
            |--h1
            |--p
        |--section{'id': 'section1'}
            |--h1
            |--p
            |--div
                |--p
        |--footer
            |--p
            |--nav
                |--p
    |--p"""

STRUCTUREEXPECTED2 = """
    |--p
    |--article
        |--p
    |--p"""

def test_struct():
    md = markdown.Markdown(extensions=["ocxsect"])
    html = md.convert(TESTINPUT)
    assert md.tree_diagram == STRUCTUREEXPECTED

def test_html():
    md = markdown.Markdown(extensions=["ocxsect"])
    html = md.convert(TESTINPUT)
    assert html == HTMLEXPECTED

def test_2():
    md = markdown.Markdown(extensions=["ocxsect"])
    html2 = md.convert(TESTINPUT2)
    assert html2 == HTMLEXPECTED2
    assert md.tree_diagram == STRUCTUREEXPECTED2
