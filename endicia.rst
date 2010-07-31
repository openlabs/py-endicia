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

Shipping Label API
------------------
    .. autoclass:: ShippingLabelAPI

        .. automethod:: __init__

			Other than the parameters given above, you may also pass the following fields: -

            * labelsize 
            * imageformat - EPL2, GIF, JPEG, PDF, PNG, ZPLII
            * imageresolution - 203 (203 dpi) or 300 (300 dpi)
            * sundayholidaydelivery - True/False, 
            * showreturnaddress - True/False, 
            * stealth - True/False, 
            * noweekendselivery - True/False, 
            * trackingnumber - Text, 
            * insuredvalue - Currency (5.2 format), 
            * origincountry - Text
            * And many others. Keep in mind that while you pass any parameter, keep it in lower case. 


        .. automethod:: to_xml

        .. automethod:: send_request

Buying Postage API
------------------
    .. autoclass:: BuyingPostageAPI

        .. automethod:: __init__

        .. automethod:: to_xml

        .. automethod:: send_request

Changing PassPhrase API
-----------------------
    .. autoclass:: ChangingPassPhraseAPI

        .. automethod:: __init__

        .. automethod:: to_xml

        .. automethod:: send_request

Calculating Postage API
-----------------------
    .. autoclass:: CalculatingPostageAPI


        .. automethod:: __init__


        .. automethod:: to_xml

        .. automethod:: send_request


