#!/usr/bin/env python3
"""
CI/CD Challenge Runner
=======================
Run this script to check your workflow files and see your progress.

Usage:
    python run.py          # Check all workflows
    python run.py --test   # Run tests locally
"""

import subprocess
import sys
import os
import re
from pathlib import Path

# Colors for terminal output
class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    BOLD = '\033[1m'
    END = '\033[0m'

# For Windows compatibility
if sys.platform == 'win32':
    os.system('color')


def print_header():
    """Print the challenge header."""
    print(f"\n{Colors.CYAN}{'='*60}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.CYAN}  🚀 CI/CD Pipeline Challenge{Colors.END}")
    print(f"{Colors.CYAN}{'='*60}{Colors.END}\n")


def load_yaml_content(file_path):
    """Load YAML file content as string."""
    try:
        with open(file_path, 'r') as f:
            return f.read()
    except FileNotFoundError:
        return None


def check_ci_workflow(content):
    """Check CI workflow for required elements."""
    checks = []
    points = 0
    max_points = 25

    if content is None:
        return [("ci.yml exists", False, "File not found")], 0, max_points

    # Check triggers
    has_push = 'push:' in content and ('branches:' in content or 'main' in content)
    has_pr = 'pull_request:' in content
    if has_push and has_pr:
        checks.append(("Triggers configured", True, "push + pull_request"))
        points += 5
    elif has_push or has_pr:
        checks.append(("Triggers configured", False, "Missing push or pull_request trigger"))
        points += 2
    else:
        checks.append(("Triggers configured", False, "No triggers configured"))

    # Check Python setup
    if 'setup-python' in content:
        checks.append(("Python setup", True, "actions/setup-python"))
        points += 5
    else:
        checks.append(("Python setup", False, "Missing setup-python action"))

    # Check dependencies
    if 'pip install' in content and 'requirements.txt' in content:
        checks.append(("Dependencies install", True, "pip install -r requirements.txt"))
        points += 5
    else:
        checks.append(("Dependencies install", False, "Missing pip install"))

    # Check linting
    if 'flake8' in content:
        checks.append(("Linting", True, "flake8 configured"))
        points += 5
    else:
        checks.append(("Linting", False, "Missing flake8"))

    # Check tests
    if 'pytest' in content:
        checks.append(("Tests", True, "pytest configured"))
        points += 5
    else:
        checks.append(("Tests", False, "Missing pytest"))

    return checks, points, max_points


def check_build_workflow(content):
    """Check build workflow for required elements."""
    checks = []
    points = 0
    max_points = 25

    if content is None:
        return [("build.yml exists", False, "File not found")], 0, max_points

    # Check Docker setup
    if 'docker/setup-buildx-action' in content:
        checks.append(("Docker Buildx", True, "Configured"))
        points += 5
    else:
        checks.append(("Docker Buildx", False, "Missing setup-buildx-action"))

    # Check registry login
    if 'docker/login-action' in content:
        checks.append(("Registry login", True, "login-action configured"))
        points += 5
    else:
        checks.append(("Registry login", False, "Missing login-action"))

    # Check ghcr.io
    if 'ghcr.io' in content:
        checks.append(("GitHub Registry", True, "ghcr.io configured"))
        points += 5
    else:
        checks.append(("GitHub Registry", False, "Missing ghcr.io"))

    # Check build-push-action
    if 'docker/build-push-action' in content:
        checks.append(("Build & Push", True, "build-push-action configured"))
        points += 5
    else:
        checks.append(("Build & Push", False, "Missing build-push-action"))

    # Check permissions
    if 'permissions:' in content and 'packages: write' in content:
        checks.append(("Permissions", True, "packages: write"))
        points += 5
    else:
        checks.append(("Permissions", False, "Missing packages: write permission"))

    return checks, points, max_points


def check_deploy_workflow(content):
    """Check deploy workflow for required elements."""
    checks = []
    points = 0
    max_points = 25

    if content is None:
        return [("deploy.yml exists", False, "File not found")], 0, max_points

    # Check staging job
    if 'staging' in content.lower():
        checks.append(("Staging job", True, "Staging deployment configured"))
        points += 5
    else:
        checks.append(("Staging job", False, "Missing staging deployment"))

    # Check production job
    if 'production' in content.lower():
        checks.append(("Production job", True, "Production deployment configured"))
        points += 5
    else:
        checks.append(("Production job", False, "Missing production deployment"))

    # Check environment
    if 'environment:' in content:
        checks.append(("Environments", True, "GitHub environments configured"))
        points += 5
    else:
        checks.append(("Environments", False, "Missing environment configuration"))

    # Check conditional deployment
    if 'if:' in content:
        checks.append(("Conditional deploy", True, "Conditions configured"))
        points += 5
    else:
        checks.append(("Conditional deploy", False, "Missing deployment conditions"))

    # Check release trigger
    if 'release:' in content or "github.event_name == 'release'" in content:
        checks.append(("Release trigger", True, "Production on release"))
        points += 5
    else:
        checks.append(("Release trigger", False, "Missing release trigger"))

    return checks, points, max_points


