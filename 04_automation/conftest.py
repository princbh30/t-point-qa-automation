import os
import json
import pytest
from playwright.sync_api import Page, Locator

# Configure viewport size for stable desktop layout
@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    return {
        **browser_context_args,
        "viewport": {
            "width": 1920,
            "height": 1080
        }
    }

# Custom Locator Timeout Exception
class LocatorTimeoutException(Exception):
    def __init__(self, locator_key, url, attempted_selectors, message):
        self.locator_key = locator_key
        self.url = url
        self.attempted_selectors = attempted_selectors
        super().__init__(message)

# Load locators once
@pytest.fixture(scope="session")
def locators():
    locators_path = "/Users/prince.bharti/Desktop/QA_Automation_Hub/T Point/03_locators/locators.json"
    if not os.path.exists(locators_path):
        raise FileNotFoundError(f"Locators file not found at: {locators_path}")
    with open(locators_path, "r") as f:
        return json.load(f)

# Find element with fallback logic
def find_element(page: Page, locator_key: str, locators_dict: dict, timeout_ms: int = 5000) -> Locator:
    if locator_key not in locators_dict:
        raise ValueError(f"Locator key '{locator_key}' not found in locators.json")
    
    entry = locators_dict[locator_key]
    selectors = entry["selectors"]
    url = entry["url"]
    
    levels = ["primary", "secondary", "tertiary", "quaternary"]
    attempted = []
    
    for level in levels:
        selector = selectors.get(level)
        if not selector:
            continue
        attempted.append((level, selector))
        try:
            # Wait for element to be visible/interactable
            loc = page.locator(selector)
            loc.wait_for(state="visible", timeout=timeout_ms)
            return loc
        except Exception:
            continue
            
    # Self-Healing: Try opening parent dropdown menus if the element is hidden
    parts = locator_key.split('_', 1)
    if len(parts) == 2:
        prefix, suffix = parts[0], parts[1]
        
        # Check which menu it belongs to
        parent_menu_key = None
        if "tutorial" in suffix.lower() and suffix.lower() != "link_tutorials":
            parent_menu_key = f"{prefix}_link_tutorials"
        elif "interview" in suffix.lower() and suffix.lower() != "link_interviews":
            parent_menu_key = f"{prefix}_link_interviews"
        elif "compiler" in suffix.lower() and suffix.lower() != "link_compilers":
            parent_menu_key = f"{prefix}_link_compilers"
            
        if parent_menu_key and parent_menu_key in locators_dict:
            print(f"[Self-Healing] Element '{locator_key}' is hidden. Attempting to hover parent menu '{parent_menu_key}'...")
            try:
                # Find and hover parent menu item
                parent_loc = find_element(page, parent_menu_key, locators_dict, timeout_ms=1000)
                parent_loc.hover()
                page.wait_for_timeout(500)
                
                # Retry finding the target element after hovering
                for level in levels:
                    selector = selectors.get(level)
                    if not selector:
                        continue
                    try:
                        loc = page.locator(selector)
                        loc.wait_for(state="visible", timeout=timeout_ms)
                        return loc
                    except Exception:
                        continue
            except Exception as e:
                print(f"[Self-Healing] Warning: Failed to hover parent menu '{parent_menu_key}': {e}")

    # Raise exception if all levels failed
    msg = f"Locator key '{locator_key}' failed on all levels. Attempted: {attempted}"
    raise LocatorTimeoutException(locator_key, url, attempted, msg)

# SmartPage Wrapper for test code readability
class SmartPage:
    def __init__(self, page: Page, locators_dict: dict):
        self.page = page
        self.locators_dict = locators_dict
        
    def find(self, locator_key: str, timeout_ms: int = 5000) -> Locator:
        return find_element(self.page, locator_key, self.locators_dict, timeout_ms)
        
    def click(self, locator_key: str, timeout_ms: int = 5000, restore_state: bool = False):
        old_url = self.page.url
        loc = self.find(locator_key, timeout_ms)
        try:
            loc.click(timeout=3000)
        except Exception as e:
            try:
                # Force click fallback if normal click fails (e.g. obscured/overlay)
                loc.scroll_into_view_if_needed()
                loc.click(force=True, timeout=2000)
            except Exception as e2:
                entry = self.locators_dict[locator_key]
                url = entry["url"]
                selectors = entry["selectors"]
                attempted = [(k, v) for k, v in selectors.items() if v]
                msg = f"Failed clicking element '{locator_key}': {e2}"
                raise LocatorTimeoutException(locator_key, url, attempted, msg) from e2
        
        if restore_state:
            self.page.wait_for_timeout(300)
            if self.page.url != old_url:
                print(f"[Navigation Guard] Restoring page state: going back from {self.page.url} to {old_url}")
                try:
                    self.page.go_back()
                    self.page.wait_for_load_state("domcontentloaded")
                except Exception as e:
                    print(f"[Navigation Guard] Warning: Failed to go back: {e}")
        
    def fill(self, locator_key: str, value: str, timeout_ms: int = 5000):
        loc = self.find(locator_key, timeout_ms)
        try:
            loc.fill(value, timeout=3000)
        except Exception as e:
            entry = self.locators_dict[locator_key]
            url = entry["url"]
            selectors = entry["selectors"]
            attempted = [(k, v) for k, v in selectors.items() if v]
            msg = f"Failed filling element '{locator_key}': {e}"
            raise LocatorTimeoutException(locator_key, url, attempted, msg) from e
        
    def goto(self, url: str):
        self.page.goto(url)

# smart_page fixture for tests
@pytest.fixture
def smart_page(page: Page, locators: dict):
    # Dynamic page state load during self-healing
    healing_url = os.environ.get("HEALING_URL")
    if healing_url:
        print(f"\n[Self-Healing] Loading page state dynamically from locator URL: {healing_url}")
        page.goto(healing_url)
    return SmartPage(page, locators)

# Capture locator failure metadata for self-healing loop
@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    
    # Log details when a test fails during the execution phase
    if rep.failed and call.when == "call":
        excinfo = call.excinfo
        if excinfo and issubclass(excinfo.type, LocatorTimeoutException):
            exc = excinfo.value
            os.makedirs("reports/failures", exist_ok=True)
            failure_data = {
                "test_name": item.nodeid,
                "locator_key": exc.locator_key,
                "url": exc.url,
                "attempted": exc.attempted_selectors,
                "message": str(exc)
            }
            safe_name = "".join([c if c.isalnum() else "_" for c in item.nodeid])
            with open(f"reports/failures/{safe_name}.json", "w") as f:
                json.dump(failure_data, f)
