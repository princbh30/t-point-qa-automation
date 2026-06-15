import os
import json
import urllib.parse
from playwright.sync_api import sync_playwright

TARGET_URL = "https://www.tpointtech.com"
OUTPUT_DIR = "/Users/prince.bharti/Desktop/QA_Automation_Hub/T Point/01_discovery"
OUTPUT_FILE = os.path.join(OUTPUT_DIR, "ui_map_1A.json")
SCREENSHOTS_DIR = os.path.join(OUTPUT_DIR, "screenshots")

# Ensure directories exist
os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(SCREENSHOTS_DIR, exist_ok=True)

# Javascript to be executed in the browser context
EXTRACT_ELEMENTS_JS = """
() => {
    function getImplicitRole(el) {
        let tag = el.tagName.toLowerCase();
        let role = el.getAttribute('role');
        if (role) return role.trim();
        if (tag === 'a') return 'link';
        if (tag === 'button') return 'button';
        if (tag === 'textarea') return 'textbox';
        if (tag === 'select') return 'combobox';
        if (tag === 'input') {
            let type = el.getAttribute('type') || 'text';
            type = type.toLowerCase();
            if (['button', 'submit', 'reset'].includes(type)) return 'button';
            if (type === 'checkbox') return 'checkbox';
            if (type === 'radio') return 'radio';
            if (['text', 'email', 'url', 'search', 'tel', 'password'].includes(type)) return 'textbox';
        }
        return tag;
    }

    function getAriaLabelOrName(el) {
        if (el.getAttribute('aria-label')) {
            return el.getAttribute('aria-label').trim();
        }
        if (el.getAttribute('aria-labelledby')) {
            let targetId = el.getAttribute('aria-labelledby');
            let target = document.getElementById(targetId);
            if (target && target.innerText) {
                return target.innerText.trim();
            }
        }
        if (el.tagName.toLowerCase() === 'input' && el.id) {
            let label = document.querySelector(`label[for="${el.id}"]`);
            if (label && label.innerText) {
                return label.innerText.trim();
            }
        }
        if (el.getAttribute('alt')) {
            return el.getAttribute('alt').trim();
        }
        if (el.getAttribute('title')) {
            return el.getAttribute('title').trim();
        }
        if (el.getAttribute('placeholder')) {
            return el.getAttribute('placeholder').trim();
        }
        if (el.innerText) {
            let text = el.innerText.trim();
            if (text.length > 50) {
                text = text.substring(0, 47) + '...';
            }
            return text;
        }
        return '';
    }

    function getStableClasses(el) {
        let classes = Array.from(el.classList);
        let stable = classes.filter(cls => {
            if (['active', 'show', 'hide', 'open', 'closed', 'selected', 'disabled', 'enabled', 'focus', 'hover', 'is-active', 'current'].includes(cls)) return false;
            if (/[a-zA-Z]+[0-9]+[a-zA-Z]+/.test(cls)) return false;
            if (cls.length > 35) return false;
            return true;
        });
        if (stable.length > 0) {
            let tag = el.tagName.toLowerCase();
            return `${tag}.${stable.join('.')}`;
        }
        return '';
    }

    function getStableRelativeXPath(element) {
        let paths = [];
        for (let el = element; el && el.nodeType === 1; el = el.parentNode) {
            if (el.id) {
                paths.unshift(`/*[@id="${el.id}"]`);
                break;
            }
            let index = 0;
            let hasSiblingsWithSameTag = false;
            if (el.parentNode) {
                let siblings = el.parentNode.children;
                for (let i = 0; i < siblings.length; i++) {
                    let sibling = siblings[i];
                    if (sibling.tagName === el.tagName) {
                        if (sibling === el) {
                            index = i + 1;
                        } else {
                            hasSiblingsWithSameTag = true;
                        }
                    }
                }
            }
            let tagName = el.tagName.toLowerCase();
            let pathIndex = hasSiblingsWithSameTag ? `[${index}]` : '';
            paths.unshift(`${tagName}${pathIndex}`);
        }
        return paths.length ? '//' + paths.join('/') : null;
    }

    const interactiveSelectors = [
        'a', 'button', 'input', 'select', 'textarea',
        '[role="button"]', '[role="link"]', '[role="checkbox"]', '[role="radio"]',
        '[tabindex="0"]', '[onclick]'
    ];

    const elements = document.querySelectorAll(interactiveSelectors.join(', '));
    const results = [];

    elements.forEach((el, index) => {
        // Skip hidden or non-visible elements
        const rect = el.getBoundingClientRect();
        if (rect.width === 0 && rect.height === 0) return;
        
        const style = window.getComputedStyle(el);
        if (style.display === 'none' || style.visibility === 'hidden') return;

        let tag = el.tagName.toLowerCase();
        let role = getImplicitRole(el);
        let name = getAriaLabelOrName(el);
        
        // Build the unique key name
        let pageName = window.location.pathname.replace(/\\//g, '_').replace(/^_+|_+$/g, '') || 'home';
        let cleanName = name ? name.toLowerCase().replace(/[^a-z0-9]+/g, '_').replace(/^_+|_+$/g, '') : '';
        if (cleanName.length > 25) {
            cleanName = cleanName.substring(0, 25);
        }
        let elId = el.id ? el.id.toLowerCase().replace(/[^a-z0-9]+/g, '_') : '';
        let nameAttr = el.getAttribute('name') ? el.getAttribute('name').toLowerCase().replace(/[^a-z0-9]+/g, '_') : '';
        
        let suffix = elId || nameAttr || cleanName || `idx_${index}`;
        let key = `${pageName}_${role}_${suffix}`;
        
        let fallbacks = [];
        
        // 1. Primary
        let dataTestId = el.getAttribute('data-testid') || el.getAttribute('data-qa');
        if (dataTestId) {
            fallbacks.push(`[data-testid="${dataTestId}"]`);
        }
        
        // 2. Secondary
        if (name) {
            fallbacks.push(`role=${role}[name="${name}"]`);
        } else {
            fallbacks.push(`role=${role}`);
        }
        
        // 3. Tertiary
        if (el.id) {
            fallbacks.push(`#${el.id}`);
        }
        if (el.getAttribute('name')) {
            fallbacks.push(`[name="${el.getAttribute('name')}"]`);
        }
        let stableClass = getStableClasses(el);
        if (stableClass) {
            fallbacks.push(stableClass);
        }
        
        // 4. Quaternary
        let xpath = getStableRelativeXPath(el);
        if (xpath) {
            fallbacks.push(xpath);
        }
        
        results.push({ key, fallbacks });
    });

    return results;
}
"""

