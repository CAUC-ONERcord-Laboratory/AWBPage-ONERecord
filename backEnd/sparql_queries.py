class InvolvedParty:
    shipper="""PREFIX cargo: <https://onerecord.iata.org/ns/cargo#>
                PREFIX ParticipantIdentifier:  <https://onerecord.iata.org/ns/code-lists/ParticipantIdentifier#>
                SELECT ?Name ?Address 
                WHERE { 
                        ?waybill a cargo:Waybill.
                        ?waybill cargo:involvedParties [ 
                        <https://onerecord.iata.org/ns/cargo#partyRole>  ParticipantIdentifier:SHP ;
                        cargo:partyDetails [
                            cargo:name ?Name ;
                            cargo:basedAtLocation/cargo:locationName ?Address
                        ]
                    ]   
                }"""
    consinee="""PREFIX cargo: <https://onerecord.iata.org/ns/cargo#> 
                    PREFIX ParticipantIdentifier: <https://onerecord.iata.org/ns/code-lists/ParticipantIdentifier#>
                    SELECT ?Name ?Address
                    WHERE { 
                            ?waybill cargo:involvedParties [ 
                            cargo:partyRole ParticipantIdentifier:CNE ;
                            cargo:partyDetails [
                                cargo:name ?Name ;
                                cargo:basedAtLocation/cargo:locationName ?Address
                            ]
                            ]
                    }"""
    airline="""PREFIX cargo: <https://onerecord.iata.org/ns/cargo#> 
                    PREFIX ParticipantIdentifier: <https://onerecord.iata.org/ns/code-lists/ParticipantIdentifier#>
                    SELECT ?Name ?Airlinecode
                    WHERE { 
                            ?waybill cargo:involvedParties [ 
                            cargo:partyRole ParticipantIdentifier:AIR ;
                            cargo:partyDetails [
                                cargo:name ?Name ;
                                cargo:airlineCode ?Airlinecode
                            ]
                        ]
                    }"""
    carrierAgent="""PREFIX cargo: <https://onerecord.iata.org/ns/cargo#> 
                    PREFIX ParticipantIdentifier: <https://onerecord.iata.org/ns/code-lists/ParticipantIdentifier#>
                    SELECT ?Name
                    WHERE { 
                        ?waybill cargo:involvedParties [ 
                        cargo:partyRole ParticipantIdentifier:AGT ;
                        cargo:partyDetails [
                            cargo:name ?Name
                            ]
                        ]
                    }"""
    accountingInformation="""PREFIX cargo: <https://onerecord.iata.org/ns/cargo#>
                            SELECT ?accountingNoteText
                            WHERE { 
                                ?waybill cargo:accountingNotes [ 
                                cargo:accountingNoteText ?accountingNoteText ;
                                ]
                            }"""

