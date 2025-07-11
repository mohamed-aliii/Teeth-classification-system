import os
from dotenv import load_dotenv
from tensorflow.keras.models import load_model
load_dotenv()

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

APP_NAME = os.getenv("APP_NAME")
VERSION = os.getenv('APP_VERSION')  
API_KEY = os.getenv('API_KEY')


MODEL_PATH = os.path.join(BASE_DIR, "Artifacts", 'teeth_classification_model.h5')
try:
    if os.path.exists(MODEL_PATH):
        model = load_model(MODEL_PATH)
        print(f"Model loaded successfully ")
    else:
        print(f"Model file not found ")
        model = None
except Exception as e:
    print(f"Error loading model: {str(e)}")
    model = None

def is_valid_api_key(user_key: str) -> bool:
    print(f"Comparing user_key: {user_key} with API_KEY: {API_KEY}")
    return user_key == API_KEY
