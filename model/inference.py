import torch
import torchvision.transforms as transforms
from PIL import Image
import json
import io
import torch.nn.functional as F

# Define number of classes
NUM_CLASSES = 3  # Update based on your dataset

# Preprocessing function for Streamlit
transform = transforms.Compose([
    transforms.Resize((512, 512)),
    transforms.ToTensor(),
    transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225]),
])

@torch.no_grad()
def load_model():
    """Loads the trained ResNet50 model"""
    model = torch.hub.load('pytorch/vision:v0.10.0', 'resnet50', pretrained=False)
    model.fc = torch.nn.Linear(2048, NUM_CLASSES)
    
    try:
        model.load_state_dict(torch.load("model/resnet50_prakriti.pth", map_location="cpu"))
        model.eval()
        return model
    except Exception as e:
        print(f"Model loading failed: {e}")
        return None

def predict_prakriti(image_bytes):
    """Takes image bytes, processes it, and returns the predicted Prakriti type with confidence."""
    try:
        # Load class labels
        with open("model/class_indices.json", "r") as f:
            class_idx = json.load(f)

        # Convert bytes to PIL Image
        img = Image.open(io.BytesIO(image_bytes)).convert("RGB")
        img_tensor = transform(img).unsqueeze(0)
        model = load_model()
        if model is None:
            return "Model unavailable", None
            
        output = model(img_tensor)
        probabilities = F.softmax(output, dim=1)
        confidence, predicted = torch.max(probabilities, 1)

        predicted_class = class_idx.get(str(predicted.item()), "Unknown")
        confidence_percentage = confidence.item() * 100

        return predicted_class, confidence_percentage
        
    except Exception as e:
        print(f"Prediction error: {e}")
        return "Error", None