# Security Scanner for Somn Project
# Run: python security_scan.py [--full] [--output REPORT]

import argparse
import json
import os
import sys
from pathlib import Path
from datetime import datetime

# ANSI color codes
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
RESET = '\033[0m'

def print_header(text):
    print(f"\n{BLUE}{'='*60}{RESET}")
    print(f"{BLUE}{text}{RESET}")
    print(f"{BLUE}{'='*60}{RESET}\n")

def print_success(text):
    print(f"{GREEN}✓ {text}{RESET}")

def print_warning(text):
    print(f"{YELLOW}⚠ {text}{RESET}")

def print_error(text):
    print(f"{RED}✗ {text}{RESET}")

def scan_hardcoded_secrets(path: str) -> list:
    """Scan for hardcoded secrets, API keys, passwords."""
    print_header("Scanning for Hardcoded Secrets")

    patterns = [
        ('password = "', 'Hardcoded password'),
        ('api_key = "', 'Hardcoded API key'),
        ('secret = "', 'Hardcoded secret'),
        ('token = "', 'Hardcoded token'),
        ('aws_access', 'AWS credentials'),
        ('-----BEGIN RSA PRIVATE KEY-----', 'Private key'),
    ]

    findings = []
    project_root = Path(path)

    for py_file in project_root.rglob('*.py'):
        if 'test' in str(py_file):
            continue

        try:
            with open(py_file, 'r', encoding='utf-8') as f:
                for i, line in enumerate(f, 1):
                    for pattern, desc in patterns:
                        if pattern in line and not line.strip().startswith('#'):
                            findings.append({
                                'file': str(py_file.relative_to(project_root)),
                                'line': i,
                                'issue': desc,
                                'severity': 'HIGH'
                            })
                            print_warning(f"{py_file.name}:{i} - {desc}")
        except Exception:
            pass

    print_success(f"Found {len(findings)} potential hardcoded secrets")
    return findings

def scan_sql_injection(path: str) -> list:
    """Scan for SQL injection vulnerabilities."""
    print_header("Scanning for SQL Injection Patterns")

    patterns = [
        (r'execute\([^)]*\+[^)]*\)', 'String concatenation in execute()'),
        (r'cursor\.execute\([^)]*%s[^)]*\+', 'Potential SQL injection'),
    ]

    findings = []
    project_root = Path(path)

    for py_file in project_root.rglob('*.py'):
        try:
            with open(py_file, 'r', encoding='utf-8') as f:
                content = f.read()
                for i, line in enumerate(content.split('\n'), 1):
                    for pattern, desc in patterns:
                        import re
                        if re.search(pattern, line):
                            findings.append({
                                'file': str(py_file.relative_to(project_root)),
                                'line': i,
                                'issue': desc,
                                'severity': 'MEDIUM'
                            })
                            print_warning(f"{py_file.name}:{i} - {desc}")
        except Exception:
            pass

    print_success(f"Found {len(findings)} potential SQL injection patterns")
    return findings

def scan_input_validation(path: str) -> list:
    """Scan for missing input validation."""
    print_header("Scanning for Input Validation")

    findings = []
    project_root = Path(path)

    # Check for eval/exec usage
    for py_file in project_root.rglob('*.py'):
        try:
            with open(py_file, 'r', encoding='utf-8') as f:
                for i, line in enumerate(f, 1):
                    if 'eval(' in line or 'exec(' in line:
                        findings.append({
                            'file': str(py_file.relative_to(project_root)),
                            'line': i,
                            'issue': 'Use of eval/exec - potential code injection',
                            'severity': 'HIGH'
                        })
                        print_error(f"{py_file.name}:{i} - Dangerous eval/exec usage")
        except Exception:
            pass

    print_success(f"Found {len(findings)} input validation issues")
    return findings

