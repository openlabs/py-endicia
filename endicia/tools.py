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
