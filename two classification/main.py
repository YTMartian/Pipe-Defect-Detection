from torchvision.datasets import ImageFolder
from torch.utils.data import DataLoader
from torch.autograd import Variable
from torchvision import transforms
import matplotlib.pyplot as plt
import numpy as np
import torchvision
import torch
import time

batch_size = 32
lr = 1e-3
epochs = 120
momentum = 0.9
weight_decay = 1e-2

transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize((.5, .5, .5), (.5, .5, .5)),
])
trainSet = ImageFolder(root='data/train/', transform=transform)
valSet = ImageFolder(root='data/val/', transform=transform)
trainLoader = DataLoader(dataset=trainSet, batch_size=batch_size, shuffle=True)
valLoader = DataLoader(dataset=valSet, batch_size=batch_size, shuffle=True)

model = torchvision.models.MobileNetV2(num_classes=2).cuda()
optimizer = torch.optim.SGD(model.parameters(), lr=lr, momentum=momentum, weight_decay=weight_decay)
criterion = torch.nn.CrossEntropyLoss()

log_train_loss = []
log_train_accuracy = []
log_val_loss = []
log_val_accuracy = []
best = 0

start_time = time.time()

for i in range(epochs):
    # training.
    train_loss = 0
    train_acc = 0
    for images, labels in trainLoader:
        images, labels = Variable(images).cuda(), Variable(labels).cuda()
        out = model(images)
        loss = criterion(out, labels)
        train_loss += loss.data.item()
        predict = torch.max(out, 1)[1]
        correct = (predict == labels).sum()
        train_acc += correct.data.item()
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
    log_train_loss.append(float('%.8f' % (train_loss / len(trainSet))))
    log_train_accuracy.append(float('%.8f' % (train_acc / len(trainSet))))
    print('epoch {} train loss:{:.8f}, train acc:{:.8f} '.format(i, train_loss / len(trainSet),
                                                                 train_acc / len(trainSet)),
          end=' ')
    # evaluation.
    model.eval()
    eval_loss = 0
    eval_acc = 0
    for images, labels in valLoader:
        images, labels = Variable(images).cuda(), Variable(labels).cuda()
        out = model(images)
        loss = criterion(out, labels)
        eval_loss += loss.data.item()
        predict = torch.max(out, 1)[1]
        correct = (predict == labels).sum()
        eval_acc += correct.data.item()
    log_val_loss.append(float('%.8f' % (eval_loss / len(valSet))))
    log_val_accuracy.append(float('%.8f' % (eval_acc / len(valSet))))
    print('validation loss:{:.8f},validation acc:{:.8f}'.format(eval_loss / len(valSet), eval_acc / len(valSet)))
    if float(eval_acc / len(valSet)) > best:
        best = float(eval_acc / len(valSet))
        torch.save(model.state_dict(), 'model.pt')  # state_dict():only save the weights.
        print('save in epoch ', i)

print('time cost: {}s'.format(time.time() - start_time))

print(log_train_loss)
print(log_train_accuracy)
print(log_val_loss)
print(log_val_accuracy)
# set image size.
F = plt.gcf()
Size = F.get_size_inches()
F.set_size_inches(Size[0] * 3, Size[1] * 3, forward=True)
# set font.
font = {'weight': 'normal', 'size': 32}
plt.rc('font', **font)
# set margin.
plt.subplots_adjust(hspace=0.22)

axis_x = range(0, epochs)

plt.subplot(2, 1, 1)
plt.plot(axis_x, log_train_loss, 'o-', label='train')
plt.plot(axis_x, log_val_loss, 'o-', label='test')
plt.legend(bbox_to_anchor=(1, 0), loc=3, borderaxespad=0)
plt.ylabel('Loss', color='C0')
plt.subplot(2, 1, 2)
plt.plot(axis_x, log_train_accuracy, 'o-', label='train')
plt.plot(axis_x, log_val_accuracy, 'o-', label='test')
plt.legend(bbox_to_anchor=(1, 0), loc=3, borderaxespad=0)
plt.xlabel('Epochs', color='C0')
plt.ylabel('Accuracy', color='C0')
# to save the entire image.
plt.savefig("result.jpg", dpi=300, bbox_inches='tight')
plt.show()
