import cv2
import numpy as np
import joblib
import os

# Load the trained model (if available)
model_path = "pancreas_model.pkl"
model = joblib.load(model_path) if os.path.exists(model_path) else None

def is_ct_scan_image(image):
    """
    Accept only grayscale or black-white images (CT/MRI scans).
    Reject if any strong color presence is found.
    """
    image_small = cv2.resize(image, (128, 128))
    image_small = image_small.astype(np.int16)
    b, g, r = cv2.split(image_small)
    diff1 = np.abs(r - g)
    diff2 = np.abs(g - b)
    diff3 = np.abs(b - r)
    color_pixels = np.sum((diff1 > 5) | (diff2 > 5) | (diff3 > 5))
    total_pixels = image_small.shape[0] * image_small.shape[1]
    color_ratio = color_pixels / total_pixels
    # If more than 1% pixels are colored -> not CT scan
    return color_ratio <= 0.01

def preprocess_image(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    equalized = cv2.equalizeHist(blurred)
    return equalized

def segment_image(preprocessed):
    _, binary = cv2.threshold(preprocessed, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    kernel = np.ones((5,5), np.uint8)
    opening = cv2.morphologyEx(binary, cv2.MORPH_OPEN, kernel)
    return opening

def extract_features(segmented):
    contours, _ = cv2.findContours(segmented, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    features = {
        'num_contours': len(contours),
        'total_area': 0,
        'avg_circularity': 0,
        'max_contour_area': 0,
        'contour_density': 0,
        'avg_intensity': np.mean(segmented),
        'intensity_std': np.std(segmented),
        'texture_uniformity': 0,
        'edge_density': 0,
        'shape_complexity': 0
    }

    image_area = segmented.shape[0] * segmented.shape[1]
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

    if np.max(segmented) > 0:
        features['texture_uniformity'] = np.sum(np.square(segmented / np.max(segmented)))

    return features


def process_image(image):
    # Step 1: Check if it’s a CT scan
    if not is_ct_scan_image(image):
        return {'error': 'This is not a valid CT scan image. Please upload a grayscale CT or MRI scan.'}

    # Step 2: Preprocess and segment
    preprocessed = preprocess_image(image.copy())
    segmented = segment_image(preprocessed.copy())
    features = extract_features(segmented.copy())

    # 🟩 Add this visualization step back:
    feature_vis = cv2.cvtColor(segmented, cv2.COLOR_GRAY2BGR)
    cv2.drawContours(feature_vis, cv2.findContours(segmented, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[0], -1, (0, 255, 0), 2)
    cv2.putText(feature_vis, "Feature-Detected Regions", (10, 25),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

    # Step 3: Predict with ML model
    if model:
        feature_values = np.array(list(features.values())).reshape(1, -1)
        prediction = model.predict(feature_values)[0]
        probability = model.predict_proba(feature_values)[0][prediction]

        # 🧠 Type mapping for better display
        cancer_types = {
            0: "Healthy / Non-Cancerous",
            1: "Pancreatic Ductal Adenocarcinoma",
            2: "Neuroendocrine Tumor",
            3: "Mucinous Cystic Neoplasm"
        }

        cancer_type = cancer_types.get(prediction, "Unknown Type")
        cancer_stage = "Detected" if prediction != 0 else "Healthy"
        confidence = float(probability)
    else:
        cancer_type = "Model Not Trained"
        cancer_stage = "N/A"
        confidence = 0.0

    # Step 4: Return all steps for display & report
    return {
        'steps': {
            'original': image,
            'preprocessed': cv2.cvtColor(preprocessed, cv2.COLOR_GRAY2BGR),
            'segmented': cv2.cvtColor(segmented, cv2.COLOR_GRAY2BGR),
            'features': feature_vis
        },
        'cancer_type': cancer_type,
        'cancer_stage': cancer_stage,
        'confidence': confidence
    }
