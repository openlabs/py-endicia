# -*- coding: utf-8 -*-
"""
    endicia python API

    The Endicia Label Server produces an integrated label image, complete
    with Stealth (hidden) postage, return addresses, verified delivery
    addresses, and service barcodes (Delivery Confirmation, Signature
    Confirmation, Certified Mail with optional Electronic Return Receipt,
    Express Mail, Confirm Services, or customs forms).

    The basic concept around the Endicia Label Server is to provide partners,
    developers, and integrators with the ability to print US Postal Service
    pre-paid shipping labels with postage.

    :copyright: © 2010 by Openlabs Business Solutions
    :copyright: © 2013 by Openlabs Technologies & Consulting (P) Limited
    :license: GPL v 3, see LICENSE for more details.
"""
import urllib
import urllib2

from lxml import etree
from lxml.etree import ETXPath
from .exceptions import RequestError
from .tools import transform_to_xml
from .data_structures import Element


class APIBaseClass(object):
    """
    Base class object other models have to inherit
    """
    def __init__(self, requesterid, accountid, passphrase, test, **kwargs):
        """
        Validates RequesterID, AccountID and passphrase

        :param requesterid: *(Text, 50)* Requester ID (also called Partner ID)
                            uniquely identifies the system making the request.
                            Endicia assigns this ID.

                            The Test Server does not authenticate the
                            RequesterID. Any text value of 1 to 50 characters
                            is valid.
        :param accountid: *(Numeric, 6)* Account ID for the Endicia postage
                            account.
        :param passphrase: *(Text, 64)* Pass Phrase for the Endicia
                   postage account.
        :param test: Yes - Use Sample Postage for testing (Default)

                     No - Use Real Postage
        """
        self.requesterid = requesterid
        self.accountid = accountid
        self.passphrase = passphrase
        self.test = test
        if test:
            self.base_url = 'https://www.envmgr.com/'
            self.base_namespace = 'www.envmgr.com/'
        else:
            self.base_url = 'https://LabelServer.Endicia.com/'
            self.base_namespace = 'www.envmgr.com/'
        self.url = None

        self.required_elements = [
            'RequesterID',
            'AccountID',
            'PassPhrase',
        ]
        self.valid_elements = []
        # A flag to be set to say if the transaction was successful
        self.flags = {
            'Status': None,
            'ErrorMessage': None,
        }
        self.response = self.namespace = None

    def to_xml(self, as_string=True):
        """
        Constructs XML message to be sent and returns it
        """
        raise Exception('Not Implemented Yet')

    def add_data(self, data):
        """
        :param data: dictionary of element and value
        """
        self.__dict__.update(
            dict([
                 (key.lower(), value)
                 for (key, value) in data.items()
                 ])
        )

    @property
    def success(self):
        """
        Returns True if the transaction was success
        """
        if self.flags['Status'] in ['0', 0]:
            return True
        return False

    @property
    def error(self):
        """
        Returns error if exists
        """
        return self.flags['ErrorMessage']

    def _set_flags(self, response):
        """
        Sets flags if any
        """
        xml_result = etree.fromstring(response)
        if self.namespace:
            self.flags['Status'] = ETXPath(
                '//%sStatus' % self.namespace
            )(xml_result)[0].text
            error_message = ETXPath(
                '//%sErrorMessage' % self.namespace
            )(xml_result)
        else:
            error_message = ETXPath(
                '//%sErrorMsg' % self.namespace
            )(xml_result)
            self.flags['Status'] = 0
        self.flags['ErrorMessage'] = error_message and \
            error_message[0].text or None
        self.response = xml_result
        return response

    def request(self, values):
        """
        Sends information to the server and returns the response
        """
        data = urllib.urlencode(values)
        req = urllib2.Request(self.url, data)
        response = urllib2.urlopen(req).read()
        return self._set_flags(response)


