"""
Various Data structures

Element is a data structure to represent a HTML tag and its
value in a simple way.

To use the data structure:

>>> from endicia import Element
>>> name = Element(tag='name', data='Sharoon Thomas')
>>> age = Element(tag='Age', data=22)

For more examples of How element can be used refer to the ``examples.py``
"""

from collections import namedtuple

Element = namedtuple('Element', 'tag data')


class BaseStruct(object):
    """
    Base data structure
    """
    def __init__(self):
        """
        Initialise
        """
        self.keys = None

    @property
    def data(self):
        _data = {}
        for key in self.keys:
            if hasattr(self, key) and getattr(self, key) is not None:
                _data[key] = getattr(self, key)
        return _data


class FromAddress(BaseStruct):
    """
    From Address object
    """
    def __init__(self, **kwargs):
        """
        Initialise class attributes
        """
        super(FromAddress, self).__init__()
        self.keys = [
            'FromName',
            'FromCompany',
            'ReturnAddress1',
            'ReturnAddress2',
            'ReturnAddress3',
            'ReturnAddress4',
            'FromCity',
            'FromState',
            'FromPostalCode',
            'FromPhone',
            'FromEMail'
        ]
        self.__dict__.update(dict.fromkeys(self.keys))
        self.__dict__.update(kwargs)


class ToAddress(BaseStruct):
    """
    To address object
    """
    def __init__(self, **kwargs):
        """
        Initialise
        """
        super(ToAddress, self).__init__()
        self.keys = [
            'ToName',
            'ToCompany',
            'ToAddress1',
            'ToAddress2',
            'ToAddress3',
            'ToAddress4',
            'ToCity',
            'ToState',
            'ToPostalCode',
            'ToCountry',
            'ToCountryCode',
            'ToPhone',
            'ToEMail'
        ]
        self.__dict__.update(dict.fromkeys(self.keys))
        self.__dict__.update(kwargs)


class LabelRequest(BaseStruct):
    """
    Base structure for label
    """
    def __init__(self, **kwargs):
        super(LabelRequest, self).__init__()
        self.keys = [
            'ImageRotation',
            'ImageResolution',
            'LabelType',
            'LabelSubtype',
            'ImageFormat',
            'Test',
            'LabelSize'
        ]
        self.__dict__.update({
            'Test': 'YES',
            # 'LabelType':'Default',
            # 'LabelSubtype':'None',
            # 'LabelSize':'4x6',
            # 'ImageFormat':'PNG',
            # 'ImageResolution':'300',
            # 'ImageRotation':'None',
        })
        self.__dict__.update(kwargs)
