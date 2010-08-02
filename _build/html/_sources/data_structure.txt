.. data_structure: Data Structure


Data Structures
***************

.. automodule:: data_structures

Base Structure
--------------

	.. autoclass:: BaseStruct

        .. automethod:: __init__

From Address
------------

	.. autoclass:: FromAddress

        .. automethod:: __init__

The parameters that can be passed are :

            * FromName
            * FromCompany
            * ReturnAddress1
            * ReturnAddress2
            * ReturnAddress3
            * ReturnAddress4
            * FromCity
            * FromState
            * FromPostalCode
            * FromPhone
            * FromEMail

To Address
----------

	.. autoclass:: ToAddress

        .. automethod:: __init__

The parameters that can be passed are :

            * ToName
            * ToCompany
            * ToAddress1
            * ToAddress2
            * ToAddress3
            * ToAddress4
            * ToCity
            * ToState
            * ToPostalCode
            * ToCountry
            * ToCountryCode
            * ToPhone
            * ToEMail


Label Request
-------------

	.. autoclass:: LabelRequest

        .. automethod::__init__

The parameters that can be passed are :

            * ImageRotation
            * ImageResolution
            * LabelType
            * LabelSubtype
            * ImageFormat
            * Test
            * LabelSize
