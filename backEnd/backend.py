from flask import Flask, request, jsonify
from flask_cors import CORS
from rdflib import Graph
import json
from sparql_queries import *
import time
import requests
from collections import defaultdict

app = Flask(__name__)

CORS(app, resources={r"/query": {"origins": "http://127.0.0.1:3000"}})
query_actions = {
    # #相关方信息
    # "Shipper": InvolvedParty.shipper,
    # "Consignee": InvolvedParty.consinee,
    # "Issued_by":InvolvedParty.airline,
    # "Issuing_Carrier_Agent":InvolvedParty.carrierAgent,
    # "Accounting_Information":InvolvedParty.accountingInformation,
    # #航班信息
    # "To": FightInformation.arrivalLocation,
    # "Airport_of_Departure": FightInformation.departureLocation,
    # "First_Carrier": FightInformation.airlineCode,
    # "Airport_of_Destination": FightInformation.arrivalLocation,
    # "Flight": FightInformation.transportIdentifier,
    # "Date": FightInformation.departureDate,

    #PieceLevel
    "No_of_Pieces": PieceLevel.piecesCount,
    "Piece_References_URL": PieceLevel.pieceReferenceURL,
                'goodsDescription': PieceLevel.goodsDescription,


    # #Basic Waybill Information
    # "No_of_Pieces": BasicWaybillInformation.pieceReferences,
    # "Signature_of_Shipper_or_his_Agent": BasicWaybillInformation.consignorDeclarationSignature,
    # "Executed_Date": BasicWaybillInformation.carrierDeclarationDate,
    # "Excuted_Place": BasicWaybillInformation.carrierDeclarationPlace, 

    # #费用相关
    # "WT_VAL": Charge.weightValuationIndicator,
    # "Other": Charge.otherChargesIndicator,
    # "Declared_Value_For_Carriage": Charge.declaredValueForCarriage,
    # "Declared_Value_For_Customs": Charge.declaredValueForCustoms,
    # "Amount_of_Insurance": Charge.insuredAmount,
    # "Rate_Charge": Charge.rateCharge,
    # "Other_Charges": Charge.othercharge,
    # "Rate_Class_Code": Charge.rateClassCode,

    # "Total": "",
    # "Weight_Charge_Prepaid": "",

    # "Total_Other_Charges_Due_Agent": Charge.dueAgent,
    # "Total_Other_Charges_Due_Carrier": Charge.dueCarrier,
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
    
    return jsonify(response)

class JsonldProcessor:
    def __init__(self, jsonld_data):
        self.jsonld_data = jsonld_data
        self.graph = Graph()
        self.graph.parse(data=json.dumps(jsonld_data), format='json-ld')
        with open('graph_output.ttl', 'w') as f:
            f.write(self.graph.serialize(format='turtle'))
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

def getPieceData(url):
    try:
        # 发送 GET 请求
        response = requests.get(url)
        
        # 检查响应状态码（200 表示成功）
        if response.status_code == 200:
            # 解析 JSON 数据
            json_data = response.json()
            print("Piece获取成功！")
            # print(json_data)
            return json_data
        else:
            print(f"请求失败，状态码：{response.status_code}")

    except requests.exceptions.RequestException as e:
        print(f"请求异常：{e}")
    except ValueError as e:
        print(f"JSON 解析失败：{e}")
class PieceDataProcessor:
    """处理 Piece 数据"""
    def __init__(self,pieceURL):
        self.urlList=list(pieceURL)
        # 使用嵌套字典存储所有属性数据
        self.attributes = defaultdict(dict)
        # 存储处理器实例
        self.processors = {}
        # 定义需要提取的属性和对应查询
        self.QUERY_MAPPING = {
            'grossWeight': PieceLevel.weight.grossWeight,
            'chargeableWeight': PieceLevel.weight.chargeableWeight,
            'dimensions': PieceLevel.dimensions,
            'goodsDescription': PieceLevel.goodsDescription,
            # 可扩展其他属性
        }
        self.total_attribute={}

    def process_pieces(self, result_dict):
        """处理所有piece数据"""
        for url, piece_data in result_dict.items():
            try:
                processor = JsonldProcessor(piece_data)
                self.processors[url] = processor
                
                # 为每个属性执行查询
                for attr, query in self.QUERY_MAPPING.items():
                    try:
                        result = processor.execute_sparql_query(query)
                        self.attributes[attr][url] = float(result)


                    except Exception as e:
                        print(f"{url} 的 {attr} 查询失败: {str(e)}")
                        self.attributes[attr][url] = None
                        
            except Exception as e:
                print(f"处理器创建失败 {url}: {str(e)}")
                continue

    def get_total(self, attribute):
        """获取指定属性的总和"""
        values = [v for v in self.attributes[attribute].values() if v is not None]
        return sum(values) if values else 0

    def get_attribute_data(self, attribute):
        """获取指定属性的完整数据"""
        return dict(self.attributes[attribute])
    def attributeTotal(self):

        result_dict = {str(item[0]): getPieceData(str(item[0])) for item in self.urlList}#获取piece数据存在字典中
        # 假设已经获取result_dict
        self.process_pieces(result_dict)
        
        # 获取各属性数据
        gross_weights = self.get_attribute_data('grossWeight')
        chargeable_weights = self.get_attribute_data('chargeableWeight')
        dimensions = self.get_attribute_data('dimensions')
        goods_descriptions = self.get_attribute_data('goodsDescription')
        
        # 计算总和
        total_gross = self.get_total('grossWeight')
        total_chargeable = self.get_total('chargeableWeight')
        total_dimensions = self.get_total('dimensions')
        # total_goods_descriptions = self.get_total('goodsDescription')
        
        #存入字典
        self.total_attribute["total_gross"]  = total_gross
        self.total_attribute["total_chargeable"]  = total_chargeable
        self.total_attribute["total_dimensions"]  = total_dimensions

        print("毛重数据:", gross_weights)
        print("计费重数据:", chargeable_weights)
        print("尺寸数据:", dimensions)
        print("货物描述数据:", goods_descriptions)
        print(f"总毛重: {total_gross}, 总计费重: {total_chargeable}")

        return self.total_attribute


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)