class ShippingLabelAPI(APIBaseClass):
    """
    To request a shipping label, use the GetPostageLabel or the
    GetPostageLabelXML Web method of the Endicia Label Server Web Service.
    """
    def __init__(self,
                 label_request,
                 weight_oz,
                 partner_customer_id,
                 partner_transaction_id,
                 mail_class='First',
                 **kwargs):
        """
        :param label_request: Label request object
        :param weight_oz: *(Numeric, 4.1)* Weight of the package, in ounces.
        :param partner_customer_id: *(Text, 25)* A unique identifier for the
                                    partner's end-user printing the label
                                    (user id)
        :param partner_transaction_id: *(Text, 25)* A unique identifier for the
                                    partner's end-user's transaction such as
                                    invoice, transaction number, etc.
        :param mail_class:  Possible values for this field are:

                            **Domestic Options**

                            * Express: Express Mail
                            * First: First-Class Package Service and First-Class Mail Parcel
                            * LibraryMail: Library Mail
                            * MediaMail: Media Mail
                            * StandardPost: Standard Post (formerly called Parcel Post)
                            * ParcelSelect: Parcel Select or Parcel Select Lightweight
                            * Priority: Priority Mail
                            * CriticalMail: CriticalMail

                            **International Options**

                            * ExpressMailInternational
                            * FirstClassMailInternational
                            * FirstClassPackageInternationalService
                            * PriorityMailInternationalGXG (For future use)

        :param requesterid: *(Text, 50)* Requester ID (also called Partner ID)
                            uniquely identifies the system making the request.
                            Endicia assigns this ID.

                            The Test Server does not authenticate the
                            RequesterID. Any text value of 1 to 50 characters
                            is valid.
        :param accountid: *(Numeric, 6)* Account ID for the Endicia postage
                            account.
        :param passphrase: *(Text, 64)* Pass Phrase for the Endicia
                   postage account.
        :param test: Yes - Use Sample Postage for testing (Default)

                     No - Use Real Postage

        All the elements mentioned hereafter are sent to the API by using
        add_data() method.

        Example ::
                shipping_label_api.add_data(
                                    {
                        'LabelSubtype': 'Integrated'
                                    }
                        )

        :param LabelType: (Attribute)

                    * Default - Create label based on mail class(Default)
                    * CertifiedMail - Create Certified Mail label.
                    * DestinationConfirm - Create PLANET Code label using Destination Confirm service.

                        .. note::
                                Use of the DestinationConfirm label type requires special approval from Endicia and the USPS.
                                For more details, contact the Endicia Label Server Team.

                    * Domestic - Create domestic label. Requires use of the LabelSubtype element.
                    * International - Create international label.

                    When the value of this element is set to Domestic or International, the label will be returned as separate images within the Label node of the LabelRequestResponse XML.


        :param LabelSubtype: (Attribute)

                    * Integrated - Create an integrated label. The integrated form type must be specified in the IntegratedFormType element.
                    * None - No label subtype (Default).

                    Required when label type is Domestic. If a value for this element is supplied, it must be set to Integrated when label type is Domestic or International.

        :param LabelSize: (Attribute) -

                For Default label type:

                * 4x6		-			4" W x 6" H (Default)
                * 4x5		-			4" W x 5" H
                * 4x4.5		-			4" W x 4.5" H
                * DocTab    -			4" W x 6.75" H, Eltron Doc-Tab label
                * 6x4       -            6" W x 4" H (not available for Express Mail, EPL2 and ZPLII labels)

                For DestinationConfirm label type:

                * 7x3		-			7" W x 3" H (Default)
                * 6x4		-			6" W x 4" H
                * Dymo30384		-		DYMO #30384 2-part internet label
                * EnvelopeSize10	-	#10 Envelope
                * Mailer7x5		-		7" W x 5" H

                For CertifiedMail label type:

                * 4x6		-			4" W x 6" H (Default)
                * 7x4		-			7" W x 4" H
                * 8x3		-			8" W x 3" H
                * Booklet   -           9" W x 6" H envelope
                * EnvelopeSize10    -     #10 Envelope

        :param ImageFormat: (Attribute)

            * EPL2   :  EPL2 programming language
            * GIF    :  GIF
            * JPEG   :  JPEG
            * PDF    :  PDF
            * PNG    :  PNG (Default)
            * ZPLII  :  ZPL II programming language

            .. note::
                * Only GIF is available for international labels created using LabelType of Default.
                * EPL2 and ZPLII are supported for:
                        - Default label type for domestic mail classes.
                        - Domestic or International label type when used with integrated form type 2976.
                        - International label type when used with Priority Mail, International Flat Rate, Envelope and Small Flat Rate, Box and First Class Mail International.
                * The label image returned in the response for EPL2 and ZPLII labels contain binary data, which require special handling.
        :param ImageResolution: (Attribute)

            * 203 - 203dpi
            * 300 - 300dpi

        :param ImageRotation: (Attribute)

                * None			-		No rotation (Default).
                * Rotate90		-		Rotate label image 90 degrees.
                * Rotate180		-		Rotate label image 180 degrees.
                * Rotate270     -       Rotate label image 270 degrees.

        :param DateAdvance: (Numeric)

                0-7 			-		The number of days to advance date on the indicium.
                                    Maximum value: 7 days.

        :param MailpieceShape: (Text)

                * Card
                * Letter
                * Flat
                * Parcel
                * LargeParcel
                * IrregularParcel
                * OversizedParcel
                * FlatRateEnvelope
                * FlatRatePaddedEnvelope
                * SmallFlatRateBox
                * MediumFlatRateBox
                * LargeFlatRateBox

        :param MailPeiceDimensions:

            * Length (Numeric) - 3.3
            * Width (Numeric) - 3.3
            * Height (Numeric) - 3.3

        :param AutomationRate: (Text)

                * TRUE		-		Use applicable automation rate for selected mail class.
                * FALSE		-		Use retail price. (Default)

                Available only for letter shape mailpiece using First-Class.

        :param Machinable: (Text)

                * TRUE		-		Mailpiece is machinable.(Default)
                * FALSE		-		Mailpiece is non-machinable.

            If a Parcel Select mailpiece marked as machinable is over 35 lbs. in weight or its MailpieceShape is set to OversizedParcel, it will automatically be charged the non-machinable price.

        :param ServiceLevel: (Text)

            * NextDay        -      Next Day
            * 2ndDay         -      Second Day
            * POToAddressee  -      Post Office to Addressee Service

            Applies only to Express Mail.

        :param SundayHolidayDelivery: (Text) - For Express Mail only:

            * TRUE - Request Sunday/Holiday Delivery Service.
            * FALSE - Do not deliver on Sunday or holiday. (Default)

        :param SortType: (Text) - BMC/FiveDigit/MixedBMC/Nonpresorted/Presorted/SCF/SinglePiece/ThreeDigit

            Required for Parcel Select and Standard Mail. Defaults to SinglePiece for mailpieces which do not require a sort type.

        :param IncludePostage: (Text) - TRUE/FALSE - Include Postage on the Label or not
        :param ReplyPostage: (Text) -

            * TRUE - Print reply postage on the label which means the Sender's and Recipient's address will be swapped when printing.
            * FALSE - Do not print reply postage.(Default)

            Can only be with label type of Default or DestinationConfirm. Not available for Express Mail, international mail, integrated labels or when Return Receipt is requested.

        :param ShowReturnAddress: (Text)

            * TRUE - Print sender's address on the label. (Default)
            * FALSE - Do not print sender's address on the label.

            Defaults to TRUE for integrated labels. Even though this element can be used to hide the return address in the label, the USPS rules requires that a return address must appear on the mailpiece in specific circumstances. For more information, see the USPS Domestic Mail Manual.

        :param Stealth: (Text)

            * TRUE - Turn on the use of "stealth" or hidden postage. (Default)
            * FALSE - Turn off stealth.

            * Stealth cannot be used with COD, USPS Insurance, Registered Mail, Automation rate, LabelSize of EnvelopeSize10 and Card shape mailpieces.
            * For Standard Mail, Stealth is turned on.

        :param ValidateAddress: (Text)

            * TRUE - Validate all addresses.(Default)
            * FALSE - Bypass address validation(requires partner to do Address Validation).

        :param SignatureWaiver: (Text) - For Express Mail Only.

            * TRUE - Request waiver of signature for receipt of mailpiece.
            * FALSE - Request signature for receipt of mailpiece. (Default)

            Endicia recommends that the value of this element be set to TRUE.

        :param NoWeekendDelivery: (Text) - For Express Mail Only.

            * TRUE - Request that mailpiece should NOT be delivered on a Saturday.
            * FALSE - FALSE Request that mailpiece can be delivered on a Saturday (Default)

        :param Services:

            * CertifiedMail: (Attribute) - OFF/ON - The default value is ON for CertifiedMail label type; otherwise, it is OFF.
                                          Available for First-Class and Priority Mail.

            * COD: (Attribute) - OFF/ON - (Must affix a completed COD Form 3816 to the mailpiece and take it to the retail USPS counter)

            * DeliveryConfirmation: (Attribute) - OFF/ON - The value of this element is automatically set by the Endicia Label Server based on other elements in the LabelRequest XML. Do not supply a value for this element. It will be ignored.

            * ElectronicReturnReceipt: (Attribute) - OFF/ON - To receive Electronic Return Receipt delivery information, the partner must be registered as a Bulk Proof of Delivery Client with the USPS and develop the software to download the extract file from USPS. The Mailer ID assigned by the USPS for this purpose must be specified in the  BpodClientDUNSNumber element.

            * InsuredMail: (Attribute)

                * OFF - No insurance requested.(Default)
                * ON - USPS Insurance requested (must affix a completed Form 3813 or 3813-P to the mailpiece and take it to the retail USPS counter).
                * USPSOnline - USPS Online Insurance requested.
                * Endicia - Endicia Insurance requested (Maximum insurable value: $10,000)

                USPS Online Insurance is available only for mailpieces with Delivery or Signature Confirmation.

                USPS insurance is not allowed for International Mail or when Stealth or ReplyPostage is set to TRUE.

                Endicia insurance fee is not included in the postage price. It is billed to your account.

            * RestrictedDelivery: (Attribute) - OFF/ON
            * ReturnReceipt: (Attribute)

                * OFF  -  Return Receipt not requested.(Default)
                * ON - Return Receipt requested(must affix a completed Return Receipt Form 3811 to the mailpiece and take it to the retail USPS counter).

                Can only be used with label type of Default or DestinationConfirm. Not supported for International Mail.

            * SignatureConfirmation: (Attribute) - OFF/ON

                Can only be used with label type of Default.

        :param TrackingNumber: (Text)

            * 22 - PIC
            * 14 - Planet Code
            * 12 - Planet Code

            This element must not be supplied when label type is Domestic. Not used for international mail.

        :param CostCenter: (Numeric, 8) - Cost-center code for accounting purposes.
        :param Value: (Currency, 5.2) - Value of the MailPiece.

            When a customs form is requested and the individual customs item elements are not supplied, then this value should be set to the total customs value. Ignored when CustomsInfo is supplied.

        :param InsuredValue: (Currency, 5.2) - Required if insurance or COD is requested for the mailpiece
        :param CODAmount: (Currency, 5.2) - Required if COD is requested for the mailpiece.
        :param Description: (Text, 50) Description of the item shipped. Used for authentication by recipient.

            When requesting an International Mail label or a customs form, a value is required if the LabelRequest XML does not contain any customs declaration elements.

        :param IntegratedFormType: (Text)

            * Form2976  Form 2976
            * Form2976A Form 2976-A
            * Required when label subtype is Integrated.

        :param CustomsFormType: (Text) -

            * None      - No Customs Form (Default)
            * Form2976  - Same as CN22
            * Form2976A - Same as CP72
            * Used for APO/FPO and other destinations as required by USPS regulations. Do not use with integrated labels or international mail.

        :param CustomsFormImageFormat: (Text)

            * GIF : GIF
            * JPEG : JPEG
            * PDF : PDF
            * PNG : PNG (Default)
            * Do not use with integrated labels or international mail.

        :param CustomsFormImageResolution: (Text) -

            * 300 - 300 dpi

        :param OriginCountry: (Text) - Country of Origin of the item. This must be a valid, USPS recognized country.

            Required for International Mail items or when requesting a customs form. Ignored when CustomsInfo is supplied.

        :param ContentsType: (Text) - Documents/Gift/Merchandise/Other/ReturnedGoods/Sample

                        Category of the customs items. Used in customs forms and international labels.

            * Default value is Other.
            * Value of ReturnedGoods is not available for Priority Mail International Flat Rate Envelope and Customs Form 2976.
            * Ignored when CustomsInfo is supplied.

        :param ContentsExplanation: (Text) - Explanation of the customs items. Used in customs forms and international labels.

            * Required if ContentsType is Other.
            * Ignored when CustomsInfo is supplied.

        :param NonDeliveryOption: (Text) - Abandon / Return(Default)

                         Non-delivery instructions.Used in customs forms and international labels. Ignored when CustomsInfo is supplied.

        :param ReferenceID: (Text) - A Reference value for the logs
        :param **PartnerCustomerID**: (Text) - A unique identifier for the partner's end-user printing the label

        :param **PartnerTransactionID**: (Text) - A unique identifier for the partner's end-user's transaction such as invoice, transaction number, etc.

        :param BpodClientDunsNumber: (Numeric - 9) - Mailer ID of the partner assigned by USPS.

            Allows the partner to receive Electronic Return Receipt information from USPS in an extract file uniquely generated for them, provided they have established themselves with USPS as a Bulk Proof of Delivery Client.

        :param RubberStamp1: (Text, 50) - User-supplied text to print on the label.
        :param RubberStamp2: (Text, 50) - User-supplied text to print on the label.
        :param RubberStamp3: (Text, 50) - User-supplied text to print on the label.

        :param EntryFacility: (Text) - Postal facility where the mail is entered. If this element is not set to Other, the ZIP Code of this facility must be specified in POZipCode. Required for Parcel Select and Standard Mail.

            * DBMC - Destination BMC
            * DDU  - Destination Delivery Unit
            * DSCF - Destination Sectional Center Facility
            * OBMC - Origin BMC
            * Other - Other postal facility (Default)


        :param POZipCode: (Text) - ZIP Code of Post Office or collection box where item is mailed. May be different than FromPostalCode. Used for determining the zone and calculating the postage price. Required when EntryFacility is not set to Other. The value of this element must contain the zip code of the postal facility specified in EntryFacility.

        :param ShipDate: (Date) - MM/DD/YYYY - Date mailpiece is shipped. Required for Express Mail Sunday/Holiday Delivery Service. Ignored for other mail classes.
        :param ShipTime: (Time) - HH:MM AM or HH:MM PM - Time mailpiece is shipped. Applies only to Express Mail Sunday/Holiday Delivery Service. Ignored for other mail classes. If this element is not supplied, it defaults to 12:01 AM.

        :param EelPfc: (Text) - Exemption or Exclusion Legend (EEL) or a Proof of Filing Citation (PFC).
                    Required for shipments to an international destination or to an overseas U.S. Territory. It is recommended to supply a value for this element as the USPS will likely require it in the near future.

        :param CustomsCertify: (Text) - TRUE/FALSE -  TRUE means the customs information is certified to be correct and the CustomsSigner name should be printed.

        :param CustomsSigner: (Text - 47) -  Name of person certifying that the customs information is correct. This name prints on the customs form in place of a signature if CustomsCertify is TRUE. Required if CustomsCertify is TRUE.

        :param ResponseOptions: (Node) - Optional XML elements to include in the LabelRequestResponse.

            * PostagePrice (Text) - TRUE/FALSE - TRUE means the response contains the PostagePrice node.

        :param CustomsInfo: (Node) - Required when using Integrated Labels.

            * ContentsType: (Text) - Documents/Gift/Merchandise/Other/ReturnedGoods/Sample
            * ContentsExplanation: (Text) - Explanation of the customs items. Required if ContentsType is Other.
            * RestrictionType: (Text) None/Other/Quarantine/SanitaryPhytosanitaryInspection
            * RestrictionCommments: (Text, 25) -

                * None (Default)
                * Other
                * Quarantine
                * SanitaryPhytosanitaryInspection

            * SendersCustomsReference: (Text, 14) - Sender's Customs Reference
            * ImportersCustomsReference: (Text, 40) - Importer's Customs Reference
            * LicenseNumber: (Text, 16) - License Number
            * CertificateNumber: (Text, 12) - Certificate Number
            * InvoiceNumber: (Text, 15) - Invoice Number
            * NonDeliveryOption: (Text) - Abondon / Return (Default)
            * InsuredNumber: (Text, 13) - *For Future Use*
            * EelPfc: (Text, 35) -

                * Exemption or Exclusion Legend (EEL) or a Proof of Filing Citation (PFC).
                * Required for shipments to an international destination or to an overseas U.S. Territory.
                * It is recommended to supply a value for this element as the USPS will likely require it in the near future.

            * **CustomsItems**: (Node) - [1 .. 30]

                * **Description** (Text, 30) - Description of the customs item.
                * **Quantity** (Numeric, 3) - Quantity of the customs item. Must be greater than zero.
                * **Weight**  (Numeric, 4) - Weight of the customs item. Must be specified in whole ounces and greater than zero and cannot exceed 1120 ounces (70 pounds).
                * **Value** (Currency, 5.2) - Value of the customs item. Must be greater than zero.
                * HSTariffNumber (Text, 6) - 6-digit HS tariff number.
                * CountryOfOrigin (Text, 2) - Two character country code of the country where the customs items originated.

        **The elements mentioned below are not supplied directly but via *FromAddress* and *ToAddress* Methods**

        :param FromName: (Text, 47) - Either FromName or FromCompany must contain a value. For customs forms, this element must contain at least two words.

        :param FromCompany: (Text, 47) - Either FromName or FromCompany must contain a value.

        :param **ReturnAddress1**: (Text, 47) - First delivery address line of sender
        :param ReturnAddress2: (Text, 47) - Second delivery address line of sender
        :param ReturnAddress3: (Text, 47) - Third delivery address line of sender
        :param ReturnAddress4: (Text, 47) - Fourth delivery address line of sender

            .. note::
                Do not use **ReturnAddress3** and **ReturnAddress4** when label type is Domestic or International and a label subtype value is supplied

        :param **FromCity**: (Text, 50) - Sender's city.
                        Allowed characters: A-Z a-z hyphen period space

        :param **FromState**: (Text, 25) - Sender's state or province
        :param **FromPostalCode**: (Text, 10) - Sender's postal code. The format is either ZIP5 only or ZIP+4 for US addresses.
        :param FromZIP4: (Text, 4) - +4 add-on for US addresses. Ignored if FromPostalCode contains the ZIP4 value.
        :param FromCountry: (Text, 50) - Sender's country. This value should be left blank for USA addresses.

        :param FromPhone: (Text, 10) Phone number of sender (required for Express Mail and international mail). 10 digits required (including area code) with no punctuation. Use format: 2125551234

        :param FromEMail: (Text, 64) - E-mail address of sender.
        :param ToName: (Text, 47) - Recipient's name. For Express Mail and international mail: Either ToName or ToCompany must contain a value.
        :param ToCompany: (Text, 47) - Recipient's company name. For Express Mail and international mail: Either ToName or ToCompany must contain a value.
        :param **ToAddress1**: (Text, 47) - First delivery address line of recipient.

            * A value is optional only when ToCompany contains a value.
            * Express Mail labels are limited to four lines in the destination address for all label sizes.
            * 4X5 and 4x4.5 labels are limited to five lines in the destination address.

        :param ToAddress2: (Text, 47) - Second delivery address line of recipient.
        :param ToAddress3: (Text, 47) - Third delivery address line of recipient.
        :param ToAddress4: (Text, 47) - Fourth delivery address line of recipient.

            .. note::
                Do not use ToAddress3 and ToAddredd4 when label type is domestic.

        :param **ToCity**: (Text, 50) - Recipient's City
        :param **ToState**: (Text, 25) - Recipient's state or province
        :param **ToPostalCode**: (Text, 4/15) - Recipient's postal code.

            * For Domestic Mail, the format is ZIP5 (required).
            * For International Mail (optional).


        :param ToZIP4: (Text, 4) - +4 add-on for US addresses
        :param ToDeliveryPoint: (Text, 2) - +2 Delivery Point for US Addresses
        :param ToCountry: (Text, 50) - Recipient's Country. Required for International Mail.  Ignored when label type is International and a label subtype value is supplied. In this case, the ToCountryCode element must be used.

        :param ToCountryCode: (Text, 2) - ToCountryCode Text 2 Two-character country code of the recipient's country. Required when label type is International and a label subtype value is supplied.

        :param ToPhone: (Text, 10/30) - Recipient's Phone Number.

            * 10 For Domestic mail: 10 digits including area code with no punctuation. For example: 2125551234. If supplied value is not in the correct format, it will be ignored.
            * 30 For International mail, up to 30 digits with no punctuation.

        :param ToEMail: (Text, 64) - E-mail address of recipient.

        **The following five sets of customs item elements are ignored when CustomsInfo is supplied.**

                    Set 1

                    #. CustomsDescription1 (Text, 50)
                    #. CustomsQuantity1 (Numeric, 8)
                    #. CustomsWeight1 (Numeric, 4)
                    #. CustomsValue1 (Currency, 5.2)
                    #. CustomsCountry1 (Text, 50)

            Set 2

                    #. CustomsDescription2 (Text, 50)
                    #. CustomsQuantity2 (Numeric, 8)
                    #. CustomsWeight2 (Numeric, 4)
                    #. CustomsValue2 (Currency, 5.2)
                    #. CustomsCountry2 (Text, 50)

            Set 3

                    #. CustomsDescription3 (Text, 50)
                    #. CustomsQuantity3 (Numeric, 8)
                    #. CustomsWeight3 (Numeric, 4)
                    #. CustomsValue3 (Currency, 5.2)
                    #. CustomsCountry3 (Text, 50)

            Set 4

                    #. CustomsDescription4 (Text, 50)
                    #. CustomsQuantity4 (Numeric, 8)
                    #. CustomsWeight4 (Numeric, 4)
                    #. CustomsValue4 (Currency, 5.2)
                    #. CustomsCountry4 (Text, 50)

            Set 5

                    #. CustomsDescription5 (Text, 50)
                    #. CustomsQuantity5 (Numeric, 8)
                    #. CustomsWeight5 (Numeric, 4)
                    #. CustomsValue5 (Currency, 5.2)
                    #. CustomsCountry5 (Text, 50)

        """
        super(ShippingLabelAPI, self).__init__(**kwargs)

        self.labelrequest = label_request
        self.mailclass = mail_class
        self.weightoz = weight_oz
        self.partnercustomerid = partner_customer_id
        self.partnertransactionid = partner_transaction_id
        #
        # Above are the required elements
        #
        self.dateadvance = 0
        self.mailpieceshape = None
        self.mailpiecedimensions = {
            'Length': 0,
            'Width': 0,
            'Height': 0
        }
        self.machinable = 'TRUE'
        self.servicelevel = None
        self.sundayholidaydelivery = 'FALSE'
        self.sorttype = 'SinglePiece'
        self.includepostage = 'TRUE'
        self.replypostage = 'FALSE'
        self.showreturnaddress = 'TRUE'
        self.stealth = 'TRUE'
        self.validateaddress = 'TRUE'
        self.signaturewaiver = 'TRUE'
        self.noweekenddelivery = 'FALSE'
        self.services = {
            'CertifiedMail': 'ON',
            'COD': 'OFF',
            'ElectronicReturnReceipt': 'OFF',
            'InsuredMail': 'OFF',
            'RestrictedDelivery': 'OFF',
            'ReturnReceipt': 'OFF',
            'SignatureConfirmation': 'OFF'
        }
        self.required_elements.extend([
                                      'MailClass',
                                      'WeightOz',
                                      'PartnerCustomerID',
                                      'PartnerTransactionID',
                                      'ReturnAddress1',
                                      'FromCity',
                                      'FromState',
                                      'FromPostalCode',
                                      'ToAddress1',
                                      'ToCity',
                                      'ToState',
                                      'ToPostalCode'
                                      ])
        self.valid_elements.extend(self.required_elements)
        self.valid_elements.extend([
            'LabelSubtype',
            'CustomsCertify',
            'CustomsSigner',
            'EelPfc',
            'DateAdvance',
            'MailpieceShape',
            'CustomsInfo',
            'MailpieceDimensions',
            'Machinable',
            'ServiceLevel',
            'SundayHolidayDelivery',
            'SortType',
            'IncludePostage',
            'ReplyPostage',
            'ShowReturnAddress',
            'Stealth',
            'ValidateAddress',
            'SignatureWaiver',
            'NoWeekendDelivery',
            'Value',
            'InsuredValue',
            'CODAmount',
            'Description',
            'CustomsFormType',
            'IntegratedFormType',
            'CustomsFormImageFormat',
            'CustomsFormImageResolution',
            'OriginCountry',
            'ContentsType',
            'ContentsExplanation',
            'NonDeliveryOption',
            'ReferenceID',

            'FromName',
            'FromCompany',
            'ReturnAddress2',
            'ReturnAddress3',
            'ReturnAddress4',
            'FromPhone',
            'FromEMail'

            'ToName',
            'ToCompany',
            'ToCountry',
            'ToCountryCode',
            'ToPhone',
            'ToEMail',
            'ToAddress2',
            'ToAddress3',
        ]
        )
        self.namespace = '{' + self.base_namespace + 'LabelService}'
        self.url = self.base_url + \
            "LabelService/EwsLabelService.asmx/GetPostageLabelXML"

    def to_xml(self, as_string=True):
        """
        Convert the data To xml
        """
        labelrequest = etree.Element("LabelRequest", **self.labelrequest.data)
        for element in self.valid_elements:
            if not hasattr(self, element.lower()):
                #
                # If element is not there then bypass it
                #
                continue
            value = getattr(self, element.lower())
            if value:
                if type(value) == dict and not any(value.values()):
                    # If the element is a dictionary and there are
                    # no valid values, then dont add it to the XML
                    continue
                transform_to_xml(labelrequest, value, element)
        if as_string:
            return etree.tostring(labelrequest, pretty_print=True)
        else:
            return labelrequest

    def send_request(self):
        """
        Sends the request to the server
        """
        response = self.request({'labelRequestXML': self.to_xml()})
        if self.success:
            return response
        else:
            raise RequestError(self.error)


