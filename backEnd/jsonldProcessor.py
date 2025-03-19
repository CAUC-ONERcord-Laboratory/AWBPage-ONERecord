from rdflib import Graph
import json
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

        # 将 SPARQL 结果转换为 JSON 格式
        rows = list(results)#List便于统计行数
        print("rows",rows)
        print("rows[0]:",rows[0])
        if not rows:  # 空结果快速返回
            return []       
        # 根据结果行数分发处理逻辑
        return (

            handle_single_row(rows[0]) if len(rows[0]) == 1 
            else handle_multiple_rows(rows)
        )


def handle_single_row(row):
    """ 解析单列值 """
    for key, value in row.asdict().items(): 
        # print(f"[Key] {key} [Value] {value}")   
        # 所有value转化为float，否则为str    
        if 'value' in key.lower():
            # print(f"[Charge Value] {key}")
            return safe_float_convert(value)
        return value



def safe_float_convert(s):
    """ 安全转换为浮点数 """
    try:
        return float(s)
    except ValueError:
        return s


def handle_multiple_rows(rows):
    """ 处理多行结果 """
    result_dict = {}
    for k, v in rows[0].asdict().items():
        if 'Value' in str(k):
            result_dict[str(k)] = float(v)
        else:
            result_dict[str(k)] = str(v)
    return result_dict