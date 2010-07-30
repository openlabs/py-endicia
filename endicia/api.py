"""
Api for Web-based, on-demand services of the USPS
provided by Endicia

The description as given by Endicia doc is below:
-------------------------------------------------
The Endicia Label Server produces an integrated label image, 
complete with Stealth (hidden) postage, return addresses, 
verified delivery addresses, and service barcodes 

(Delivery Confirmation, Signature Confirmation, 
Certified Mail with optional Electronic Return Receipt, 
Express Mail, Confirm Services, or customs forms).

The basic concept around the Endicia Label Server is to provide partners, 
developers, and integrators with the ability to print US Postal Service 
pre-paid shipping labels with postage.

"""
import urllib
import urllib2
from lxml import etree
from lxml.etree import ETXPath
from endicia.exceptions import RequestError

class APIBaseClass(object):
    """
    Base class object other models have to inherit
    """
    def __init__(self, requesterid,
                 accountid, passphrase,
                 test, **kwargs):
        """
        Validates ReqID, AccID and passphrase
        """
        self.requesterid = requesterid
        self.accountid = accountid
        self.passphrase = passphrase
        self.test = test
        if test:
            self.base_url = 'https://www.envmgr.com/'
            self.base_namespace = 'www.envmgr.com/' 
        else:
            self.base_url = 'http://www.endicia.com/'
            self.base_namespace = 'www.endicia.com/'
        self.url = None     #Inherit and modify
        #------------------------------------
        self.required_elements = [
                                'RequesterID',
                                'AccountID',
                                'PassPhrase',
                                    ]
        self.valid_elements = []
        #A flag to be set to say if the transaction was successful
        self.flags = {
                      'Status':None,
                      'ErrorMessage':None,
                      }
        self.response = self.namespace = None
        
    def to_xml(self, as_string=True):
        """
        Constructs XML message to be sent and returns it
        """
        raise Exception('Not Implemented Yet')

    def add_data(self, data):
        """
        :param data: dictionary of element and value
        """
        self.__dict__.update(
                             dict([
                                   (key.lower(), value) \
                                        for (key, value) in data.items()
                                   ])
                             )
    
    @property
    def success(self):
        """
        Returns True if the transaction was success
        """
        if self.flags['Status'] in ['0', 0]:
            return True
        return False
    
    @property
    def error(self):
        """
        Returns error if exists
        """
        return self.flags['ErrorMessage']
    
    def _set_flags(self, response):
        """
        Sets flags if any
        """
        xml_result = etree.fromstring(response)
        
        self.flags['Status'] = ETXPath(
                                       '//%sStatus' % self.namespace
                                        )(xml_result)[0].text
        error_message = ETXPath(
                                 '//%sErrorMessage' % self.namespace
                                        )(xml_result)
        self.flags['ErrorMessage'] = error_message and \
                                        error_message[0].text or None
        self.response = xml_result
        return response
    
    def request(self, values):
        """
        Sends information to the server and returns the response
        """
        data = urllib.urlencode(values)
        req = urllib2.Request(self.url, data)
        response = urllib2.urlopen(req).read()
        return self._set_flags(response)


