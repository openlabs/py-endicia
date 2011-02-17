""
from lxml import etree

def parse_response(response, namespace=''):
    """
    Parses XML response as string to readable keys and values
    in a dictionary
    """
    response_dict = {}
    xml_result = etree.fromstring(response)
    for element in xml_result.iter():
        response_dict[element.tag.replace(namespace, '')] = element.text
    return response_dict

def transform_to_xml(root, data, name=None):
    """
    Adds data to root XML element

    :param root: The instance of lxml.etree to which data is added
    :param data: The data to add

                 >>> from endicia.tools import transform_to_xml
                 >>> from endicia import Element
                 >>> from lxml import etree
                 >>> root = etree.Element('root')
                 >>> etree.tostring(root)
                 '<root/>'

                 If the data is of type dictionary then the key is
                 treated as an attribute and the value as its value, eg:

                 >>> transform_to_xml(root, {'attribute':'attribute_value'})
                     <Element root at 121b1e0>
                 >>> etree.tostring(root)
                     <root attribute="attribute_value"/>

                 If data is of type list, then the items in the list are
                 expected to be of 'Element' data type. Each item of the list
                 becomes a sub element of the root node with tag as tag and
                 the data supplied is applied with the properties of this
                 function.

                 >>> name = Element('name', 'Sharoon Thomas')
                 >>> age = Element('age', 22)
                 >>> location = Element('location',[
                                         Element('city','Manchester'),
                                         Element('postcode','M145EU')])
                 >>> transform_to_xml(root, [name, age, location])
                     <Element root at 121b1e0>
                 >>> etree.tostring(root)
                 
                The XML is ::

                    <root attribute="attribute_value">
                         <name>Sharoon Thomas</name>
                         <age>22</age>
                         <location>
                             <city>Manchester</city>
                             <postcode>M145EU</postcode>
                         </location>
                     </root>

             If anything else is supplied, its assumed to be the text of
             the element

    :return: The mangled data, root or sub_element whichever got changed
    """
    if not name:
        if type(data) == dict:
            for (attr_name, attr_value) in data.items():
                root.set(attr_name, unicode(attr_value))
            return root
        elif type(data) == list:
            for sub_element_data in data:
                sub_element = etree.SubElement(root, 
                                               sub_element_data.tag)
                transform_to_xml(sub_element, sub_element_data.data)
            return root
        else:
            root.text = unicode(data)
    else:
        sub_element = etree.SubElement(root, name)
        transform_to_xml(sub_element, data)
        return sub_element 
