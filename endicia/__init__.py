#!/usr/local/bin/python
# coding: latin-1
"""
Integration with
ENDICIA LABEL SERVER
Version 5.0 (Build 3826)

(c) 2010 - Today Sharoon Thomas, 
(c) 2010 - Today Open Labs Business Solutions
"""
from api import ShippingLabelAPI, BuyingPostageAPI, \
                ChangingPassPhraseAPI, CalculatingPostageAPI, \
                AccountStatusAPI, RefundRequestAPI, SCANFormAPI
                
from data_structures import FromAddress, ToAddress, \
    LabelRequest, Element


__version__ = '0.2.1'
