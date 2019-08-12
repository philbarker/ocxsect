from markdown.extensions import Extension
from markdown.preprocessors import Preprocessor
from markdown.treeprocessors import Treeprocessor
import xml.etree.ElementTree as ET
import re

START_SECTION = r"~~([SCHFNDA])([^~]*)~~"
END_SECTION = r"~~/([SCHFNDA])~~"


class OCXMetadata(Extension):
    """Python-Markdown extension for parsing OCX metadata from YAML."""

    def extendMarkdown(self, md):
        md.registerExtension(self)
        self.md = md
        md.preprocessors.register(OCXSectionPreprocessor(md), "ocxsection", 29)
        md.treeprocessors.register(OCXSectionTreeProcessor(md), "ocxsection", 29)


class OCXSectionPreprocessor(Preprocessor):
    """Clean up the input, checking for start and end tags that don't have a blank line before or after, and for use of lower case letter in tags"""

    START_RE = re.compile(START_SECTION, re.IGNORECASE)
    END_RE = re.compile(END_SECTION, re.IGNORECASE)

    def run(self, lines):
        after_tag = False  # used to indicate we are looking at line after tag
        new_lines = []
        for line in lines:
            if after_tag:  # we at a line after a start or end tag
                if "" != line:  # make sure it is followed by a blank
                    new_lines.append("")
                after_tag = False  # reset flag
            match = self.START_RE.match(line)
            if match:  # we have a start tag,
                # make sure it is upper case
                after_tag = True
                line = line.replace(match.group(1), match.group(1).upper())
                if new_lines and "" != new_lines[-1]:
                    # make sure line before is blank
                    new_lines.append("")
            match = self.END_RE.match(line)
            if match:  # we have an end tag,
                # make sure it is upper case
                after_tag = True
                line = line.replace(match.group(1), match.group(1).upper())
                if new_lines and "" != new_lines[-1]:
                    # make sure line before is blank
                    new_lines.append("")
            new_lines.append(line)
        return new_lines


class OCXSectionTreeProcessor(Treeprocessor):
    START_RE = re.compile(START_SECTION)
    END_RE = re.compile(END_SECTION)
    BAD_URI_FRAG_CHARS = "[^A-Za-z0-9!$-()+]"  # really stingy in what's allowed

    def run(self, root):
        ancestors = [root]
        self.section(root, ancestors)
        self.md.tree_diagram = ""
        self.set_tree_diagram(root, 0)

    def section(self, node, new_ancestors):
        # rebuild the elment tree by running through all the nodes, and recursively
        # through the children of those nodes, replacing any p elements that
        # indicate the start of a sectioning element (e.g. ~~S~~) with a new section
        # into which subsequent nodes are moved until an element indicating the
        # end of of a section.
        # node : element in oringinal eTree whose children are processed;
        # new_ancestors : stack of ancestors in eTree being created;
        # note, the node being processed won't be in the eTree created if it marks
        # the beginning of end of a section.
        # a list of nodes in the eTree at the start is made, new nodes are added
        # to the end of the eTree as they are processed, and the orginal node
        # removed.
        for child in list(node):
            # the list is immutable, so we run through the *original* nodes in the
            # eTree removing them when done and adding the new processed nodes to
            # the end
            if child.text:
                start_match = self.START_RE.match(child.text)
            else:
                start_match = False
            if start_match:
                # we have a node that indicates the start of a section
                # there is nothing to keep in such a node
                node.remove(child)
                # determine which sectioning elmt
                if "S" == start_match.group(1):
                    newsect_type = "section"
                elif "C" == start_match.group(1):
                    newsect_type = "chapter"
                elif "A" == start_match.group(1):
                    newsect_type = "article"
                elif "H" == start_match.group(1):
                    newsect_type = "header"
                elif "F" == start_match.group(1):
                    newsect_type = "footer"
                elif "N" == start_match.group(1):
                    newsect_type = "nav"
                elif "D" == start_match.group(1):
                    newsect_type = "div"
                #                else:
                # regex won't match anything else
                # find id attribute of new section, if any
                if start_match.group(2):
                    # make sure id has no bad characters in it
                    i = re.sub(self.BAD_URI_FRAG_CHARS, "", start_match.group(2))
                    attr = {"id": i}
                else:
                    attr = {}
                # create new section
                newsect = ET.SubElement(new_ancestors[-1], newsect_type, attr)
                # this new section will be the new parent until we get to end marker
                new_ancestors.append(newsect)
            elif child.text and self.END_RE.match(child.text.upper()):
                # we have reached an end of section marker
                # nothing to keep in such a node
                node.remove(child)
                # revert to using previous new_ancestor as new parent
                new_ancestors.pop()
            else:
                node.remove(child)  # remove from original place in tree
                new_ancestors[-1].append(child)  # append to the latest new ancestor
                new_ancestors.append(child)
                self.section(child, new_ancestors)  # recurse through nodes children
        new_ancestors.pop()

    def set_tree_diagram(self, node, depth):
        ldepth = depth + 1
        for child in list(node):
            attrib = str(child.attrib) if child.attrib else ""
            line = "\n" + ldepth * "    " + "|--"
            self.md.tree_diagram = self.md.tree_diagram + line + child.tag + attrib
            self.set_tree_diagram(child, ldepth)


def makeExtension(**kwargs):
    # allows calling of extension by string which is not dot-noted
    return OCXMetadata(**kwargs)
