from rest_framework.views import APIView
from rest_framework.response import Response
from api.utils.auth import LuffyAuth
from django.conf import settings
from django_redis import get_redis_connection
import json
from api.utils.response import BaseResponse
from api import models
import datetime

class PaymentViewSet(APIView):

    authentication_classes =  [LuffyAuth,]
    conn = get_redis_connection("default")

    def post(self,request,*args,**kwargs):
        ret = BaseResponse()
        try:
            # 在重复提交支付请求时清空当前用户结算中心的上一次的数据
            # luffy_payment_1_*
            # luffy_payment_coupon_1
            key_list = self.conn.keys( settings.PAYMENT_KEY %(request.auth.user_id,"*",) )
            key_list.append(settings.PAYMENT_COUPON_KEY %(request.auth.user_id,))
            self.conn.delete(*key_list)

            #存放所有的课程支付信息：包括（课程信息、优惠券信息、策略信息）
            payment_dict = {}
            #没有绑定课程的优惠券
            global_coupon_dict = {
                "coupon":{},
                "default_coupon":0
            }

            # 1. 在支付中心获取用户所有的需要结算课程ID
            course_id_list = request.data.get('courseids')  #由前端放松的请求提供，此处postman处理
            for course_id in course_id_list:
                car_key = settings.SHOPPING_CAR_KEY %(request.auth.user_id,course_id,)

                # 1.1 检测用户要结算的课程是否已经加入购物车
                if not self.conn.exists(car_key):
                    ret.code = 1001
                    ret.error = "课程需要先加入购物车才能结算"
                # 1.2 从购物车中获取信息，放入到结算中心。
                #所有的策略信息
                policy = json.loads(self.conn.hget(car_key, 'policy').decode('utf-8'))
                #默认策略的id
                default_policy = self.conn.hget(car_key, 'default_policy').decode('utf-8')
                #获取默认策略的信息
                policy_info = policy[default_policy]

                #存放每个课程的支付信息
                payment_course_dict = {
                    "course_id":str(course_id),
                    "title":self.conn.hget(car_key, 'title').decode('utf-8'),
                    "img":self.conn.hget(car_key, 'img').decode('utf-8'),
                    "policy_id":default_policy,
                    "coupon":{},#优惠券信息
                    "default_coupon":0
                }
                #更新字典，将一个字典加入到另外一个字典
                #将默认的策略信息添加到课程信息中
                payment_course_dict.update(policy_info)
                #将课程的支付信息存放到所有的课程信息字典中,
                # 课程id为key，（课程信息、优惠券信息、策略信息）为value
                payment_dict[str(course_id)] = payment_course_dict


            # 2. 获取所有的优惠券
            ctime = datetime.date.today()
            coupon_list = models.CouponRecord.objects.filter(
                account=request.auth.user,
                status=0,
                coupon__valid_begin_date__lte=ctime,
                coupon__valid_end_date__gte=ctime,
            )

            for item in coupon_list:
                # 1、只处理绑定课程的优惠券
                #########################没有绑定课程的优惠券############################
                if not item.coupon.object_id:
                    # 优惠券ID
                    coupon_id = item.id
                    # 优惠券类型：满减、折扣、立减
                    coupon_type = item.coupon.coupon_type
                    info = {}
                    info['coupon_type'] = coupon_type
                    info['coupon_display'] = item.coupon.get_coupon_type_display()
                    if coupon_type == 0:  # 立减
                        info['money_equivalent_value'] = item.coupon.money_equivalent_value
                    elif coupon_type == 1:  # 满减券
                        info['money_equivalent_value'] = item.coupon.money_equivalent_value
                        info['minimum_consume'] = item.coupon.minimum_consume
                    else:  # 折扣
                        info['off_percent'] = item.coupon.off_percent

                    global_coupon_dict['coupon'][coupon_id] = info
                    continue


                #########################绑定课程的优惠券############################
                # 优惠券绑定课程的ID
                coupon_course_id = str(item.coupon.object_id)
                # 优惠券ID
                coupon_id = item.id
                # 优惠券类型：满减、折扣、立减
                coupon_type = item.coupon.coupon_type
                info = {}
                info['coupon_type'] = coupon_type
                info['coupon_display'] = item.coupon.get_coupon_type_display()
                if coupon_type == 0: # 立减
                    info['money_equivalent_value'] = item.coupon.money_equivalent_value
                elif coupon_type == 1: # 满减券
                    info['money_equivalent_value'] = item.coupon.money_equivalent_value
                    info['minimum_consume'] = item.coupon.minimum_consume
                else: # 折扣
                    info['off_percent'] = item.coupon.off_percent

                if coupon_course_id not in payment_dict:
                    # 获取到优惠券，但是没有购买此课程
                    continue
                # 将优惠券设置到指定的课程的支付支付信息的优惠券中
                payment_dict[coupon_course_id]['coupon'][coupon_id] = info



            # 3. 将绑定优惠券课程+全站优惠券 写入到redis中（结算中心）。
            # 3.1 绑定课程的优惠券放入redis
            # 课程id为key，（课程信息、优惠券信息、策略信息）为value
            # payment_dict[str(course_id)] = payment_course_dict
            for cid,cinfo in payment_dict.items():
                pay_key = settings.PAYMENT_KEY %(request.auth.user_id,cid,) #redis中支付信息的key(客户id_课程id)
                cinfo['coupon'] = json.dumps(cinfo['coupon'])
                self.conn.hmset(pay_key,cinfo)
            # 3.2 将全站优惠券写入redis
            gcoupon_key = settings.PAYMENT_COUPON_KEY %(request.auth.user_id,)  #redis中支付信息的key(客户id)
            global_coupon_dict['coupon'] = json.dumps(global_coupon_dict['coupon'])
            self.conn.hmset(gcoupon_key,global_coupon_dict)

        except Exception as e:
            pass

        return Response(ret.dict)

    #修改支付中心的优惠券信息
    def patch(self,request,*args,**kwargs):
        ret = BaseResponse()
        try:
            # 1. 用户提交要修改的优惠券
            course = request.data.get('courseid')
            #如果传了就转成字符串，否则为None
            course_id = str(course) if course else course

            coupon_id = str(request.data.get('couponid'))

            # payment_global_coupon_1
            #全局优惠券redis的id
            redis_global_coupon_key = settings.PAYMENT_COUPON_KEY %(request.auth.user_id,)

            # 1、course_id为空，只传优惠券id：表示修改全站优惠券
            if not course_id:
                #1.1、coupon_id为0，表示不使用优惠券；请求数据：{"couponid":0}
                if coupon_id == "0":
                    self.conn.hset(redis_global_coupon_key,'default_coupon',coupon_id)
                    ret.data = "修改成功"
                    return Response(ret.dict)

                # 1.2、使用全局优惠券,请求数据：{"couponid":2}
                # 获取所有的全局优惠券信息
                coupon_dict = json.loads(self.conn.hget(redis_global_coupon_key,'coupon').decode('utf-8'))

                # 1.3、判断用户选择得优惠券是否合法
                if coupon_id not in coupon_dict:
                    ret.code = 1001
                    ret.error = "全站优惠券不存在"
                    return Response(ret.dict)

                # 如果合法：设置选择的优惠券
                self.conn.hset(redis_global_coupon_key, 'default_coupon', coupon_id)
                ret.data = "修改成功"
                return Response(ret.dict)

            # 2、course_id和coupon_id都不空，表示：修改绑定课程优惠券
            # luffy_payment_1_1
            redis_payment_key = settings.PAYMENT_KEY % (request.auth.user_id, course_id,)
            # 2.1、coupon_id为0，不使用优惠券
            if coupon_id == "0":
                self.conn.hset(redis_payment_key,'default_coupon',coupon_id)
                ret.data = "修改成功"
                return Response(ret.dict)

            # 2.2、使用优惠券
            # 获取该课程所有的优惠券信息
            coupon_dict = json.loads(self.conn.hget(redis_payment_key,'coupon').decode('utf-8'))

            # 2.3、判断用户选择得优惠券是否合法
            if coupon_id not in coupon_dict:
                ret.code = 1010
                ret.error = "课程优惠券不存在"
                return Response(ret.dict)

            # 如果合法：设置选择的优惠券
            self.conn.hset(redis_payment_key,'default_coupon',coupon_id)

        except Exception as e:
            ret.code = 1111
            ret.error = "修改失败"

        return Response(ret.dict)

    #查看执行中心的数据
    def get(self,request,*args,**kwargs):
        ret = BaseResponse()
        try:
            # luffy_payment_1_*：支付信息
            redis_payment_key = settings.PAYMENT_KEY %(request.auth.user_id,"*",)

            # luffy_payment_coupon_1：全局优惠券信息
            redis_global_coupon_key = settings.PAYMENT_COUPON_KEY %(request.auth.user_id,)

            # 1. 获取绑定课程信息
            course_list = []
            for key in self.conn.scan_iter(redis_payment_key):
                info = {}
                data = self.conn.hgetall(key)
                for k,v in data.items():
                    kk = k.decode('utf-8')
                    if kk == "coupon":
                        info[kk] = json.loads(v.decode('utf-8'))
                    else:
                        info[kk] = v.decode('utf-8')
                course_list.append(info)

            # 2.全站优惠券
            global_coupon_dict = {
                'coupon':json.loads(self.conn.hget(redis_global_coupon_key,'coupon').decode('utf-8')),
                'default_coupon':self.conn.hget(redis_global_coupon_key,'default_coupon').decode('utf-8')
            }

            ret.data = {
                "course_list":course_list,
                "global_coupon_dict":global_coupon_dict
            }
        except Exception as e:
            ret.code = 1001
            ret.error = "获取失败"

        return Response(ret.dict)