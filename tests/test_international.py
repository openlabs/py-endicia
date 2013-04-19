# -*- coding: utf-8 -*-
"""
    test_international_mail

    :copyright: © 2010 by Open Labs Business Solutions
    :copyright: © 2011-2013 by Openlabs Technologies & Consulting (P) Limited
    :license: BSD, see LICENSE for more details.
"""
import unittest
import base64

from endicia import ShippingLabelAPI, Element, LabelRequest, FromAddress, ToAddress
from endicia.tools import parse_response

REQUESTER_ID = 123456
ACCOUNT_ID = 123456
PASSPHRASE = "PassPhrase"


class BaseTestCase(unittest.TestCase):
    """
    A base test case to support the creation of supporting documents
    """

    def make_from_address(self):
        """
        Returns an instance of :class:`FromAddress` with a valid USA address
        """
        return FromAddress(
            FromName="John Doe",
            ReturnAddress1="123 Main Street",
            FromCity="Boise",
            FromState="ID",
            FromPostalCode="83702",
            FromZIP4="7261",
            FromPhone="8005551212"
        )

    def make_to_address(self, country):
        """
        Returns an instance of :class:`FromAddress` with a valid USA address

        :param country: the country for which the to address must be made
        """
        if country == "IN":
            return ToAddress(
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


class TestInternationalShipping(BaseTestCase):
    """
    Test with values for an international shipment
    """

    def test_pmi(self):
        """
        Test creating a PMI shipment
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
            mail_class='PriorityMailInternational',
            EelPfc='Testing',
            CustomsCertify='TRUE',
            CustomsSigner='John',
        )

        # A US address to an IN address
        from_address = self.make_from_address()
        to_address = self.make_to_address('IN')
        shipping_label_api.add_data(from_address.data)
        shipping_label_api.add_data(to_address.data)

        customs_item1 = [
            Element('Description', 'My Beautiful Shoes'),
            Element('Quantity', 1),
            Element('Weight', 10),
            Element('Value', 50),
        ]
        customs_item2 = [
            Element('Description', 'My Beautiful Dress'),
            Element('Quantity', 1),
            Element('Weight', 10),
            Element('Value', 50),
        ]
        shipping_label_api.add_data({
            'customsinfo': [
            Element('CustomsItems', [
            Element('CustomsItem', customs_item1),
            Element('CustomsItem', customs_item2)
            ]),
                Element('EelPfc', 'Testing'),
                Element('ContentsType', 'Merchandise')
            ],
            'EelPfc': 'Testing',
            'ValidateAddress': 'FALSE',
            'Value': '100.00',
            'Description': 'Some Fancy Stuffs',
            'LabelSubtype': 'Integrated',
            'IntegratedFormType': 'Form2976',
            'CustomsCertify': 'TRUE',
            'CustomsSigner': 'John',
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

    def test_fcpis(self):
        """
        Test the creation of First-Class Package International Service (FCPIS)
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
            mail_class='FirstClassPackageInternationalService',
            EelPfc='Testing',
            CustomsCertify='TRUE',
            CustomsSigner='John',
        )

        # A US address to an IN address
        from_address = self.make_from_address()
        to_address = self.make_to_address('IN')
        shipping_label_api.add_data(from_address.data)
        shipping_label_api.add_data(to_address.data)

        customs_item1 = [
            Element('Description', 'My Beautiful Shoes'),
            Element('Quantity', 1),
            Element('Weight', 10),
            Element('Value', 50),
        ]
        customs_item2 = [
            Element('Description', 'My Beautiful Dress'),
            Element('Quantity', 1),
            Element('Weight', 10),
            Element('Value', 50),
        ]
        shipping_label_api.add_data({
            'customsinfo': [
            Element('CustomsItems', [
            Element('CustomsItem', customs_item1),
            Element('CustomsItem', customs_item2)
            ]),
                Element('EelPfc', 'Testing'),
                Element('ContentsType', 'Merchandise')
            ],
            'EelPfc': 'Testing',
            'ValidateAddress': 'FALSE',
            'Value': '100.00',
            'Description': 'Some Fancy Stuffs',
            'LabelSubtype': 'Integrated',
            'IntegratedFormType': 'Form2976',
            'CustomsCertify': 'TRUE',
            'CustomsSigner': 'John',
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


def suite():
    '''
    Test Suite
    '''
    suite = unittest.TestSuite()
    suite.addTests(
        unittest.TestLoader().loadTestsFromTestCase(TestInternationalShipping)
    )
    return suite


if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=2).run(suite())
