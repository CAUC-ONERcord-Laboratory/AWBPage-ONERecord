import threading
from rdflib import Graph

def test_thread(graph):
    try:
        graph.query("""PREFIX cargo: <https://onerecord.iata.org/ns/cargo#> 
                    PREFIX code: <https://onerecord.iata.org/ns/code-lists/> 
                    SELECT ?name 
                    WHERE { 
                        ?party a cargo:Party ; 
                        cargo:partyRole <https://onerecord.iata.org/ns/code-lists/ParticipantIdentifier#SHP> ; 
                        cargo:partyDetails [ cargo:name ?name ] . 
                    }""")
    except Exception as e:
        print(f"Error: {e}")

g = Graph()
g.parse(data="""{
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
    }""", format='json-ld')
threads = [threading.Thread(target=test_thread, args=(g,)) for _ in range(10)]
[t.start() for t in threads]
[t.join() for t in threads]