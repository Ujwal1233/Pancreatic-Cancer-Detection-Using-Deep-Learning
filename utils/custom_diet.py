def generate_custom_diet(age, gender, scan_count, cancer_detected):
    diet = []

    # ------------------------------
    # AGE-BASED RECOMMENDATIONS
    # ------------------------------
    if age < 25:
        diet.append("🍎 Add energy-rich fruits & smoothies for metabolism.")
    elif 25 <= age < 40:
        diet.append("🥗 High-fiber foods like oats, spinach & broccoli.")
    elif 40 <= age < 60:
        diet.append("🍵 Add green tea, reduce salt & oily foods.")
    else:
        diet.append("🍚 Soft, easy-to-digest foods with light spices.")

    # ------------------------------
    # GENDER-BASED RECOMMENDATIONS
    # ------------------------------
    if gender.lower() == "male":
        diet.append("💪 Increase protein intake: eggs, lentils, grilled fish.")
    elif gender.lower() == "female":
        diet.append("🌸 Iron-rich foods: beets, spinach, dates, legumes.")
    else:
        diet.append("🌿 Balanced plant-based diet recommended.")

    # ------------------------------
    # HISTORY OF CANCER DETECTION
    # ------------------------------
    if cancer_detected:
        diet.extend([
            "🍓 Anti-inflammatory foods: turmeric, berries, green tea.",
            "🥬 Cruciferous vegetables: cabbage, kale, cauliflower.",
            "🍠 Avoid red meat, cheese & high-fat dairy."
        ])
    else:
        diet.append("👍 Continue a balanced low-fat, low-sugar diet.")

    # ------------------------------
    # SCAN COUNT BASED
    # ------------------------------
    if scan_count >= 3:
        diet.append("📉 Frequent scans detected — follow a consistent low-fat diet.")
        diet.append("💧 Drink 3L water daily & avoid late-night meals.")

    return diet
