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
    arrivalLocation="""PREFIX cargo: <https://onerecord.iata.org/ns/cargo#> 
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
                    SELECT ?code 
                    WHERE { 
                        ?waybill a cargo:Waybill ;
                        cargo:departureLocation ?location .
                        ?location a cargo:Location ; 
                        cargo:locationCodes ?locationCodes . 
                        ?locationCodes cargo:code ?code .
                    
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

                      SELECT ?departureDate
                      WHERE {
                        # 从 Waybill 导航到 TransportLegs
                        ?waybill a cargo:Waybill ;
                          cargo:referredBookingOption/cargo:bookingRequest/cargo:forBookingOption/cargo:transportLegs ?transportLeg .

                        # 提取 departureDate 的 xsd:dateTime 值
                        ?transportLeg cargo:departureDate ?dateNode .
                        BIND(STRDT(STR(?dateNode), xsd:dateTime) AS ?departureDate)
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
                                    SELECT ?consignorDeclarationSignature
                                    WHERE {
                                      # 直接匹配 Waybill 的 consignorDeclarationSignature 属性
                                      ?waybill a cargo:Waybill ;
                                        cargo:consignorDeclarationSignature ?consignorDeclarationSignature .
                                    }"""


    carrierDeclarationSignature="""PREFIX cargo: <https://onerecord.iata.org/ns/cargo#>

                                    SELECT ?carrierDeclarationSignature
                                    WHERE {
                                      # 直接匹配 Waybill 的 consignorDeclarationSignature 属性
                                      ?waybill a cargo:Waybill ;
                                        cargo:carrierDeclarationSignature ?carrierDeclarationSignature .
                                    }
                                    """

    carrierDeclarationDate="""PREFIX cargo: <https://onerecord.iata.org/ns/cargo#>
                               PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>

                                SELECT ?Date
                                WHERE {
                                  # 直接匹配 Waybill 的 carrierDeclarationDate 属性
                                  ?waybill a cargo:Waybill ;
                                    cargo:carrierDeclarationDate ?dateNode .

                                  # 提取 xsd:dateTime 类型的值（注意数据中实际只有日期部分）
                                  BIND(STRDT(STR(?dateNode), xsd:dateTime) AS ?Date)
                                }
                                    """

    carrierDeclarationPlace="""PREFIX cargo: <https://onerecord.iata.org/ns/cargo#>

                                SELECT ?code
                                WHERE {
                                  # 从 Waybill 导航到 Location
                                  ?waybill a cargo:Waybill ;
                                    cargo:carrierDeclarationPlace ?place .

                                  # 提取 Location 的 locationCodes 中的 code
                                  ?place cargo:locationCodes/cargo:code ?code .
                                }
                                    """
