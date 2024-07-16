import os
import numpy as np
from tensorflow.keras.preprocessing import image
from tensorflow.keras.models import load_model

# Load the pre-trained model
model = load_model('./models/currency_classifier_resnet50.h5')

# Define the data directory
data_dir = '../datasets/train/'  # Update this to your training data directory

# Get class names from the training data directory
class_names = sorted(os.listdir(data_dir))

def predict(img_path):
    # Load and preprocess the image
    img = image.load_img(img_path, target_size=(224, 224))
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    img_array /= 255.0

    # Make a prediction
    predictions = model.predict(img_array)
    predicted_class_index = np.argmax(predictions, axis=1)[0]
    predicted_class_name = class_names[predicted_class_index]
    return predicted_class_name

# Path to the directory containing images
img_dir = '../datasets/test/'  # Update this to your directory

# Iterate over all files in the directory
for img_filename in os.listdir(img_dir):
    img_path = os.path.join(img_dir, img_filename)
    if os.path.isfile(img_path) and img_filename.lower().endswith(('.png', '.jpg', '.jpeg')):
        try:
            predicted_class = predict(img_path)
            print(f'Image: {img_filename} - Predicted Class: {predicted_class}')
        except Exception as e:
            print(f"An error occurred while processing {img_filename}: {e}")
    else:
        print(f"Skipping non-image file: {img_filename}")
