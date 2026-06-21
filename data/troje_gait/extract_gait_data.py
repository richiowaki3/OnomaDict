# extract_gait_data.py
import re
import json

path = r"C:\Users\richi\.gemini\antigravity\scratch\bmwalker.js"

try:
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
        
    print(f"Reading {path}...")
    
    data = {
        "meanwalker": {},
        "bodyStructureaxis": [],
        "weightaxis": [],
        "nervousaxis": [],
        "happyaxis": []
    }
    
    # 1. Parse indexed arrays (meanwalker)
    pattern_indexed = r'this\.(\w+)\[(\d+)\]\s*=\s*new\s+Array\((.*?)\);'
    matches_indexed = re.findall(pattern_indexed, content, re.DOTALL)
    print(f"Found {len(matches_indexed)} indexed array assignments.")
    for name, idx_str, values_str in matches_indexed:
        idx = int(idx_str)
        clean_str = re.sub(r'//.*', '', values_str) # remove comments
        clean_str = clean_str.replace('\n', ' ').replace('\r', ' ')
        values = [float(x.strip()) for x in clean_str.split(',') if x.strip()]
        if name in data:
            data[name][idx] = values

    # 2. Parse non-indexed arrays (bodyStructureaxis, weightaxis, nervousaxis, happyaxis)
    pattern_non_indexed = r'this\.(bodyStructureaxis|weightaxis|nervousaxis|happyaxis)\s*=\s*new\s+Array\((.*?)\);'
    matches_non_indexed = re.findall(pattern_non_indexed, content, re.DOTALL)
    print(f"Found {len(matches_non_indexed)} non-indexed array assignments.")
    for name, values_str in matches_non_indexed:
        clean_str = re.sub(r'//.*', '', values_str) # remove comments
        clean_str = clean_str.replace('\n', ' ').replace('\r', ' ')
        values = [float(x.strip()) for x in clean_str.split(',') if x.strip()]
        if name in data:
            data[name] = values
            
    # Save to JSON
    output_path = r"c:\Users\richi\.antigravity\scratch\gait_data.json"
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
        
    print(f"Successfully extracted gait data and saved to {output_path}!")
    
    # Print summary
    print(f"  meanwalker: {list(data['meanwalker'].keys())} (dimensions: {[len(data['meanwalker'][k]) for k in data['meanwalker']]})")
    for key in ["bodyStructureaxis", "weightaxis", "nervousaxis", "happyaxis"]:
        print(f"  {key}: length {len(data[key])}")
        
except Exception as e:
    print("Error:", e)
