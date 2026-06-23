import csv
import json
import os

def csv_to_json():
    csv_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'onomatopoeia_dictionary.csv')
    json_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'onomatopoeia_dictionary.json')
    
    if not os.path.exists(csv_path):
        print(f"Error: CSV file not found at {csv_path}")
        return
        
    with open(csv_path, mode='r', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        items = []
        for row in reader:
            # Parse types
            # x1-x4 (effort)
            effort = {
                "weight": int(row["x1"]),
                "time": int(row["x2"]),
                "space": int(row["x3"]),
                "flow": int(row["x4"])
            }
            # x5-x8 (acoustic)
            acoustic = {
                "hardness": int(row["x5"]),
                "moisture": int(row["x6"]),
                "freq_hz": float(row["x7_hz"]),
                "freq_norm": float(row["x7_norm"]),
                "decay": int(row["x8"])
            }
            # x9-x12 (extended)
            extended = {
                "reynolds": float(row["x9_re"]),
                "reynolds_norm": float(row["x9_norm"]),
                "boyle": int(row["x10"]),
                "temp_code": row["x11"],
                "temp_ord": int(row["x11_ord"]),
                "color_hex": row["x12"],
                "lab": [float(row["L"]), float(row["a"]), float(row["b"])]
            }
            # x13-x16 (phrasing)
            phrasing = {
                "accent": int(row["x13_accent"]),
                "contour": int(row["x14_contour"]),
                "meter": int(row["x15_meter"]),
                "regularity": int(row["x16_regularity"])
            }
            
            item = {
                "word": row["word"],
                "ipa_original": row["ipa_original"],
                "ipa_clean": row["ipa_clean"],
                "ipa_changed": int(row["ipa_changed"]),
                "effort": effort,
                "acoustic": acoustic,
                "extended": extended,
                "phrasing": phrasing,
                "rationale": row["rationale"],
                "flags": row["flags"],
                "morph_type": row["morph_type"]
            }
            items.append(item)
            
    with open(json_path, mode='w', encoding='utf-8') as f:
        # Use indent=1 to match the 1-space indentation of the original JSON
        json.dump(items, f, ensure_ascii=False, indent=1)
        f.write('\n') # trailing newline
        
    print(f"Successfully converted CSV to JSON: {json_path}")

if __name__ == '__main__':
    csv_to_json()
