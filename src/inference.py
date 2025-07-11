from src.config import model
import numpy as np
import cv2


def preprocess_image(image):
    image = cv2.resize(image, (224, 224))
    image = image / 255.0
    image = np.expand_dims(image, axis=0)
    return image

def get_class_name(class_index):
    class_names = {
        0: "Condition Of Soft Tissues",
        1: "Candidiasis",
        2: "Gum disease",
        3: "Mucocele",
        4: "Oral Cancer",
        5: "Oral Lichen Planus",
        6: "Odontogenic Tumer"
    }
    return class_names.get(class_index, "Unknown Class")


def predict(image):
    if model is None:
        raise ValueError("Model is not loaded. Please check the model path and loading process.")
    
    preprocessed_image = preprocess_image(image)
    predictions = model.predict(preprocessed_image)
    predicted_class = np.argmax(predictions, axis=1)[0]
    confidence = np.max(predictions)
    predicted_class_name = get_class_name(predicted_class)
    return predicted_class_name, confidence