class BuyingPostageAPI(APIBaseClass):
    """
    To add postage to an account, use the BuyPostage
    or the BuyPostageXML Web method of the Endicia Label
    Server Web Service.
    """
    def __init__(self,
                 request_id,
                 recredit_amount,
                 **kwargs):
        '''
        :param request_id: *(Text,50)* Request ID to uniquely identify this
                           Recredit request. This will be returned in response.
        :param recredit_amount: Amount of postage, in dollars, to add to the
                                account. Either use a predefined amount from
                                the list or enter any value up to 99999.99.

                                The minimum amount of postage that can
                                be purchased is $10. The maximum
                                amount is based on the settings of the
                                account.

                                Given predefined amounts are - $10, $25, $50,
                                $100, $250, $500, $1000, $2500, $5000, $7500, $10000,
                                $20000. Must be in given in Text.

                                Else in currency any amount, at least $10.00
                                and up to $99,999.99, in unit of dollars and
                                rounded to the nearest cent.

        :param requesterid: (Text, 50) : Requester ID (also called Partner ID) is used to uniquely identify the system making the request. This ID is assigned by Endicia.
        :param accountid: (Numeric, 6) : Account ID for the Endicia postage account.
        :param passphrase: (Text, 64) : Pass Phrase for the Endicia postage account.
        :param test: Yes - Use Sample Postage for testing (Default)

                     No - Use Real Postage
        '''
        super(BuyingPostageAPI, self).__init__(**kwargs)

        self.requestid = request_id
        self.recredit_amount = recredit_amount
        self.namespace = '{' + self.base_namespace + 'LabelService}'
        self.url = self.base_url + \
            "LabelService/EwsLabelService.asmx/BuyPostageXML"

    def to_xml(self, as_string=True):
        """
        Convert the data To xml
        """
        recreditrequest = etree.Element("RecreditRequest")

        transform_to_xml(recreditrequest,
                         self.requestid, 'RequestID')
        transform_to_xml(recreditrequest,
                         self.requesterid, 'RequesterID')
        transform_to_xml(recreditrequest,
                         [
                         Element('AccountID', self.accountid),
                         Element('PassPhrase', self.passphrase),
                          ],
                         'CertifiedIntermediary')
        transform_to_xml(recreditrequest,
                         self.recredit_amount, 'RecreditAmount')
        if as_string:
            return etree.tostring(recreditrequest, pretty_print=True)
        else:
            return recreditrequest

    def send_request(self):
        """
        Sends the request to the server
        """
        response = self.request({'recreditRequestXML': self.to_xml()})
        if self.success:
            return response
        else:
            raise RequestError(self.error)


