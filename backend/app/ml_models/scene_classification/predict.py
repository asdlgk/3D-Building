import torch
import torch.nn.functional as F
from PIL import Image
from torchvision import transforms

CLASS_NAMES = ['教室', '实验室', '图书馆', '体育馆', '食堂']

def predict_image(image_path):
    """使用预训练模型进行场景分类"""
    model = torch.load('model.pth', map_location='cpu')
    model.eval()
    
    transform = transforms.Compose([
        transforms.Resize(256),
        transforms.CenterCrop(224),
        transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
    ])
    
    image = Image.open(image_path).convert('RGB')
    tensor = transform(image).unsqueeze(0)
    
    with torch.no_grad():
        outputs = model(tensor)
        probs = F.softmax(outputs, dim=1)
    
    _, preds = torch.max(outputs, 1)
    return {
        'class': CLASS_NAMES[preds.item()],
        'confidence': round(probs[preds].item(), 4)
    }
