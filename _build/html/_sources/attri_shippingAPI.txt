.. _additional_param:

Parameters for Shipping Label API
=================================

#. Test (Attribute) - Yes/No

    Yes - Use sample postage for testing.

    No - Use real postage. (Default)


#. LabelType (Attribute)

	* Default - Create label based on mail class(Default)
	* CertifiedMail - Create Certified Mail label.
	* DestinationConfirm - Create PLANET Code label using Destination Confirm service.

		.. note:: 
			Use of the DestinationConfirm label type requires special approval from Endicia and the USPS. 
			For more details, contact the Endicia Label Server Team.

	* Domestic - Create domestic label. Requires use of the LabelSubtype element.
	* International - Create international label. When the value of this element is set to Domestic or International, the label will be returned as separate images within the Label node of the LabelRequestResponse XML.


#. LabelSubtype (Attribute) 
	
	* Integrated - Create an integrated label. The integrated form type must be specified in the IntegratedFormType element.
	* None - No label subtype (Default). Required when label type is Domestic. If a value for this element is supplied, it must be set to Integrated when label type is Domestic or International.

#. LabelSize (Attribute) - 

	For Default label type:

	* 4×6		-			4" W × 6" H (Default)
	* 4×5		-			4" W × 5" H
	* 4×4.5		-			4" W × 4.5" H
	* DocTab    -			4” W × 6.75” H, Eltron Doc-Tab label
	* 6×4       -            6" W × 4" H (not available for Express Mail, EPL2 and ZPLII labels)

	For DestinationConfirm label type:

	* 7×3		-			7" W × 3" H (Default)
	* 6×4		-			6" W × 4" H
	* Dymo30384		-		DYMO #30384 2-part internet label
	* EnvelopeSize10	-	#10 Envelope
	* Mailer7x5		-		7" W × 5" H

	For CertifiedMail label type:
	
	* 4×6		-			4" W × 6" H (Default)
	* 7×4		-			7" W × 4" H
	* 8×3		-			8” W × 3” H
	* Booklet   -           9” W × 6 ”H envelope
	* EnvelopeSize10    -     #10 Envelope

#. ImageFormat (Attribute)

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

#. ImageResolution (Attribute)

    * 203 - 203dpi
    * 300 - 300dpi

#. ImageRotation (Attribute)

	* None			-		No rotation (Default).
	* Rotate90		-		Rotate label image 90 degrees.
	* Rotate180		-		Rotate label image 180 degrees.
	* Rotate270     -       Rotate label image 270 degrees.      

#. DateAdvance (Numeric)

	0-7 			-		The number of days to advance date on the indicium. 
                            Maximum value: 7 days.

#. MailpieceShape (Text)

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

#. MailPeiceDimensions
    
    * Length (Numeric) - 3.3
    * Width (Numeric) - 3.3
    * Height (Numeric) - 3.3

#. AutomationRate (Text)

	* TRUE		-		Use applicable automation rate for selected mail class.
	* FALSE		-		Use retail price. (Default) Available only for letter shape mailpiece using First-Class.

#. Machinable (Text)

	* TRUE		-		Mailpiece is machinable.(Default)
	* FALSE		-		Mailpiece is non-machinable.
                        If a Parcel Select mailpiece
                        marked as machinable is over
                        35 lbs. in weight or its
                        MailpieceShape is set to
                        OversizedParcel, it will
                        automatically be charged the
                        non-machinable price.

#. ServiceLevel (Text)  
    * NextDay        -      Next Day
    * 2ndDay         -      Second Day
    * POToAddressee  -      Post Office to Addressee Service Applies only to Express Mail.

#. SundayHolidayDelivery (Text) - For Express Mail only:

    * TRUE - Request Sunday/Holiday Delivery Service.
    * FALSE - Do not deliver on Sunday or holiday. (Default)

#. SortType (Text) - BMC/FiveDigit/MixedBMC/Nonpresorted/Presorted/SCF/SinglePiece/ThreeDigit
#. IncludePostage (Text) - TRUE/FALSE - Include Postage on the Label or not
#. ReplyPostage (Text) - 

    * TRUE - Print reply postage on the label which means the Sender’s and Recipient’s address will be swapped when printing.
    * FALSE - Do not print reply postage.(Default)

      Can only be with label type of Default or DestinationConfirm. Not available for Express Mail, international mail, integrated labels or when Return Receipt
      is requested.

#. ShowReturnAddress (Text) 

    * TRUE - Print sender’s address on the label. (Default)
    * FALSE - Do not print sender’s address on the label.

        Defaults to TRUE for integrated labels. Even though this element can be used to hide the return address in the label, the USPS rules requires that a return
        address must appear on the mailpiece in specific circumstances. For more information, see the USPS Domestic Mail Manual.

