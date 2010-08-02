.. endicia: Endicia

Python - Endicia API
********************

.. automodule:: api

API Base Class
--------------

    .. autoclass:: APIBaseClass


        .. automethod:: __init__
            
        .. automethod:: to_xml

        .. automethod:: add_data

        .. automethod:: success

        .. automethod:: error

        .. automethod:: _set_flags

        .. automethod:: request       

Shipping Label API
------------------

    .. autoclass:: ShippingLabelAPI

        .. automethod:: __init__

        .. automethod:: to_xml

        .. automethod:: send_request

        Example of a Shipping Label is as follows::

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
            where 
                REQUESTER_ID = 123456
                ACCOUNT_ID = 123456
                PASSPHRASE = "PassPhrase"

                label_request = LabelRequest()

Buying Postage API
------------------

    .. autoclass:: BuyingPostageAPI

        .. automethod:: __init__

        .. automethod:: to_xml

        .. automethod:: send_request

        Example of a Buying Postage is as follows::

            recredit_request_api = BuyingPostageAPI(
                                   request_id='098765',
                                   recredit_amount=500.00,
                                   requesterid=REQUESTER_ID,
                                   accountid=ACCOUNT_ID,
                                   passphrase=PASSPHRASE,
                                   test=True,
                                   )

Changing PassPhrase API
-----------------------

    .. autoclass:: ChangingPassPhraseAPI

        .. automethod:: __init__

        .. automethod:: to_xml

        .. automethod:: send_request

        Example of a Changing Passphrase is as follows::

                change_pp_api = ChangingPassPhraseAPI(
                                   request_id='098765',
                                   new_pass_phrase='my new password',
                                   requesterid=REQUESTER_ID,
                                   accountid=ACCOUNT_ID,
                                   passphrase=PASSPHRASE,
                                   test=True,
                                      )

Calculating Postage API
-----------------------

    .. autoclass:: CalculatingPostageAPI


        .. automethod:: __init__


        .. automethod:: to_xml

        .. automethod:: send_request

        Example of a Calculating Postage Fees is as follows::

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

