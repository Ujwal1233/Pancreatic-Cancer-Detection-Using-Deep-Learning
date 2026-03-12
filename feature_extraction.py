import os
import cv2
import numpy as np
import pandas as pd
from utils.image_processing import preprocess_image, segment_image, extract_features

def extract_features_from_folder(folder_path, label):
    data = []
    for file in os.listdir(folder_path):
        if file.lower().endswith(('.png', '.jpg', '.jpeg')):
            path = os.path.join(folder_path, file)
            image = cv2.imread(path)
            if image is None:
                continue
            preprocessed = preprocess_image(image)
            segmented = segment_image(preprocessed)
            _, features = extract_features(segmented)
            features['label'] = label
            data.append(features)
    return data

if __name__ == "__main__":
    cancer_folder = "dataset/cancerous"
    non_cancer_folder = "dataset/non_cancerous"

    cancer_data = extract_features_from_folder(cancer_folder, 1)
    non_cancer_data = extract_features_from_folder(non_cancer_folder, 0)

    all_data = cancer_data + non_cancer_data
    df = pd.DataFrame(all_data)
    df.to_csv("features_dataset.csv", index=False)

    print("✅ Features extracted and saved to features_dataset.csv")
