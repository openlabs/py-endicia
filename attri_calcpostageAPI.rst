.. _postageapi: Postage Api

Parameters for Calculatin Postage and Fees API
**********************************************

#. RequesterID (Text, 50) : Requester ID (also called Partner ID) is used to uniquely identify the system making the request. This ID is assigned by Endicia.
#. CertifiedIntermediary (Node) : Certified Intermediary (CI) account authentication information.
#. AccountID (Numeric, 6) : Account ID for the Endicia postage account.
#. PassPhrase (Text, 64) : Pass Phrase for the Endicia postage account.
#. MailClass (Text)

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

#. Pricing (Text)

    * CommercialBase : Commercial Base pricing.
    * CommercialPlus : Commercial Plus pricing.
    * Retail : Retail pricing.

    If this element is not supplied, pricing will be based on the MailClass and any qualified discounts available to AccountID.
    
    .. note::
        If this element is set to CommercialPlus, but the account does not qualify for such pricing, the Web method will return an error.

#. WeightOz (Numeric, 4.1) : Weight of the package, in ounces.
#. MailpieceShape (Text) : Card / Letter / Flat / Parcel / LargeParcel / IrregularParcel / OversizedParcel / FlatRateEnvelope / FlatRatePaddedEnvelope / SmallFlatRateBox / MediumFlatRateBox / LargeFlatRateBox 

    * Shape of the mailpiece.
    * Starting in May 2009, FlatRateBox has been replaced with MediumFlatRateBox.
    * The Flat Rate Padded Envelope is only available to qualifying Priority Mail Commercial Plus customers. The Label Server will return an error if this shape is used with any other pricing.

#. MailpieceDimensions (Node):  Dimensions of the mailpiece. Required for calculating Cubic pricing and for Priority Mail mailpieces going to Zones 5-8 which are over 1 cubic foot. Ignored if MailpieceShape is set to either LargeParcel or OversizedParcel. **All values must be in inches.**

        * Length (Numeric, 3.3) : Length of the mailpiece.
        * Width (Numeric, 3.3) : Width of the mailpiece.
        * Height (Numeric, 3.3) : Height (or thickness) of the mailpiece.

#. AutomationRate (Text)

    * TRUE : Use applicable automation rate for selected mail class.
    * FALSE : Use retail price. (Default)
    * Available only for letter shape mailpiece using First-Class.

#. Machinable (Text)

    * TRUE : Package is machinable. (Default) Package is non-machinable.
    * FALSE : If a Parcel Select mailpiece marked as machinable is over 35 lbs. in weight or its MailpieceShape is set to OversizedParcel, it will automatically be charged the non- machinable rate.
                                          
#. ServiceLevel (Text)
#. SundayHolidayDelivery (Text) : For Express Mail only:

    * TRUE : Request Sunday/Holiday Delivery Service.
    * FALSE : Do not deliver on Sunday or holiday. (Default)

#. SortType (Text) : BMC / FiveDigit / MixedBMC / Nonpresorted / Presorted / SCF / SinglePiece / ThreeDigit

    * Sort level for applicable mail classes.
    * Required for Parcel Select and Standard Mail.
    * Defaults to SinglePiece for mailpieces which do not require a sort type.

#. Services (Node) : Special Services requested for the package.
    
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

#. Value (Currency, 5.2) : Value of the item(s) in the mailpiece
#. CODAmount (Currency, 5.2) : COD amount to collect. Required if COD is requested for the mailpiece.
#. InsuredValue (Currency, 5.2) : Insured value of the mailpiece. Required if insurance or COD is requested for the mailpiece.
#. EntryFacility (Text) : Postal facility where the mail is entered. The zip code of this facility must be specified in POZipCode. Required for Parcel Select and Standard Mail.

    * DBMC : Destination BMC
    * DDU : Destination Delivery Unit
    * DSCF : Destination Sectional Center Facility
    * OBMC : Origin BMC
    * Other : Other postal facility (Default)

#.   FromPostalCode (Text, 5) : Sender‘s postal code. The format is ZIP5. For Parcel Select and Standard Mail, the value of this element contains the zip code of the postal facility specified in EntryFacility. Recipient‘s postal code.

#. ToPostalCode (Text)

    * 5: For Domestic Mail, the format is ZIP5 (required).
    * 15: For International Mail (optional).

#. ToCountry (Text, 50) : Recipient‘s country. Required for International Mail. Use either ToCountry or ToCountryCode.
#. ToCountryCode (Text, 2) : Two character country code of the recipient’s country. Required for International Mail. Use either ToCountry or ToCountryCode.
#. ShipDate (Date, MM/DD/YYYY) : Date mailpiece is shipped. Required for Express Mail Sunday/Holiday Delivery Service. Ignored for other mail classes.
#. ShipTime (Time, HH:MM AM or HH:MM PM) : Time mailpiece is shipped. Applies only to Express Mail Sunday/Holiday Delivery Service. Ignored for other mail classes. If this element is not supplied, it defaults to 12:01 AM.

#. ResponseOptions(Node) : Optional XML elements to include in the PostageRateResponse.

    * PostagePrice (Attribute)

        * TRUE : TRUE means the response contains the PostagePrice node.
        * FALSE
