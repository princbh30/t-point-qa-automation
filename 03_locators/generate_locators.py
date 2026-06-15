import os
import json
import re

ui_map_path = "/Users/prince.bharti/Desktop/QA_Automation_Hub/T Point/01_discovery/ui_map_1A.json"
locators_dir = "/Users/prince.bharti/Desktop/QA_Automation_Hub/T Point/03_locators"
locators_json_path = os.path.join(locators_dir, "locators.json")

os.makedirs(locators_dir, exist_ok=True)

with open(ui_map_path, 'r') as f:
    ui_map = json.load(f)

# Element mapping to user friendly types
element_map = {
    'link': 'Link',
    'button': 'Button',
    'textbox': 'Input',
    'input': 'Input',
    'combobox': 'Select',
    'select': 'Select',
    'checkbox': 'Checkbox',
    'radio': 'Radio',
    'div': 'Div',
    'span': 'Span',
    'heading': 'Heading',
}

def parse_element(key, selectors):
    parts = key.split('_')
    role = parts[1] if len(parts) > 1 else 'element'
    element_type = element_map.get(role, role.capitalize())
    
    label = ""
    placeholder = ""
    
    # Try to find name in role selector: e.g. role=link[name="Tutorials"]
    for s in selectors:
        if s.startswith('role='):
            m = re.search(r'name="([^"]+)"', s)
            if m:
                label = m.group(1)
            break
            
    if not label:
        suffix = "_".join(parts[2:])
        if not suffix.startswith("idx_"):
            label = suffix.replace('_', ' ').capitalize()
            
    # Check if there is a placeholder
    for s in selectors:
        if 'placeholder=' in s:
            m = re.search(r'placeholder="([^"]+)"', s)
            if m:
                placeholder = m.group(1)
                
    if 'search' in key.lower() and element_type == 'Input':
        if not label:
            label = "Search"
        if not placeholder:
            placeholder = "Search..."
            
    if 'email' in key.lower() and element_type == 'Input':
        if not label:
            label = "Email Address"
        if not placeholder:
            placeholder = "Enter your email"
            
    return element_type, label, placeholder

locators = {}

for key, selectors in ui_map.items():
    # Split by first underscore to get module name
    parts = key.split('_', 1)
    module_name = parts[0]
    
    element_type, label, placeholder = parse_element(key, selectors)
    
    # Clean and pad selectors to have exactly 4 levels: primary, secondary, tertiary, quaternary
    cleaned_selectors = []
    for s in selectors:
        # If it starts with / or //, prefix with xpath=
        if s.startswith('/') or s.startswith('//'):
            cleaned_selectors.append(f"xpath={s}")
        else:
            cleaned_selectors.append(s)
            
    # Fill up to 4 selectors
    while len(cleaned_selectors) < 4:
        if cleaned_selectors:
            cleaned_selectors.append(cleaned_selectors[-1])
        else:
            cleaned_selectors.append("") # fallback
            
    selectors_dict = {
        "primary": cleaned_selectors[0],
        "secondary": cleaned_selectors[1],
        "tertiary": cleaned_selectors[2],
        "quaternary": cleaned_selectors[3]
    }
    
    # Determine the module URL using target URL base http://tpointtech.com
    base_url = "http://tpointtech.com"
    if module_name == 'home':
        url = base_url + "/"
    else:
        url = f"{base_url}/{module_name}"
        
    locators[key] = {
        "type": element_type.lower(),
        "label": label,
        "placeholder": placeholder,
        "selectors": selectors_dict,
        "url": url
    }

# Write locators.json
with open(locators_json_path, 'w') as f:
    json.dump(locators, f, indent=2)

print(f"Generated locators.json with {len(locators)} entries.")