class ShippingLabelAPI(APIBaseClass):
    """
    To request a shipping label, use the GetPostageLabel or the 
    GetPostageLabelXML Web method of the Endicia Label Server Web Service.
    """
    def __init__(self,
                 label_request,
                 weight_oz,
                 partner_customer_id,
                 partner_transaction_id,
                 mail_class='First',
                 **kwargs):
        """
        :param label_request: Label request object
        :param weight_oz: Weight of the package, in ounces.
        :param partner_customer_id: A unique identifier for the partner's 
                                    end-user printing the label (user id)
        :param partner_transaction_id: A unique identifier for the partner's 
                                    end-user's transaction such as invoice, 
                                    transaction number, etc.
        :param mail_class:  Express 
                            First 
                            Library Mail 
                            MediaMail 
                            ParcelPost
                            ParcelSelect
                            Priority
                            StandardMail
                            
                            ExpressMailInternational
                            FirstClassMailInternational 
                            PriorityMailInternational
        """
        super(ShippingLabelAPI, self).__init__(**kwargs)
        
        self.labelrequest = label_request
        self.mailclass = mail_class
        self.weightoz = weight_oz
        self.partnercustomerid = partner_customer_id
        self.partnertransactionid = partner_transaction_id
        #
        #Above are the required elements
        #
        self.dateadvance = 0
        self.mailpieceshape = None
        self.mailpiecedimensions = {
                                  'Length':0,
                                  'Width':0,
                                  'Height':0
                                  }
        self.machinable = 'TRUE'
        self.servicelevel = None
        self.sundayholidaydelivery = 'FALSE'
        self.sorttype = 'SinglePiece'
        self.includepostage = 'TRUE'
        self.replypostage = 'FALSE'
        self.showreturnaddress = 'TRUE'
        self.stealth = 'TRUE'
        self.validateaddress = 'TRUE'
        self.signaturewaiver = 'TRUE'
        self.noweekenddelivery = 'FALSE'
        self.services = {
                       'CertifiedMail':'ON',
                       'COD':'OFF',
                       'ElectronicReturnReceipt':'OFF',
                       'InsuredMail':'OFF',
                       'RestrictedDelivery':'OFF',
                       'ReturnReceipt':'OFF',
                       'SignatureConfirmation':'OFF'
                       }
        self.required_elements.extend([
                                  'MailClass',
                                  'WeightOz',
                                  'PartnerCustomerID',
                                  'PartnerTransactionID',
                                  'ReturnAddress1',
                                  'FromCity',
                                  'FromState',
                                  'FromPostalCode',
                                  'ToAddress1',
                                  'ToCity',
                                  'ToState',
                                  'ToPostalCode'
                                  ])
        self.valid_elements.extend(self.required_elements) 
        self.valid_elements.extend([
                                    'DateAdvance',
                                    'MailpieceShape',
                                    'MailpieceDimensions',
                                    'Machinable',
                                    'ServiceLevel',
                                    'SundayHolidayDelivery',
                                    'SortType',
                                    'IncludePostage',
                                    'ReplyPostage',
                                    'ShowReturnAddress',
                                    'Stealth',
                                    'ValidateAddress',
                                    'SignatureWaiver',
                                    'NoWeekendDelivery',
                                 
                                     'FromName',
                                     'FromCompany',
                                     'ReturnAddress2',
                                     'ReturnAddress3',
                                     'ReturnAddress4',
                                     'FromPhone',
                                     'FromEMail'

                                     'ToName',
                                     'ToCompany',
                                     'ToCountry',
                                     'ToCountryCode',
                                     'ToPhone',
                                     'ToEMail'
                                     ]
        )
        self.namespace = '{' + self.base_namespace + 'LabelService}'
        self.url = self.base_url + "LabelService/EwsLabelService.asmx/GetPostageLabelXML"
        
    def to_xml(self, as_string=True):
        """
        Convert the data To xml
        """
        labelrequest = etree.Element("LabelRequest", **self.labelrequest.data)
        for element in self.valid_elements:
            if not hasattr(self, element.lower()):
                #
                #If element is not there then bypass it
                #
                continue
            value = getattr(self, element.lower())
            if value:
                sub_element = etree.SubElement(labelrequest, element)
                if type(value) == dict:
                    #
                    # If value is dictionary, make it attributes
                    #
                    for attr_name, attr_value in value.items():
                        sub_element.set(attr_name, unicode(attr_value))
                else:
                    #
                    # Make the value the text
                    #
                    sub_element.text = unicode(value)
        if as_string:
            return etree.tostring(labelrequest, pretty_print=True)
        else:
            return labelrequest

    def send_request(self):
        """
        Sends the request to the server
        """
        response = self.request({'labelRequestXML':self.to_xml()})
        if self.success:
            return response
        else:
            raise RequestError(self.error)
        
        
class BuyingPostageAPI(APIBaseClass):
    """
    To add postage to an account, use the BuyPostage 
    or the BuyPostageXML Web method of the Endicia Label 
    Server Web Service.
    """
    def __init__(self,
                 request_id,
                 recredit_amount,
                 **kwargs):
        super(BuyingPostageAPI, self).__init__(**kwargs)
        
        self.requestid = request_id
        self.recredit_amount = recredit_amount
        self.namespace = '{' + self.base_namespace + 'LabelService}'
        self.url = self.base_url + \
                    "LabelService/EwsLabelService.asmx/BuyPostageXML"
    
    def to_xml(self, as_string=True):
        recreditrequest = etree.Element("RecreditRequest")
        
        sub_element = etree.SubElement(recreditrequest,
                                       'RequesterID')
        sub_element.text = unicode(self.requesterid)
        
        sub_element = etree.SubElement(recreditrequest,
                                       'RequestID')
        sub_element.text = unicode(self.requestid)
        
        sub_element = etree.SubElement(recreditrequest,
                                       'CertifiedIntermediary')
        sub_element2 = etree.SubElement(sub_element, 'AccountID')
        sub_element2.text = unicode(self.accountid)
        sub_element2 = etree.SubElement(sub_element, 'PassPhrase')
        sub_element2.text = unicode(self.passphrase)
        
        sub_element = etree.SubElement(recreditrequest,
                                       'RecreditAmount')
        sub_element.text = unicode(self.recredit_amount)
        if as_string:
            return etree.tostring(recreditrequest, pretty_print=True)
        else:
            return recreditrequest
    
    def send_request(self):
        """
        Sends the request to the server
        """
        response = self.request({'recreditRequestXML':self.to_xml()})
        if self.success:
            return response
        else:
            raise RequestError(self.error)


