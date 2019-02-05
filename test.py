import markdown, unittest
from ocxmd import OCXMetadata
#test input with various potential issues
# - lower case and upper case tags
# - no blank lines around section tags
# - section tag on first line
# - section id with space in it
# - section id with a # in it
# - section id with a " in it
TESTINPUT = '''~~C "lesson1">~~
~~h~~
# Markdown structure test
This is in the header section of a chapter. The chapter has id #lesson1. The header has no id.
~~/h~~
~~S section #1~~
# Activity 1
This is in a regular section (id #section1) of a chapter
~~/S~~
~~F~~
This is in the footer of the chapter
~~/F~~
~~/C~~
This is after the chapter
'''
HTMLEXPECTED = '''<chapter id="lesson1"><header><h1>Markdown structure test</h1><p>This is in the header section of a chapter. The chapter has id #lesson1. The header has no id.</p></header><section id="section1"><h1>Activity 1</h1><p>This is in a regular section (id #section1) of a chapter</p></section><footer><p>This is in the footer of the chapter</p></footer></chapter><p>This is after the chapter</p>'''
METADATAEXPECTED = {1: {'@context': ['http://schema.org', {'oer': 'http://oerschema.org/'}, {'ocx': 'https://github.com/K12OCX/k12ocx-specs/'}], '@id': '#lesson1', 'name': 'Test Lesson 1', '@type': ['oer:Lesson', 'CreativeWork'], 'learningResourceType': 'LessonPlan', 'hasPart': {'@id': '#activity1'}, 'author': {'@type': 'Person', 'name': 'Fred Blogs'}}, 2: {'@context': ['http://schema.org', {'oer': 'http://oerschema.org/'}, {'ocx': 'https://github.com/K12OCX/k12ocx-specs/'}], '@id': '#activity1', '@type': ['oer:Activity', 'CreativeWork'], 'name': 'Test Activity 1.1', 'learningResourceType': 'Activity'}}
STRUCTUREEXPECTED = '''\n    |--chapter{'id': 'lesson1'}\n        |--header\n            |--h1\n            |--p\n        |--section{'id': 'section1'}\n            |--h1\n            |--p\n        |--footer\n            |--p\n    |--p'''
class TestOCXMD(unittest.TestCase):
    md = markdown.Markdown(extensions = ['ocxsect'])
    html = md.convert(TESTINPUT)
    print(md.tree_diagram)
    print(html)
    def test_html(self):
        self.assertEqual(self.html, HTMLEXPECTED)
    def test_struct(self):
        self.assertEqual(self.md.tree_diagram, STRUCTUREEXPECTED)

if '__main__' == __name__:
    unittest.main()
