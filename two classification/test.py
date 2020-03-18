from ghost_mobilenetv2 import GhostMobileNetV2
from mobilenetv2_1 import MobileNetV2_1
from mobilenetv3 import MobileNetV3
from torch.autograd import Variable
from torchvision import transforms
from ghost_net import GhostNet
from PIL import Image
import torchvision
import random
import torch
import glob
import time

transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize((.5, .5, .5), (.5, .5, .5)),
])

weight_names = ['mobilenetv2-result.weight', 'mobilenetv3 small-result.weight', 'mobilenetv3 large-result.weight',
                'ghostnet-result.weight',
                'mobilenetv2-with-ghost-module-result.weight', 'mobilenetv2_1-result.weight', 'vgg16-model.pth']

images = glob.glob('data/val/normal/*')
t = glob.glob('data/val/abnormal/*')
images = images + t
random.shuffle(images)
images = images[:500]
imgs = []
for image in images:  # to reduce the influence of the disk performance.
    img = Image.open(image)
    img = transform(img).cuda()
    img.unsqueeze_(dim=0)
    imgs.append(img)
for weight_name in weight_names:
    model = None
    print(weight_name)
    if weight_name == 'mobilenetv2-result.weight':
        model = torchvision.models.MobileNetV2(num_classes=2).cuda()
        model.load_state_dict(torch.load('results/results2/mobilenetv2-result.weight'))
    elif weight_name == 'mobilenetv3 small-result.weight':
        model = MobileNetV3(n_class=2, mode='small').cuda()
        model.load_state_dict(torch.load('results/results2/mobilenetv3 small-result.weight'))
    elif weight_name == 'mobilenetv3 large-result.weight':
        model = MobileNetV3(n_class=2, mode='large').cuda()
        model.load_state_dict(torch.load('results/results2/mobilenetv3 large-result.weight'))
    elif weight_name == 'ghostnet-result.weight':
        model = GhostNet(num_classes=2).cuda()
        model.load_state_dict(torch.load('results/results2/ghostnet-result.weight'))
    elif weight_name == 'mobilenetv2-with-ghost-module-result.weight':
        model = GhostMobileNetV2(num_classes=2).cuda()
        model.load_state_dict(torch.load('results/results2/mobilenetv2-with-ghost-module-result.weight'))
    elif weight_name == 'mobilenetv2_1-result.weight':
        model = MobileNetV2_1(num_classes=2).cuda()
        model.load_state_dict(torch.load('results/results2/mobilenetv2_1-result.weight'))
    elif weight_name == 'vgg16-model.pth':
        model = torch.load('results/results1/vgg16-model.pth').cuda()
    model.eval().cuda()
    res = {0: 0, 1: 0}  # 0 is abnormal and 1 is normal.
    start = time.time()
    for img in imgs:
        out = model(img)
        res[torch.max(out, 1)[1].item()] += 1
    print(res)
    time_cost = time.time() - start
    print(time_cost, 's')
    print('fps:{:.1f}'.format(len(images) / time_cost))