class ChangingPassPhraseAPI(APIBaseClass):
    """
    To change the Pass Phrase for an account, use the API
    """
    def __init__(self,
                 request_id,
                 new_pass_phrase,
                 **kwargs):
        '''
        :param request_id: *(Text-50)* Request ID to uniquely identify this
                          Recredit request. This will be returned in response.
        :param new_pass_phrase: *(Text-64)* New Pass Phrase for the Endicia
                                postage account.Pass Phrase must be at least 5
                                characters long with a maximum of 64 characters.
                                For added security, the PassPhrase should be at
                                least 10 characters long and include more than
                                one word, use at least one uppercase and
                                lowercase letter, one number and one non-text
                                character (e.g. punctuation). A PassPhrase
                                which has been used previously will be rejected.
        :param requesterid: (Text, 50) : Requester ID (also called Partner ID) is used to uniquely identify the system making the request. This ID is assigned by Endicia.
        :param accountid: (Numeric, 6) : Account ID for the Endicia postage account.
        :param passphrase: (Text, 64) : Pass Phrase for the Endicia postage account.
        :param test: Yes - Use Sample Postage for testing (Default)

                     No - Use Real Postage
        '''

        super(ChangingPassPhraseAPI, self).__init__(**kwargs)

        self.requestid = request_id
        self.new_pass_phrase = new_pass_phrase
        self.namespace = '{' + self.base_namespace + 'LabelService}'
        self.url = self.base_url + \
                    "LabelService/EwsLabelService.asmx/ChangePassPhraseXML"

    def to_xml(self, as_string=True):
        """
        Convert the data To xml
        """
        changepassphraserequest = etree.Element("ChangePassPhraseRequest")

        transform_to_xml(changepassphraserequest,
                         self.requestid, 'RequestID')
        transform_to_xml(changepassphraserequest,
                         self.requesterid, 'RequesterID')
        transform_to_xml(changepassphraserequest,
                         [
                          Element('AccountID', self.accountid),
                          Element('PassPhrase', self.passphrase),
                          ],
                         'CertifiedIntermediary')
        transform_to_xml(changepassphraserequest,
                         self.new_pass_phrase, 'NewPassPhrase')

        if as_string:
            return etree.tostring(changepassphraserequest, pretty_print=True)
        else:
            return changepassphraserequest

    def send_request(self):
        """
        Sends the request to the server
        """
        response = self.request({'changePassPhraseRequestXML': self.to_xml()})
        if self.success:
            return response
        else:
            raise RequestError(self.error)


