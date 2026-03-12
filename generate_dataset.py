import os
import cv2
import numpy as np
import pandas as pd
from tqdm import tqdm

# =========================
# Feature Extraction Function (same as your app)
# =========================
def extract_image_features(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    equalized = cv2.equalizeHist(blurred)

    # Threshold and Morphological operations
    _, binary = cv2.threshold(equalized, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    kernel = np.ones((5, 5), np.uint8)
    opened = cv2.morphologyEx(binary, cv2.MORPH_OPEN, kernel)

    # Find contours
    contours, _ = cv2.findContours(opened, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    image_area = opened.shape[0] * opened.shape[1]

    # Initialize features
    features = {
        'num_contours': len(contours),
        'total_area': 0,
        'avg_circularity': 0,
        'max_contour_area': 0,
        'contour_density': 0,
        'avg_intensity': np.mean(opened),
        'intensity_std': np.std(opened),
        'texture_uniformity': 0,
        'edge_density': 0,
        'shape_complexity': 0
    }

    total_perimeter = 0
    for contour in contours:
        area = cv2.contourArea(contour)
        perimeter = cv2.arcLength(contour, True)
        features['total_area'] += area
        total_perimeter += perimeter
        if area > features['max_contour_area']:
            features['max_contour_area'] = area
        if perimeter > 0:
            circularity = 4 * np.pi * area / (perimeter ** 2)
            complexity = (perimeter ** 2) / (4 * np.pi * area)
            features['avg_circularity'] += circularity
            features['shape_complexity'] += complexity

    if len(contours) > 0:
        features['avg_circularity'] /= len(contours)
        features['shape_complexity'] /= len(contours)
        features['contour_density'] = features['total_area'] / image_area
        features['edge_density'] = total_perimeter / image_area

    if np.max(opened) > 0:
        features['texture_uniformity'] = np.sum(np.square(opened / np.max(opened)))

    return features


# =========================
# Dataset Creation Function
# =========================
def create_feature_dataset(base_dir="datasets"):
    data = []
    classes = ["cancerous", "non_cancerous"]

    for label in classes:
        folder_path = os.path.join(base_dir, label)
        if not os.path.exists(folder_path):
            print(f"⚠️ Folder not found: {folder_path}")
            continue

        print(f"\n🔍 Extracting features from: {folder_path}")
        for filename in tqdm(os.listdir(folder_path)):
            if filename.lower().endswith((".png", ".jpg", ".jpeg")):
                img_path = os.path.join(folder_path, filename)
                image = cv2.imread(img_path)
                if image is None:
                    continue

                features = extract_image_features(image)
                features['label'] = 1 if label == "cancerous" else 0  # 1 = cancer, 0 = normal
                data.append(features)

    df = pd.DataFrame(data)
    df.to_csv("features_dataset.csv", index=False)
    print("\n✅ Dataset created successfully: features_dataset.csv")
    print(f"Total images processed: {len(df)}")


# =========================
# Main
# =========================
if __name__ == "__main__":
    create_feature_dataset()
