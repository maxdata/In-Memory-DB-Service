#!/usr/bin/env python3
"""
Test Report Generator for In-Memory Database Service
Runs all test suites and generates XML coverage report for analysis
"""

import subprocess
import sys
import re
import os
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Tuple
import xml.etree.ElementTree as ET
import platform
import shutil

class TestReportGenerator:
    def __init__(self):
        self.report_dir = Path(__file__).parent / "test_reports"
        self.report_dir.mkdir(exist_ok=True)
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.backend_dir = Path(__file__).parent.parent
        self.coverage_data = {}
        self.reuse_coverage = os.environ.get('REUSE_COVERAGE') == '1'
        self.coverage_xml = self.report_dir / "coverage.xml"
        
        # Clear coverage data at start unless reusing
        if not self.reuse_coverage and self.coverage_xml.exists():
            self.coverage_xml.unlink()

    def run_test_suite(self, test_file: str) -> Tuple[str, int, int, int, float]:
        """Run a test suite and return its output and statistics."""
        try:
            # Use pytest with coverage only if not reusing existing coverage
            cmd = ["python", "-m", "pytest", f"tests/test_src/{test_file}", "-v"]
            
            if not self.reuse_coverage:
                cmd.extend([
                    "--cov=app",
                    "--cov-append",
                    f"--cov-report=xml:{self.coverage_xml}",
                    "--cov-report=term-missing",
                    "--no-cov-on-fail"
                ])
            
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                cwd=str(self.backend_dir)
            )
            output = result.stdout + result.stderr
            
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

    def parse_coverage_data(self):
        """Parse coverage data from coverage.xml file."""
        if not self.coverage_xml.exists():
            return None

        try:
            tree = ET.parse(self.coverage_xml)
            root = tree.getroot()
            
            coverage_data = {}
            total_statements = 0
            total_missing = 0
            
            # Parse each class (file) coverage data
            for package in root.findall('.//package'):
                for class_elem in package.findall('.//class'):
                    filename = class_elem.get('filename')
                    if not filename:
                        continue
                        
                    # Get line counts
                    statements = 0
                    missing = 0
                    
                    # Count lines
                    for line in class_elem.findall('.//line'):
                        if line.get('hits') == '0':
                            missing += 1
                        statements += 1
                    
                    if statements > 0:
                        coverage = ((statements - missing) / statements * 100)
                    else:
                        coverage = 0.0
                        
                    coverage_data[filename] = {
                        'statements': statements,
                        'missing': missing,
                        'coverage': coverage
                    }
                    
                    total_statements += statements
                    total_missing += missing
            
            # Calculate total coverage
            if total_statements > 0:
                total_coverage = ((total_statements - total_missing) / total_statements * 100)
            else:
                total_coverage = 0.0
                
            coverage_data['total'] = {
                'statements': total_statements,
                'missing': total_missing,
                'coverage': total_coverage
            }
            
            return coverage_data
            
        except Exception as e:
            print(f"Error parsing coverage data: {e}")
            return None

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
        now = datetime.now()
        markdown_content = [
            "# Test Results Report\n",
            f"Generated: {now.strftime('%Y-%m-%d %H:%M:%S')}  \n",
            f"Python Version: {platform.python_version()}\n"
        ]

        # Calculate totals
        total_passed = sum(results['passed'] for results in report_data['results'].values())
        total_failed = sum(results['failed'] for results in report_data['results'].values())
        total_errors = sum(results['errors'] for results in report_data['results'].values())
        total_time = sum(results['execution_time'] for results in report_data['results'].values())

        # Test category descriptions
        category_descriptions = {
            "config": "Configuration and environment setup tests",
            "models": "Data model validation and schema tests",
            "utils": "Utility function and helper method tests",
            "database": "In-memory database operations and data persistence tests",
            "api_main": "Core API functionality and endpoint tests",
            "api_utils": "API utility functions and middleware tests",
            "services": "Business logic and service layer tests",
            "normal": "Standard use case and happy path tests",
            "edge": "Edge cases, error handling, and boundary condition tests",
            "performance": "Performance benchmarks and load testing"
        }

        # Add overall summary section in a compact format
        overall_summary = (
            "## Overall Summary\n"
            f"### Total Results\n"
            f"🟢 **Total Passed**: {total_passed}  \n"
            f"🔴 **Total Failed**: {total_failed}  \n"
            f"🟡 **Total Errors**: {total_errors}  \n"
            f"⏱️ **Total Time**: {total_time:.2f}s\n\n"
            f"### Results by Category\n"
            "| Category | Description | Passed | Failed | Errors | Time (s) |\n"
            "|----------|-------------|--------:|--------:|--------:|---------:|\n"
        )
        
        # Add results for each test category in a table format
        for suite_name, results in report_data['results'].items():
            description = category_descriptions.get(suite_name, "Additional tests")
            overall_summary += (
                f"| **{suite_name.replace('_', ' ').title()}** | "
                f"{description} | "
                f"✓ {results['passed']} | "
                f"✗ {results['failed']} | "
                f"! {results['errors']} | "
                f"{results['execution_time']:.2f} |\n"
            )
        
        markdown_content.append(overall_summary)

        # Add coverage summary if available
        coverage_data = self.parse_coverage_data()
        if coverage_data:
            total_cov = coverage_data.get('total', {})
            markdown_content.append(f"""## Coverage Summary
📊 **Overall Coverage**: {total_cov.get('coverage', 0):.2f}%  
📝 **Total Statements**: {total_cov.get('statements', 0)}  
❌ **Missing Statements**: {total_cov.get('missing', 0)}

### Coverage by File
| File | Coverage % | Statements | Missing |
|------|------------|------------|---------|""")
            # Add file-specific coverage data in a compact format
            for filename, stats in coverage_data.items():
                if filename != 'total':
                    markdown_content.append(
                        f"| {filename} | {stats['coverage']:.2f}% | {stats['statements']} | {stats['missing']} |"
                    )

            markdown_content.append("\n")

        # Add individual test suite results
        for suite_name, results in report_data['results'].items():
            markdown_content.append(f"""## {suite_name.title()} Tests
🟢 **Passed**: {results['passed']}  
🔴 **Failed**: {results['failed']}  
🟡 **Errors**: {results['errors']}  
⏱ **Time**: {results['execution_time']:.2f}s

### Detailed Output
```
{results['output']}
```
""")

            if suite_name == "performance" and "metrics" in results:
                markdown_content.append("""### Performance Metrics
| Operation | Min (μs) | Max (μs) | Mean (μs) | OPS |
|-----------|----------|----------|-----------|-----|""")
                for op, metrics in results["metrics"].items():
                    markdown_content.append(
                        f"| {op} | {metrics['min_us']:.2f} | {metrics['max_us']:.2f} | {metrics['mean_us']:.2f} | {metrics['ops']:.2f} |"
                    )

            # Add a separator between test suites
            markdown_content.append("\n---\n")

        return "\n".join(markdown_content)

    def generate_report(self) -> None:
        """Generate comprehensive test report."""
        print("Starting test report generation...")
        
        if not self.reuse_coverage:
            print("Generating fresh coverage data...")
        else:
            print("Reusing existing coverage data...")
        
        # Define test suites to run
        test_suites = {
            "config": "test_config.py",
            "models": "test_models.py",
            "utils": "test_utils.py",
            "database": "test_db.py",
            "api_main": "test_api_main.py",
            "api_utils": "test_api_utils.py",
            "services": "test_services.py",
            "normal": "test_api_normal.py",
            "edge": "test_api_edge_cases.py",
            "performance": "test_api_performance.py"
        }
        
        results = {}
        
        # Run each test suite
        for suite_name, test_file in test_suites.items():
            print(f"\nRunning {suite_name} tests...")
            output, passed, failed, errors, execution_time = self.run_test_suite(test_file)
            
            results[suite_name] = {
                'output': output,
                'passed': passed,
                'failed': failed,
                'errors': errors,
                'execution_time': execution_time
            }
            
            # Print summary for this suite
            print(f"✓ Passed: {passed}")
            print(f"✗ Failed: {failed}")
            print(f"! Errors: {errors}")
            print(f"Time: {execution_time:.2f}s")
            
            # Add performance metrics if available
            if suite_name == "performance":
                results[suite_name]['metrics'] = self.parse_performance_metrics(output)
        
        # Generate markdown report
        report_data = {'results': results}
        markdown_content = self.generate_markdown_report(report_data)
        
        # Save markdown report
        report_file = self.report_dir / f"test_report_{self.timestamp}.md"
        report_file.write_text(markdown_content)
        
        # Print final summary
        print("\nTest report generation completed.")
        print(f"\nReports available at:")
        print(f"- Markdown Report: {report_file}")
        print(f"- XML Coverage: {self.coverage_xml}")

def main():
    """Main entry point."""
    generator = TestReportGenerator()
    generator.generate_report()

if __name__ == "__main__":
    main() 