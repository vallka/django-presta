import re 
from django.shortcuts import render
from django.views import generic
from rest_framework import serializers

import logging
logger = logging.getLogger(__name__)

from .models import *

# Create your views here.
class IndexView(generic.ListView):

    def get_queryset(self):
        """
        """
        qs = DHLParcel.objects.using('presta').raw(DHL_sql('o',''))
        logger.error('get_queryset')
        logger.error(qs)
        return qs

class DHLSerializer(serializers.ModelSerializer):
    class Meta:
        model = DHLParcel
        fields = '__all__'

class UPSSerializer0(serializers.ModelSerializer):
    class Meta:
        model = UPSParcel
        fields = '__all__'

class UPSSerializer(serializers.BaseSerializer):
    def to_representation(self, instance):
        return {
            "ShipmentRequest": {
                "Shipment": {
                    "Description": instance.Description,
                    "ReferenceNumber" : {
                        "Value": instance.ReferenceNumber
                    },
                    "Shipper": {
                        "Name": "GellifiQue Ltd",
                        "AttentionName": "Margaryta",
                        "TaxIdentificationNumber": "",
                        "Phone": {
                            "Number": "447746358920"
                        },
                        "ShipperNumber": "2V813A",
                        "Address": {
                            "AddressLine": "41 Deantown Avenue Whitecraig",
                            "City": "Musselburgh",
                            "StateProvinceCode": "East Lothian",
                            "PostalCode": "EH21 8NS",
                            "CountryCode": "GB"
                        }
                    },
                    "ShipTo": {
                        "Name": instance.ShipTo_Name,
                        "AttentionName": instance.ShipTo_AttentionName,
                        "EMailAddress": instance.ShipTo_EMailAddress,
                        "Phone": {
                            "Number": re.sub(r'^0','44',re.sub(r'\D','',instance.ShipTo_Phone_Number))
                        },
                        "Address": {
                            "AddressLine": [instance.ShipTo_Address_AddressLine1,instance.ShipTo_Address_AddressLine2],
                            "City": instance.ShipTo_Address_City,
                            "PostalCode": instance.ShipTo_Address_PostalCode,
                            "CountryCode": instance.ShipTo_Address_CountryCode
                        }
                    },
                    "ShipFrom": {
                        "Name": "GellifiQue Ltd",
                        "AttentionName": "Margaryta",
                        "TaxIdentificationNumber": "",
                        "Phone": {
                            "Number": "447746358920"
                        },
                        "ShipperNumber": "0001",
                        "Address": {
                            "AddressLine": "41 Deantown Avenue Whitecraig",
                            "City": "Musselburgh",
                            "PostalCode": "EH21 8NS",
                            "CountryCode": "GB"
                        }
                    },
                    "PaymentInformation": {
                        "ShipmentCharge": {
                            "Type": "01",
                            "BillShipper": {
                                "AccountNumber": "2V813A"
                            }
                        }
                    },
                    "Service": {
                        "Code": "11",
                        "Description": "Standard"
                    },
                    "Package": [
                        {
                            "Description": "Manicure Accessories",
                            "Packaging": {
                                "Code": "02"
                            },
                            "PackageWeight": {
                                "UnitOfMeasurement": {
                                    "Code": "KGS"
                                },
                                "Weight": str(instance.Package_Weight)
                            },
                            "PackageServiceOptions": ""
                        }
                    ],
                    "ItemizedChargesRequestedIndicator": "",
                    "RatingMethodRequestedIndicator": "",
                    "TaxInformationIndicator": "",
                    "ShipmentRatingOptions": {
                        "NegotiatedRatesIndicator": ""
                    }
                },
                "LabelSpecification": {
                    "LabelImageFormat": {
                        "Code": "GIF"
                    }
                }
            }
        }

class UPSLabelSerializer(serializers.BaseSerializer):
    def to_representation(self, instance):
        return {
            "LabelRecoveryRequest": {
                "LabelSpecification": {
                    "LabelImageFormat": {
                            "Code": "GIF"
                    },
                },
                "TrackingNumber": str(instance.ShippingNumber)
            }
        }        