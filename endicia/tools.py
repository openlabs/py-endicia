""
from lxml import etree

def parse_response(response, namespace=''):
    """
    Parses XML response as string to readable keys and values
    """
    response_dict = {}
    xml_result = etree.fromstring(response)
    for element in xml_result.iter():
        response_dict[element.tag.replace(namespace, '')] = element.text
    return response_dict

def transform_to_xml(root, data, name=None):
    """
    Adds data to root XML element
    
    Returns the mangled data, root or sub_element
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
