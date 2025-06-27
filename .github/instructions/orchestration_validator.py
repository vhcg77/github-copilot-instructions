#!/usr/bin/env python3
"""
Comprehensive GitHub Copilot Orchestration Validator

This script validates the complete orchestration of GitHub Copilot configuration
according to best practices and official documentation.
"""

import json
import sys
from pathlib import Path
from typing import Any, Dict, List, Tuple


class CopilotOrchestrationValidator:
    """Validates the complete GitHub Copilot orchestration."""

    def __init__(self):
        self.base_path = Path(".")
        self.github_instructions = self.base_path / ".github" / "instructions"
        self.vscode_settings = self.base_path / ".vscode" / "settings.json"
        self.main_instructions = self.base_path / ".github" / "copilot-instructions.md"

    def validate_directory_structure(self) -> List[Tuple[str, bool, str]]:
        """Validate the directory structure follows best practices."""
        checks = []

        # Core directory structure
        required_dirs = [
            (".github", "GitHub configuration directory"),
            (".github/instructions", "Instructions root directory"),
            (".github/instructions/roles", "Role-specific instructions"),
            (".github/instructions/tasks", "Task-specific instructions"),
            (".github/instructions/prompts", "Prompt files"),
            (".vscode", "VS Code configuration"),
        ]

        for dir_path, description in required_dirs:
            path = self.base_path / dir_path
            checks.append(
                (
                    f"Directory: {dir_path}",
                    path.exists() and path.is_dir(),
                    f"{description} - {'✓' if path.exists() else '✗'}",
                )
            )

        return checks

    def validate_vscode_settings(self) -> List[Tuple[str, bool, str]]:
        """Validate VS Code settings for proper Copilot configuration."""
        checks = []

        if not self.vscode_settings.exists():
            checks.append(("VS Code settings.json", False, "File not found"))
            return checks

        try:
            with open(self.vscode_settings, "r", encoding="utf-8") as f:
                content = f.read()
                # Clean comments
                lines = []
                for line in content.split("\n"):
                    if "//" in line and not line.strip().startswith('"'):
                        line = line.split("//")[0]
                    lines.append(line)
                clean_content = "\n".join(lines)
                settings = json.loads(clean_content)
        except json.JSONDecodeError as e:
            checks.append(("VS Code settings.json", False, f"JSON parsing error: {e}"))
            return checks

        # Essential Copilot settings
        essential_settings = {
            "github.copilot.chat.codeGeneration.useInstructionFiles": (
                True,
                "Must be enabled for instruction files",
            ),
            "chat.promptFiles": (True, "Required for prompt files to work"),
        }

        for setting, (expected, description) in essential_settings.items():
            actual = settings.get(setting)
            is_correct = actual == expected
            checks.append(
                (
                    f"Setting: {setting}",
                    is_correct,
                    f"{description} - Expected: {expected}, Found: {actual}",
                )
            )

        # Check instruction file references
        code_gen_instructions = settings.get(
            "github.copilot.chat.codeGeneration.instructions", []
        )
        if isinstance(code_gen_instructions, list) and len(code_gen_instructions) > 0:
            checks.append(
                (
                    "Code generation instructions configured",
                    True,
                    f"Found {len(code_gen_instructions)} instruction files",
                )
            )

            for instruction in code_gen_instructions:
                if isinstance(instruction, dict) and "file" in instruction:
                    file_path = Path(instruction["file"])
                    checks.append(
                        (
                            f"Instruction file: {instruction['file']}",
                            file_path.exists(),
                            f"Referenced in settings - {'✓' if file_path.exists() else '✗'}",
                        )
                    )
        else:
            checks.append(
                (
                    "Code generation instructions configured",
                    False,
                    "No instruction files configured in settings",
                )
            )

        # Check prompt files configuration
        prompt_locations = settings.get("chat.promptFilesLocations", {})
        expected_locations = [
            ".github/instructions",
            ".github/instructions/prompts",
            ".github/instructions/roles",
            ".github/instructions/tasks",
        ]

        for location in expected_locations:
            is_configured = prompt_locations.get(location, False)
            checks.append(
                (
                    f"Prompt location: {location}",
                    is_configured,
                    f"Configured in settings - {'✓' if is_configured else '✗'}",
                )
            )

        # Check security exclusions
        copilot_enable = settings.get("github.copilot.enable", {})
        if isinstance(copilot_enable, dict):
            security_patterns = ["secrets", ".env", "terraform.tfstate", ".key", ".pem"]
            has_security = any(
                pattern in str(copilot_enable) for pattern in security_patterns
            )
            checks.append(
                (
                    "Security exclusions",
                    has_security,
                    (
                        "Security-sensitive files properly excluded"
                        if has_security
                        else "Consider adding security exclusions"
                    ),
                )
            )

        return checks

    def validate_main_instructions(self) -> List[Tuple[str, bool, str]]:
        """Validate the main instruction file."""
        checks = []

        if not self.main_instructions.exists():
            checks.append(("Main instructions file", False, "File not found"))
            return checks

        with open(self.main_instructions, "r", encoding="utf-8") as f:
            content = f.read()

        # Check for essential sections
        required_sections = [
            ("About Me", "Personal context for Copilot"),
            ("About This Project", "Project-specific context"),
            ("Tech Stack", "Technology stack definition"),
            ("How to Use Specific Instructions", "Instructions hierarchy"),
            ("Automatic Inference System", "Role and task inference"),
            ("Quality Assurance", "Quality standards"),
            ("Critical Anti-Patterns", "What to avoid"),
            ("Configuration Validation", "Setup verification"),
        ]

        for section, description in required_sections:
            has_section = section in content
            checks.append(
                (
                    f"Main instructions - {section}",
                    has_section,
                    f"{description} - {'✓' if has_section else '✗'}",
                )
            )

        # Check for hierarchical references
        hierarchy_refs = [
            ".github/instructions/roles/",
            ".github/instructions/tasks/",
            ".github/instructions/prompts/",
        ]

        for ref in hierarchy_refs:
            has_ref = ref in content
            checks.append(
                (
                    f"Hierarchy reference: {ref}",
                    has_ref,
                    f"Referenced in main instructions - {'✓' if has_ref else '✗'}",
                )
            )

        return checks

    def validate_role_files(self) -> List[Tuple[str, bool, str]]:
        """Validate role instruction files."""
        checks = []

        roles_dir = self.github_instructions / "roles"
        if not roles_dir.exists():
            checks.append(("Roles directory", False, "Directory not found"))
            return checks

        # Expected role files based on the main instructions
        expected_roles = [
            "data-scientist.md",
            "data-engineer.md",
            "mlops-engineer.md",
            "cloud-architect.md",
            "frontend-developer.md",
            "qa-engineer.md",
            "business-analyst.md",
            "project-manager.md",
            "visualization-engineer.md",
        ]

        for role_file in expected_roles:
            role_path = roles_dir / role_file
            checks.append(
                (
                    f"Role file: {role_file}",
                    role_path.exists(),
                    f"Role-specific instructions - {'✓' if role_path.exists() else '✗'}",
                )
            )

            # Check content quality for existing files
            if role_path.exists():
                with open(role_path, "r", encoding="utf-8") as f:
                    content = f.read()

                # Check for essential role sections
                essential_sections = [
                    "Tech Stack",
                    "Core Responsibilities",
                    "Key Principles",
                ]
                has_essential = any(
                    section in content for section in essential_sections
                )

                # Check for frontmatter
                has_frontmatter = content.startswith("---")

                # Check for code examples
                has_code_examples = "```" in content

                quality_score = sum([has_essential, has_frontmatter, has_code_examples])
                checks.append(
                    (
                        f"Role quality: {role_file}",
                        quality_score >= 2,
                        f"Quality score: {quality_score}/3 (structure, frontmatter, examples)",
                    )
                )

        return checks

    def validate_task_files(self) -> List[Tuple[str, bool, str]]:
        """Validate task instruction files."""
        checks = []

        tasks_dir = self.github_instructions / "tasks"
        if not tasks_dir.exists():
            checks.append(("Tasks directory", False, "Directory not found"))
            return checks

        # Essential task files
        essential_tasks = [
            "code-generation.md",
            "code-review.md",
            "context-management.md",
            "notebook-eda.md",
            "architecture-design.md",
            "test-generation.md",
        ]

        for task_file in essential_tasks:
            task_path = tasks_dir / task_file
            checks.append(
                (
                    f"Task file: {task_file}",
                    task_path.exists(),
                    f"Task-specific instructions - {'✓' if task_path.exists() else '✗'}",
                )
            )

            # Check content quality
            if task_path.exists():
                with open(task_path, "r", encoding="utf-8") as f:
                    content = f.read()

                # Check for frontmatter
                has_frontmatter = content.startswith("---")

                # Check for actionable content
                actionable_indicators = [
                    "Rules",
                    "Steps",
                    "Examples",
                    "Patterns",
                    "Checklist",
                ]
                has_actionable = any(
                    indicator in content for indicator in actionable_indicators
                )

                # Check for code examples
                has_code_examples = "```" in content

                # Check for anti-patterns
                has_anti_patterns = (
                    "Anti-Pattern" in content or "DON'T" in content or "❌" in content
                )

                quality_score = sum(
                    [
                        has_frontmatter,
                        has_actionable,
                        has_code_examples,
                        has_anti_patterns,
                    ]
                )
                checks.append(
                    (
                        f"Task quality: {task_file}",
                        quality_score >= 3,
                        f"Quality score: {quality_score}/4 (frontmatter, actionable, examples, anti-patterns)",
                    )
                )

        return checks

    def validate_prompt_files(self) -> List[Tuple[str, bool, str]]:
        """Validate prompt files."""
        checks = []

        prompts_dir = self.github_instructions / "prompts"
        if not prompts_dir.exists():
            checks.append(("Prompts directory", False, "Directory not found"))
            return checks

        # Check for .prompt.md files (VS Code prompt files)
        prompt_files = list(prompts_dir.glob("*.prompt.md"))
        checks.append(
            (
                "Prompt files found",
                len(prompt_files) > 0,
                f"Found {len(prompt_files)} .prompt.md files",
            )
        )

        # Essential prompt files
        essential_prompts = [
            "generate-eda-notebook.prompt.md",
            "create-gcp-architecture.prompt.md",
        ]

        for prompt_file in essential_prompts:
            prompt_path = prompts_dir / prompt_file
            checks.append(
                (
                    f"Prompt file: {prompt_file}",
                    prompt_path.exists(),
                    f"Essential prompt file - {'✓' if prompt_path.exists() else '✗'}",
                )
            )

            # Check content quality
            if prompt_path.exists():
                with open(prompt_path, "r", encoding="utf-8") as f:
                    content = f.read()

                # Check for frontmatter
                has_frontmatter = content.startswith("---")

                # Check for step-by-step instructions
                has_steps = "Step" in content or "step" in content

                # Check for code examples
                has_code_examples = "```" in content

                # Check for context management
                has_context = "Context" in content or "context" in content

                quality_score = sum(
                    [has_frontmatter, has_steps, has_code_examples, has_context]
                )
                checks.append(
                    (
                        f"Prompt quality: {prompt_file}",
                        quality_score >= 3,
                        f"Quality score: {quality_score}/4 (frontmatter, steps, examples, context)",
                    )
                )

        return checks

    def validate_orchestration_consistency(self) -> List[Tuple[str, bool, str]]:
        """Validate consistency across the orchestration."""
        checks = []

        # Check if VS Code settings reference existing files
        if self.vscode_settings.exists():
            try:
                with open(self.vscode_settings, "r", encoding="utf-8") as f:
                    content = f.read()
                    # Clean comments
                    lines = []
                    for line in content.split("\n"):
                        if "//" in line and not line.strip().startswith('"'):
                            line = line.split("//")[0]
                        lines.append(line)
                    clean_content = "\n".join(lines)
                    settings = json.loads(clean_content)

                # Check instruction file references
                code_gen_instructions = settings.get(
                    "github.copilot.chat.codeGeneration.instructions", []
                )
                referenced_files = []
                for instruction in code_gen_instructions:
                    if isinstance(instruction, dict) and "file" in instruction:
                        referenced_files.append(instruction["file"])

                # Verify all referenced files exist
                all_exist = all(Path(f).exists() for f in referenced_files)
                checks.append(
                    (
                        "Settings-File consistency",
                        all_exist,
                        (
                            f"All {len(referenced_files)} referenced files exist"
                            if all_exist
                            else "Some referenced files missing"
                        ),
                    )
                )

            except (json.JSONDecodeError, Exception) as e:
                checks.append(
                    ("Settings-File consistency", False, f"Error reading settings: {e}")
                )

        # Check role-task alignment
        roles_dir = self.github_instructions / "roles"
        tasks_dir = self.github_instructions / "tasks"

        if roles_dir.exists() and tasks_dir.exists():
            role_files = list(roles_dir.glob("*.md"))
            task_files = list(tasks_dir.glob("*.md"))

            # Check if main instructions references match actual files
            if self.main_instructions.exists():
                with open(self.main_instructions, "r", encoding="utf-8") as f:
                    main_content = f.read()

                # Check role references
                role_refs_in_main = [
                    f.stem for f in role_files if f.stem in main_content
                ]
                role_coverage = (
                    len(role_refs_in_main) / len(role_files) if role_files else 0
                )

                checks.append(
                    (
                        "Role-Main consistency",
                        role_coverage >= 0.8,
                        f"{len(role_refs_in_main)}/{len(role_files)} roles referenced in main instructions",
                    )
                )

        return checks

    def run_validation(self) -> Dict[str, Any]:
        """Run complete validation and return results."""
        print("🔍 Comprehensive GitHub Copilot Orchestration Validation")
        print("=" * 70)

        all_checks = []

        # Run all validation categories
        validations = [
            ("Directory Structure", self.validate_directory_structure),
            ("VS Code Settings", self.validate_vscode_settings),
            ("Main Instructions", self.validate_main_instructions),
            ("Role Files", self.validate_role_files),
            ("Task Files", self.validate_task_files),
            ("Prompt Files", self.validate_prompt_files),
            ("Orchestration Consistency", self.validate_orchestration_consistency),
        ]

        results = {}
        total_passed = 0
        total_failed = 0

        for category, validator in validations:
            print(f"\n📋 {category}")
            print("-" * 50)

            checks = validator()
            category_passed = 0
            category_failed = 0

            for check_name, success, details in checks:
                status = "✅" if success else "❌"
                print(f"{status} {check_name}")
                if details and (not success or "✓" in details or "✗" in details):
                    print(f"   {details}")

                if success:
                    category_passed += 1
                    total_passed += 1
                else:
                    category_failed += 1
                    total_failed += 1

            results[category] = {
                "passed": category_passed,
                "failed": category_failed,
                "total": len(checks),
            }

            print(f"   📊 {category}: {category_passed}/{len(checks)} passed")

        # Summary
        print("\n" + "=" * 70)
        print(f"📊 FINAL SUMMARY: {total_passed} passed, {total_failed} failed")

        if total_failed == 0:
            print("🎉 Perfect! GitHub Copilot is optimally orchestrated.")
            status = "perfect"
        elif total_failed <= 3:
            print("✅ Good! Minor issues that can be addressed.")
            status = "good"
        elif total_failed <= 6:
            print("⚠️  Moderate issues. Review and fix key problems.")
            status = "moderate"
        else:
            print("❌ Significant issues. Major restructuring needed.")
            status = "poor"

        results["summary"] = {
            "total_passed": total_passed,
            "total_failed": total_failed,
            "status": status,
        }

        return results


def main():
    """Main validation function."""
    validator = CopilotOrchestrationValidator()
    results = validator.run_validation()

    # Exit with appropriate code
    if results["summary"]["status"] in ["perfect", "good"]:
        return 0
    else:
        return 1


if __name__ == "__main__":
    sys.exit(main())
