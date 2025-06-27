#!/usr/bin/env python3
"""
GitHub Copilot Configuration Validator

This script validates that GitHub Copilot is properly configured
with all instruction files and settings, including the new improvements.
"""

import json
import sys
from pathlib import Path
from typing import Dict, List, Tuple, Any


def load_vscode_settings() -> Dict[str, Any]:
    """Load VS Code settings.json file."""
    settings_path = Path(".vscode/settings.json")
    if not settings_path.exists():
        raise FileNotFoundError("VS Code settings.json not found")

    with open(settings_path, "r", encoding="utf-8") as f:
        content = f.read()
        # Remove comments for JSON parsing
        lines = content.split("\n")
        clean_lines = []
        for line in lines:
            # Remove line comments
            if "//" in line and not line.strip().startswith('"'):
                line = line.split("//")[0]
            clean_lines.append(line)
        clean_content = "\n".join(clean_lines)
        return json.loads(clean_content)


def check_copilot_config(settings: Dict[str, Any]) -> List[Tuple[str, bool, str]]:
    """Check core Copilot configuration settings."""
    checks = []

    # Check essential settings
    required_settings = {"github.copilot.chat.codeGeneration.useInstructionFiles": True}

    for setting, expected in required_settings.items():
        actual = settings.get(setting)
        is_correct = actual == expected
        message = f"Expected: {expected}, Found: {actual}"
        checks.append((setting, is_correct, message))

    # Check Copilot enable setting with security considerations
    copilot_enable = settings.get("github.copilot.enable", {})

    # It's OK to have exclusions for security files - this is actually good practice
    if isinstance(copilot_enable, dict):
        has_security_exclusions = any(
            pattern in str(copilot_enable)
            for pattern in ["secrets", ".env", "terraform.tfstate", ".key", ".pem"]
        )
        if has_security_exclusions:
            checks.append(
                (
                    "github.copilot.enable (with security exclusions)",
                    True,
                    "Security exclusions detected - this is good practice",
                )
            )
        else:
            checks.append(
                ("github.copilot.enable", True, f"Configuration: {copilot_enable}")
            )
    else:
        checks.append(
            (
                "github.copilot.enable",
                copilot_enable is True,
                f"Expected: dict or True, Found: {copilot_enable}",
            )
        )

    return checks


def check_instruction_files(settings: Dict[str, Any]) -> List[Tuple[str, bool, str]]:
    """Check that instruction files exist and are referenced."""
    checks = []

    # Check main instruction file
    main_instruction = Path(".github/copilot-instructions.md")
    checks.append(
        (
            "Main instruction file",
            main_instruction.exists(),
            f"File exists: {main_instruction.exists()}",
        )
    )

    # Check task instruction files from settings
    task_instructions = settings.get(
        "github.copilot.chat.codeGeneration.instructions", []
    )
    for instruction in task_instructions:
        if isinstance(instruction, dict) and "file" in instruction:
            file_path = Path(instruction["file"])
            file_exists = file_path.exists()
            checks.append(
                (
                    f"Task instruction: {instruction['file']}",
                    file_exists,
                    f"File exists: {file_exists}",
                )
            )

    return checks


def check_role_files() -> List[Tuple[str, bool, str]]:
    """Check role instruction files."""
    checks = []

    roles_dir = Path(".github/instructions/roles")
    checks.append(
        (
            "Roles directory",
            roles_dir.exists(),
            f"Directory exists: {roles_dir.exists()}",
        )
    )

    expected_roles = ["data-scientist.md", "data-engineer.md", "mlops-engineer.md"]

    for role_file in expected_roles:
        role_path = roles_dir / role_file
        checks.append(
            (
                f"Role file: {role_file}",
                role_path.exists(),
                f"File exists: {role_path.exists()}",
            )
        )

    return checks


def check_task_files() -> List[Tuple[str, bool, str]]:
    """Check task instruction files."""
    checks = []

    tasks_dir = Path(".github/instructions/tasks")

    expected_tasks = [
        "code-generation.md",
        "code-review.md",
        "context-management.md",  # New file we created
    ]

    for task_file in expected_tasks:
        task_path = tasks_dir / task_file
        checks.append(
            (
                f"Task file: {task_file}",
                task_path.exists(),
                f"File exists: {task_path.exists()}",
            )
        )

    # Check if context-management.md has proper content
    context_mgmt_path = tasks_dir / "context-management.md"
    if context_mgmt_path.exists():
        with open(context_mgmt_path, "r", encoding="utf-8") as f:
            content = f.read()
            has_examples = "Example VS Code tabs:" in content
            has_checklists = "Context Validation Checklist" in content
            checks.append(
                (
                    "Context management content quality",
                    has_examples and has_checklists,
                    f"Has examples: {has_examples}, Has checklists: {has_checklists}",
                )
            )

    return checks