class CalculatingPostageAPI(APIBaseClass):
    """
    Calculate the Postage and Fees for a Single Mailpiece
    """
    def __init__(self,
                 mailclass,
                 weightoz,
                 from_postal_code,
                 to_postal_code,
                 to_country_code,
                 **kwargs):
        '''

        :param requesterid: (Text, 50) : Requester ID (also called Partner ID) is used to uniquely identify the system making the request. This ID is assigned by Endicia.

        :param mailclass: (Text)

            * Domestic:

                #. Express : Express Mail
                #. First : First-Class Mail
                #. LibraryMail : Library Mail
                #. MediaMail : Media Mail
                #. ParcelPost : Parcel Post
                #. ParcelSelect : Parcel Select
                #. Priority : Priority Mail
                #. StandardMail : Standard Mail

            * International:

                #. ExpressMailInternational : Express Mail International
                #. FirstClassMailInternational : First-Class Mail International
                #. PriorityMailInternational :  Priority Mail International

        :param weightoz: (Numeric, 4.1) : Weight of the package, in ounces.

        :param from_postal_code: (Text, 5) : Sender's postal code. The format is ZIP5. For Parcel Select and Standard Mail, the value of this element contains the zip code of the postal facility specified in EntryFacility. Recipient's postal code.

        :param to_postal_code: (Text)

            * 5: For Domestic Mail, the format is ZIP5 (required).
            * 15: For International Mail (optional).

        :param to_country_code: (Text, 2) : Two character country code of the recipient's country. Required for International Mail. Use either ToCountry or ToCountryCode.

        All the elements mentioned hereafter are sent to the API by using add_data() method.
        =====================================================================================
        Example ::
                shipping_label_api.add_data(
                                    {
                        'Pricing': 'CommercialBase'
                                    }
                        )

        :param CertifiedIntermediary: (Node) : Certified Intermediary (CI) account authentication information.
            * AccountID: (Numeric, 6) : Account ID for the Endicia postage account.
            * PassPhrase: (Text, 64) : Pass Phrase for the Endicia postage account.

        :param Pricing: (Text)

            * CommercialBase : Commercial Base pricing.
            * CommercialPlus : Commercial Plus pricing.
            * Retail : Retail pricing.

            If this element is not supplied, pricing will be based on the MailClass and any qualified discounts available to AccountID.

            .. note::
                If this element is set to CommercialPlus, but the account does not qualify for such pricing, the Web method will return an error.

        :param MailpieceShape: (Text) : Card / Letter / Flat / Parcel / LargeParcel / IrregularParcel / OversizedParcel / FlatRateEnvelope / FlatRatePaddedEnvelope / SmallFlatRateBox / MediumFlatRateBox / LargeFlatRateBox

            * Shape of the mailpiece.
            * Starting in May 2009, FlatRateBox has been replaced with MediumFlatRateBox.
            * The Flat Rate Padded Envelope is only available to qualifying Priority Mail Commercial Plus customers. The Label Server will return an error if this shape is used with any other pricing.

        :param MailpieceDimensions: (Node):  Dimensions of the mailpiece. Required for calculating Cubic pricing and for Priority Mail mailpieces going to Zones 5-8 which are over 1 cubic foot. Ignored if MailpieceShape is set to either LargeParcel or OversizedParcel. **All values must be in inches.**

            * Length (Numeric, 3.3) : Length of the mailpiece.
            * Width (Numeric, 3.3) : Width of the mailpiece.
            * Height (Numeric, 3.3) : Height (or thickness) of the mailpiece.

        :param AutomationRate: (Text)

            * TRUE : Use applicable automation rate for selected mail class.
            * FALSE : Use retail price. (Default)
            * Available only for letter shape mailpiece using First-Class.

        :param Machinable: (Text)

            * TRUE : Package is machinable. (Default) Package is non-machinable.
            * FALSE : If a Parcel Select mailpiece marked as machinable is over 35 lbs. in weight or its MailpieceShape is set to OversizedParcel, it will automatically be charged the non- machinable rate.

        :param ServiceLevel: (Text)

        :param SundayHolidayDelivery: (Text) : For Express Mail only:

            * TRUE : Request Sunday/Holiday Delivery Service.
            * FALSE : Do not deliver on Sunday or holiday. (Default)

        :param SortType: (Text) : BMC / FiveDigit / MixedBMC / Nonpresorted / Presorted / SCF / SinglePiece / ThreeDigit

            * Sort level for applicable mail classes.
            * Required for Parcel Select and Standard Mail.
            * Defaults to SinglePiece for mailpieces which do not require a sort type.

        :param Services: (Node) : Special Services requested for the package.

            * CertifiedMail (Attribute)

                * OFF : Certified Mail not requested.
                * ON : Certified Mail requested.

            * COD (Attribute)

                * OFF : COD not requested.
                * ON : COD requested.

            * DeliveryConfirmation (Attribute)

                * OFF : Delivery Confirmation not requested. (Default)
                * ON : Delivery Confirmation requested.

            * ElectronicReturnReceipt (Attribute)

                * OFF : Electronic Return Receipt not requested. (Default)
                * ON : Electronic Return Receipt requested.

             * InsuredMail (Attribute)

                * OFF : No insurance requested. (Default)
                * ON : USPS Insurance requested.
                * UspsOnline : USPS Online Insurance requested.
                * ENDICIA : Endicia Insurance requested (Maximum insurable value: $10,000)

                .. note::
                    * USPS Online Insurance is available only for mailpieces with Delivery or Signature Confirmation.
                    * USPS Insurance is not allowed for International Mail.
                    * Endicia insurance fee is not included in the postage price. It is billed to your account.

            * RestrictedDelivery (Attribute)

                * OFF : Restricted Delivery not requested.(Default)
                * ON : Restricted Delivery requested.

            * ReturnReceipt (Attribute)

                * OFF : Return Receipt not requested.(Default)
                * ON : Return Receipt requested.

            * SignatureConfirmation (Attribute)

                * OFF : Signature Confirmation not requested. (Default)
                * ON : Signature Confirmation requested.

        :param Value: (Currency, 5.2) : Value of the item(s) in the mailpiece
        :param CODAmount: (Currency, 5.2) : COD amount to collect. Required if COD is requested for the mailpiece.
        :param InsuredValue: (Currency, 5.2) : Insured value of the mailpiece. Required if insurance or COD is requested for the mailpiece.
        :param EntryFacility: (Text) : Postal facility where the mail is entered. The zip code of this facility must be specified in POZipCode. Required for Parcel Select and Standard Mail.

            * DBMC : Destination BMC
            * DDU : Destination Delivery Unit
            * DSCF : Destination Sectional Center Facility
            * OBMC : Origin BMC
            * Other : Other postal facility (Default)

        :param ToCountry: (Text, 50) : Recipient's country. Required for International Mail. Use either ToCountry or ToCountryCode.

        :param ShipDate: (Date, MM/DD/YYYY) : Date mailpiece is shipped. Required for Express Mail Sunday/Holiday Delivery Service. Ignored for other mail classes.
        :param ShipTime: (Time, HH:MM AM or HH:MM PM) : Time mailpiece is shipped. Applies only to Express Mail Sunday/Holiday Delivery Service. Ignored for other mail classes. If this element is not supplied, it defaults to 12:01 AM.

        :param ResponseOptions: (Node) : Optional XML elements to include in the PostageRateResponse.

            * PostagePrice (Attribute)

                * TRUE : TRUE means the response contains the PostagePrice node.
                * FALSE
        '''
        super(CalculatingPostageAPI, self).__init__(**kwargs)

        self.mailclass = mailclass
        self.weightoz = weightoz
        self.frompostalcode = from_postal_code
        self.topostalcode = to_postal_code
        self.tocountrycode = to_country_code
        self.valid_elements.extend([
                                    'RequesterID',
                                    'MailClass',
                                    'Pricing',
                                    'WeightOz',
                                    'MailpieceShape',
                                    'MailpieceDimensions',
                                    'AutomationRate',
                                    'Machinable',
                                    'ServiceLevel',
                                    'SundayHolidayDelivery',
                                    'SortType',
                                    'Services',
                                    'Value',
                                    'CODAmount',
                                    'InsuredValue',

                                     'EntryFacility',
                                     'FromPostalCode',
                                     'ToPostalCode',
                                     'ToCountry',
                                     'ToCountryCode',
                                     'ShipDate',
                                     'ShipTime'

                                     ]
        )
        self.namespace = '{' + self.base_namespace + 'LabelService}'
        self.url = self.base_url + \
                    "LabelService/EwsLabelService.asmx/CalculatePostageRateXML"

    def to_xml(self, as_string=True):
        """
        Convert the data To xml
        """
        calculatepostagerequest = etree.Element("PostageRateRequest")

        transform_to_xml(calculatepostagerequest,
                         self.requesterid, 'RequesterID')
        transform_to_xml(calculatepostagerequest,
                         [
                          Element('AccountID', self.accountid),
                          Element('PassPhrase', self.passphrase),
                          ],
                         'CertifiedIntermediary')

        for element in self.valid_elements:
            if not hasattr(self, element.lower()):
                # If element is not there then bypass it
                continue
            value = getattr(self, element.lower())
            transform_to_xml(calculatepostagerequest, value, element)

        transform_to_xml(calculatepostagerequest,
                         {'PostagePrice': 'TRUE'},
                         'ResponseOptions')
        if as_string:
            return etree.tostring(calculatepostagerequest, pretty_print=True)
        else:
            return calculatepostagerequest

    def send_request(self):
        """
        Sends the request to the server
        """
        response = self.request({'postageRateRequestXML': self.to_xml()})
        if self.success:
            return response
        else:
            raise RequestError(self.error)


