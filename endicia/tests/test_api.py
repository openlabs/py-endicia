'''
Created on 28 Jul 2010

@author: sharoonthomas
'''
import unittest
from endicia import ShippingLabelAPI, BuyingPostageAPI, ChangingPassPhraseAPI,\
                    LabelRequest, FromAddress, ToAddress, CalculatingPostageAPI
from endicia.exceptions import RequestError
from endicia.tools import parse_response

REQUESTER_ID = 123456
ACCOUNT_ID = 123456
PASSPHRASE = "PassPhrase"

class TestAPI(unittest.TestCase):


    def setUp(self):
        pass


    def tearDown(self):
        pass


    def test0005_label_request(self):
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
                               )
        shipping_label_api.to_xml()
        #
        #Now try to fetch label
        #
        self.assertRaises(RequestError, shipping_label_api.send_request)
        print "Error: %s" % shipping_label_api.error
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
                               ToName="Amine Khechfe",
                               ToCompany="Endicia",
                               ToAddress1="247 High Street",
                               ToCity="Palo Alto",
                               ToState="CA",
                               ToPostalCode="84301",
                               ToZIP4="0000",
                               ToDeliveryPoint="00",
                               ToPhone="8005763279"
                               )
        shipping_label_api.add_data(from_address.data)
        shipping_label_api.add_data(to_address.data)
        response = shipping_label_api.send_request()
        print shipping_label_api.to_xml()
        assert shipping_label_api.success == True
        parse_response(response, shipping_label_api.namespace)
    
    def test0010_recredit_request(self):
        recredit_request_api = BuyingPostageAPI(
                                   request_id='098765',
                                   recredit_amount=500.00,
                                   requesterid=REQUESTER_ID,
                                   accountid=ACCOUNT_ID,
                                   passphrase=PASSPHRASE,
                                   test=True,
                               )
        recredit_request_api.to_xml()
        response = recredit_request_api.send_request()
        parse_response(response, recredit_request_api.namespace)
    
    def test0020_change_passphrase_request(self):
        change_passphrase_request_api = ChangingPassPhraseAPI(
                                   request_id='098765',
                                   new_pass_phrase='my new password',
                                   requesterid=REQUESTER_ID,
                                   accountid=ACCOUNT_ID,
                                   passphrase=PASSPHRASE,
                                   test=True,
                               )
        change_passphrase_request_api.to_xml()
        response = change_passphrase_request_api.send_request()
        parse_response(response, change_passphrase_request_api.namespace)
    
    def test0030_calculating_postage_request(self):
        calculate_postage_request = CalculatingPostageAPI(
                                       mailclass='First',
                                       weightoz=10.00,
                                       from_postal_code="83702",
                                       to_postal_code="84301",
                                       to_country_code="US",
                                       requesterid=REQUESTER_ID,
                                       accountid=ACCOUNT_ID,
                                       passphrase=PASSPHRASE,
                                       test=True,                                    
                                    )
        calculate_postage_request.to_xml()
        response = calculate_postage_request.send_request()
        parse_response(response, calculate_postage_request.namespace)
        
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
