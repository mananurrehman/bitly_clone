import subprocess
import json
from datetime import datetime

def run_tests():
    # Run pytest with coverage and html report
    result = subprocess.run(
        ["pytest", "--cov=.", "--cov-report=html", "--html=test_report.html", "--self-contained-html", "-v"],
        capture_output=True,
        text=True
    )
    
    # Create test summary
    summary = {
        "timestamp": datetime.now().isoformat(),
        "exit_code": result.returncode,
        "passed": "passed" in result.stdout.lower(),
        "output": result.stdout
    }
    
    with open("test_summary.json", "w") as f:
        json.dump(summary, f)
    
    return result.returncode

if __name__ == "__main__":
    exit(run_tests())