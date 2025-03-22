#!/usr/bin/env python3
"""
Test Report Generator for In-Memory Database Service
Runs all test suites and generates HTML reports
"""

import subprocess
import sys
import re
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Tuple

class TestReportGenerator:
    def __init__(self):
        self.report_dir = Path(__file__).parent / "test_reports"
        self.report_dir.mkdir(exist_ok=True)
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.backend_dir = Path(__file__).parent.parent

    def run_test_suite(self, test_file: str) -> Tuple[str, int, int, int, float]:
        """Run a test suite and return its output and statistics."""
        try:
            # Use pytest module path
            cmd = ["python", "-m", "pytest", f"tests/{test_file}", "-v"]
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                cwd=str(self.backend_dir)
            )
            output = result.stdout + result.stderr
            
            # Remove pytest configuration and environment information
            output = re.sub(r"platform.*?python\n", "", output)
            output = re.sub(r"rootdir:.*?\n", "", output)
            output = re.sub(r"plugins:.*?\n", "", output)
            output = re.sub(r"cachedir:.*?\n", "", output)
            output = re.sub(r"configfile:.*?\n", "", output)

            # Parse test results
            passed = len(re.findall(r"PASSED", output))
            failed = len(re.findall(r"FAILED", output))
            errors = len(re.findall(r"ERROR", output))
            
            # Extract execution time
            time_match = re.search(r"in (\d+\.\d+)s", output)
            execution_time = float(time_match.group(1)) if time_match else 0.0

            return output, passed, failed, errors, execution_time
        except Exception as e:
            print(f"Error running tests: {e}")
            return str(e), 0, 0, 0, 0.0

    def parse_performance_metrics(self, output: str) -> Dict:
        """Parse performance metrics from pytest-benchmark output."""
        metrics = {}
        try:
            # Find the benchmark table section
            benchmark_section = re.search(
                r"----------------------.*?benchmark.*?\n(.*?)\n-+\n(.*?)\n-+",
                output,
                re.DOTALL
            )
            
            if benchmark_section:
                # Get the lines containing the actual benchmark data
                data_lines = benchmark_section.group(2).strip().split("\n")
                
                for line in data_lines:
                    # Extract the test name (everything before the first number)
                    name_match = re.match(r"([^\d]+?)\s+\d", line)
                    if name_match:
                        name = name_match.group(1).strip()
                        
                        # Extract the numeric values using regex
                        # Looking for patterns like: 743.0409 (1.0)
                        numbers = re.findall(r"([\d,]+\.?\d*)\s+\([^)]+\)", line)
                        if len(numbers) >= 4:  # We need at least min, max, mean, and ops
                            metrics[name] = {
                                "min_us": float(numbers[0].replace(",", "")),
                                "max_us": float(numbers[1].replace(",", "")),
                                "mean_us": float(numbers[2].replace(",", "")),
                                "ops": float(numbers[-2].replace(",", ""))  # OPS is second to last
                            }
        except Exception as e:
            print(f"Error parsing performance metrics: {e}")
        return metrics

    def generate_markdown_report(self, report_data: Dict) -> str:
        """Generate Markdown report content."""
        markdown = f"""# Test Results Report

Generated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}  
Python Version: {sys.version.split()[0]}

## Overall Summary

"""
        # Add overall summary
        total_passed = sum(results['passed'] for results in report_data['results'].values())
        total_failed = sum(results['failed'] for results in report_data['results'].values())
        total_errors = sum(results['errors'] for results in report_data['results'].values())
        total_time = sum(results['execution_time'] for results in report_data['results'].values())

        markdown += f"""🟢 **Passed**: {total_passed}  
🔴 **Failed**: {total_failed}  
🟡 **Errors**: {total_errors}  
⏱ **Total Time**: {total_time:.2f}s

"""

        # Add individual test suite results
        for suite_name, results in report_data['results'].items():
            markdown += f"""## {suite_name.title()} Tests

🟢 **Passed**: {results['passed']}  
🔴 **Failed**: {results['failed']}  
🟡 **Errors**: {results['errors']}  
⏱ **Time**: {results['execution_time']:.2f}s

### Detailed Output
```
{results['output']}
```

"""

            if suite_name == "performance" and "metrics" in results:
                markdown += """### Performance Metrics

| Operation | Min (μs) | Max (μs) | Mean (μs) | OPS |
|-----------|----------|----------|-----------|-----|
"""
                for op, metrics in results["metrics"].items():
                    markdown += f"""| {op} | {metrics['min_us']:.2f} | {metrics['max_us']:.2f} | {metrics['mean_us']:.2f} | {metrics['ops']:.2f} |
"""

            # Add a separator between test suites
            markdown += "---\n\n"

        return markdown

    def generate_report(self) -> None:
        """Generate comprehensive test report."""
        test_suites = {
            "normal": "test_api_normal.py",
            "edge": "test_api_edge_cases.py",
            "performance": "test_api_performance.py"
        }

        report_data = {
            "timestamp": self.timestamp,
            "python_version": sys.version,
            "results": {}
        }

        for suite_name, test_file in test_suites.items():
            print(f"\nRunning {suite_name} tests...")
            output, passed, failed, errors, time = self.run_test_suite(test_file)
            
            report_data["results"][suite_name] = {
                "passed": passed,
                "failed": failed,
                "errors": errors,
                "execution_time": time,
                "output": output
            }

            # Print immediate results
            print(f"✓ Passed: {passed}")
            print(f"✗ Failed: {failed}")
            print(f"! Errors: {errors}")
            print(f"Time: {time:.2f}s")

            if suite_name == "performance":
                metrics = self.parse_performance_metrics(output)
                report_data["results"][suite_name]["metrics"] = metrics

        # Generate and save Markdown report
        markdown_content = self.generate_markdown_report(report_data)
        report_file = self.report_dir / f"test_report_{self.timestamp}.md"
        with open(report_file, 'w') as f:
            f.write(markdown_content)
        print(f"\nMarkdown report saved: {report_file}")

def main():
    """Main function to run test report generation."""
    print("Starting test report generation...")
    generator = TestReportGenerator()
    generator.generate_report()
    print("\nTest report generation completed.")

if __name__ == "__main__":
    main() 