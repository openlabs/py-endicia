"""
Various Data structures
"""
from collections import namedtuple

Element = namedtuple('Element', 'tag data')

class BaseStruct(object):
    """
    Base data structure
    """
    def __init__(self):
        self.keys = None
        
    @property
    def data(self):
        _data = {}
        for key in self.keys:
            if not getattr(self, key) is None:
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
                            'Test':'YES',
                            'LabelType':'Default',
                            'LabelSubtype':'None',
                            'LabelSize':'4x6',
                            'ImageFormat':'PNG',
                            'ImageResolution':'300',
                            'ImageRotation':'None',
                            })
        self.__dict__.update(kwargs)
    


