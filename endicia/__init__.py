# -*- coding: utf-8 -*-
"""
    __init__

    :copyright: © 2010 by Openlabs Business Solutions
    :copyright: © 2011-2013 by Openlabs Technologies & Consulting (P) Limited
    :license: BSD, see LICENSE for more details.
"""
from api import ShippingLabelAPI, BuyingPostageAPI, \
    ChangingPassPhraseAPI, CalculatingPostageAPI, \
    AccountStatusAPI, RefundRequestAPI, SCANFormAPI

from data_structures import FromAddress, ToAddress, \
    LabelRequest, Element

from .version import __version__
