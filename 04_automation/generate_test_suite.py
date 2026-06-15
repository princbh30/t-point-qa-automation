import os
import glob
import re

test_cases_dir = "/Users/prince.bharti/Desktop/QA_Automation_Hub/T Point/02_test_cases"
output_file = "/Users/prince.bharti/Desktop/QA_Automation_Hub/T Point/04_automation/test_suite.py"

files = sorted(glob.glob(os.path.join(test_cases_dir, "*.md")))

code_lines = [
    "# Automated Test Suite for T Point",
    "# Generated dynamically from test case markdown specifications",
    "import pytest",
    "",
]

for file in files:
    filename = os.path.basename(file)
    # Extract module name from TC_MODULE_<name>.md
    m = re.match(r"TC_MODULE_(.+)\.md", filename)
    if not m:
        continue
    module_name = m.group(1)
    
    # Replace hyphen with underscore for Python function naming rules
    func_name = f"test_MODULE_{module_name.replace('-', '_')}"
    
    code_lines.append(f"def {func_name}(smart_page):")
    code_lines.append(f'    """Test case for module: {module_name}"""')
    
    # Parse the steps
    with open(file, 'r') as f:
        lines = f.readlines()
        
    in_steps = False
    for line in lines:
        line_str = line.strip()
        if line_str.startswith("- **Steps**"):
            in_steps = True
            continue
        if in_steps:
            if line_str.startswith("- **Expected Result**") or line_str.startswith("##"):
                in_steps = False
                continue
            if line_str:
                cleaned = line_str.split('.', 1)[-1].strip() if '.' in line_str else line_str
                code_lines.append(f"    # Step: {cleaned}")
                
                # Replace url domain
                cleaned_url = cleaned.replace("https://www.tpointtech.com", "http://tpointtech.com")
                
                if cleaned.startswith("Navigate to"):
                    url_m = re.search(r"Navigate to (https?://\S+)", cleaned_url)
                    if url_m:
                        url = url_m.group(1)
                        code_lines.append(f'    smart_page.goto("{url}")')
                elif "Input" in cleaned and "into" in cleaned:
                    input_m = re.search(r'Input "([^"]+)" into `([^`]+)`', cleaned)
                    if input_m:
                        value = input_m.group(1)
                        key = input_m.group(2)
                        code_lines.append(f'    smart_page.fill("{key}", "{value}")')
                else:
                    # Find all elements (backticked keys)
                    keys = re.findall(r'`([^`]+)`', cleaned)
                    # Check if this step is a verification click step where we should restore state
                    is_verification_step = ("header navigation links" in cleaned or 
                                            "Scroll to footer and verify/click links" in cleaned or
                                            "execute search query" in cleaned)
                    
                    for key in keys:
                        if is_verification_step:
                            code_lines.append(f'    smart_page.click("{key}", restore_state=True)')
                        else:
                            code_lines.append(f'    smart_page.click("{key}")')
                        
    code_lines.append("") # empty line between functions

# Write to test_suite.py
with open(output_file, 'w') as f:
    f.write("\n".join(code_lines) + "\n")

print(f"Generated test_suite.py with {len(files)} tests.")
