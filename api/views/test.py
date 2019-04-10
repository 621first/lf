#
#
# # redis的功能 写死的数据
#
#
#
# import json
# import redis
#
# from django.shortcuts import render, HttpResponse
# from django_redis import get_redis_connection
#
# """
# redis->{
#     shopping_car:{
#         用户ID:{
#             课程1:{
#                 title:'金融量化分析入门',
#                 img:'/xx/xx/xx.png',
#                 policy:{
#                     10: {'name':'有效期1个月','price':599},
#                     11: {'name':'有效期3个月','price':1599},
#                     13: {'name':'有效期6个月','price':2599},
#                 },
#                 default_policy:12
#             },
#         },
#     }
# }
# """
#
#
#
#
# def test_redis(request):
#     conn = get_redis_connection("default")
#     conn.hset('shopping_car', 'xiaoqiang', json.dumps(
#         {'课程1': {
#             'title': '金融量化分析入门',
#             'img': '/xx/xx/xx.png',
#             'policy': {
#                 10: {'name': '有效期1个月', 'price': 599},
#                 11: {'name': '有效期3个月', 'price': 1599},
#                 13: {'name': '有效期6个月', 'price': 2599},
#             },
#             'default_policy': 12
#         }}, ensure_ascii=False))
#     print(conn.hget('shopping_car', 'xiaoqiang'))
#     return HttpResponse('Test OK...')