class AccountStatusAPI(APIBaseClass):
    """
    To get the status of an account
    """
    def __init__(self,
                 request_id,
                 **kwargs):
        '''
        :param request_id: ID to uniquely identify this request. (Returned in
                           response)
        :param requesterid: *(Text, 50)* Requester ID (also called Partner ID)
                            uniquely identifies the system making the request.
                            Endicia assigns this ID.

        :param accountid: *(Numeric, 6)* Account ID for the Endicia postage
                            account.
        :param passphrase: *(Text, 64)* Pass Phrase for the Endicia
                   postage account.
        :param test: Yes - Use Sample Postage for testing (Default)

                     No - Use Real Postage
        '''
        super(AccountStatusAPI, self).__init__(**kwargs)

        self.requestid = request_id
        self.namespace = '{' + self.base_namespace + 'LabelService}'
        self.url = self.base_url + \
            "LabelService/EwsLabelService.asmx/GetAccountStatusXML"

    def to_xml(self, as_string=True):
        """
        Convert the data to XML
        """
        get_account_status_request = etree.Element("AccountStatusRequest")
        transform_to_xml(
            get_account_status_request,
            self.requestid, 'RequestID')
        transform_to_xml(
            get_account_status_request,
            self.requesterid, 'RequesterID')
        transform_to_xml(
            get_account_status_request,
            [
                Element('AccountID', self.accountid),
                Element('PassPhrase', self.passphrase),
                ],
            'CertifiedIntermediary')
        if as_string:
            return etree.tostring(
                get_account_status_request, pretty_print=True
                )
        else:
            return get_account_status_request

    def send_request(self):
        """
        Sends the request to the server
        """
        response = self.request({'accountStatusRequestXML': self.to_xml()})
        if self.success:
            return response
        else:
            raise RequestError(self.error)


