import torch
import torch.nn as nn
from efficientnet_pytorch import EfficientNet

class EfficientNetV2(nn.Module):
    def __init__(self, num_classes=5):
        super().__init__()
        self.base = EfficientNet.from_pretrained('efficientnet-b3')
        self.classifier = nn.Sequential(
            nn.Dropout(0.5),
            nn.Linear(self.base._fc.in_features, 512),
            nn.ReLU(),
            nn.Linear(512, num_classes)
        )
    
    def forward(self, x):
        features = self.base.extract_features(x)
        features = nn.functional.adaptive_avg_pool2d(features, 1)
        return self.classifier(features.view(features.size(0), -1))

def load_pretrained(ckpt_path):
    model = EfficientNetV2()
    model.load_state_dict(torch.load(ckpt_path, map_location='cpu'))
    model.eval()
    return model
