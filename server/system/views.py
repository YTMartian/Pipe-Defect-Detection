from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.shortcuts import render
import numpy as np
import base64
import cv2


def index(request):
    return render(request, 'system/index.html')


"""
获取并处理图像，返回结果
"""


def handle(request):
    # 获取robot摄像头图像
    img = cv2.imread('C:/Users/YTMartian/Desktop/111.jpg')

    # cv2 image转base64
    _, buffer = cv2.imencode('.png', img)
    data = base64.b64encode(buffer)
    return HttpResponse(data, content_type="image/png")  # 返回图片类型