#. Stealth (Text)

    * TRUE - Turn on the use of "stealth" or hidden postage. (Default)
    * FALSE - Turn off stealth.

    * Stealth cannot be used with COD, USPS Insurance, Registered Mail, Automation rate, LabelSize of EnvelopeSize10 and Card shape mailpieces.
    * For Standard Mail, Stealth is turned on.

#. ValidateAddress (Text) - TRUE/FALSE - Validate all addresses.
#. SignatureWaiver (Text) - TRUE/FALSE - For Express Mail Only.

    * TRUE - Request waiver of signature for receipt of mailpiece.
    * FALSE - Request signature for receipt of mailpiece. (Default)


#. NoWeekendDelivery (Text) - TRUE/FALSE - For Express Mail Only. Saturday Delivery.
#. Services

        #. CertifiedMail (Attribute) - OFF/ON - The default value is ON for CertifiedMail label type; otherwise, it is OFF. 
                                              Available for First-Class and Priority Mail.

        #. COD (Attribute) - OFF/ON - (Must affix a completed COD Form 3816 to the mailpiece and take it to the retail USPS counter)

        #. DeliveryConfirmation (Attribute) - OFF/ON - The value of this element is automatically set by the Endicia Label Server based on other elements in the LabelRequest XML. Do not supply a value for this element. It will be ignored.

        #. ElectronicReturnReceipt (Attribute) - OFF/ON - To receive Electronic Return Receipt delivery information, the partner must be registered as a Bulk Proof of Delivery Client with the USPS and develop the software to download the extract file from USPS. The Mailer ID assigned by the USPS for this purpose must be specified in the  BpodClientDUNSNumber element.

        #. InsuredMail (Attribute) 

            * OFF - No insurance requested.(Default)
            * ON - USPS Insurance requested (must affix a completed Form 3813 or 3813-P to the mailpiece and take it to the retail USPS counter).
            * USPSOnline - USPS Online Insurance requested.
            * Endicia - Endicia Insurance requested (Maximum insurable value: $10,000)

        #. RestrictedDelivery (Attribute) - OFF/ON
        #. ReturnReceipt (Attribute) 

            * OFF  -  Return Receipt not requested.(Default)
            * ON - Return Receipt requested(must affix a completed Return Receipt Form 3811 to the mailpiece and take it to the retail USPS counter). Can only be used with label type of Default or DestinationConfirm. Not supported for International Mail.

        #. SignatureConfirmation (Attribute) - OFF/ON

#. TrackingNumber (Text) 
    
    * 22 - PIC
    * 14 - Planet Code
    * 12 - Planet Code

    This element must not be supplied when label type is Domestic. Not used for international mail.

#. CostCenter (Numeric, 8) - Cost-center code for accounting purposes.
#. Value (Currency, 5.2) - Value of the MailPiece. When a customs form is requested and the individual customs item elements are not supplied, then this value should be set to the total customs value. Ignored when CustomsInfo is supplied.

#. InsuredValue (Currency, 5.2) - Required if insurance or COD is requested for the mailpiece
#. CODAmount (Currency, 5.2) - Required if COD is requested for the mailpiece.
#. Description (Text, 50) Description of the item shipped. Used for authentication by recipient. When requesting an International Mail label or a customs form, a value is required if the LabelRequest XML does not contain any customs declaration elements.

#. IntegratedFormType (Text)

    * Form2976  Form 2976
    * Form2976A Form 2976-A
    * Required when label subtype is Integrated.

#. CustomsFormType (Text) -

    * None      - No Customs Form (Default)
    * Form2976  - Same as CN22
    * Form2976A - Same as CP72
    * Used for APO/FPO and other destinations as required by USPS regulations. Do not use with integrated labels or international mail.

#. CustomsFormImageFormat (Text)

    * GIF : GIF
    * JPEG : JPEG
    * PDF : PDF
    * PNG : PNG (Default)
    * Do not use with integrated labels or international mail. 


#. CustomsFormImageResolution (Text) - 

    * 300 - 300 dpi

#. OriginCountry (Text) - Country of Origin of the item. This must be a valid, USPS recognized country. Required for International Mail items or when requesting a customs form. Ignored when CustomsInfo is supplied.

#. ContentsType (Text) - Documents/Gift/Merchandise/Other/ReturnedGoods/Sample

                        Category of the customs items. Used in customs forms and international labels.

    * Default value is Other. 
    * Value of ReturnedGoods is not available for Priority Mail International Flat Rate Envelope and Customs Form 2976. 
    * Ignored when CustomsInfo is supplied.

#. ContentsExplanation (Text) - Explanation of the customs items. Used in customs forms and international labels. 

    * Required if ContentsType is Other. 
    * Ignored when CustomsInfo is supplied.