def check_all_workflows():
    """Check all workflow files."""
    print_header()
    print(f"  {Colors.BOLD}Checking your CI/CD workflows...{Colors.END}\n")

    workflows_dir = Path(__file__).parent / ".github" / "workflows"

    total_points = 0
    max_total = 0

    workflow_checks = [
        ("ci.yml", "CI Pipeline", check_ci_workflow, 25),
        ("build.yml", "Build Pipeline", check_build_workflow, 25),
        ("deploy.yml", "Deploy Pipeline", check_deploy_workflow, 25),
    ]

    for filename, display_name, check_func, max_pts in workflow_checks:
        file_path = workflows_dir / filename
        content = load_yaml_content(file_path)
        checks, points, max_points = check_func(content)

        total_points += points
        max_total += max_points

        # Print results
        status_icon = f"{Colors.GREEN}✅{Colors.END}" if points == max_points else f"{Colors.YELLOW}⏳{Colors.END}"
        print(f"  {status_icon} {Colors.BOLD}{display_name}{Colors.END} ({points}/{max_points} points)")

        for check_name, passed, detail in checks:
            icon = f"{Colors.GREEN}✓{Colors.END}" if passed else f"{Colors.RED}✗{Colors.END}"
            detail_str = f" - {detail}" if detail else ""
            print(f"      {icon} {check_name}{detail_str}")

        print()

    # Add bonus points section
    print(f"  {Colors.BOLD}Bonus Points:{Colors.END}")

    # Check if tests pass locally
    print(f"      ⏳ Branch protection - Configure in GitHub Settings")
    print(f"      ⏳ Secrets management - Configure in GitHub Secrets")
    print()

    # Progress bar
    progress_pct = int((total_points / max_total) * 100) if max_total > 0 else 0
    bar_filled = int(progress_pct / 5)
    bar_empty = 20 - bar_filled

    bar_color = Colors.GREEN if progress_pct >= 80 else Colors.YELLOW
    print(f"  {Colors.BOLD}Score:{Colors.END}")
    print(f"  {bar_color}{'█' * bar_filled}{'░' * bar_empty}{Colors.END} {total_points}/{max_total} points ({progress_pct}%)")

    if progress_pct == 100:
        print(f"\n  {Colors.GREEN}{Colors.BOLD}🎉 All workflows complete!{Colors.END}")
        print(f"  {Colors.CYAN}Push to GitHub and watch your pipelines run!{Colors.END}")
    elif progress_pct >= 80:
        print(f"\n  {Colors.GREEN}Almost there! Check the items marked with ✗{Colors.END}")
    else:
        print(f"\n  {Colors.CYAN}Keep going! See README.md for guidance.{Colors.END}")

    print()
    return progress_pct == 100


def run_tests():
    """Run tests locally."""
    print_header()
    print(f"  {Colors.BOLD}Running tests locally...{Colors.END}\n")

    # Check if pytest is installed
    try:
        import pytest
    except ImportError:
        print(f"  {Colors.RED}❌ pytest not installed{Colors.END}")
        print(f"  {Colors.YELLOW}Run: pip install pytest{Colors.END}\n")
        return

    # Run pytest
    print(f"  {Colors.CYAN}Running: pytest tests/ -v{Colors.END}\n")
    result = subprocess.run(
        [sys.executable, "-m", "pytest", "tests/", "-v"],
        cwd=str(Path(__file__).parent)
    )

    print()
    if result.returncode == 0:
        print(f"  {Colors.GREEN}✅ All tests passed!{Colors.END}")
        print(f"  {Colors.CYAN}Your CI pipeline will also pass these tests.{Colors.END}")
    else:
        print(f"  {Colors.RED}❌ Some tests failed.{Colors.END}")
        print(f"  {Colors.YELLOW}Fix these before pushing - CI will fail!{Colors.END}")
    print()


def main():
    """Main entry point."""
    import argparse

    parser = argparse.ArgumentParser(description="CI/CD Challenge Runner")
    parser.add_argument("--test", action="store_true", help="Run tests locally")

    args = parser.parse_args()

    os.chdir(Path(__file__).parent)

    if args.test:
        run_tests()
    else:
        check_all_workflows()


if __name__ == "__main__":
    main()