def scan_file_operations(path: str) -> list:
    """Scan for unsafe file operations."""
    print_header("Scanning for Unsafe File Operations")

    findings = []
    project_root = Path(path)

    unsafe_patterns = [
        ('os.chmod(', 'Unsafe chmod without mode'),
        ('os.open(', 'Using os.open without flags'),
        ('Path(__file__).parent', 'Path traversal potential'),
    ]

    for py_file in project_root.rglob('*.py'):
        try:
            with open(py_file, 'r', encoding='utf-8') as f:
                for i, line in enumerate(f, 1):
                    for pattern, desc in unsafe_patterns:
                        if pattern in line and not line.strip().startswith('#'):
                            findings.append({
                                'file': str(py_file.relative_to(project_root)),
                                'line': i,
                                'issue': desc,
                                'severity': 'LOW'
                            })
                            print_warning(f"{py_file.name}:{i} - {desc}")
        except Exception:
            pass

    print_success(f"Found {len(findings)} file operation concerns")
    return findings

def scan_dependency_vulnerabilities() -> list:
    """Check for known vulnerable dependencies."""
    print_header("Checking Dependencies")

    findings = []

    # Check if safety is available
    try:
        import subprocess
        result = subprocess.run(
            ['pip', 'list', '--format=freeze'],
            capture_output=True,
            text=True
        )

        packages = result.stdout.strip().split('\n')
        print_success(f"Checking {len(packages)} installed packages...")

        # Basic check for known problematic versions
        known_issues = {
            'django': ('<3.0', 'CVE-2021-44420'),
            'flask': ('<1.0', 'Old Flask version'),
        }

        for package in packages:
            if '==' in package:
                name, version = package.split('==')
                if name.lower() in known_issues:
                    threshold, cve = known_issues[name.lower()]
                    if version < threshold[1:]:
                        findings.append({
                            'package': name,
                            'version': version,
                            'issue': f'Version {version} {threshold} - {cve}',
                            'severity': 'HIGH'
                        })
                        print_error(f"{name}=={version} - {cve}")

    except Exception as e:
        print_warning(f"Could not check dependencies: {e}")

    print_success(f"Found {len(findings)} dependency issues")
    return findings

def generate_report(findings: list, output_path: str):
    """Generate JSON report."""
    report = {
        'timestamp': datetime.now().isoformat(),
        'total_findings': len(findings),
        'by_severity': {
            'HIGH': len([f for f in findings if f.get('severity') == 'HIGH']),
            'MEDIUM': len([f for f in findings if f.get('severity') == 'MEDIUM']),
            'LOW': len([f for f in findings if f.get('severity') == 'LOW']),
        },
        'findings': findings
    }

    with open(output_path, 'w') as f:
        json.dump(report, f, indent=2)

    print(f"\nReport saved to: {output_path}")
    return report

def main():
    parser = argparse.ArgumentParser(description='Security Scanner for Somn')
    parser.add_argument('--path', default='.', help='Project root path')
    parser.add_argument('--output', default='security_report.json', help='Output report path')
    parser.add_argument('--full', action='store_true', help='Run full scan')
    args = parser.parse_args()

    print_header(f"Somn Security Scanner v6.1")
    print(f"Scanning: {args.path}")
    print(f"Time: {datetime.now().isoformat()}")

    all_findings = []

    # Run scans
    all_findings.extend(scan_hardcoded_secrets(args.path))

    if args.full:
        all_findings.extend(scan_sql_injection(args.path))
        all_findings.extend(scan_input_validation(args.path))
        all_findings.extend(scan_file_operations(args.path))
        all_findings.extend(scan_dependency_vulnerabilities())

    # Generate report
    report = generate_report(all_findings, args.output)

    # Summary
    print_header("Scan Summary")
    print(f"Total Findings: {report['total_findings']}")
    print(f"  HIGH:   {report['by_severity']['HIGH']}")
    print(f"  MEDIUM: {report['by_severity']['MEDIUM']}")
    print(f"  LOW:    {report['by_severity']['LOW']}")

    if report['by_severity']['HIGH'] > 0:
        print_error("\n⚠️  HIGH severity issues found! Please review.")
        sys.exit(1)
    else:
        print_success("\n✓ No critical security issues found.")
        sys.exit(0)

if __name__ == '__main__':
    main()
