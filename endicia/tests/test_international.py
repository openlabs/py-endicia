'''
Created on 30 Aug 2010

@author: sharoonthomas
(C) Copyright 2010: Sharoon Thomas
'''
import unittest
import base64
from lxml import etree
from endicia import ShippingLabelAPI, BuyingPostageAPI, \
                    ChangingPassPhraseAPI, Element, \
                    LabelRequest, FromAddress, ToAddress, \
                    CalculatingPostageAPI
                    
from endicia.exceptions import RequestError
from endicia.tools import parse_response, transform_to_xml

REQUESTER_ID = 123456
ACCOUNT_ID = 123456
PASSPHRASE = "PassPhrase"

class TestInternationalShipping(unittest.TestCase):
    """
    Test with values for an international shipment
    """
    label_request = LabelRequest()
    shipping_label_api = ShippingLabelAPI(
         label_request=label_request,
         weight_oz=10,
         partner_customer_id=1,
         partner_transaction_id=1020,
         requesterid=REQUESTER_ID,
         accountid=ACCOUNT_ID,
         passphrase=PASSPHRASE,
         test=True,
         mail_class='PriorityMailInternational'
         )
    from_address = FromAddress(
        FromName="John Doe",
        ReturnAddress1="123 Main Street",
        FromCity="Boise",
        FromState="ID",
        FromPostalCode="83702",
        FromZIP4="7261",
        FromPhone="8005551212"
        )    
    to_address = ToAddress(
        ToName="Sharoon Thomas",
        ToCompany="Open Labs Technologies",
        ToAddress1="R-5/13 Raj Nagar",
        ToCity="Ghaziabad",
        ToState="UP",
        ToCountry="India",
        ToPostalCode="201003",
        ToZIP4="0000",
        ToDeliveryPoint="00",
        ToPhone="01204272022"
        )
    shipping_label_api.add_data(from_address.data)
    shipping_label_api.add_data(to_address.data)
    
    customs_item1 = [
        Element('Description','My Beautiful Shoes'),
        Element('Quantity', 1),
        Element('Weight', 10),
        Element('Value', 50),
    ]
    customs_item2 = [
        Element('Description','My Beautiful Dress'),
        Element('Quantity', 1),
        Element('Weight', 10),
        Element('Value', 50),
    ]
    shipping_label_api.add_data({
            'customsinfo':[
                Element('CustomsItems', [
                        Element('CustomsItem', customs_item1),
                        Element('CustomsItem', customs_item2)
                        ]),
                Element('ContentsType', 'Merchandise')
                ],
            'ValidateAddress':'FALSE',
            'Value':'100.00',
            'Description':'Some Fancy Stuff',
#            'LabelSubtype':'Integrated',
            'CustomsFormType':'Form2976'
            })
    print shipping_label_api.to_xml()
    response = shipping_label_api.send_request()
    assert shipping_label_api.success == True
    parsed_response = parse_response(response, shipping_label_api.namespace)
    print parsed_response.keys()
    filename = '/tmp/' + parsed_response['TrackingNumber'] + '.gif'
    f = open(filename, 'wb')
    f.write(base64.decodestring(parsed_response['Base64LabelImage']))
    f.close()
    print "New Label at: %s" % filename

if __name__ == "__main__":
    unittest.main()
