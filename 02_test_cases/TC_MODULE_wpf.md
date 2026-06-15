# Test Case: MODULE_wpf | UI Verification and Navigation
- **Preconditions**: User is on page https://www.tpointtech.com/wpf
- **Steps**:
  1. Navigate to https://www.tpointtech.com/wpf
  2. Verify and click header navigation links: `wpf_link_tutorials` (Element: Link, Label: "Tutorials"), `wpf_link_interviews` (Element: Link, Label: "Interviews"), `wpf_link_compilers` (Element: Link, Label: "Compilers")
  3. Input "Python" into `wpf_textbox_searchinput` (Element: Input, Label: "Search...", Placeholder: "Search...")
  4. Click `wpf_button_searchbtn` (Element: Button, Text: "Search") to execute search query
  5. Click `wpf_link_next` (Element: Link, Text: "next →") to navigate to the next page
  6. Input "testuser@example.com" into `wpf_textbox_email` (Element: Input, Label: "Your Email", Placeholder: "Enter your email")
  7. Click `wpf_button_subscribebtn` (Element: Button, Text: "Subscribe") to subscribe to newsletter
  8. Scroll to footer and verify/click links: `wpf_link_privacy_policy` (Element: Link, Label: "Privacy Policy"), `wpf_link_about_us` (Element: Link, Label: "About Us"), `wpf_link_contact_us` (Element: Link, Label: "Contact Us")
- **Expected Result**: The page loads successfully, and all interactive elements are responsive. Navigation links load their target pages, search displays correct results, and form inputs function as expected.

