import os
import cv2
import numpy as np

def preprocess_image(img_path):
    img = cv2.imread(img_path)
    img = cv2.resize(img, (224, 224))
    img = img.astype('float32') / 255.0
    return img

def preprocess_data(data_dir):
    categories = os.listdir(data_dir)
    data = []
    labels = []
    for category in categories:
        category_path = os.path.join(data_dir, category)
        for img_name in os.listdir(category_path):
            img_path = os.path.join(category_path, img_name)
            img = preprocess_image(img_path)
            data.append(img)
            labels.append(category)
    data = np.array(data)
    labels = np.array(labels)
    return data, labels
