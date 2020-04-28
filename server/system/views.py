from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.shortcuts import render
import numpy as np
import sys

sys.path.append("F:/Graduation-Project/Pipe Defect Detection");
from models import *
from utils.datasets import *
from utils.utils import *
import random
import torch
import base64
import cv2
import random
from .UNet import UNet
from torchvision import transforms

img_size = None
yolov3_model = None
unet_model = None
names = None
colors = None

style = 'unet'


def index(request):
    return render(request, 'system/index.html')


"""
获取并处理图像，返回结果
"""

video = cv2.VideoCapture('F:/Graduation-Project/排水管道系统/PipeSight/Videos/a4gptz2rl45.mp4')
current_frame = 1
total_frame = video.get(cv2.CAP_PROP_FRAME_COUNT)

meter = 9e-7
longitudes_ = [116.3975, 116.3975, 116.3974974, 116.3974974, 116.3971, 116.39571, 116.39557, 116.39289, 116.39219,
               116.3919, 116.3919004, 116.3919004, 116.39296, 116.39447, 116.39558]
latitudes_ = [39.90801, 39.90795, 39.9079546, 39.9079546, 39.90795, 39.90793, 39.90793, 39.90783, 39.90781, 39.90752,
              39.9075183, 39.9075183, 39.90754, 39.9076, 39.90763]
latitudes = []
longitudes = []
insert_per = int(total_frame / len(longitudes_))
for i in range(len(longitudes_) - 1):
    add_ = (longitudes_[i + 1] - longitudes_[i]) / insert_per
    for j in range(insert_per):
        longitudes.append(longitudes_[i] + j * add_)
for i in range(len(latitudes_) - 1):
    add_ = (latitudes_[i + 1] - latitudes_[i]) / insert_per
    for j in range(insert_per):
        latitudes.append(latitudes_[i] + j * add_)
while len(longitudes) < total_frame:
    longitudes.append(longitudes[-1])
while len(latitudes) < total_frame:
    latitudes.append(latitudes[-1])
longitude = longitudes[0]
latitude = latitudes[0]


def handle(request):
    global video
    global current_frame
    global initialization
    global longitude, latitude
    # 获取robot摄像头图像
    _, img = video.read()
    current_frame += 1
    if current_frame == total_frame:
        current_frame = 1
        video.set(cv2.CAP_PROP_POS_FRAMES, 1)
    try:
        if style == 'yolov3':
            img, count = yolov3_detect(img)
        elif style == 'unet':
            img, count = unet_detect(img)
    except:
        print('detect failed.')
    # cv2 image转base64
    _, buffer = cv2.imencode('.png', img)
    data = base64.b64encode(buffer)
    '''test gps'''
    '''START'''
    # 为了同时传输图像和经纬度坐标
    if current_frame < len(longitudes):
        longitude = longitudes[current_frame]
        latitude = latitudes[current_frame]
    else:
        longitude += (random.random() - 0.5) / 2000
        latitude += (random.random() - 0.5) / 4000
    latitude_ = '{:.10f}'.format(latitude)
    longitude_ = '{:.10f}'.format(longitude)
    max_len = max(len(latitude_), len(longitude_))
    while len(latitude_) < max_len:
        latitude_ += '0'
    while len(longitude_) < max_len:
        longitude_ += '0'
    latitude_ = latitude_[:14]
    longitude_ = longitude_[:14]
    latitude_ = bytes(latitude_, encoding='utf-8')
    longitude_ = bytes(longitude_, encoding='utf-8')
    '''END'''
    color = '1' if count > 0 else '0'  # 0 is normal.
    color = bytes(color, encoding='utf-8')
    data += latitude_ + longitude_ + color
    return HttpResponse(data, content_type="image/png")  # 返回图片类型


def load_yolov3():
    global img_size, yolov3_model, names, colors
    # load yolov3 model.
    img_size = 416
    yolo = 'yolov3-tiny'
    weights = 'F:/Graduation-Project/Pipe Defect Detection/model/{}.pt'.format(yolo)
    cfg = 'F:/Graduation-Project/Pipe Defect Detection/model/{}.cfg'.format(yolo)
    names = 'F:/Graduation-Project/Pipe Defect Detection/model/my.names'
    # Initialize model
    yolov3_model = Darknet(cfg, img_size)

    # Load weights
    attempt_download(weights)
    yolov3_model.load_state_dict(torch.load(weights, map_location='cuda:0')['model'])

    # Eval mode
    yolov3_model.eval().cuda()

    # Get names and colors
    names = load_classes(names)
    colors = [[random.randint(0, 255) for _ in range(3)] for _ in range(len(names))]
    print('load model successful.')


def yolov3_detect(img0):
    global img_size, yolov3_model, names, colors
    # Padded resize
    img = letterbox(img0, new_shape=img_size)[0]

    # Convert
    img = img[:, :, ::-1].transpose(2, 0, 1)  # BGR to RGB, to 3x416x416
    img = np.ascontiguousarray(img, dtype=np.float32)  # uint8 to fp16/fp32
    img /= 255.0  # 0 - 255 to 0.0 - 1.0

    # Get detections
    img = torch.from_numpy(img).cuda()
    if img.ndimension() == 3:
        img = img.unsqueeze(0)
    pred = yolov3_model(img)[0]

    # Apply NMS
    pred = non_max_suppression(pred, conf_thres=0.3)
    count = 0

    # Process detections
    for i, det in enumerate(pred):  # detections per image

        s = '%gx%g ' % img.shape[2:]  # print string
        if det is not None and len(det):
            # Rescale boxes from img_size to im0 size
            det[:, :4] = scale_coords(img.shape[2:], det[:, :4], img0.shape).round()

            # Print results
            for c in det[:, -1].unique():
                n = (det[:, -1] == c).sum()  # detections per class
                s += '%g %ss, ' % (n, names[int(c)])  # add to string

            # Write results
            for *xyxy, conf, cls in det:
                label = '%s %.2f' % (names[int(cls)], conf)
                plot_one_box(xyxy, img0, label=label, color=colors[int(cls)])
                count += 1
    return img0, count


def load_unet():
    global unet_model
    unet_model = UNet(n_class=1).cuda()
    unet_model.load_state_dict(torch.load(r'F:\Graduation-Project\实现\unet\data\[32, 64, 128, 256].weight'))


trans = transforms.Compose([
    transforms.ToTensor(),
])


def unet_detect(image):
    global unet_model
    image_size = 256
    h, w = image.shape[:2]
    image2 = cv2.resize(image, (image_size, image_size)) / 255.0
    image2 = np.array(image2)
    image2 = trans(image2)
    image2 = torch.unsqueeze(image2, 0).cuda()
    image2 = image2.type(torch.cuda.FloatTensor)
    result = unet_model(image2)
    result = result > 0.2
    result = result.view(result.size(0), result.size(2), result.size(3), result.size(1))
    result = result.cpu().numpy()

    img = result[0] * 210.0
    count = 0
    try:
        img = cv2.resize(img, (w, h))
        img2 = np.zeros_like(image)
        #         img2[:,:,0] = img
        img2[:, :, 1] = img
        #         img2[:,:,2] = img
        #         print(img.shape)
        out_img = cv2.add(image, img2)
        if np.mean(img2) > 0.9:
            count = 1
    except:
        print('failed.')
        return image, 0
    return out_img, count


if style == 'yolov3':
    load_yolov3()
elif style == 'unet':
    load_unet()
