from torch.autograd import Variable
from torchvision import transforms
from PIL import Image
import torchvision
import torch
import glob
import time
import cv2

video = cv2.VideoCapture()
video.open('test.mp4')
total_frame_number = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize((.5, .5, .5), (.5, .5, .5)),
])
# model = torchvision.models.vgg16(num_classes=2).cuda()
# model.load_state_dict(torch.load('results/vgg16-model.pt'))
model = torch.load('results/mobilebetv2-model.pth').cuda()
model.eval().cuda()
start = time.time()
res = {0: 0, 1: 0}  # 0 is abnormal and 1 is normal.
for i in range(0, total_frame_number):
    try:
        video.set(cv2.CAP_PROP_POS_FRAMES, i)
        flag, img = video.read()
        img = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
        img = transform(img).cuda()
        img.unsqueeze_(dim=0)
        # img = Variable(img).cuda()
        # model.eval().cuda()
        out = model(img)
        # print(torch.max(out, 1)[1].item())
        res[torch.max(out, 1)[1].item()] += 1
        if i == 500:
            break
    except:
        print('frame {} failed.'.format(i))
# images = glob.glob('data/val/normal/*')
# for image in images:
#     img = Image.open(image)
#     img = transform(img).cuda()
#     img.unsqueeze_(dim=0)
#     # img = Variable(img).cuda()
#     # model.eval()
#     out = model(img)
#     # print(out)
#     # print(torch.max(out, 1)[1].item())
#     res[torch.max(out, 1)[1].item()] += 1
print(res)
time_cost = time.time() - start
print(time_cost, 's')
print('fps:{:.1f}'.format(500 / time_cost))