#. NonDeliveryOption (Text) - Abandon / Return(Default)   

                         Non-delivery instructions.Used in customs forms and international labels. Ignored when CustomsInfo is supplied.

#. ReferenceID (Text) - A Reference value for the logs
#. **PartnerCustomerID** (Text) - A unique identifier for the partner's end-user printing the label

#. **PartnerTransactionID** (Text) - A unique identifier for the partner's end-user's transaction such as invoice, transaction number, etc.

#. BpodClientDunsNumber (Numeric - 9) - Mailer ID of the partner assigned by USPS. Allows the partner to receive Electronic Return Receipt information from USPS in an extract file uniquely generated for them, provided they have established themselves with USPS as a Bulk Proof of Delivery Client.

#. RubberStamp1 (Text, 50) - 	User-supplied text to print on the label.
#. RubberStamp2 (Text, 50) - 	User-supplied text to print on the label.
#. RubberStamp3 (Text, 50) - 	User-supplied text to print on the label.

#. EntryFacility (Text) - Postal facility where the mail is entered. If this element is not set to Other, the ZIP Code of this facility must be specified in POZipCode. Required for Parcel Select and Standard Mail.

    * DBMC - Destination BMC
    * DDU  - Destination Delivery Unit
    * DSCF - Destination Sectional Center Facility
    * OBMC - Origin BMC
    * Other - Other postal facility (Default)


#. POZipCode (Text) - ZIP Code of Post Office or collection box where item is mailed. May be different than FromPostalCode. Used for determining the zone and calculating the postage price. Required when EntryFacility is not set to Other. The value of this element must contain the zip code of the postal facility specified in EntryFacility.

#. ShipDate (Date) - MM/DD/YYYY - Date mailpiece is shipped. Required for Express Mail Sunday/Holiday Delivery Service. Ignored for other mail classes.
#. ShipTime (Time) - HH:MM AM or HH:MM PM - Time mailpiece is shipped. Applies only to Express Mail Sunday/Holiday Delivery Service. Ignored for other mail classes. If this element is not supplied, it defaults to 12:01 AM.

#. EelPfc (Text) - Exemption or Exclusion Legend (EEL) or a Proof of Filing Citation (PFC).
                    Required for shipments to an international destination or to an overseas U.S. Territory. It is recommended to supply a value for this element as the USPS will likely require it in the near future.

#. CustomsCertify (Text) - TRUE/FALSE -  TRUE means the customs information is certified to be correct and the CustomsSigner name should be printed.

#. CustomsSigner (Text - 47) -  Name of person certifying that the customs information is correct. This name prints on the customs form in place of a signature if CustomsCertify is TRUE. Required if CustomsCertify is TRUE.

#. ResponseOptions (Node) - Optional XML elements to include in the LabelRequestResponse.

    * PostagePrice (Text) - TRUE/FALSE - TRUE means the response contains the PostagePrice node.

#. FromName (Text, 47) - Either FromName or FromCompany must contain a value. For customs forms, this element must contain at least two words.

#. FromCompany (Text, 47) - Either FromName or FromCompany must contain a value.

#. **ReturnAddress1** (Text, 47) - First delivery address line of sender
#. ReturnAddress2 (Text, 47) - Second delivery address line of sender
#. ReturnAddress3 (Text, 47) - Third delivery address line of sender
#. ReturnAddress4 (Text, 47) - Fourth delivery address line of sender

    .. note::
        Do not use **ReturnAddress3** and **ReturnAddress4** when label type is Domestic or International and a label subtype value is supplied

#. **FromCity** (Text, 50) - Sender's city.
                        Allowed characters: A-Z a-z hyphen period space

#. **FromState** (Text, 25) - Sender's state or province
#. **FromPostalCode** (Text, 10) - Sender‘s postal code. The format is either ZIP5 only or ZIP+4 for US addresses.
#. FromZIP4 (Text, 4) - +4 add-on for US addresses. Ignored if FromPostalCode contains the ZIP4 value.
#. FromCountry (Text, 50) - Sender's country. This value should be left blank for USA addresses.

#. FromPhone (Text, 10) Phone number of sender (required for Express Mail and international mail). 10 digits required (including area code) with no punctuation. Use format: 2125551234

#. FromEMail (Text, 64) - E-mail address of sender.
#. ToName (Text, 47) - Recipient’s name. For Express Mail and international mail: Either ToName or ToCompany must contain a value.
#. ToCompany (Text, 47) - Recipient’s company name. For Express Mail and international mail: Either ToName or ToCompany must contain a value.
#. **ToAddress1** (Text, 47) - First delivery address line of recipient. 

    * A value is optional only when ToCompany contains a value. 
    * Express Mail labels are limited to four lines in the destination address for all label sizes.
    * 4X5 and 4x4.5 labels are limited to five lines in the destination address.

