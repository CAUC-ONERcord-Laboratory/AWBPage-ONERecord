from rdflib import Graph
import json
class JsonldProcessor:
    def __init__(self, jsonld_data):
        self.jsonld_data = jsonld_data
        self.graph = Graph()
        self.graph.parse(data=json.dumps(jsonld_data), format='json-ld')
        # with open('graph_output.ttl', 'w') as f:
        #     f.write(self.graph.serialize(format='turtle'))
    
    def execute_sparql_query(self,sparql_query):
        """执行 SPARQL 查询并返回 JSON 序列化结果"""
        results = self.graph.query(sparql_query)
        # 将 SPARQL 结果转换为 JSON 格式
        rows = list(results)#List便于统计行数
        print(rows)
        print(len(rows[0]))
        print(len(rows))
        if not rows:  # 空结果快速返回
            return []       
        # 根据结果行数分发处理逻辑
        return (
            handle_single_row(rows[0]) if len(rows) == 1
            else handle_multiple_rows(rows)  
        )


# def handle_single_row(row):
#     """ 解析单列值 """
#     if len(row) > 1:  
#         row_dict = {}
#         for k, v in row.asdict().items():
#             key = str(k)
#             value = float(v) if "Value" in key else str(v)
#             row_dict[key] = value
#         return row_dict
#     else:
#         for key, value in row.asdict().items():   
#             # 所有value转化为float，否则为str    
#             if 'value' in key.lower():
#                 return safe_float_convert(value)
#             else:
#                 return value

# def handle_multiple_rows(rows):
#     """ 将所有行转换为字典列表 """
#     print("多行数据")
#     print(rows)
#     result_list = []
#     for row in rows:  # 遍历所有行
#         row_dict = {}
#         for k, v in row.asdict().items():
#             key = str(k)
#             value = float(v) if "Value" in key else str(v)
#             row_dict[key] = value
#         result_list.append(row_dict)  # 保存每一行
#     return result_list

# def safe_float_convert(s):
#     """ 安全转换为浮点数 """
#     try:
#         return float(s)
#     except ValueError:
#         return s

def convert_row_to_dict(row):
    """通用行转换函数 (核心逻辑封装)"""
    row_dict = {}
    for k, v in row.asdict().items():
        key = str(k)
        # 统一使用小写判断，增强兼容性
        if 'value' in key.lower():
            converted = safe_float_convert(v)
        else:
            converted = str(v)
        row_dict[key] = converted
    return row_dict

def handle_single_row(row):
    """处理单行数据（保持返回类型一致性）"""
    # 统一返回字典类型，便于后续处理
    if len(row) > 1:
        return convert_row_to_dict(row)
    
    # 处理单列情况仍返回字典，保持接口一致性
    # 若确实需要返回单值，可改为返回 converted_value
    # 单列时返回基础值
    key, value = next(iter(row.asdict().items()))
    return safe_float_convert(value) if 'value' in key.lower() else str(value)

def handle_multiple_rows(rows):
    """处理多行数据（优化可读性）"""
    return [convert_row_to_dict(row) for row in rows]

def safe_float_convert(value):
    """安全转换为浮点数，失败时返回字符串"""
    try:
        return float(value)
    except (ValueError, TypeError):
        return str(value)