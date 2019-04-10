import redis
import json

conn = redis.Redis(host='140.143.227.206',port=6379,password='1234')
conn.flushall()
# v = conn.keys()
# print(v)
"""
# 用户ID: 6
redis={
    luffy_shopping_car:{
        6:{
            11:{
                'title':'21天入门到放弃',
                'src':'xxx.png'
            }
        }
    }
}

"""
# 购买的第一商品
# data_dict = {
#     11:{
#         'title':'21天入门到放弃',
#         'src':'xxx.png'
#     }
# }
# conn.hset('luffy_shopping_car','6',json.dumps(data_dict))

# 购买的第二商品
# car = conn.hget('luffy_shopping_car','6')
# car_str = str(car,encoding='utf-8')
# car_dict = json.loads(car_str)
# print(car_dict)
#
# car_dict['12'] = {
#     'title':'22天入门到放弃',
#     'src':'xxx.png'
# }
#
# print(car_dict)
#
# conn.hset('luffy_shopping_car','6',json.dumps(car_dict))