def check_prompt_files() -> List[Tuple[str, bool, str]]:
    """Check prompt instruction files."""
    checks = []

    prompts_dir = Path(".github/instructions/prompts")

    expected_prompts = [
        "generate-eda-notebook.prompt.md",
        "create-gcp-architecture.prompt.md",
    ]

    for prompt_file in expected_prompts:
        prompt_path = prompts_dir / prompt_file
        file_exists = prompt_path.exists()
        checks.append(
            (f"Prompt file: {prompt_file}", file_exists, f"File exists: {file_exists}")
        )

        # Check content quality for EDA notebook prompt
        if prompt_file == "generate-eda-notebook.prompt.md" and file_exists:
            with open(prompt_path, "r", encoding="utf-8") as f:
                content = f.read()
                has_code_examples = "```python" in content
                has_context_steps = "Context Management" in content
                has_actionable_steps = (
                    "Step-by-step" in content or "## Steps" in content
                )

                checks.append(
                    (
                        "EDA prompt content quality",
                        has_code_examples
                        and has_context_steps
                        and has_actionable_steps,
                        f"Code examples: {has_code_examples}, Context steps: {has_context_steps}, Actionable: {has_actionable_steps}",
                    )
                )

    return checks


def check_content_improvements() -> List[Tuple[str, bool, str]]:
    """Check that files contain improved content with concrete examples."""
    checks = []

    # Check data scientist role improvements
    ds_role_path = Path(".github/instructions/roles/data-scientist.md")
    if ds_role_path.exists():
        with open(ds_role_path, "r", encoding="utf-8") as f:
            content = f.read()
            has_workflows = "Standard Workflows" in content
            has_code_patterns = "```python" in content
            has_context_integration = "Context Integration" in content

            checks.append(
                (
                    "Data scientist role improvements",
                    has_workflows and has_code_patterns and has_context_integration,
                    f"Workflows: {has_workflows}, Code patterns: {has_code_patterns}, Context: {has_context_integration}",
                )
            )

    # Check code generation task improvements
    code_gen_path = Path(".github/instructions/tasks/code-generation.md")
    if code_gen_path.exists():
        with open(code_gen_path, "r", encoding="utf-8") as f:
            content = f.read()
            has_specific_patterns = "Specific Code Patterns" in content
            has_anti_patterns = "Anti-Patterns" in content
            has_context_mgmt = "Context Management" in content

            checks.append(
                (
                    "Code generation task improvements",
                    has_specific_patterns and has_anti_patterns and has_context_mgmt,
                    f"Patterns: {has_specific_patterns}, Anti-patterns: {has_anti_patterns}, Context: {has_context_mgmt}",
                )
            )

    return checks


def main():
    """Run all validation checks."""
    print("🔍 Validating GitHub Copilot Configuration...")
    print("=" * 60)

    try:
        settings = load_vscode_settings()
        print("✅ VS Code settings loaded successfully")
    except Exception as e:
        print(f"❌ Failed to load VS Code settings: {e}")
        return 1

    all_checks = []
    all_checks.extend(check_copilot_config(settings))
    all_checks.extend(check_instruction_files(settings))
    all_checks.extend(check_role_files())
    all_checks.extend(check_task_files())
    all_checks.extend(check_prompt_files())
    all_checks.extend(check_content_improvements())

    # Print results
    passed = 0
    failed = 0

    for check_name, success, details in all_checks:
        status = "✅" if success else "❌"
        print(f"{status} {check_name}")
        if not success or details != f"File exists: {success}":
            print(f"   {details}")

        if success:
            passed += 1
        else:
            failed += 1

    print("\n" + "=" * 60)
    print(f"📊 Summary: {passed} passed, {failed} failed")

    if failed == 0:
        print("🎉 All checks passed! Copilot is properly configured with improvements.")
        return 0
    else:
        print("⚠️  Some checks failed. Please review the configuration.")
        return 1


if __name__ == "__main__":
    exit_code = main()

    # Handle settings file issues
    if exit_code != 0:
        print("\n🔧 Troubleshooting Tips:")
        print("1. Ensure .vscode/settings.json exists and is valid JSON")
        print("2. Check that instruction files exist in .github/instructions/")
        print(
            "3. Verify github.copilot.chat.codeGeneration.useInstructionFiles is true"
        )
        print("4. Run 'code --install-extension github.copilot' if needed")

    sys.exit(exit_code)
