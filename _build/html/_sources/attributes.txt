.. attributes: Attributes

Additional Parameters
=====================

#. LabelType (Attribute)

	* Default -               Create label based on mail class(Default)
	* CertifiedMail -         Create Certified Mail label.
	* DestinationConfirm      Create PLANET Code label
		                      using Destination Confirm service.

		.. note:: 
			Use of the DestinationConfirm label type requires special approval from Endicia and the USPS. 
			For more details, contact the Endicia Label Server Team.

	* Domestic                Create domestic label. Requires use of the LabelSubtype element.
		           		      Create international label.
	* International			When the value of this element is set to Domestic or International, the label will be
							returned as separate images within the Label node of the LabelRequestResponse XML.


#. LabelSubtype (Attribute) 
	
	* Integrated			Create an integrated label. The integrated form type must be specified in the IntegratedFormType element.
	* None					No label subtype (Default). Required when label type is Domestic. If a value for this element is supplied, it must be set to Integrated wh								en label type is Domestic or International. 

#. LabelSize (Attribute) - 

	For Default label type:

	* 4×6					4" W × 6" H (Default)
	* 4×5					4" W × 5" H
	* 4×4.5					4" W × 4.5" H
							4” W × 6.75” H, Eltron Doc-Tab
							DocTab label
	* 6×4                   6" W × 4" H (not available for Express Mail, EPL2 and ZPLII labels)

	For DestinationConfirm label type:

	* 7×3					7" W × 3" H (Default)
	* 6×4					6" W × 4" H
	* Dymo30384				DYMO #30384 2-part internet
	* EnvelopeSize10		label
	* Mailer7x5				#10 Envelope
							7" W × 5" H

	For CertifiedMail label type:
	
	* 4×6					4" W × 6" H (Default)
	* 7×4					7" W × 4" H
							8” W × 3” H
	* 8×3					9” W × 6 ”H envelope
	* Booklet
	* EnvelopeSize10         #10 Envelope

#. ImageRotation (Attribute)

	* None					No rotation (Default).
	* Rotate90				Rotate label image 90 degrees.
	* Rotate180				Rotate label image 180 degrees.
	* Rotate270             Rotate label image 270 degrees.      

#. DateAdvance (Numeric)

	0-7 					The number of days to advance date on the indicium. Maximum value: 7 days.

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

#. Length (Numeric) - 3.3
#. Width (Numeric) - 3.3
#. Height (Numeric) - 3.3

#. AutomationRate (Text)

	* TRUE				Use applicable automation rate for selected mail class.
	* FALSE				Use retail price. (Default) Available only for letter shape mailpiece using First-Class.

#.  Machinable (Text)

	* TRUE				Mailpiece is machinable.(Default)
	* FALSE				Mailpiece is non-machinable.
                        If a Parcel Select mailpiece
                        marked as machinable is over
                        35 lbs. in weight or its
                        MailpieceShape is set to
                        OversizedParcel, it will
                        automatically be charged the
                        non-machinable price.


#. FromName 
#. FromCompany
#. ReturnAddress1
#. ReturnAddress2
#. ReturnAddress3
#. ReturnAddress4
#. FromCity
#. FromState
#. FromPostalCode
#. FromZIP4
#. FromCountry
#. FromPhone
#. FromEMail
#. ToName
#. ToCompany
#. ToAddress1
#. ToAddress2
#. ToAddress3
#. ToAddress4
#. ToCity
#. ToState
#. ToPostalCode
#. ToZIP4
#. ToDeliveryPoint
#. ToCountry
#. ToCountryCode
#. ToPhone
#. ToEMail
#. RubberStamp1 (Text) 50 	User-supplied text to print on the label.
#. RubberStamp2
#. RubberStamp3
#. MailpieceDimensions     Node
#. ServiceLevel              Text
#. SundayHolidayDelivery     Text - TRUE/FALSE
#. SortType                  Text - BMC/FiveDigit/MixedBMC/Nonpresorted/Presorted/SCF/SinglePiece/ThreeDigit
#. IncludePostage			   Text - TRUE/FALSE
#. ReplyPostage			   Text - TRUE/FALSE
#. ValidateAddress      Text - TRUE/FALSE
#. SignatureWaiver      Text - TRUE/FALSE
#. NoWeekendDelivery    Text - TRUE/FALSE
#. Services                   Node
#. CertifiedMail (Attribute) OFF/ON
#. COD (Attribute) OFF/ON
#. DeliveryConfirmation (Attribute) OFF/ON
#. ElectronicReturnReceipt (Attribute) OFF/ON
#. InsuredMail (Attribute) OFF/ON
#. RestrictedDelivery (Attribute) OFF/ON
#. ReturnReceipt (Attribute) OFF/ON
#. SignatureConfirmation (Attribute) OFF/ON
#. MailpieceDimensions (Node)
#. ServiceLevel (Text) - TRUE/FALSE
#. TrackingNumber (Text) - 22 - PIC/14 - Planet Code/12 - Planet Code
#. CostCenter (Numeric) 8
#. Value (Currency) 5.2
#. InsuredValue (Currency) 5.2
#. CODAmount (Currency) 5.2
#. Description (Text)
#. IntegratedFormType (Text) 
#. CustomsFormType (Text)
#. CustomsFormImageFormat (Text)
#. CustomsFormImageResolution (Text)
#. OriginCountry (Text)
#. ContentsType (Text)
#. ContentsExplanation (Text)
#. NonDeliveryOption (Text)
#. ReferenceID (Text)
#. PartnerCustomerID (Text)
#. PartnerTransactionID (Text)
#. BpodClientDunsNumber (Numeric)
#. EntryFacility (Text)
#. POZipCode (Text)
#. ShipDate (Date)
#. ShipTime (Time)
#. EelPfc (Text)
#. CustomsCertify (Text)
#. CustomsSigner (Text)
#. ResponseOptions (Node)
#. PostagePrice (Text) - TRUE/FALSE
#. CustomsInfo (Node)
#. ContentsType (Text)
#. ContentsExplanation (Text)
#. RestrictionType (Text)
#. RestrictionCommments (Text)
#. SendersCustomsReference (Text)
#. ImportersCustomsReference (Text)
#. LicenseNumber (Text)
#. CertificateNumber (Text)
#. InvoiceNumber (Text)
#. NonDeliveryOption (Text)
#. InsuredNumber (Text)
#. EelPfc (Text)
#. CustomsItems (Node)

#. CustomsItem

		* Description
		* Quantity
		* Weight
		* Value
		* HSTariffNumber
		* CountryOfOrigin

#. The following five sets of customs item elements are ignored when CustomsInfo is supplied.

		#. CustomsDescription1
		#. CustomsQuantity1
		#. CustomsWeight1
		#. CustomsValue1
		#. CustomsCountry1
		#. CustomsDescription2
		#. CustomsQuantity2
		#. CustomsWeight2
		#. CustomsValue2
		#. CustomsCountry2
		#. CustomsDescription3
		#. CustomsQuantity3
		#. CustomsWeight3
		#. CustomsValue3
		#. CustomsCountry3
		#. CustomsDescription4
		#. CustomsQuantity4
		#. CustomsWeight4
		#. CustomsValue4
		#. CustomsCountry5
		#. CustomsDescription5
		#. CustomsQuantity5
		#. CustomsWeight5
		#. CustomsValue5
		#. CustomsCountry5