class RefundRequestAPI(APIBaseClass):
    "To cancel a shipment and request refund for it"
    def __init__(self,
                 pic_numbers,
                 production_url="",
                 **kwargs):
        '''
        :param accountid: (Numeric, 6) : Account ID for the Endicia postage account.
        :param passphrase: (Text, 64) : Pass Phrase for the Endicia postage account.
        :param test: Yes - Use Sample Postage for testing (Default)

                     No - Use Real Postage
        :param pic_numbers: [(Numeric, 30)] : List of Package PIC Number
                    (Tracking Number)
        :param production_url: RefundRequest requires a separate production URL
            which is sent to the shipper in a separate 'WELCOME' mail by Endicia
        '''
        super(RefundRequestAPI, self).__init__(**kwargs)

        self.pic_numbers = pic_numbers
        self.namespace = ''
        if production_url:
            self.url = self.production_url
        else:
            self.url = 'https://www.endicia.com/ELS/ELSServices.cfc?wsdl'

    def to_xml(self, as_string=True):
        """
        Convert the data to XML
        """
        refund_request = etree.Element("RefundRequest")

        transform_to_xml(refund_request,
                         self.accountid, 'AccountID')
        transform_to_xml(refund_request,
                         self.passphrase, 'PassPhrase')
        transform_to_xml(refund_request,
                         self.test, 'Test')

        transform_to_xml(refund_request, [
            Element('PICNumber', pic_number) for pic_number in self.pic_numbers
        ], 'RefundList')

        if as_string:
            return etree.tostring(refund_request, pretty_print=True)
        else:
            return refund_request

    def send_request(self):
        """
        Sends the request to the server
        """
        response = self.request({
            'method': 'RefundRequest',
            'XMLInput': self.to_xml()})
        if self.success:
            return response
        else:
            raise RequestError(self.error)