class Charge:
        weightValuationIndicator="""
                                    PREFIX cargo: <https://onerecord.iata.org/ns/cargo#>
                                    PREFIX PrepaidCollectIndicator: <https://onerecord.iata.org/ns/code-lists/PrepaidCollectIndicator#>
                                    SELECT ?weightValuationIndicator
                                    WHERE { 
                                        ?waybill cargo:weightValuationIndicator ?weightValuationIndicator.
                                    }
                                    """
        otherChargesIndicator="""
                                PREFIX cargo: <https://onerecord.iata.org/ns/cargo#>
                                PREFIX PrepaidCollectIndicator: <https://onerecord.iata.org/ns/code-lists/PrepaidCollectIndicator#>
                                SELECT ?otherChargesIndicator
                                WHERE { 
                                    ?waybill cargo:otherChargesIndicator ?otherChargesIndicator.
                                }
                                """
        declaredValueForCarriage="""
                                    PREFIX cargo: <https://onerecord.iata.org/ns/cargo#>
                                    SELECT ?Unit ?Value
                                    WHERE { 
                                        ?waybill cargo:declaredValueForCarriage [
                                                    cargo:currencyUnit ?Unit ;
                                                    cargo:numericalValue ?Value
                                                    ].
                                    }
                                    """
        declaredValueForCustoms=""" 
                                PREFIX cargo: <https://onerecord.iata.org/ns/cargo#>
                                    SELECT ?unit ?Value
                                    WHERE { 
                                        ?waybill cargo:declaredValueForCustoms [
                                                    cargo:currencyUnit ?unit ;
                                                    cargo:numericalValue ?Value
                                                    ].
                                    } 
                                """
        insuredAmount="""
                        PREFIX cargo: <https://onerecord.iata.org/ns/cargo#>
                        SELECT ?unit ?Value
                        WHERE { 
                            ?waybill cargo:insuredAmount [
                                        cargo:currencyUnit ?unit ;
                                        cargo:numericalValue ?Value
                                        ].
                        }
                        """
        rateCharge="""  
                        PREFIX cargo: <https://onerecord.iata.org/ns/cargo#>
                        SELECT ?unit ?Value
                        WHERE { 
                            ?waybill cargo:rateCharge [
                                        cargo:currencyUnit ?unit ;
                                        cargo:numericalValue ?Value
                                        ].
                        }
                        """
        # "Total": "",
        # "Weight_Charge_Prepaid": "",
        othercharge=""" PREFIX cargo: <https://onerecord.iata.org/ns/cargo#>
                        SELECT ?otherChargeCode ?resonDescription ?Value ?Unit ?entitlement
                        WHERE { 
                                ?waybill cargo:otherCharges [
                                        a cargo:OtherCharge ;
                                        cargo:otherChargeCode ?otherChargeCode ;
                                        cargo:entitlement ?entitlement ;
                                        cargo:reasonDescription ?resonDescription ;
                                        cargo:otherChargeAmount [
                                            cargo:currencyUnit ?Unit ;
                                            cargo:numericalValue ?Value
                                        ]
                                 ]
                        }
                        """
        rateClassCode="""                        PREFIX cargo: <https://onerecord.iata.org/ns/cargo#>
                        SELECT ?rateClassCode
                        WHERE { 
                            ?waybill cargo:rateClassCode ?rateClassCode.
                        }"""
        # "Total_Other_Charges_Due_Carrier": Charge.dueCarrier,
        # "Total_Prepaid": "",
        # "Total_Collect":"",
class PieceLevel:
        piecesCount="""
                        PREFIX cargo: <https://onerecord.iata.org/ns/cargo#>

                        SELECT (COUNT(?pieceRef) AS ?pieceCount)
                        WHERE {
                        # 定位到具体的 WaybillLineItem
                        ?waybillLineItem a cargo:WaybillLineItem ;
                        
                        cargo:pieceReferences ?pieceRef .
                        }
                        GROUP BY ?waybillLineItem
                        """
        pieceReferenceURL="""PREFIX cargo: <https://onerecord.iata.org/ns/cargo#>

                        SELECT ?pieceURL
                        WHERE {
                        ?waybillLineItem a cargo:WaybillLineItem ;
                                        cargo:pieceReferences ?pieceURL .
                        }"""
        class weight:
            grossWeight="""
                        PREFIX cargo: <https://onerecord.iata.org/ns/cargo#>

                        SELECT ?numericalValue
                        WHERE {
                        # 匹配类型为 cargo:Piece 的节点
                        ?piece a cargo:Piece ;
                                # 获取其 cargo:grossWeight 属性
                                cargo:grossWeight/cargo:numericalValue ?numericalValue ;
                        }"""
            chargeableWeight="""
                        PREFIX cargo: <https://onerecord.iata.org/ns/cargo#>
                        PREFIX code:  <https://onerecord.iata.org/ns/code-lists/>

                        SELECT ?numericalValue
                        WHERE {
                        ?piece a cargo:Piece ;
                                cargo:volumetricWeight/cargo:chargeableWeight/cargo:numericalValue ?numericalValue ;

                        }"""