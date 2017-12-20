# CamRest676_chinese
CamRest676 is an English data set, I translate it into Chinese for training nlu.
CamRest676/Cam676_to_nlu.py 

功能：对CamRest676.json进行处理

```
# 处理思路
1.翻译原句
‘I am wanting an expensive restaurant that offers African food. What is their number?’
‘我想找一家提供非洲食物的昂贵的餐厅，请问电话是多少？’
2.翻译标注结果
[{"act": "request", "slots": [["slot","phone"]]}, 
{"act": "inform", "slots": [["food","african"]]}, 
{"act": "inform", "slots": [["pricerange", "expensive"]]}]
set(["request","phone", None],["inform", "food", "非洲的"],["inform", "pricerange", "昂贵的"])
3.匹配并返回标注结果
对于["inform", "food", "非洲的"]，将"非洲的"与翻译的句子匹配，标注对应的字
对于["request","phone", None]，将"phone"翻译为"电话"与翻译的句子匹配，标注对应的字
4.对于匹配不上的，写入CamRest676/CamRest676_no_match
5.对于一些比较多的匹配错误，比如‘南部’，‘南方’之类的，进行二次处理
```
CamRest676/no_match_process.py

功能：对匹配不上的句子进行规则的处理

data_gennerate.py

功能：从原始数据集中提取TC-Bot需要的知识库，goal_set等数据

数据：

- CamRest676.json：原始的数据集
- CamRest676_no_match：经过处理后仍然匹配不到结果的句子，还有244条
- CamRest_usable_2273.json：可用的中文版训练数据，共2273条
- CamRestDB.json：所有的餐厅信息，每一条为一家餐厅的信息，英文
- CamRestOTGY.json：所有slot的值的统计结果
- goal_set2.json：处理得到的user_goal
