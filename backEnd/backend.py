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

    try:
        waybill_data = data['waybill']
        print("Received waybill data:", waybill_data)  # 添加调试日志
        
        # 如果是简单格式，直接返回
        if isinstance(waybill_data, dict) and 'Name' in waybill_data and 'Address' in waybill_data:
            response = {
                "Shipper": {
                    "Name": waybill_data['Name'],
                    "Address": waybill_data['Address']
                }
            }
            print("Response for simple format:", response)  # 添加调试日志
            return jsonify(response)
            
        # 否则使用 ONE Record 格式处理
        processor = JsonldProcessor(waybill_data)
        
        # 获取发货人信息
        shipper_result = processor.execute_sparql_query(InvolvedParty.shipper)
        print("SPARQL query result:", shipper_result)  # 添加调试日志
        
        # 获取收货人信息
        consignee_result = processor.execute_sparql_query(InvolvedParty.consinee)
        response = {
            "Shipper": {
                "Name": shipper_result.get("Name", "") if shipper_result else "",
                "Address": shipper_result.get("Address", "") if shipper_result else ""
            },
            "Consignee": {
                "Name": consignee_result.get("Name", "") if consignee_result else "",
                "Address": consignee_result.get("Address", "") if consignee_result else ""
            }
        }
        
        print("Response for ONE Record format:", response)  # 添加调试日志
        return jsonify(response)
    except Exception as e:
        print("Error:", str(e))  # 添加调试日志
        return jsonify({"error": str(e)}), 500

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
            
            # 如果只有一行，返回单个字典 {}
            elif len(rows) == 1:
                return {
                    str(var): str(val) 
                    for var, val in rows[0].asdict().items()
                }
            
            # 如果有多行，返回列表 [ {}, {}, ... ]
            else:
                return [
                    {
                        str(var): str(val) 
                        for var, val in row.asdict().items()
                    } 
                    for row in rows
                ]




if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)