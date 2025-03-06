#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Project Validator for "The Yoga Spot" - Part C
This script checks if your project meets the requirements for the third part of the assignment.
"""

import os
import re
import sys
import importlib.util
from pathlib import Path
import ast


class ProjectValidator:
    def __init__(self, project_path="."):
        self.project_path = Path(project_path)
        self.results = {
            "structure": {"status": "Not checked", "details": []},
            "routing": {"status": "Not checked", "details": []},
            "database": {"status": "Not checked", "details": []},
            "forms": {"status": "Not checked", "details": []},
            "templates": {"status": "Not checked", "details": []},
            "readme": {"status": "Not checked", "details": []},
            "requirements": {"status": "Not checked", "details": []},
        }
        self.passed = 0
        self.total = 7  # Total number of categories

    def run_all_checks(self):
        """Run all validation checks"""
        print("Starting project validation...\n")

        self.check_project_structure()
        self.check_routing()
        self.check_database()
        self.check_forms()
        self.check_templates()
        self.check_readme()
        self.check_requirements()

        self.print_summary()

    def check_project_structure(self):
        """Check if the project structure meets the requirements"""
        print("Checking project structure...")
        required_files = ["app.py", "db_connector.py", "requirements.txt"]
        required_dirs = ["static", "templates", "pages"]

        # Check for required files
        for file in required_files:
            if (self.project_path / file).exists():
                self.results["structure"]["details"].append(f"✅ Found required file: {file}")
            else:
                self.results["structure"]["details"].append(f"❌ Missing required file: {file}")

        # Check for required directories
        for directory in required_dirs:
            if (self.project_path / directory).is_dir():
                self.results["structure"]["details"].append(f"✅ Found required directory: {directory}")
            else:
                self.results["structure"]["details"].append(f"❌ Missing required directory: {directory}")

        # Check if pages directory has the required structure
        if (self.project_path / "pages").is_dir():
            page_dirs = [d for d in (self.project_path / "pages").iterdir() if d.is_dir()]
            self.results["structure"]["details"].append(f"📂 Found {len(page_dirs)} page directories inside 'pages/'")

            for page_dir in page_dirs:
                has_init = (page_dir / "__init__.py").exists()
                has_py = any(f.suffix == ".py" and f.name != "__init__.py" for f in page_dir.iterdir())
                has_templates = (page_dir / "templates").is_dir()
                has_static = (page_dir / "static").is_dir()

                if has_py and has_templates:
                    self.results["structure"]["details"].append(
                        f"  ✅ {page_dir.name} has Python file(s) and templates directory")
                else:
                    if not has_py:
                        self.results["structure"]["details"].append(f"  ❌ {page_dir.name} missing Python file(s)")
                    if not has_templates:
                        self.results["structure"]["details"].append(f"  ❌ {page_dir.name} missing templates directory")

        # Set overall status
        if "❌" in str(self.results["structure"]["details"]):
            self.results["structure"]["status"] = "❌ Incomplete"
        else:
            self.results["structure"]["status"] = "✅ Complete"
            self.passed += 1

    def check_routing(self):
        """Check if routing is properly configured"""
        print("Checking routing configuration...")

        app_py = self.project_path / "app.py"
        if not app_py.exists():
            self.results["routing"]["status"] = "❌ Failed - app.py not found"
            self.results["routing"]["details"].append("❌ Cannot check routing without app.py")
            return

        # Parse app.py to check for blueprint registrations
        with open(app_py, "r", encoding="utf-8") as f:
            content = f.read()

        # Check for blueprint imports
        blueprint_imports = re.findall(r'from\s+pages\.(\w+)\.(\w+)\s+import\s+(\w+)', content)
        if blueprint_imports:
            self.results["routing"]["details"].append(f"✅ Found {len(blueprint_imports)} blueprint imports")
            for imp in blueprint_imports:
                self.results["routing"]["details"].append(f"  📄 {imp[0]}.{imp[1]} → {imp[2]}")
        else:
            self.results["routing"]["details"].append("❌ No blueprint imports found")

        # Check for blueprint registrations
        blueprint_registrations = re.findall(r'app\.register_blueprint\((\w+)', content)
        if blueprint_registrations:
            self.results["routing"]["details"].append(f"✅ Found {len(blueprint_registrations)} blueprint registrations")
            for reg in blueprint_registrations:
                self.results["routing"]["details"].append(f"  📄 {reg}")
        else:
            self.results["routing"]["details"].append("❌ No blueprint registrations found")

        # Check for searchClasses/search_classes issue
        if "searchClasses" in content and "search_classes" in content:
            self.results["routing"]["details"].append(
                "⚠️ Found both 'searchClasses' and 'search_classes' in app.py - potential naming inconsistency")

        # Check for error handlers
        if "errorhandler" in content:
            self.results["routing"]["details"].append("✅ Found error handler(s)")
        else:
            self.results["routing"]["details"].append("⚠️ No error handlers found")

        # Set overall status
        if "❌" in str(self.results["routing"]["details"]):
            self.results["routing"]["status"] = "❌ Incomplete"
        else:
            self.results["routing"]["status"] = "✅ Complete"
            self.passed += 1

    def check_database(self):
        """Check if database connection and queries are properly implemented"""
        print("Checking database implementation...")

        db_connector = self.project_path / "db_connector.py"
        analyze_db = self.project_path / "analyzeDB.py"

        # Check for db_connector.py
        if not db_connector.exists():
            self.results["database"]["details"].append("❌ db_connector.py not found")
        else:
            self.results["database"]["details"].append("✅ Found db_connector.py")

            # Check db_connector.py content
            with open(db_connector, "r", encoding="utf-8") as f:
                content = f.read()

            # Check for MongoDB connection
            if "MongoClient" in content:
                self.results["database"]["details"].append("✅ Found MongoDB connection setup")
            else:
                self.results["database"]["details"].append("❌ No MongoDB connection found")

            # Count function definitions as potential queries
            func_count = len(re.findall(r'def\s+\w+\(', content))
            self.results["database"]["details"].append(f"📊 Found {func_count} function definitions in db_connector.py")

            # Check for CRUD operations
            crud_checks = {
                "select": ["find", "find_one", "aggregate"],
                "insert": ["insert", "insert_one", "insert_many", "save"],
                "update": ["update", "update_one", "update_many"],
                "delete": ["delete", "remove", "delete_one", "delete_many"]
            }

            crud_found = {}
            for operation, keywords in crud_checks.items():
                found = False
                for keyword in keywords:
                    if keyword in content:
                        found = True
                        break
                crud_found[operation] = found

            for operation, found in crud_found.items():
                if found:
                    self.results["database"]["details"].append(f"✅ Found {operation.upper()} operation(s)")
                else:
                    self.results["database"]["details"].append(f"❌ No {operation.upper()} operation found")

        # Check for analyzeDB.py
        if not analyze_db.exists():
            self.results["database"]["details"].append("❌ analyzeDB.py not found")
        else:
            self.results["database"]["details"].append("✅ Found analyzeDB.py")

            # Check analyzeDB.py content
            with open(analyze_db, "r", encoding="utf-8") as f:
                content = f.read()

            if "print" in content and "find" in content:
                self.results["database"]["details"].append("✅ analyzeDB.py appears to print data from database")
            else:
                self.results["database"]["details"].append("⚠️ analyzeDB.py might not print data from database")

        # Set overall status
        if "❌" in str(self.results["database"]["details"]):
            self.results["database"]["status"] = "❌ Incomplete"
        else:
            self.results["database"]["status"] = "✅ Complete"
            self.passed += 1

    def check_forms(self):
        """Check if forms are properly implemented"""
        print("Checking form implementation...")

        # Look for HTML files that might contain forms
        html_files = []
        for root, _, files in os.walk(self.project_path):
            for file in files:
                if file.endswith(".html"):
                    html_files.append(os.path.join(root, file))

        forms_found = 0
        validation_client = 0
        validation_server = 0

        # Check each HTML file for forms
        for html_file in html_files:
            with open(html_file, "r", encoding="utf-8") as f:
                content = f.read()

            # Count forms
            forms_in_file = content.count("<form")
            if forms_in_file > 0:
                forms_found += forms_in_file
                self.results["forms"]["details"].append(
                    f"📝 Found {forms_in_file} form(s) in {os.path.basename(html_file)}")

                # Check for client-side validation
                if "required" in content or "pattern=" in content or "minlength=" in content:
                    validation_client += 1
                    self.results["forms"]["details"].append(f"  ✅ Client-side validation found")
                else:
                    self.results["forms"]["details"].append(f"  ⚠️ No obvious client-side validation")

                # Check for action attribute
                if 'action="' in content or "action='" in content:
                    self.results["forms"]["details"].append(f"  ✅ Form action attribute found")
                else:
                    self.results["forms"]["details"].append(f"  ❌ No form action attribute found")

        # Check Python files for server-side validation
        py_files = []
        for root, _, files in os.walk(self.project_path):
            for file in files:
                if file.endswith(".py"):
                    py_files.append(os.path.join(root, file))

        # Check for validation in Python files
        for py_file in py_files:
            with open(py_file, "r", encoding="utf-8") as f:
                content = f.read()

            # Simple heuristic for validation: check for form handling and validation patterns
            if "request.form" in content and ("validate" in content or "if not" in content or "errors" in content):
                validation_server += 1
                self.results["forms"]["details"].append(
                    f"✅ Possible server-side validation found in {os.path.basename(py_file)}")

        if forms_found == 0:
            self.results["forms"]["details"].append("❌ No forms found in HTML files")
        else:
            self.results["forms"]["details"].append(f"📊 Total forms found: {forms_found}")
            self.results["forms"]["details"].append(f"📊 Forms with client-side validation: {validation_client}")
            self.results["forms"]["details"].append(f"📊 Files with server-side validation: {validation_server}")

        # Set overall status
        if forms_found > 0 and (validation_client > 0 or validation_server > a0):
            self.results["forms"]["status"] = "✅ Complete"
            self.passed += 1
        else:
            self.results["forms"]["status"] = "❌ Incomplete"

    def check_templates(self):
        """Check if HTML pages are properly converted to Flask templates"""
        print("Checking templates implementation...")

        # Find all HTML files in templates directories
        template_files = []
        for root, _, files in os.walk(self.project_path):
            if "templates" in root:
                for file in files:
                    if file.endswith(".html"):
                        template_files.append(os.path.join(root, file))

        if not template_files:
            self.results["templates"]["details"].append("❌ No template files found")
            self.results["templates"]["status"] = "❌ Incomplete"
            return

        self.results["templates"]["details"].append(f"📊 Found {len(template_files)} template files")

        jinja_features = {
            "extends": 0,
            "block": 0,
            "url_for": 0,
            "if": 0,
            "for": 0,
            "include": 0
        }

        # Check each template file for Jinja features
        for template_file in template_files:
            with open(template_file, "r", encoding="utf-8") as f:
                content = f.read()

            # Count Jinja features
            template_features = []

            if "{% extends" in content:
                jinja_features["extends"] += 1
                template_features.append("extends")

            if "{% block" in content:
                jinja_features["block"] += 1
                template_features.append("block")

            if "url_for" in content:
                jinja_features["url_for"] += 1
                template_features.append("url_for")

            if "{% if" in content:
                jinja_features["if"] += 1
                template_features.append("if")

            if "{% for" in content:
                jinja_features["for"] += 1
                template_features.append("for")

            if "{% include" in content:
                jinja_features["include"] += 1
                template_features.append("include")

            if template_features:
                self.results["templates"]["details"].append(
                    f"✅ {os.path.basename(template_file)}: {', '.join(template_features)}")
            else:
                self.results["templates"]["details"].append(
                    f"⚠️ {os.path.basename(template_file)}: No Jinja features detected")

        # Summarize Jinja features
        self.results["templates"]["details"].append(f"📊 Templates using extends: {jinja_features['extends']}")
        self.results["templates"]["details"].append(f"📊 Templates using blocks: {jinja_features['block']}")
        self.results["templates"]["details"].append(f"📊 Templates using url_for: {jinja_features['url_for']}")
        self.results["templates"]["details"].append(f"📊 Templates using if statements: {jinja_features['if']}")
        self.results["templates"]["details"].append(f"📊 Templates using for loops: {jinja_features['for']}")

        # Check for base.html
        base_html = any(os.path.basename(f) == "base.html" for f in template_files)
        if base_html:
            self.results["templates"]["details"].append("✅ Found base.html template")
        else:
            self.results["templates"]["details"].append("⚠️ No base.html template found")

        # Set overall status
        if jinja_features["extends"] > 0 and jinja_features["block"] > 0 and jinja_features["url_for"] > 0:
            self.results["templates"]["status"] = "✅ Complete"
            self.passed += 1
        else:
            self.results["templates"]["status"] = "❌ Incomplete"

    def check_readme(self):
        """Check if README.md is properly implemented"""
        print("Checking README.md...")

        readme = self.project_path / "README.md"

        if not readme.exists():
            self.results["readme"]["details"].append("❌ README.md not found")
            self.results["readme"]["status"] = "❌ Incomplete"
            return

        self.results["readme"]["details"].append("✅ Found README.md")

        with open(readme, "r", encoding="utf-8") as f:
            content = f.read()

        # Check README content
        sections = {
            "project description": ["about", "description", "overview", "הסבר", "רעיון", "תיאור"],
            "workflow/actions": ["workflow", "actions", "steps", "how to", "usage", "פעולות", "שימוש"],
            "screenshots": ["screenshot", "image", "picture", "img", "תמונ", "צילומ"]
        }

        for section, keywords in sections.items():
            section_found = False
            for keyword in keywords:
                if keyword.lower() in content.lower():
                    section_found = True
                    break

            if section_found:
                self.results["readme"]["details"].append(f"✅ README appears to include '{section}'")
            else:
                self.results["readme"]["details"].append(f"❌ README might be missing '{section}'")

        # Check length
        words = re.findall(r'\w+', content)
        self.results["readme"]["details"].append(f"📊 README contains approximately {len(words)} words")

        if len(words) < 100:
            self.results["readme"]["details"].append("⚠️ README might be too short")

        # Check if README contains images
        if "![" in content or "<img" in content:
            self.results["readme"]["details"].append("✅ README appears to include images")
        else:
            self.results["readme"]["details"].append("⚠️ README might be missing images")

        # Set overall status
        if "❌" in str(self.results["readme"]["details"]):
            self.results["readme"]["status"] = "❌ Incomplete"
        else:
            self.results["readme"]["status"] = "✅ Complete"
            self.passed += 1

    def check_requirements(self):
        """Check if requirements.txt is properly implemented"""
        print("Checking requirements.txt...")

        requirements = self.project_path / "requirements.txt"

        if not requirements.exists():
            self.results["requirements"]["details"].append("❌ requirements.txt not found")
            self.results["requirements"]["status"] = "❌ Incomplete"
            return

        self.results["requirements"]["details"].append("✅ Found requirements.txt")

        with open(requirements, "r", encoding="utf-8") as f:
            content = f.read()

        # Check common requirements
        required_packages = ["flask", "pymongo", "dnspython"]
        packages = []

        for line in content.splitlines():
            if line.strip() and not line.startswith("#"):
                package = line.split("==")[0].split(">=")[0].strip().lower()
                packages.append(package)

        self.results["requirements"]["details"].append(f"📊 Found {len(packages)} packages in requirements.txt")

        for package in required_packages:
            if any(p.lower() == package.lower() for p in packages):
                self.results["requirements"]["details"].append(f"✅ Found required package: {package}")
            else:
                self.results["requirements"]["details"].append(f"❌ Missing required package: {package}")

        # Set overall status
        if all(any(p.lower() == req.lower() for p in packages) for req in required_packages):
            self.results["requirements"]["status"] = "✅ Complete"
            self.passed += 1
        else:
            self.results["requirements"]["status"] = "❌ Incomplete"

    def print_summary(self):
        """Print summary of validation results"""
        print("\n" + "=" * 50)
        print("PROJECT VALIDATION SUMMARY")
        print("=" * 50)

        for category, result in self.results.items():
            print(f"\n{category.upper()} - {result['status']}")
            for detail in result["details"]:
                print(f"  {detail}")

        print("\n" + "=" * 50)
        print(
            f"OVERALL PROGRESS: {self.passed}/{self.total} categories complete ({int(self.passed / self.total * 100)}%)")
        print("=" * 50)

        if self.passed == self.total:
            print("\n🎉 Congratulations! Your project appears to meet all the requirements!")
        else:
            print("\n⚠️ Your project is not yet complete. Please address the issues above.")


if __name__ == "__main__":
    # Use provided path or current directory
    path = sys.argv[1] if len(sys.argv) > 1 else "."

    validator = ProjectValidator(path)
    validator.run_all_checks()