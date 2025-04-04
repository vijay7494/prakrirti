import supabase
import streamlit as st
import torch
import torchvision.transforms as transforms
import json
import io

# Supabase Configuration
#supabase url
#service role key supabase
SUPABASE_BUCKET = "prakriti_images"  # New bucket name

@st.cache_resource
def init_supabase():
    return supabase.create_client(SUPABASE_URL, SUPABASE_KEY)

def create_bucket(bucket_name="prakriti_images"):
    """Creates a new bucket in Supabase Storage if it doesn't exist"""
    client = init_supabase()
    try:
        # First check if bucket exists
        buckets = client.storage.list_buckets()
        bucket_exists = False
        for bucket in buckets:
            if hasattr(bucket, 'name') and bucket.name == bucket_name:
                bucket_exists = True
                break
        
        if bucket_exists:
            st.success(f"Bucket '{bucket_name}' already exists")
            return True
            
        # Create the bucket with proper options if it doesn't exist
        response = client.storage.create_bucket(
            bucket_name,
            options={
                "public": True,
                "allowed_mime_types": ["image/jpeg", "image/png", "image/jpg"],
                "file_size_limit": 5242880  # 5MB limit
            }
        )
        
        st.success(f"Successfully created bucket: {bucket_name}")
        return True
    except Exception as e:
        st.error(f"Failed to create bucket: {str(e)}")
        return False

def upload_image_to_supabase(image_data, image_name, bucket=SUPABASE_BUCKET):
    """Uploads image to Supabase Storage using bytes or file-like object and filename"""
    client = init_supabase()
    image_path = f"uploads/{image_name}"
    
    try:
        # If image_data is bytes, create a file-like object
        if isinstance(image_data, bytes):
            file_obj = io.BytesIO(image_data)
        else:
            file_obj = image_data
            
        # Upload using file-like object
        response = client.storage.from_(bucket).upload(
            path=image_path,
            file=file_obj.read(),  # Read the bytes from the BytesIO object
            file_options={
                "cache-control": "3600",
                "upsert": False,
                "content-type": "image/jpeg"  # Specify content type
            }
        )

        # Get the public URL
        public_url = client.storage.from_(bucket).get_public_url(image_path)
        return public_url
    except Exception as e:
        st.error(f"Image upload failed: {str(e)}")
        return None

@st.cache_resource
def load_model():
    """Loads the trained ResNet50 model"""
    NUM_CLASSES = 3
    model = torch.hub.load('pytorch/vision:v0.10.0', 'resnet50', pretrained=False)
    model.fc = torch.nn.Linear(2048, NUM_CLASSES)
    
    try:
        model.load_state_dict(torch.load("model/resnet50_prakriti.pth", map_location="cpu"))
        model.eval()
        return model
    except Exception as e:
        st.error(f"Model loading failed: {e}")
        return None

def predict_prakriti(image_bytes):
    """Predicts Prakriti type from image bytes"""
    try:
        with open("model/class_indices.json", "r") as f:
            class_idx = json.load(f)

        # Image transformation pipeline
        transform = transforms.Compose([
            transforms.Resize((512, 512)),
            transforms.ToTensor(),
            transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
        ])

        # Convert bytes to PIL Image via BytesIO
        img = Image.open(io.BytesIO(image_bytes)).convert("RGB")
        img_tensor = transform(img).unsqueeze(0)

        # Model prediction
        model = load_model()
        if model is None:
            return "Model unavailable"
            
        with torch.no_grad():
            outputs = model(img_tensor)
            _, predicted = torch.max(outputs, 1)

        return class_idx.get(str(predicted.item()), "Unknown")
    
    except Exception as e:
        st.error(f"Prediction error: {str(e)}")
        return "Error"
