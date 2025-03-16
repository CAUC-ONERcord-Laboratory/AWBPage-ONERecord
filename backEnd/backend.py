from flask import Flask, request, jsonify
from flask_cors import CORS
from rdflib import Graph
from rdflib.plugins.sparql import processUpdate
import json
from sparql_queries import *
import time

app = Flask(__name__)

CORS(app, resources={r"/query": {"origins": "http://127.0.0.1:3000"}})


@app.route('/query', methods=['POST'])
def handle_query():
    # 校验请求数据格式
    data = request.get_json()
    if not data or 'waybill' not in data:
        return jsonify({"error": "Missing 'waybill' in request body"}), 400
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
        "No_of_Pieces": BasicWaybillInformation.pieceReferences,
        "Signature_of_Shipper_or_his_Agent": BasicWaybillInformation.consignorDeclarationSignature,
        "Executed_Date": BasicWaybillInformation.carrierDeclarationDate,
        "Excuted_Place": BasicWaybillInformation.carrierDeclarationPlace, 

        #费用相关
        "WT_VAL": Charge.weightValuationIndicator,
        "Other": Charge.otherChargesIndicator,
        "Declared_Value_For_Carriage": Charge.declaredValueForCarriage,
        "Declared_Value_For_Customs": Charge.declaredValueForCustoms,
        "Amount_of_Insurance": Charge.insuredAmount,
        "Rate_Charge": Charge.rateCharge,

        # "Total": "",
        # "Weight_Charge_Prepaid": "",
        "Other_Charges": Charge.othercharge,
        # "Total_Other_Charges_Due_Agent": Charge.dueAgent,
        # "Total_Other_Charges_Due_Carrier": Charge.dueCarrier,
        # "Total_Prepaid": "",
        # "Total_Collect":"",
        "Rate_Class_Code": Charge.rateClassCode,
        # "Currency": ""
    }
    response = {}
    processor = JsonldProcessor(data['waybill'])
    
    total_start_time = time.perf_counter()  # 记录总耗时
    for key, query in query_actions.items():
        start_time = time.perf_counter()  # 记录开始时间
        try:
            result = processor.execute_sparql_query(query)
            response[key] = result
        except Exception as e:
            response[f"{key}_error"] = str(e)
        finally:  # 无论成功与否都会执行
            duration = time.perf_counter() - start_time  # 计算耗时
            # 打印带查询标识和耗时的信息（保留2位小数）
            print(f"Query '{key}' executed in {duration:.6f} seconds")
    total_duration = time.perf_counter() - total_start_time  # 计算总耗时
    print(f"Total execution time: {total_duration:.6f} seconds")
    
    return jsonify(response)

class JsonldProcessor:
    def __init__(self, jsonld_data):
        self.jsonld_data = jsonld_data
        self.graph = Graph()
        self.graph.parse(data=json.dumps(jsonld_data), format='json-ld')
    
    def jsonld_to_rdf_graph(self):
        """将 JSON-LD 数据转换为 RDF 图"""
        return self.graph
    def execute_sparql_query(self,sparql_query):
        """执行 SPARQL 查询并返回 JSON 序列化结果"""
        results = self.graph.query(sparql_query)
        # print(results)
        # 将 SPARQL 结果转换为 JSON 格式
        if results.type == 'SELECT':
            # 将结果转换为列表，以便获取行数
            rows = list(results)
            
            # 如果没有结果，返回空列表 []
            if len(rows) == 0:
                return []
            
            elif len(rows) == 1:
                result_row = rows[0]  # 直接操作 ResultRow 对象
                if len(result_row) == 1:  # 检查结果行是否只有一个元素
                    # 直接提取第一个元素的 URI 字符串
                    return str(rows[0][0])  # 例如 'https://onerecord.iata.org/ns/code-lists/RateClassCode#Q'
                else:
                    # 如果是多列结果，保持原逻辑转为字典（可选）
                    return {str(k): str(v) for k, v in result_row.asdict().items()}
            
            # 如果有多行，返回列表 [ {}, {}, ... ]
            else:

                # for row in rows:
                #     print(row)
                return [
                    {
                        str(var): str(val) 
                        for var, val in row.asdict().items()
                    } 
                    for row in rows
                ]




if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)