## Semantic References for Healing
- `wpf_link_idx_0 | Link | Label: ""`
- `wpf_textbox_searchinput | Input | Placeholder: "Search..." / Label: "Search..."`
- `wpf_button_searchbtn | Button | Label: "Search"`
- `wpf_link_tutorials | Link | Label: "Tutorials"`
- `wpf_link_interviews | Link | Label: "Interviews"`
- `wpf_link_compilers | Link | Label: "Compilers"`
- `wpf_div_idx_147 | Div | Label: ""`
- `wpf_div_idx_148 | Div | Label: ""`
- `wpf_div_idx_149 | Div | Label: ""`
- `wpf_div_idx_150 | Div | Label: ""`
- `wpf_div_idx_151 | Div | Label: ""`
- `wpf_button_idx_152 | Button | Label: ""`
- `wpf_link_python_tutorial | Link | Label: "Python Tutorial"`
- `wpf_link_java_tutorial | Link | Label: "Java Tutorial"`
- `wpf_link_javascript_tutorial | Link | Label: "JavaScript Tutorial"`
- `wpf_link_sql_tutorial | Link | Label: "SQL Tutorial"`
- `wpf_link_c_tutorial | Link | Label: "C Tutorial"`
- `wpf_link_html_tutorial | Link | Label: "HTML Tutorial"`
- `wpf_link_css_tutorial | Link | Label: "CSS Tutorial"`
- `wpf_link_react_tutorial | Link | Label: "React Tutorial"`
- `wpf_link_nodejs_tutorial | Link | Label: "NodeJS Tutorial"`
- `wpf_link_sprint_boot_tutorial | Link | Label: "Sprint Boot Tutorial"`
- `wpf_link_php_tutorial | Link | Label: "PHP Tutorial"`
- `wpf_link_mysql_tutorial | Link | Label: "MYSQL Tutorial"`
- `wpf_link_mongodb_tutorial | Link | Label: "MongoDB Tutorial"`
- `wpf_link_ai_tutorial | Link | Label: "AI Tutorial"`
- `wpf_link_machine_learning_tutorial | Link | Label: "Machine Learning Tutorial"`
- `wpf_link_dsa_tutorial | Link | Label: "DSA Tutorial"`
- `wpf_link_dbms_tutorial | Link | Label: "DBMS Tutorial"`
- `wpf_link_os_tutorial | Link | Label: "OS Tutorial"`
- `wpf_button_wpf_tutorial | Button | Label: "WPF Tutorial"`
- `wpf_link_wpf | Link | Label: "WPF"`
- `wpf_link_wpf_in_c | Link | Label: "WPF in C#"`
- `wpf_link_wpf_listbox | Link | Label: "WPF ListBox"`
- `wpf_link_wpf_vs_winform | Link | Label: "WPF vs WinForm"`
- `wpf_link_wpf_button_control | Link | Label: "WPF Button Control"`
- `wpf_link_wpf_checkbox_control | Link | Label: "WPF CheckBox Control"`
- `wpf_link_wpf_combobox | Link | Label: "WPF ComboBox"`
- `wpf_link_stackpanel_control | Link | Label: "StackPanel Control"`
- `wpf_link_wpf_dockpanel_layout | Link | Label: "WPF DockPanel Layout"`
- `wpf_link_wpf_canvas_panel | Link | Label: "WPF Canvas Panel"`
- `wpf_link_wpf_dialog_box | Link | Label: "WPF Dialog Box"`
- `wpf_link_wpf_context_menu | Link | Label: "WPF Context Menu"`
- `wpf_link_gridview_control | Link | Label: "GridView Control"`
- `wpf_link_wpf_image_control | Link | Label: "WPF Image Control"`
- `wpf_link_wpf_progress_bar | Link | Label: "WPF Progress Bar"`
- `wpf_link_radiobutton_control | Link | Label: "RadioButton Control"`
- `wpf_link_togglebutton_control | Link | Label: "ToggleButton Control"`
- `wpf_link_tooltip_control | Link | Label: "ToolTip Control"`
- `wpf_link_home | Link | Label: "Home"`
- `wpf_link_xml | Link | Label: "XML"`
- `wpf_link_html | Link | Label: "HTML"`
- `wpf_heading_these_are_topics_related_ | Heading | Label: "These are topics related to the article that might interest you"`
- `wpf_link_programming_languages | Link | Label: "programming languages"`
- `wpf_link_operating_systems | Link | Label: "Operating Systems"`
- `wpf_link_windows_os | Link | Label: "Windows OS"`
- `wpf_link_advantages_and_disadvanta | Link | Label: "Advantages and disadvantage"`
- `wpf_link_next | Link | Label: "next →"`
- `wpf_textbox_email | Input | Placeholder: "Enter your email" / Label: "Your Email"`
- `wpf_button_subscribebtn | Button | Label: "Subscribe"`
- `wpf_iframe_aswift_2 | Iframe | Label: "Advertisement"`
- `wpf_link_hr_tpointtech_com | Link | Label: "hr@tpointtech.com"`
- `wpf_link_91_9599086977 | Link | Label: "+91-9599086977"`
- `wpf_link_idx_208 | Link | Label: ""`
- `wpf_link_idx_209 | Link | Label: ""`
- `wpf_link_idx_210 | Link | Label: ""`
- `wpf_link_idx_211 | Link | Label: ""`
- `wpf_link_idx_212 | Link | Label: ""`
- `wpf_link_idx_213 | Link | Label: ""`
- `wpf_link_data_structure_tutorial | Link | Label: "Data Structure Tutorial"`
- `wpf_link_c_programming_tutorial | Link | Label: "C Programming Tutorial"`
- `wpf_link_jquery_tutorial | Link | Label: "jQuery Tutorial"`
- `wpf_link_spring_tutorial | Link | Label: "Spring Tutorial"`
- `wpf_link_python_interview_question | Link | Label: "Python Interview Questions"`
- `wpf_link_java_interview_questions | Link | Label: "Java Interview Questions"`
- `wpf_link_data_structure_interview_ | Link | Label: "Data Structure Interview Questions"`
- `wpf_link_c_interview_questions | Link | Label: "C++ Interview Questions"`
- `wpf_link_html_interview_questions | Link | Label: "HTML Interview Questions"`
- `wpf_link_javascript_interview_ques | Link | Label: "JavaScript Interview Questions"`
- `wpf_link_jquery_interview_question | Link | Label: "jQuery Interview Questions"`
- `wpf_link_sql_interview_questions | Link | Label: "SQL Interview Questions"`
- `wpf_link_power_bi_interview_questi | Link | Label: "Power BI Interview Questions"`
- `wpf_link_online_c_compiler | Link | Label: "Online C Compiler"`
- `wpf_link_online_r_compiler | Link | Label: "Online R Compiler"`
- `wpf_link_online_php_compiler | Link | Label: "Online PHP Compiler"`
- `wpf_link_online_java_compiler | Link | Label: "Online Java Compiler"`
- `wpf_link_online_html_editor | Link | Label: "Online HTML Editor"`
- `wpf_link_online_swift_compiler | Link | Label: "Online Swift Compiler"`
- `wpf_link_online_python_compiler | Link | Label: "Online Python Compiler"`
- `wpf_link_online_javascript_editor | Link | Label: "Online JavaScript Editor"`
- `wpf_link_online_typescript_editor | Link | Label: "Online TypeScript Editor"`
- `wpf_link_latest_post | Link | Label: "Latest Post"`
- `wpf_link_tutorials_list | Link | Label: "Tutorials List"`
- `wpf_link_privacy_policy | Link | Label: "Privacy Policy"`
- `wpf_link_about_us | Link | Label: "About Us"`
- `wpf_link_contact_us | Link | Label: "Contact Us"`
