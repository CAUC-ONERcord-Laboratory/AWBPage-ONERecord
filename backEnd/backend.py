from flask import Flask, request, jsonify
from flask_cors import CORS
from sparql_queries import *
import time
from jsonldProcessor import JsonldProcessor
from pieceDataProcessor import PieceDataProcessor

app = Flask(__name__)

CORS(app, resources={r"/query": {"origins": "http://127.0.0.1:3000"}})
query_actions = {
    #相关方信息
    "Shipper": InvolvedParty.shipper,
    "Consignee": InvolvedParty.consinee,
    "Issued_by":InvolvedParty.airline,
    "Issuing_Carrier_Agent":InvolvedParty.carrierAgent,
    "Accounting_Information":InvolvedParty.accountingInformation,
    #航班信息
    "To": FightInformation.arrivalLocation,
    "Airport_of_Departure": FightInformation.departureLocation,
    "First_Carrier": FightInformation.airlineCode,
    "Airport_of_Destination": FightInformation.arrivalLocation,
    "Flight": FightInformation.transportIdentifier,
    "Date": FightInformation.departureDate,

    #PieceLevel
    "No_of_Pieces": PieceLevel.piecesCount,
    "Piece_References_URL": PieceLevel.pieceReferenceURL,


    #Basic Waybill Information
    "Waybill_Number": BasicWaybillInformation.waybillNumber,
    "Signature_of_Shipper_or_his_Agent": BasicWaybillInformation.consignorDeclarationSignature,
    "Signature_of_Carrier_or_its_Agent": BasicWaybillInformation.carrierDeclarationSignature,
    "Executed_Date": BasicWaybillInformation.carrierDeclarationDate,
    "Executed_Place": BasicWaybillInformation.carrierDeclarationPlace, 


    # #费用相关
    "WT_VAL": Charge.weightValuationIndicator,
    "Other": Charge.otherChargesIndicator,
    "Declared_Value_For_Carriage": Charge.declaredValueForCarriage,
    "Declared_Value_For_Customs": Charge.declaredValueForCustoms,
    "Amount_of_Insurance": Charge.insuredAmount,
    "Rate_Charge": Charge.rateCharge,
    "Other_Charges": Charge.othercharge,
    "Rate_Class_Code": Charge.rateClassCode,
    
    #需要计算得出的费用

    # "Weight_Charge_Prepaid": "",

    "Total_Other_Charges_Due_Agent": Charge.needToCulculate.durAgent,
    "Total_Other_Charges_Due_Carrier": Charge.needToCulculate.dueCarrier,
    # "Total_Prepaid": "",
    # "Total_Collect":"",

    # "Currency": ""
}


@app.route('/query', methods=['POST'])
def handle_query():
    # 校验请求数据格式
    data = request.get_json()
    if not data or 'waybill' not in data:
        return jsonify({"error": "Missing 'waybill' in request body"}), 400

    response = {}
    waybillProcessor = JsonldProcessor(data['waybill'])
    with open('graph_output.ttl', 'w') as f:
         f.write(waybillProcessor.graph.serialize(format='turtle'))

    #处理Piece数据
    pieceURL=waybillProcessor.graph.query(PieceLevel.pieceReferenceURL)#获取piece的URL
    print(pieceURL)
    pieceDataProcessor = PieceDataProcessor(pieceURL)
    pieceTotal=pieceDataProcessor.attributeTotal()
    response.update(pieceTotal)

    #处理Waybill数据
    total_start_time = time.perf_counter()  # 记录总耗时
    for key, query in query_actions.items():
        start_time = time.perf_counter()  # 记录开始时间
        try:
            result = waybillProcessor.execute_sparql_query(query)#执行查询

            response[key] = result
        except Exception as e:
            response[f"{key}_error"] = str(e)
        finally:  # 无论成功与否都会执行
            duration = time.perf_counter() - start_time  # 计算耗时
            # print(f"Query '{key}' executed in {duration:.6f} seconds")
    total_duration = time.perf_counter() - total_start_time  # 计算总耗时
    print(f"Total execution time: {total_duration:.6f} seconds")

    #WeightCharge计算
    response["Total_WeightCharge"] = response["Total_Chargeable_Weight"]*response["Rate_Charge"]["Value"]
    response["Total"] = response["Total_WeightCharge"]+response["Total_Other_Charges_Due_Agent"]+response["Total_Other_Charges_Due_Carrier"]
    
    return jsonify(response)




# 

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)