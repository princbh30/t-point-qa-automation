#!/usr/bin/env python3
import os
import sys
import glob
import json
import shutil
import datetime
import subprocess

def clear_failures_dir():
    failures_dir = "reports/failures"
    if os.path.exists(failures_dir):
        shutil.rmtree(failures_dir)
    os.makedirs(failures_dir, exist_ok=True)

def main():
    # 1. Generate a single timestamp for the execution run
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    report_path = f"reports/report_{timestamp}.html"
    os.makedirs("reports", exist_ok=True)
    
    print(f"============================================================")
    # Clear failures from any previous runs
    clear_failures_dir()
    
    # 2. Main Execution Run (Run all tests concurrently)
    print(f"[{datetime.datetime.now()}] Starting main execution run...")
    print(f"Consolidated report will be written to: {report_path}")
    
    # Run pytest concurrently using pytest-xdist (-n auto)
    # We use the virtual environment's pytest
    pytest_bin = "./venv/bin/pytest"
    cmd = [
        pytest_bin,
        "-n", "3",
        f"--html={report_path}",
        "--self-contained-html",
        "04_automation/test_suite.py"
    ]
    
    print(f"Running command: {' '.join(cmd)}")
    result = subprocess.run(cmd)
    
    # 3. Check for failures
    failure_files = glob.glob("reports/failures/*.json")
    if not failure_files:
        print(f"[{datetime.datetime.now()}] Main execution run finished: 100% Green!")
        print(f"Consolidated report: {report_path}")
        sys.exit(0)
        
    print(f"\n[{datetime.datetime.now()}] Main execution run finished with {len(failure_files)} failed tests.")
    print(f"Starting self-healing loop...")
    
    healed_tests = []
    failed_to_heal = []
    
    # 4. Self-Healing Loop (Re-run failed tests individually)
    # Load locators to get the URL dynamically during self-healing
    locators_path = "03_locators/locators.json"
    with open(locators_path, "r") as f:
        locators = json.load(f)
        
    # Load all failure data into memory before clearing the failures directory
    failures_to_heal = []
    for f_file in failure_files:
        try:
            with open(f_file, "r") as f:
                failures_to_heal.append(json.load(f))
        except Exception as e:
            print(f"Error reading failure file {f_file}: {e}")
            
    for fail_data in failures_to_heal:
        test_name = fail_data["test_name"]
        locator_key = fail_data["locator_key"]
        
        # Load page state dynamically during self-healing by reading "url" from locators.json
        if locator_key in locators:
            healing_url = locators[locator_key]["url"]
        else:
            healing_url = fail_data["url"]
            
        print(f"\n------------------------------------------------------------")
        print(f"[{datetime.datetime.now()}] Healing Test: {test_name}")
        print(f"Failing Locator: {locator_key}")
        print(f"Metadata-Driven Navigation URL: {healing_url}")
        
        # Clear failures directory before this individual run to detect new failures
        clear_failures_dir()
        
        # Set the HEALING_URL env variable so conftest.py loads the page state dynamically
        env = os.environ.copy()
        env["HEALING_URL"] = healing_url
        
        # Re-run individually WITHOUT generating separate HTML reports to avoid pollution
        heal_cmd = [pytest_bin, test_name]
        print(f"Running individual healing command: {' '.join(heal_cmd)}")
        heal_result = subprocess.run(heal_cmd, env=env)
        
        # Check if the test passed (no new failures registered and exit code is 0)
        new_failures = glob.glob("reports/failures/*.json")
        if heal_result.returncode == 0 and not new_failures:
            print(f"[{datetime.datetime.now()}] SUCCESS: Test {test_name} healed successfully!")
            healed_tests.append(test_name)
        else:
            print(f"[{datetime.datetime.now()}] FAILURE: Test {test_name} could not be healed.")
            failed_to_heal.append(test_name)
            
    print(f"\n============================================================")
    print(f"Self-Healing Loop Completed:")
    print(f"  Healed: {len(healed_tests)} tests")
    print(f"  Failed to Heal: {len(failed_to_heal)} tests")
    
    # Clear the HEALING_URL from environment for subsequent runs
    if "HEALING_URL" in os.environ:
        del os.environ["HEALING_URL"]
        
    # 5. Final Consolidated Report
    # If any tests were healed, compile a final 100% green report by re-running the entire suite
    if healed_tests:
        print(f"\n[{datetime.datetime.now()}] Re-running entire suite to compile a final consolidated report...")
        clear_failures_dir()
        
        final_cmd = [
            pytest_bin,
            "-n", "3",
            f"--html={report_path}",
            "--self-contained-html",
            "04_automation/test_suite.py"
        ]
        print(f"Running final command: {' '.join(final_cmd)}")
        final_result = subprocess.run(final_cmd)
        print(f"[{datetime.datetime.now()}] Final consolidated report updated at: {report_path}")
        if final_result.returncode == 0:
            print("All tests passed in final consolidated run!")
        else:
            print("Some tests still failed in final consolidated run.")
    else:
        print(f"\nNo tests were healed. Original consolidated report remains at: {report_path}")

if __name__ == "__main__":
    main()