def clean_url(url, base_domain):
    parsed = urllib.parse.urlparse(url)
    # Ensure it's internal
    if parsed.netloc and parsed.netloc != base_domain and not parsed.netloc.endswith('.' + base_domain):
        return None
    # Normalize path
    path = parsed.path
    if not path:
        path = '/'
    # Strip fragments and query parameters for crawling
    normalized = urllib.parse.urlunparse((parsed.scheme or 'https', parsed.netloc or base_domain, path, '', '', ''))
    return normalized

def crawl_site():
    print("Starting crawl of", TARGET_URL)
    parsed_target = urllib.parse.urlparse(TARGET_URL)
    base_domain = parsed_target.netloc
    
    visited_urls = set()
    url_queue = [TARGET_URL]
    
    # Store all discovered UI elements
    ui_elements = {}
    
    # Load existing maps if any
    if os.path.exists(OUTPUT_FILE):
        try:
            with open(OUTPUT_FILE, 'r') as f:
                ui_elements = json.load(f)
            print(f"Loaded {len(ui_elements)} existing elements from map.")
        except Exception as e:
            print("Failed to load existing ui_map_1A.json:", e)

    with sync_playwright() as p:
        # Try headed mode first, fallback to headless if display server is missing
        try:
            print("Attempting to launch browser in headed mode...")
            browser = p.chromium.launch(headless=False)
        except Exception as e:
            print(f"Headed launch failed ({e}). Falling back to headless mode...")
            browser = p.chromium.launch(headless=True)
            
        context = browser.new_context(viewport={"width": 1280, "height": 800})
        page = context.new_page()
        
        while url_queue:
            current_url = url_queue.pop(0)
            if current_url in visited_urls:
                continue
                
            print(f"\nNavigating to: {current_url}")
            try:
                # Go to URL and wait for DOM / network to settle
                page.goto(current_url, timeout=30000, wait_until="load")
                page.wait_for_timeout(3000) # Wait a bit for dynamic content
                
                visited_urls.add(current_url)
                
                # Take screenshot for audit trail
                safe_filename = current_url.replace("https://", "").replace("http://", "").replace("/", "_").replace(".", "_") or "home"
                screenshot_path = os.path.join(SCREENSHOTS_DIR, f"{safe_filename}.png")
                page.screenshot(path=screenshot_path)
                print(f"Screenshot saved to: {screenshot_path}")
                
                # Extract selectors
                elements = page.evaluate(EXTRACT_ELEMENTS_JS)
                print(f"Discovered {len(elements)} visible interactive elements on page.")
                
                # Add/merge findings
                for el in elements:
                    key = el['key']
                    fallbacks = el['fallbacks']
                    if key not in ui_elements:
                        ui_elements[key] = fallbacks
                    else:
                        # Append any unique new fallbacks to existing key list
                        existing = set(ui_elements[key])
                        for f in fallbacks:
                            if f not in existing:
                                ui_elements[key].append(f)
                
                # Discover more internal links on the page
                hrefs = page.evaluate("() => Array.from(document.querySelectorAll('a')).map(a => a.href)")
                
                for href in hrefs:
                    if href:
                        cleaned = clean_url(href, base_domain)
                        if cleaned and cleaned not in visited_urls and cleaned not in url_queue:
                            # Limit total crawled pages to 25 to keep execution fast and focused
                            if len(visited_urls) + len(url_queue) < 25:
                                url_queue.append(cleaned)
                                print(f"Queued internal link: {cleaned}")
                                
            except Exception as ex:
                print(f"Error crawling {current_url}: {ex}")
                
        browser.close()
        
    # Write back the inventory
    print(f"\nTotal elements in inventory: {len(ui_elements)}")
    with open(OUTPUT_FILE, 'w') as f:
        json.dump(ui_elements, f, indent=2)
    print(f"Selector map saved successfully to: {OUTPUT_FILE}")

if __name__ == "__main__":
    crawl_site()
