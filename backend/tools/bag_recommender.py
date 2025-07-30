def get_style_recommendation(input_text: str) -> str:
    """
    Generates a detailed style recommendation and search keywords from text.
    Supports personality, outfit, occasion, color, and bag style descriptions.
    """
    input_text = input_text.lower()
    result = ""
    style_keywords = []

    # --- Personality-Based ---
    if "artistic" in input_text:
        result += "Recommended Style: A hand-painted crossbody or unique tote with floral or abstract patterns.\n"
        style_keywords += ["hand painted", "artistic", "floral", "abstract"]
    elif "professional" in input_text:
        result += "Recommended Style: A structured tote or sleek satchel in neutral colors.\n"
        style_keywords += ["structured", "tote", "leather", "neutral"]
    elif "casual" in input_text:
        result += "Recommended Style: A sling or backpack with playful, practical design.\n"
        style_keywords += ["casual", "sling", "crossbody", "practical"]
    elif "elegant" in input_text or "formal" in input_text:
        result += "Recommended Style: A mini crossbody or clutch with metallic or jeweled accents.\n"
        style_keywords += ["elegant", "clutch", "mini", "metallic"]
    else:
        result += "Recommended Style: A classic crossbody or satchel with subtle patterns.\n"
        style_keywords += ["classic", "crossbody", "satchel"]

    # --- Occasion-Based ---
    if "office" in input_text:
        result += "Occasion Match: Pairs well with workwear—choose a sleek, large-capacity tote.\n"
        style_keywords += ["tote", "work", "office"]
    elif "party" in input_text or "evening" in input_text:
        result += "Occasion Match: Pairs with cocktail attire—consider metallic mini bags.\n"
        style_keywords += ["evening", "metallic", "mini", "shiny"]
    elif "travel" in input_text:
        result += "Occasion Match: Practical bags for travel—opt for multi-compartment slings.\n"
        style_keywords += ["travel", "sling", "crossbody", "compartment"]

    # --- Outfit-Based ---
    if "floral" in input_text:
        result += "Outfit Match: Compliments floral patterns with nature-inspired artwork.\n"
        style_keywords += ["floral", "garden", "nature"]
    elif "denim" in input_text:
        result += "Outfit Match: Earthy tones or bold contrast bags go well with denim.\n"
        style_keywords += ["denim", "earthy", "tan", "contrast"]
    elif "monochrome" in input_text or "solid" in input_text:
        result += "Outfit Match: Use colorful patterns to stand out against plain outfits.\n"
        style_keywords += ["colorful", "bold", "contrast"]

    # --- Color Preference ---
    if "red" in input_text:
        style_keywords += ["red", "vibrant"]
    elif "blue" in input_text:
        style_keywords += ["blue", "cool tone"]
    elif "gold" in input_text:
        style_keywords += ["gold", "luxury"]

    # --- Bag Style Mention ---
    for style in ["tote", "sling", "clutch", "backpack", "satchel", "crossbody"]:
        if style in input_text:
            style_keywords.append(style)

    # Final keyword cleanup
    unique_keywords = sorted(set(style_keywords), key=style_keywords.index)
    result += f"\nSearch Keywords: {', '.join(unique_keywords)}"
    return result
