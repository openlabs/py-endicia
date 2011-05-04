#!/usr/local/bin/python
# coding: latin-1
"""
Integration with
ENDICIA LABEL SERVER
Version 5.0 (Build 3826)

(c) 2010: Openlabs Business Solutions
(c) 2011: Openlabs Technologies & Consulting (P) Ltd.
"""
from api import ShippingLabelAPI, BuyingPostageAPI, \
                ChangingPassPhraseAPI, CalculatingPostageAPI, \
                AccountStatusAPI, RefundRequestAPI, SCANFormAPI
                
from data_structures import FromAddress, ToAddress, \
    LabelRequest, Element


__version__ = '0.2.1'