class FightInformation:
    arrivalLocationCode="""PREFIX cargo: <https://onerecord.iata.org/ns/cargo#> 
                    PREFIX code: <https://onerecord.iata.org/ns/code-lists/> 
                    SELECT ?code 
                    WHERE { 
                        ?waybill a cargo:Waybill ;
                        cargo:arrivalLocation ?location .
                        ?location a cargo:Location ; 
                        cargo:locationCodes ?locationCodes . 
                        ?locationCodes cargo:code ?code .
                    
                    }"""

    departureLocation="""PREFIX cargo: <https://onerecord.iata.org/ns/cargo#> 
                    PREFIX code: <https://onerecord.iata.org/ns/code-lists/> 
                    SELECT ?departurelocation 
                    WHERE { 
                        ?waybill a cargo:Waybill ;
                        cargo:departureLocation ?location .
                        ?location a cargo:Location ; 
                        cargo:locationCodes ?locationCodes . 
                        ?locationCodes cargo:code ?departurelocation .
                    
                    }"""

    airlineCode="""PREFIX cargo: <https://onerecord.iata.org/ns/cargo#> 
                        PREFIX code: <https://onerecord.iata.org/ns/code-lists/> 
                        SELECT ?airlineCode 
                        WHERE { 
                            ?party a cargo:Party ;
                                   cargo:partyDetails ?carrierDetails .
                            
                            ?carrierDetails a cargo:Carrier ; 
                                            cargo:airlineCode ?airlineCode . 
                        }"""

    locationName=arrivalLocationCode

    transportIdentifier="""PREFIX cargo: <https://onerecord.iata.org/ns/cargo#>
                          SELECT ?transportIdentifier
                          WHERE { 
                              ?waybill a cargo:Waybill ;
                                       cargo:referredBookingOption ?booking .

                              ?booking cargo:bookingRequest ?bookingRequest .
                              ?bookingRequest cargo:forBookingOption ?bookingOption .
                              ?bookingOption cargo:transportLegs ?transportLeg .

                              ?transportLeg a cargo:TransportLegs ;
                                            cargo:transportIdentifier ?transportIdentifier .
                          }"""

    departureDate="""PREFIX cargo: <https://onerecord.iata.org/ns/cargo#>
                      PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>

                      SELECT ?departureDateValue
                      WHERE {
                        # 从 Waybill 导航到 TransportLegs
                        ?waybill a cargo:Waybill ;
                          cargo:referredBookingOption/cargo:bookingRequest/cargo:forBookingOption/cargo:transportLegs ?transportLeg .

                        # 提取 departureDate 的 xsd:dateTime 值
                        ?transportLeg cargo:departureDate ?dateNode .
                        BIND(STRDT(STR(?dateNode), xsd:dateTime) AS ?departureDateValue)
                      }
                      """

class BasicWaybillInformation:
    pieceReferences="""PREFIX cargo: <https://onerecord.iata.org/ns/cargo#>
                        SELECT ?pieceRefId
                        WHERE {
                          # 从 Waybill 导航到 WaybillLineItem
                          ?waybill a cargo:Waybill ;
                            cargo:waybillLineItems ?lineItem .

                          # 提取 pieceReferences 的 @id 值
                          ?lineItem cargo:pieceReferences ?pieceRef .
                          BIND(STR(?pieceRef) AS ?pieceRefId)
                        }"""

    consignorDeclarationSignature="""PREFIX cargo: <https://onerecord.iata.org/ns/cargo#>
                                    SELECT ?consignorSignature
                                    WHERE {
                                      # 直接匹配 Waybill 的 consignorDeclarationSignature 属性
                                      ?waybill a cargo:Waybill ;
                                        cargo:consignorDeclarationSignature ?consignorSignature .
                                    }"""


    carrierDeclarationSignature="""PREFIX cargo: <https://onerecord.iata.org/ns/cargo#>

                                    SELECT ?consignorSignature
                                    WHERE {
                                      # 直接匹配 Waybill 的 consignorDeclarationSignature 属性
                                      ?waybill a cargo:Waybill ;
                                        cargo:carrierDeclarationSignature ?consignorSignature .
                                    }
                                    """

    carrierDeclarationDate="""PREFIX cargo: <https://onerecord.iata.org/ns/cargo#>
                               PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>

                                SELECT ?carrierDateValue
                                WHERE {
                                  # 直接匹配 Waybill 的 carrierDeclarationDate 属性
                                  ?waybill a cargo:Waybill ;
                                    cargo:carrierDeclarationDate ?dateNode .

                                  # 提取 xsd:dateTime 类型的值（注意数据中实际只有日期部分）
                                  BIND(STRDT(STR(?dateNode), xsd:dateTime) AS ?carrierDateValue)
                                }
                                    """

    carrierDeclarationPlace="""PREFIX cargo: <https://onerecord.iata.org/ns/cargo#>

                                SELECT ?locationCode
                                WHERE {
                                  # 从 Waybill 导航到 Location
                                  ?waybill a cargo:Waybill ;
                                    cargo:carrierDeclarationPlace ?place .

                                  # 提取 Location 的 locationCodes 中的 code
                                  ?place cargo:locationCodes/cargo:code ?locationCode .
                                }
                                    """

