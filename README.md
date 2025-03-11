# AWBPage-ONERecord
A web application that recognizes and fills in the AWB template with the ONE Record standard AWB-JSON-ld data

### Quick Start

Front end:

```shell
http-server -p 3000
```

Back end:

```shell
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
    "jsonld": {
    "@context": {
        "cargo": "https://onerecord.iata.org/ns/cargo#",
        "code": "https://onerecord.iata.org/ns/code-lists/"
  },
  "@type": "cargo:Waybill",
    "cargo:waybillType":{
        "@id":"cargo:MASTER"
    },
    "cargo:involvedParties": [
        {
            "@type": "cargo:Party",
            "cargo:partyDetails": {
                "@type": "cargo:Organization",
                "cargo:name": "OCS SHANGHAI CO LTD",
                "cargo:basedAtLocation":{
                    "@type": "cargo:Location",
                    "cargo:locationName":"OCS SHANGHAI CO LTD 21 KEYUAN WEI SAN LU"
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
                "cargo:name": "OCS OSAKA OFFICE",
                "cargo:basedAtLocation": {
                    "@type": "cargo:Location",
                    "cargo:locationName": "SENSHU KUKO MINAMI SENNAN SHI"
                }
            },
            "cargo:partyRole": {
                "@type": "code:ParticipantIdentifier",
                "@id": "https://onerecord.iata.org/ns/code-lists/ParticipantIdentifier#CNE"
            }
        }
        ]
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
    "consignee_info": [
        {
            "name": "OCS OSAKA OFFICE"
        }
    ],
    "shipper_info": [
        {
            "name": "OCS SHANGHAI CO LTD"
        }
    ]
}
```