class ChangingPassPhraseAPI(APIBaseClass):
    """
    To change the Pass Phrase for an account, use the API
    """
    def __init__(self,
                 request_id,
                 new_pass_phrase,
                 **kwargs):
        super(ChangingPassPhraseAPI, self).__init__(**kwargs)
        
        self.requestid = request_id
        self.new_pass_phrase = new_pass_phrase
        self.namespace = '{' + self.base_namespace + 'LabelService}'
        self.url = self.base_url + \
                    "LabelService/EwsLabelService.asmx/ChangePassPhraseXML"
    
    def to_xml(self, as_string=True):
        changepassphraserequest = etree.Element("ChangePassPhraseRequest")
        
        sub_element = etree.SubElement(changepassphraserequest,
                                       'RequesterID')
        sub_element.text = unicode(self.requesterid)
        
        sub_element = etree.SubElement(changepassphraserequest,
                                       'RequestID')
        sub_element.text = unicode(self.requestid)
        
        sub_element = etree.SubElement(changepassphraserequest,
                                       'CertifiedIntermediary')
        sub_element2 = etree.SubElement(sub_element, 'AccountID')
        sub_element2.text = unicode(self.accountid)
        sub_element2 = etree.SubElement(sub_element, 'PassPhrase')
        sub_element2.text = unicode(self.passphrase)
        
        sub_element = etree.SubElement(changepassphraserequest,
                                       'NewPassPhrase')
        sub_element.text = unicode(self.new_pass_phrase)
        if as_string:
            return etree.tostring(changepassphraserequest, pretty_print=True)
        else:
            return changepassphraserequest
    
    def send_request(self):
        """
        Sends the request to the server
        """
        response = self.request({'changePassPhraseRequestXML':self.to_xml()})
        if self.success:
            return response
        else:
            raise RequestError(self.error)


class CalculatingPostageAPI(APIBaseClass):
    """
    calculate the postage and fees for a single mailpiece
    """
    def __init__(self,
                 mailclass,
                 weightoz,
                 from_postal_code,
                 to_postal_code,
                 to_country_code,
                 **kwargs):
        super(CalculatingPostageAPI, self).__init__(**kwargs)
        
        self.mailclass = mailclass
        self.weightoz = weightoz
        self.frompostalcode = from_postal_code
        self.topostalcode = to_postal_code
        self.tocountrycode = to_country_code
        self.valid_elements.extend([
                                    'RequesterID',
                                    'MailClass',
                                    'Pricing',
                                    'WeightOz',
                                    'MailpieceShape',
                                    'MailpieceDimensions',
                                    'AutomationRate',
                                    'Machinable',
                                    'ServiceLevel',
                                    'SundayHolidayDelivery',
                                    'SortType',
                                    'Services',
                                    'Value',
                                    'CODAmount',
                                    'InsuredValue',
                                 
                                     'EntryFacility',
                                     'FromPostalCode',
                                     'ToPostalCode',
                                     'ToCountry',
                                     'ToCountryCode',
                                     'ShipDate',
                                     'ShipTime'

                                     ]
        )
        self.namespace = '{' + self.base_namespace + 'LabelService}'
        self.url = self.base_url + \
                    "LabelService/EwsLabelService.asmx/CalculatePostageRateXML"
    
    def to_xml(self, as_string=True):
        calculatepostagerequest = etree.Element("PostageRateRequest")
        
        sub_element = etree.SubElement(calculatepostagerequest,
                                       'RequesterID')
        sub_element.text = unicode(self.requesterid)
        
        sub_element = etree.SubElement(calculatepostagerequest,
                                       'CertifiedIntermediary')
        sub_element2 = etree.SubElement(sub_element, 'AccountID')
        sub_element2.text = unicode(self.accountid)
        sub_element2 = etree.SubElement(sub_element, 'PassPhrase')
        sub_element2.text = unicode(self.passphrase)
        for element in self.valid_elements:
            if not hasattr(self, element.lower()):
                #
                #If element is not there then bypass it
                #
                continue
            value = getattr(self, element.lower())
            if value:
                sub_element = etree.SubElement(calculatepostagerequest, element)
                if type(value) == dict:
                    #
                    # If value is dictionary, make it attributes
                    #
                    for attr_name, attr_value in value.items():
                        sub_element.set(attr_name, unicode(attr_value))
                else:
                    #
                    # Make the value the text
                    #
                    sub_element.text = unicode(value)
        sub_element = etree.SubElement(calculatepostagerequest,
                                       'ResponseOptions')
        sub_element.set('PostagePrice', 'TRUE')
        if as_string:
            return etree.tostring(calculatepostagerequest, pretty_print=True)
        else:
            return calculatepostagerequest
    
    def send_request(self):
        """
        Sends the request to the server
        """
        response = self.request({'postageRateRequestXML':self.to_xml()})
        if self.success:
            return response
        else:
            raise RequestError(self.error)



