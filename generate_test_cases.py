import os
import json
import re

ui_map_path = "/Users/prince.bharti/Desktop/QA_Automation_Hub/T Point/01_discovery/ui_map_1A.json"
output_dir = "/Users/prince.bharti/Desktop/QA_Automation_Hub/T Point/02_test_cases"

os.makedirs(output_dir, exist_ok=True)

with open(ui_map_path, 'r') as f:
    ui_map = json.load(f)

# Group keys by module
modules = {}
for key, selectors in ui_map.items():
    parts = key.split('_')
    module = parts[0]
    if module not in modules:
        modules[module] = []
    modules[module].append((key, selectors))

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

for module_name, elements in modules.items():
    filename = f"TC_MODULE_{module_name}.md"
    filepath = os.path.join(output_dir, filename)
    
    # Immutable check: do not touch or overwrite if already exists
    if os.path.exists(filepath):
        print(f"Skipping existing file: {filename}")
        continue
        
    print(f"Generating test case for module: {module_name}")
    
    # Determine the module URL
    if module_name == 'home':
        url = "https://www.tpointtech.com"
    else:
        url = f"https://www.tpointtech.com/{module_name}"
        
    # Categorize elements for steps
    search_input = None
    search_btn = None
    email_input = None
    subscribe_btn = None
    next_link = None
    nav_links = []
    sidebar_links = []
    footer_links = []
    other_elements = []
    
    for key, selectors in elements:
        el_type, label, placeholder = parse_element(key, selectors)
        parts = key.split('_')
        suffix = "_".join(parts[2:])
        
        # Identify key inputs and buttons
        if 'search' in key.lower() and el_type == 'Input':
            search_input = (key, el_type, label, placeholder)
        elif 'search' in key.lower() and el_type == 'Button':
            search_btn = (key, el_type, label, placeholder)
        elif 'email' in key.lower() and el_type == 'Input':
            email_input = (key, el_type, label, placeholder)
        elif 'subscribe' in key.lower() and el_type == 'Button':
            subscribe_btn = (key, el_type, label, placeholder)
        elif suffix == 'next' and el_type == 'Link':
            next_link = (key, el_type, label, placeholder)
        elif suffix in ['tutorials', 'interviews', 'compilers'] and el_type == 'Link':
            nav_links.append((key, el_type, label, placeholder))
        elif suffix in ['privacy_policy', 'about_us', 'contact_us'] and el_type == 'Link':
            footer_links.append((key, el_type, label, placeholder))
        elif not suffix.startswith('idx_') and el_type == 'Link':
            sidebar_links.append((key, el_type, label, placeholder))
        else:
            other_elements.append((key, el_type, label, placeholder))
            
    # Let's write the markdown file
    content = []
    content.append(f"# Test Case: MODULE_{module_name} | UI Verification and Navigation")
    content.append(f"- **Preconditions**: User is on page {url}")
    content.append("- **Steps**:")
    
    step_num = 1
    content.append(f"  {step_num}. Navigate to {url}")
    step_num += 1
    
    # 2. Header links
    if nav_links:
        step_desc = f"  {step_num}. Verify and click header navigation links: "
        links_str = []
        for key, el_type, label, placeholder in nav_links[:3]:
            links_str.append(f"`{key}` (Element: {el_type}, Label: \"{label}\")")
        step_desc += ", ".join(links_str)
        content.append(step_desc)
        step_num += 1
        
    # 3. Search Form
    if search_input and search_btn:
        content.append(f"  {step_num}. Input \"Python\" into `{search_input[0]}` (Element: {search_input[1]}, Label: \"{search_input[2]}\", Placeholder: \"{search_input[3]}\")")
        step_num += 1
        content.append(f"  {step_num}. Click `{search_btn[0]}` (Element: {search_btn[1]}, Text: \"{search_btn[2]}\") to execute search query")
        step_num += 1
        
    # 4. Next link / Sidebar link navigation
    if next_link:
        content.append(f"  {step_num}. Click `{next_link[0]}` (Element: {next_link[1]}, Text: \"{next_link[2]}\") to navigate to the next page")
        step_num += 1
    elif sidebar_links:
        # Choose a representative sidebar link
        key, el_type, label, placeholder = sidebar_links[0]
        content.append(f"  {step_num}. Click sidebar tutorial link `{key}` (Element: {el_type}, Text: \"{label}\") to navigate to that topic page")
        step_num += 1
        
    # 5. Email newsletter signup
    if email_input and subscribe_btn:
        content.append(f"  {step_num}. Input \"testuser@example.com\" into `{email_input[0]}` (Element: {email_input[1]}, Label: \"{email_input[2]}\", Placeholder: \"{email_input[3]}\")")
        step_num += 1
        content.append(f"  {step_num}. Click `{subscribe_btn[0]}` (Element: {subscribe_btn[1]}, Text: \"{subscribe_btn[2]}\") to subscribe to newsletter")
        step_num += 1
        
    # 6. Footer links
    if footer_links:
        step_desc = f"  {step_num}. Scroll to footer and verify/click links: "
        links_str = []
        for key, el_type, label, placeholder in footer_links[:3]:
            links_str.append(f"`{key}` (Element: {el_type}, Label: \"{label}\")")
        step_desc += ", ".join(links_str)
        content.append(step_desc)
        step_num += 1
        
    # Expected Result
    content.append("- **Expected Result**: The page loads successfully, and all interactive elements are responsive. Navigation links load their target pages, search displays correct results, and form inputs function as expected.")
    
    # Semantic References Section
    content.append("\n## Semantic References for Healing")
    for key, selectors in elements:
        el_type, label, placeholder = parse_element(key, selectors)
        desc_parts = []
        if placeholder:
            desc_parts.append(f'Placeholder: "{placeholder}"')
        if label:
            desc_parts.append(f'Label: "{label}"')
        desc_str = " / ".join(desc_parts) if desc_parts else 'Label: ""'
        content.append(f"- `{key} | {el_type} | {desc_str}`")
        
    # Write to file
    with open(filepath, 'w') as f:
        f.write("\n".join(content) + "\n")

print("Done generating test cases!")
