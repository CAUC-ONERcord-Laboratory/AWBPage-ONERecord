# AWBPage-ONERecord
A web application that recognizes and fills in the AWB template with the ONE Record standard AWB-JSON-ld data

### Quick Start

Front end:

```shell
# Node.js environment is required
http-server -p 3000
```

Back end:
python 3.12
```shell
cd backEnd
pip install -r requirements.txt
python backend.py
```

API

```http
Post http://localhost:5000/query
Content-Type: application/json
```

Body example

```json
{
    "@context": {
        "cargo": "https://onerecord.iata.org/ns/cargo#",
        "code": "https://onerecord.iata.org/ns/code-lists/"
    },
    "@type": "cargo:Waybill",
    "cargo:waybillType": {
        "@id": "cargo:MASTER"
    },
    "cargo:waybillNumber": "XXX-01961794",
    "cargo:involvedParties": [
        {
            "@type": "cargo:Party",
            "cargo:partyDetails": {
                "@type": "cargo:Organization",
                "cargo:name": "XXX SHANGHAI CO LTD",
                "cargo:basedAtLocation": {
                    "@type": "cargo:Location",
                    "cargo:locationName": "XXX SHANGHAI CO LTD 21"
                }
            },
            "cargo:partyRole": {
                "@type": "code:ParticipantIdentifier",
                "@id": "https://onerecord.iata.org/ns/code-lists/ParticipantIdentifier#SHP"
            }
        },
        {
            "@type": "cargo:Party",
            "cargo:partyDetails": {
                "@type": "cargo:Organization",
                "cargo:name": "XXX OSAKA OFFICE",
                "cargo:basedAtLocation": {
                    "@type": "cargo:Location",
                    "cargo:locationName": "SENSHU XXX OSAKA OFFICE 1-1-1"
                }
            },
            "cargo:partyRole": {
                "@type": "code:ParticipantIdentifier",
                "@id": "https://onerecord.iata.org/ns/code-lists/ParticipantIdentifier#CNE"
            }
        },
        {
            "@type": "cargo:Party",
            "cargo:partyDetails": {
                "@type": "cargo:Company",
                "cargo:name": "test_agent",
                "cargo:iataCargoAgentCode": "",
                "cargo:basedAtLocation": {
                    "@type": "cargo:Location",
                    "cargo:locationName": ""
                }
            },
            "cargo:partyRole": {
                "@type": "code:ParticipantIdentifier",
                "@id": "https://onerecord.iata.org/ns/code-lists/ParticipantIdentifier#AGT"
            }
        },
        {
            "@type": "cargo:Party",
            "cargo:partyDetails": {
                "@type": "cargo:Carrier",
                "cargo:name": "XXX Airline",
                "cargo:shortName": "XXXX",
                "cargo:airlineCode": "XX"
            },
            "cargo:partyRole": {
                "@type": "code:ParticipantIdentifier",
                "@id": "https://onerecord.iata.org/ns/code-lists/ParticipantIdentifier#AIR"
            }
        }
    ],
    "cargo:accountingNotes": [
        {
            "@type": "cargo:AccountingNote",
            "cargo:accountingNoteText": "运单修改1次"
        }
    ],
    "cargo:arrivalLocation": {
        "@type": "cargo:Location",
        "cargo:locationCodes": {
            "@type": "cargo:CodeListElement",
            "cargo:code": "KIX"
        }
    },
    "cargo:departureLocation": {
        "@type": "cargo:Location",
        "cargo:locationCodes": {
            "@type": "cargo:CodeListElement",
            "cargo:code": "TAO"
        }
    },
    "cargo:weightValuationIndicator": {
        "@type": "code:PrepaidCollectIndicator",
        "@id": "https://onerecord.iata.org/ns/code-lists/PrepaidCollectIndicator#P"
    },
    "cargo:declaredValueForCarriage": {
        "@type": "cargo:CurrencyValue",
        "cargo:currencyUnit": {
            "@type": "code:CurrencyCode",
            "@value": "CNY"
        },
        "cargo:numericalValue": 0
    },
    "cargo:declaredValueForCustoms": {
        "@type": "cargo:CurrencyValue",
        "cargo:currencyUnit": {
            "@type": "code:CurrencyCode",
            "@value": "CNY"
        },
        "cargo:numericalValue": 0
    },
    "cargo:shipment": {
        "@type": "cargo:Shipment",
        "cargo:insurance": {
            "@type": "cargo:Insurance",
            "cargo:insuredAmount": {
                "@type": "cargo:CurrencyValue",
                "cargo:currencyUnit": {
                    "@type": "code:CurrencyCode",
                    "@value": "CNY"
                },
                "cargo:numericalValue": 0
            }
        },
        "cargo:pieces": [
            {
                "@id": "https://pieces_example"
            }
        ],
        "cargo:totalGrossWeight": "",
        "cargo:totalDimensions": ""
    },
    "cargo:waybillLineItems": [
        {
            "@type": "cargo:WaybillLineItem",
            "cargo:rateClassCode": {
                "@id": "https://onerecord.iata.org/ns/code-lists/RateClassCode#Q"
            },
            "cargo:rateCharge": {
                "@type": "cargo:CurrencyValue",
                "cargo:currencyUnit": {
                    "@type": "code:CurrencyCode",
                    "@value": "CNY"
                },
                "cargo:numericalValue": 6.5
            },
            "cargo:pieceReferences": [
                {
                    "@id": "http://127.0.0.1:3000/JSON-LD/piece1.json"
                },
                {
                    "@id": "http://127.0.0.1:3000/JSON-LD/piece2.json"
                },
                {
                    "@id": "http://127.0.0.1:3000/JSON-LD/piece3.json"
                }
            ]
        }
    ],
    "cargo:referredBookingOption": {
        "@type": "cargo:Booking",
        "cargo:bookingRequest": {
            "@type": "cargo:BookingRequest",
            "cargo:forBookingOption": {
                "@type": "cargo:BookingOption",
                "cargo:transportLegs": [
                    {
                        "@type": "cargo:TransportLegs",
                        "cargo:transportIdentifier": "XX2493",
                        "cargo:departureDate": {
                            "@type": "http://www.w3.org/2001/XMLSchema#dateTime",
                            "@value": "2025-02-07T14:30:45"
                        },
                        "cargo:arrivalLocation": {
                            "@type": "cargo:Location",
                            "cargo:locationCodes": {
                                "@type": "cargo:CodeListElement",
                                "cargo:code": "KIX"
                            }
                        },
                        "cargo:departureLocation": {
                            "@type": "cargo:Location",
                            "cargo:locationCodes": {
                                "@type": "cargo:CodeListElement",
                                "cargo:code": "TAO"
                            }
                        }
                    }
                ]
            }
        }
    },
    "cargo:otherChargesIndicator": {
        "@type": "code:PrepaidCollectIndicator",
        "@id": "code:PrepaidCollectIndicator#P"
    },
    "cargo:otherCharges": [
        {
            "@type": "cargo:OtherCharge",
            "cargo:otherChargeCode": {
                "@id": "https://onerecord.iata.org/ns/code-lists/OtherChargeCode#AW"
            },
            "cargo:entitlement": {
                "@id": "https://onerecord.iata.org/ns/code-lists/EntitlementCode#C"
            },
            "cargo:reasonDescription": "Air Waybill Fee due carrier",
            "cargo:otherChargeAmount": {
                "@type": "cargo:CurrencyValue",
                "cargo:currencyUnit": {
                    "@type": "code:CurrencyCode",
                    "@value": "CNY"
                },
                "cargo:numericalValue": 50
            }
        },
        {
            "@type": "cargo:OtherCharge",
            "cargo:otherChargeCode": {
                "@id": "https://onerecord.iata.org/ns/code-lists/OtherChargeCode#IN"
            },
            "cargo:entitlement": {
                "@id": "https://onerecord.iata.org/ns/code-lists/EntitlementCode#C"
            },
            "cargo:reasonDescription": "Insurance Premium due carrier",
            "cargo:otherChargeAmount": {
                "@type": "cargo:CurrencyValue",
                "cargo:currencyUnit": {
                    "@type": "code:CurrencyCode",
                    "@value": "CNY"
                },
                "cargo:numericalValue": 12
            }
        }
    ],
    "cargo:consignorDeclarationSignature": "XXX CO LTD",
    "cargo:carrierDeclarationSignature": "XX Airline",
    "cargo:carrierDeclarationDate": {
        "@type": "http://www.w3.org/2001/XMLSchema#dateTime",
        "@value": "2025-02-06"
    },
    "cargo:carrierDeclarationPlace": {
        "@type": "cargo:Location",
        "cargo:locationCodes": {
            "@type": "cargo:CodeListElement",
            "cargo:code": "TNA"
        }
    }
}
```

