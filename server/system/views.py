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

video = cv2.VideoCapture('F:/Graduation-Project/排水管道系统/PipeSight/Videos/a4gptz2rl45.mp4')
current_frame = 1
total_frame = video.get(cv2.CAP_PROP_FRAME_COUNT)


def handle(request):
    global video
    global current_frame
    # 获取robot摄像头图像
    _, img = video.read()
    current_frame += 1
    if current_frame == total_frame:
        current_frame = 1
        video.set(cv2.CAP_PROP_POS_FRAMES, 1)

    # cv2 image转base64
    _, buffer = cv2.imencode('.png', img)
    data = base64.b64encode(buffer)
    return HttpResponse(data, content_type="image/png")  # 返回图片类型