#. ToAddress2 (Text, 47) - Second delivery address line of recipient.
#. ToAddress3 (Text, 47) - Third delivery address line of recipient.
#. ToAddress4 (Text, 47) - Fourth delivery address line of recipient.
    
    .. note::
        Do not use ToAddress3 and ToAddredd4 when label type is domestic.

#. **ToCity** (Text, 50) - Recipient's City
#. **ToState** (Text, 25) - Recipient's state or province
#. **ToPostalCode** (Text, 4/15) - Recipient‘s postal code.

    * For Domestic Mail, the format is ZIP5 (required).
    * For International Mail (optional).


#. ToZIP4 (Text, 4) - +4 add-on for US addresses
#. ToDeliveryPoint (Text, 2) - +2 Delivery Point for US Addresses
#. ToCountry (Text, 50) - Recipient's Country. Required for International Mail.  Ignored when label type is International and a label subtype value is supplied. In this case, the ToCountryCode element must be used.

#. ToCountryCode (Text, 2) - ToCountryCode Text 2 Two-character country code of the recipient’s country. Required when label type is International and a label subtype value is supplied.

#. ToPhone (Text, 10/30) - Recipient’s Phone Number.

    * 10 For Domestic mail: 10 digits including area code with no punctuation. For example: 2125551234. If supplied value is not in the correct format, it will be ignored.
    * 30 For International mail, up to 30 digits with no punctuation.

#. ToEMail (Text, 64) - E-mail address of recipient.
#. CustomsInfo (Node) - Required when using Integrated Labels.

    #. ContentsType (Text) - Documents/Gift/Merchandise/Other/ReturnedGoods/Sample
    #. ContentsExplanation (Text) - Explanation of the customs items. Required if ContentsType is Other.
    #. RestrictionType (Text) None/Other/Quarantine/SanitaryPhytosanitaryInspection
    #. RestrictionCommments (Text, 25) - 

        * None (Default)
        * Other
        * Quarantine
        * SanitaryPhytosanitaryInspection

    #. SendersCustomsReference (Text, 14) - Sender's Customs Reference
    #. ImportersCustomsReference (Text, 40) - Importer's Customs Reference
    #. LicenseNumber (Text, 16) - License Number
    #. CertificateNumber (Text, 12) - Certificate Number
    #. InvoiceNumber (Text, 15) - Invoice Number
    #. NonDeliveryOption (Text) - Abondon / Return (Default)
    #. InsuredNumber (Text, 13) - *For Future Use*
    #. EelPfc (Text, 35) - 

        * Exemption or Exclusion Legend (EEL) or a Proof of Filing Citation (PFC).
        * Required for shipments to an international destination or to an overseas U.S. Territory.
        * It is recommended to supply a value for this element as the USPS will likely require it in the near future.

    #. **CustomsItems** (Node) - [1 .. 30]

        * **Description** (Text, 30) - Description of the customs item.
        * **Quantity** (Numeric, 3) - Quantity of the customs item. Must be greater than zero.
        * **Weight**  (Numeric, 4) - Weight of the customs item. Must be specified in whole ounces and greater than zero and cannot exceed 1120 ounces (70 pounds).
        * **Value** (Currency, 5.2) - Value of the customs item. Must be greater than zero.
        * HSTariffNumber (Text, 6) - 6-digit HS tariff number.
        * CountryOfOrigin (Text, 2) - Two character country code of the country where the customs items originated. 

#. The following five sets of customs item elements are ignored when CustomsInfo is supplied.

		#. CustomsDescription1 (Text, 50)
		#. CustomsQuantity1 (Numeric, 8)
		#. CustomsWeight1 (Numeric, 4)
		#. CustomsValue1 (Currency, 5.2)
		#. CustomsCountry1 (Text, 50)


		#. CustomsDescription2 (Text, 50)
		#. CustomsQuantity2 (Numeric, 8)
		#. CustomsWeight2 (Numeric, 4)
		#. CustomsValue2 (Currency, 5.2)
		#. CustomsCountry2 (Text, 50)


		#. CustomsDescription3 (Text, 50)
		#. CustomsQuantity3 (Numeric, 8)
		#. CustomsWeight3 (Numeric, 4)
		#. CustomsValue3 (Currency, 5.2)
		#. CustomsCountry3 (Text, 50)


		#. CustomsDescription4 (Text, 50)
		#. CustomsQuantity4 (Numeric, 8)
		#. CustomsWeight4 (Numeric, 4)
		#. CustomsValue4 (Currency, 5.2)
		#. CustomsCountry4 (Text, 50)


		#. CustomsDescription5 (Text, 50)
		#. CustomsQuantity5 (Numeric, 8)
		#. CustomsWeight5 (Numeric, 4)
		#. CustomsValue5 (Currency, 5.2)
		#. CustomsCountry5 (Text, 50)