Response

| Server                      | Werkzeug/3.1.1 Python/3.12.3  |
| --------------------------- | ----------------------------- |
| Date                        | Tue, 11 Mar 2025 12:54:34 GMT |
| Content-Type                | application/json              |
| Content-Length              | 148                           |
| Access-Control-Allow-Origin | http://127.0.0.1:3000         |
| Connection                  | close                         |

**200 OK**

```json
{
    "Accounting_Information": "运单修改1次",
    "Airport_of_Departure": "TAO",
    "Airport_of_Destination": "KIX",
    "Amount_of_Insurance": {
        "Value": 0.0,
        "unit": "CNY"
    },
    "Consignee": {
        "Address": "SENSHU XXX OSAKA OFFICE 1-1-1",
        "Name": "XXX OSAKA OFFICE"
    },
    "Date": "2025-02-07T14:30:45",
    "Declared_Value_For_Carriage": {
        "Unit": "CNY",
        "Value": 0.0
    },
    "Declared_Value_For_Customs": {
        "Value": 0.0
    },
    "Executed_Date": "2025-02-06T00:00:00",
    "Executed_Place": "TNA",
    "First_Carrier": "XX",
    "Flight": "XX2493",
    "Issued_by": {
        "Airlinecode": "XX",
        "Name": "XXX Airline"
    },
    "Issuing_Carrier_Agent": "test_agent",
    "No_of_Pieces": "3",
    "Other": "P",
    "Other_Charges": [
        {
            "Unit": "CNY",
            "Value": 50.0,
            "entitlement": "C",
            "otherChargeCode": "AW",
            "reasonDescription": "Air Waybill Fee due carrier"
        },
        {
            "Unit": "CNY",
            "Value": 12.0,
            "entitlement": "C",
            "otherChargeCode": "IN",
            "reasonDescription": "Insurance Premium due carrier"
        }
    ],
    "Piece_References_URL": [
        {
            "pieceURL": "http://127.0.0.1:3000/JSON-LD/piece1.json"
        },
        {
            "pieceURL": "http://127.0.0.1:3000/JSON-LD/piece2.json"
        },
        {
            "pieceURL": "http://127.0.0.1:3000/JSON-LD/piece3.json"
        }
    ],
    "Rate_Charge": {
        "Value": 6.5,
        "unit": "CNY"
    },
    "Rate_Class_Code": "Q",
    "Shipper": {
        "Address": "XXX SHANGHAI CO LTD 21",
        "Name": "XXX SHANGHAI CO LTD"
    },
    "Signature_of_Carrier_or_its_Agent": "XX Airline",
    "Signature_of_Shipper_or_his_Agent": "XXX CO LTD",
    "To": "KIX",
    "Total": 5021.5,
    "Total_Chargeable_Weight": 763.0,
    "Total_Dimensions": 4.57,
    "Total_Goods_Descriptions": {
        "http://127.0.0.1:3000/JSON-LD/piece1.json": "EXPRESS",
        "http://127.0.0.1:3000/JSON-LD/piece2.json": "EXPRESS",
        "http://127.0.0.1:3000/JSON-LD/piece3.json": []
    },
    "Total_Gross_Weight": 391.0,
    "Total_Other_Charges_Due_Agent": 0.0,
    "Total_Other_Charges_Due_Carrier": 62.0,
    "Total_WeightCharge": 4959.5,
    "WT_VAL": "P",
    "Waybill_Number": "XXX-01961794"
}
```

### References

[RDF 和 SPARQL 初探：以维基数据为例](https://www.ruanyifeng.com/blog/2020/02/sparql.html)

[One Record Specification (Air Waybill)](https://iata-cargo.github.io/ONE-Record/development/Data-Model/waybill/)

[One Record Specification (Code Lists)](https://iata-cargo.github.io/ONE-Record/development/Data-Model/code-lists/)

[CBP Export Manifest Implementation Guide IATA Cargo-XML Messages Specification](https://www.cbp.gov/sites/default/files/assets/documents/2020-Feb/ACE%20CBP%20Export%20Manifest%20Implementation%20Guide%20v02_0.pdf)

[Air Waybill Template](https://airwaybillform.com/)
