import requests
from collections import defaultdict
from jsonldProcessor import JsonldProcessor
from sparql_queries import *
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
            return {"error": f"Request failed with status code {response.status_code}"}
            

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
                        if attr=='goodsDescription':
                            result = processor.execute_sparql_query(query)
                            self.attributes[attr][url] = result
                        else:
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
        
        #存入字典
        self.total_attribute["Total_Gross_Weight"]  = total_gross
        self.total_attribute["Total_Chargeable_Weight"]  = total_chargeable
        self.total_attribute["Total_Dimensions"]  = total_dimensions
        self.total_attribute["Total_Goods_Descriptions"]  = goods_descriptions

        print("毛重数据:", gross_weights)
        print("计费重数据:", chargeable_weights)
        print("尺寸数据:", dimensions)
        print("货物描述数据:", goods_descriptions)
        print(f"总毛重: {total_gross}, 总计费重: {total_chargeable}")

        return self.total_attribute