class SCANFormAPI(APIBaseClass):
    "To allow usage of SCAN service"
    def __init__(self,
                 pic_numbers,
                 production_url="",
                 **kwargs):
        '''
        :param accountid: (Numeric, 6) : Account ID for the Endicia postage account.
        :param passphrase: (Text, 64) : Pass Phrase for the Endicia postage account.
        :param test: Yes - Use Sample Postage for testing (Default)

                     No - Use Real Postage
        :param pic_numbers: [(Numeric, 30)] : List of Package PIC Number
                    (Tracking Number)
        :param production_url: RefundRequest requires a separate production URL
            which is sent to the shipper in a separate 'WELCOME' mail by Endicia
        '''
        super(SCANFormAPI, self).__init__(**kwargs)

        self.pic_numbers = pic_numbers
        self.namespace = ''
        if production_url:
            self.url = self.production_url
        else:
            self.url = 'https://www.endicia.com/ELS/ELSServices.cfc?wsdl'

    def to_xml(self, as_string=True):
        """
        Convert the data to XML
        """
        scan_request = etree.Element("SCANRequest")

        transform_to_xml(scan_request,
                         self.accountid, 'AccountID')
        transform_to_xml(scan_request,
                         self.passphrase, 'PassPhrase')
        transform_to_xml(scan_request,
                         self.test, 'Test')

        transform_to_xml(scan_request, [
            Element('PICNumber', pic_number) for pic_number in self.pic_numbers
        ], 'SCANList')
        if as_string:
            return etree.tostring(scan_request, pretty_print=True)
        else:
            return scan_request

    def send_request(self):
        """
        Sends the request to the server
        """
        response = self.request({
            'method': 'SCANRequest',
            'XMLInput': self.to_xml()})
        if self.success:
            return response
        else:
            raise RequestError(self.error)
