from endicia import ShippingLabelAPI, BuyingPostageAPI, \
                    ChangingPassPhraseAPI, LabelRequest, \
                    FromAddress, ToAddress, CalculatingPostageAPI, \
                    RefundRequestAPI, SCANFormAPI, Element
from endicia.exceptions import RequestError
from endicia.tools import parse_response, parse_images
import base64

REQUESTER_ID = 123456
ACCOUNT_ID = 123456
PASSPHRASE = "PassPhrase"

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

print shipping_label_api.to_xml()

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

print shipping_label_api.to_xml()

response = shipping_label_api.send_request()
parse_response(response, shipping_label_api.namespace)
"""
A more complicated example
"""
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
shipping_label_api.add_data({'customsinfo':[
            Element('CustomsItems', [
                    Element('CustomsItem', customs_item1),
                    Element('CustomsItem', customs_item2)
                    ]),
            Element('ContentsType', 'Merchandise')
]})
print shipping_label_api.to_xml()
response = shipping_label_api.send_request()
xyz = parse_response(response, shipping_label_api.namespace)
filename = '/tmp/' + xyz['PIC'] + '.png'
f = open(filename, 'wb')
f.write(base64.decodestring(xyz['Base64LabelImage']))
f.close()
print "New Label at: %s" % filename
pic_number = xyz['PIC']
#
#Buying postage API
#
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
#
#Change passphrase API
#
change_pp_api = ChangingPassPhraseAPI(
                                   request_id='098765',
                                   new_pass_phrase='my new password',
                                   requesterid=REQUESTER_ID,
                                   accountid=ACCOUNT_ID,
                                   passphrase=PASSPHRASE,
                                   test=True,
                                      )
change_pp_api.to_xml()
response = change_pp_api.send_request()
parse_response(response, change_pp_api.namespace)
#
#Calculate postage
#
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

#
#Refund Request API
#
refund_request = RefundRequestAPI(
                               pic_number=pic_number,
                               requesterid=REQUESTER_ID,
                               accountid=ACCOUNT_ID,
                               passphrase=PASSPHRASE,
                               test='Y',                                    
                            )
print refund_request.to_xml()
#response = refund_request.send_request()
#print parse_response(response, refund_request.namespace)


#
#SCAN Request API
#
scan_request = SCANFormAPI(
                               pic_number=pic_number,
                               requesterid=REQUESTER_ID,
                               accountid=ACCOUNT_ID,
                               passphrase=PASSPHRASE,
                               test='Y',                                    
                            )
print scan_request.to_xml()
response = scan_request.send_request()
print parse_response(response, scan_request.namespace)
