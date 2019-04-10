from rest_framework.views import APIView
from rest_framework.response import Response
from api.utils.auth import LuffyAuth
from django.conf import settings
# from django_redis import get_redis_connection
import json
from api.utils.response import BaseResponse
from api import models
import datetime


class OrderViewSet(APIView):

    def post(self,request,*args,**kwargs):
        """
        立即支付
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        """
        1. 获取用户提交数据
                {
                    balance:1000,
                    money:900
                }
           balance = request.data.get("balance")
           money = request.data.get("money")
           
        2. 数据验证
            - 大于等于0
            - 个人账户是否有1000贝里
            
            if user.auth.user.balance < balance:
                账户贝里余额不足
                
        优惠券ID_LIST = [1,3,4]
        总价
        实际支付
        3. 去结算中获取课程信息
            for course_dict in redis的结算中获取：
                # 获取课程ID
                # 根据course_id去数据库检查状态
                
                # 获取价格策略
                # 根据policy_id去数据库检查是否还依然存在
                
                # 获取使用优惠券ID
                # 根据优惠券ID检查优惠券是否过期
                
                # 获取原价+获取优惠券类型
                    - 立减
                        0 = 获取原价 - 优惠券金额
                        或
                        折后价格 = 获取原价 - 优惠券金额
                    - 满减：是否满足限制
                        折后价格 = 获取原价 - 优惠券金额
                    - 折扣：
                        折后价格 = 获取原价 * 80 / 100
                        
        4. 全站优惠券
            - 去数据库校验全站优惠券的合法性
            - 应用优惠券：
                - 立减
                    0 = 实际支付 - 优惠券金额
                    或
                    折后价格 =实际支付 - 优惠券金额
                - 满减：是否满足限制
                    折后价格 = 实际支付 - 优惠券金额
                - 折扣：
                    折后价格 = 实际支付 * 80 / 100
            - 实际支付
        5. 贝里抵扣
        
        6. 总金额校验
            实际支付 - 贝里 = money:900
        
        7. 为当前课程生成订单
            - 事务
                - 订单表创建一条数据 Order
                    - 订单详细表创建一条数据 OrderDetail   EnrolledCourse
                    - 订单详细表创建一条数据 OrderDetail   EnrolledCourse
                    - 订单详细表创建一条数据 OrderDetail   EnrolledCourse
                
                - 如果有贝里支付
                    - 贝里金额扣除  Account
                    - 交易记录     TransactionRecord
                
                - 优惠券状态更新   CouponRecord
                
                注意：
                    如果支付宝支付金额0，  表示订单状态：已支付
                    如果支付宝支付金额110，表示订单状态：未支付
                        - 生成URL（含订单号）
                        - 回调函数：更新订单状态
                    
        """
        pass
