"""Convert xml format file into dictionary output
Example:

xml2dict(xml.etree.ElementTree.fromstring(xml_string))

"""

import xml.etree.ElementTree

def xml2dict(element_tree):
    def internal_iter(tree, accum):
        if tree is None:
            return accum
        if tree.getchildren():
            accum[tree.tag] = {}
            for each in tree.getchildren():
                result = internal_iter(each, {})
                if each.tag in accum[tree.tag]:
                    if not isinstance(accum[tree.tag][each.tag], list):
                        accum[tree.tag][each.tag] = [
                            accum[tree.tag][each.tag]
                        ]
                    accum[tree.tag][each.tag].append(result[each.tag])
                else:
                    accum[tree.tag].update(result)
        else:
            accum[tree.tag] = tree.text
        return accum
    return internal_iter(element_tree, {})
