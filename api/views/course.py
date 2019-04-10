from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet, ViewSetMixin
from api import models
from api.serializers.course import CourseCategorySerializer, CourseSerializer,CourseDetailSerializer
from rest_framework.response import Response


class CourseCategoryView(ViewSetMixin, APIView):
    '''
    课程大类
    '''
    #测试
    def list(self, request, *args, **kwargs):
        ret = {'code': 1000, 'data': None}
        try:
            queryset = models.CourseCategory.objects.all()
            ser = CourseCategorySerializer(instance=queryset, many=True)
            ret['data'] = ser.data
        except Exception as e:
            ret['code'] = 1001
            ret['error'] = '获取课程失败'
        return Response(ret)


#继承ViewSetMixin的写法，ViewSetMixin中根据url中的参数执行请求方法对应的函数，并重写响应的函数
#由于ViewSetMixin只继承了object，所以还需要继承APIView，
class CourseView(ViewSetMixin, APIView):
    def list(self, request, *args, **kwargs):
        """
        课程列表接口
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        ret = {'code': 1000, 'data': None}
        try:
            queryset = models.Course.objects.all()
            ser = CourseSerializer(instance=queryset, many=True)
            ret['data'] = ser.data
        except Exception as e:
            ret['code'] = 1001
            ret['error'] = '获取课程失败'
        return Response(ret)

    def retrieve(self, request, *args, **kwargs):
        """
        课程详细接口
        """
        ret = {'code': 1000, 'data': None}
        try:
            # 课程ID=2
            pk = kwargs.get('pk')
            # 课程详细对象
            obj = models.CourseDetail.objects.filter(course_id=pk).first()
            ser = CourseDetailSerializer(instance=obj, many=False)
            ret['data'] = ser.data
        except Exception as e:
            ret['code'] = 1001
            ret['error'] = '获取课程详细失败'
        return Response(ret)



class GoodsListViewSet(ViewSetMixin, APIView):
    def list(self, request, *args, **kwargs):
        ret = {'code': 1000, 'data': None}
        try:
            queryset = models.Course.objects.all()
            ser = CourseSerializer(instance=queryset, many=True)
            ret['data'] = ser.data
        except Exception as e:
            ret['code'] = 1001
            ret['error'] = '获取课程失败'

        return Response(ret)

