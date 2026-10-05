'''
json.dumps(字典或列表, ensure_ascii=False)`：将
  ensure_ascii`参数确保中文能正常显示
  返回值：Json 字符串
json.loads(json字符串)`：将 Json 字符串转换为 Pyth
返回值：Python 字典 或 Python 列表
'''
import json

d = {
    "name": "周杰伦",
    "age": 11,
    "gender": "男"
}

s = json.dumps(d, ensure_ascii=False)
print(s)

l = [
    {
        "name": "周杰伦",
        "age": 11,
        "gender": "男"
    },
    {
        "name": "蔡依临",
        "age": 12,
        "gender": "女"
    },
    {
        "name": "小明",
        "age": 16,
        "gender": "男"
    }
]

print(json.dumps(l, ensure_ascii=False))

json_str = '{"name": "周杰伦", "age": 11, "gender": "男"}'
json_array_str = '[{"name": "周杰伦", "age": 11, "gender": "男"}, {"name": "蔡依临", "age": 12, "gender": "女"}]'

res_dict = json.loads(json_str)
print(res_dict, type(res_dict))

res_list = json.loads(json_array_str)
print(res_list, type(res_list))
