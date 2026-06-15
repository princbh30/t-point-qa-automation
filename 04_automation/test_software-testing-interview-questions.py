import pytest

def test_MODULE_software_testing_interview_questions(smart_page):
    """Test case for module: software-testing-interview-questions"""
    # Step: Navigate to https://www.tpointtech.com/software-testing-interview-questions
    smart_page.goto("http://tpointtech.com/software-testing-interview-questions")
    # Step: Verify and click header navigation links: `software-testing-interview-questions_link_tutorials` (Element: Link, Label: "Tutorials"), `software-testing-interview-questions_link_interviews` (Element: Link, Label: "Interviews"), `software-testing-interview-questions_link_compilers` (Element: Link, Label: "Compilers")
    smart_page.click("software-testing-interview-questions_link_tutorials", restore_state=True)
    smart_page.click("software-testing-interview-questions_link_interviews", restore_state=True)
    smart_page.click("software-testing-interview-questions_link_compilers", restore_state=True)
    # Step: Input "Python" into `software-testing-interview-questions_textbox_searchinput` (Element: Input, Label: "Search...", Placeholder: "Search...")
    smart_page.fill("software-testing-interview-questions_textbox_searchinput", "Python")
    # Step: Click `software-testing-interview-questions_button_searchbtn` (Element: Button, Text: "Search") to execute search query
    smart_page.click("software-testing-interview-questions_button_searchbtn", restore_state=True)
    # Step: Click sidebar tutorial link `software-testing-interview-questions_link_python_tutorial` (Element: Link, Text: "Python Tutorial") to navigate to that topic page
    smart_page.click("software-testing-interview-questions_link_python_tutorial")
    # Step: Input "testuser@example.com" into `software-testing-interview-questions_textbox_email` (Element: Input, Label: "Your Email", Placeholder: "Enter your email")
    smart_page.fill("software-testing-interview-questions_textbox_email", "testuser@example.com")
    # Step: Click `software-testing-interview-questions_button_subscribebtn` (Element: Button, Text: "Subscribe") to subscribe to newsletter
    smart_page.click("software-testing-interview-questions_button_subscribebtn")
    # Step: Scroll to footer and verify/click links: `software-testing-interview-questions_link_privacy_policy` (Element: Link, Label: "Privacy Policy"), `software-testing-interview-questions_link_about_us` (Element: Link, Label: "About Us"), `software-testing-interview-questions_link_contact_us` (Element: Link, Label: "Contact Us")
    smart_page.click("software-testing-interview-questions_link_privacy_policy", restore_state=True)
    smart_page.click("software-testing-interview-questions_link_about_us", restore_state=True)
    smart_page.click("software-testing-interview-questions_link_contact_us", restore_state=True)
