import torch.nn as nn
from torch import cat
num_cl = 3
linear_clf = nn.Sequential(
    nn.Linear(512, 256),
    nn.BatchNorm1d(256),
    nn.ReLU(),
    nn.Dropout(p=0.5),
    nn.Linear(256, num_cl)
)


class UNet(nn.Module):
    def __init__(self):
        super(UNet, self).__init__()

        # Encoder
        # input 3x268x268
        self.layer1_e1 = nn.Conv2d(3, 64, kernel_size=3, padding=1)  # 64x266x266
        self.layer1_e2 = nn.Conv2d(64, 64, kernel_size=3, padding=1)  # 64x264x264
        self.layer1_epool = nn.MaxPool2d(kernel_size=2, stride=2)  # 64x132x132

        # input 64x132x132
        self.layer2_e1 = nn.Conv2d(64, 128, kernel_size=3, padding=1)  # 128x130x130
        self.layer2_e2 = nn.Conv2d(128, 128, kernel_size=3, padding=1)  # 128x128x128
        self.layer2_epool = nn.MaxPool2d(kernel_size=2, stride=2)  # 128x64x64

        # input 128x64x64
        self.layer3_e1 = nn.Conv2d(128, 256, kernel_size=3, padding=1)  # 256x62x62
        self.layer3_e2 = nn.Conv2d(256, 256, kernel_size=3, padding=1)  # 256x60x60

        # Decoder
        self.layer2_upconv = nn.ConvTranspose2d(256, 128, kernel_size=2, stride=2)
        self.layer2_d1 = nn.Conv2d(256, 128, kernel_size=3, padding=1)
        self.layer2_d2 = nn.Conv2d(128, 128, kernel_size=3, padding=1)

        self.layer1_upconv = nn.ConvTranspose2d(128, 64, kernel_size=2, stride=2)
        self.layer1_d1 = nn.Conv2d(128, 64, kernel_size=3, padding=1)
        self.layer1_d2 = nn.Conv2d(64, 64, kernel_size=3, padding=1)

        self.output = nn.Conv2d(64, 1, kernel_size=1)

        self.relu = nn.ReLU(inplace=True)

    def forward(self, img):
        # Encoder
        img_layer1_e1 = self.relu(self.layer1_e1(img))
        img_layer1_e2 = self.relu(self.layer1_e2(img_layer1_e1))
        img_layer1_epool = self.layer1_epool(img_layer1_e2)

        img_layer2_e1 = self.relu(self.layer2_e1(img_layer1_epool))
        img_layer2_e2 = self.relu(self.layer2_e2(img_layer2_e1))
        img_layer2_epool = self.layer2_epool(img_layer2_e2)

        img_layer3_e1 = self.relu(self.layer3_e1(img_layer2_epool))
        img_layer3_e2 = self.relu(self.layer3_e2(img_layer3_e1))

        # Decoder
        img_layer2_upconv = self.relu(self.layer2_upconv(img_layer3_e2))
        img_layer2_transition = cat([img_layer2_e2, img_layer2_upconv], dim=1)
        img_layer2_d1 = self.relu(self.layer2_d1(img_layer2_transition))
        img_layer2_d2 = self.relu(self.layer2_d2(img_layer2_d1))

        img_layer1_upconv = self.relu(self.layer1_upconv(img_layer2_e2))
        img_layer1_transition = cat([img_layer1_e2, img_layer1_upconv], dim=1)
        img_layer1_d1 = self.relu(self.layer1_d1(img_layer1_transition))
        img_layer1_d2 = self.relu(self.layer1_d2(img_layer1_d1))

        out = self.output(img_layer1_d2)
        return out
