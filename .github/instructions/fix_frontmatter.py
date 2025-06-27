#!/usr/bin/env python3
"""
Script to standardize frontmatter in GitHub Copilot instruction files
"""

import os
import re
from pathlib import Path


def update_prompt_frontmatter():
    """Update frontmatter in prompt files to follow standard pattern."""

    # Define mappings for each file
    prompt_configs = {
        "mlops-engineer-prompts.md": {
            "applyTo": ["mlops", "deployment", "monitoring", "vertex-ai"],
            "role": "mlops-engineer",
            "description": "Prompt examples for MLOps Engineer role with Vertex AI and deployment",
            "priority": "high",
        },
        "project-manager-prompts.md": {
            "applyTo": ["project-management", "planning", "coordination"],
            "role": "project-manager",
            "description": "Prompt examples for Project Manager role",
            "priority": "medium",
        },
        "qa-engineer-prompts.md": {
            "applyTo": ["testing", "quality-assurance", "validation"],
            "role": "qa-engineer",
            "description": "Prompt examples for QA Engineer role",
            "priority": "high",
        },
        "visualization-engineer-prompts.md": {
            "applyTo": ["visualization", "dashboards", "analytics"],
            "role": "visualization-engineer",
            "description": "Prompt examples for Visualization Engineer role",
            "priority": "high",
        },
        "business-analyst-prompts.md": {
            "applyTo": ["business-analysis", "requirements", "documentation"],
            "role": "business-analyst",
            "description": "Prompt examples for Business Analyst role",
            "priority": "medium",
        },
    }

    # Task-specific prompts
    task_configs = {
        "notebook-eda-prompts.md": {
            "applyTo": ["eda", "notebooks", "analysis"],
            "task": "notebook-eda",
            "description": "Prompt examples for EDA notebook tasks",
            "priority": "high",
        },
        "test-generation-prompts.md": {
            "applyTo": ["testing", "unit-tests", "validation"],
            "task": "test-generation",
            "description": "Prompt examples for test generation tasks",
            "priority": "high",
        },
        "pull-request-prompts.md": {
            "applyTo": ["pull-request", "code-review", "collaboration"],
            "task": "pull-request",
            "description": "Prompt examples for pull request tasks",
            "priority": "medium",
        },
    }

    prompts_dir = Path(".github/instructions/prompts")
    tasks_dir = prompts_dir / "tasks"

    # Update role-based prompts
    for filename, config in prompt_configs.items():
        file_path = prompts_dir / filename
        if file_path.exists():
            update_file_frontmatter(file_path, config)
            print(f"✅ Updated {filename}")

    # Update task-based prompts
    for filename, config in task_configs.items():
        file_path = tasks_dir / filename
        if file_path.exists():
            update_file_frontmatter(file_path, config)
            print(f"✅ Updated tasks/{filename}")


def update_file_frontmatter(file_path: Path, config: dict):
    """Update frontmatter in a single file."""

    with open(file_path, "r") as f:
        content = f.read()

    # Extract existing tags if present
    existing_tags = []
    if "tags:" in content:
        tags_match = re.search(r"tags:\s*\[(.*?)\]", content, re.DOTALL)
        if tags_match:
            tags_str = tags_match.group(1)
            existing_tags = [tag.strip().strip('"') for tag in tags_str.split(",")]

    # Build new frontmatter
    frontmatter_lines = ["---"]

    if "applyTo" in config:
        apply_to_str = ", ".join([f'"{item}"' for item in config["applyTo"]])
        frontmatter_lines.append(f"applyTo: [{apply_to_str}]")

    if "role" in config:
        frontmatter_lines.append(f'role: "{config["role"]}"')

    if "task" in config:
        frontmatter_lines.append(f'task: "{config["task"]}"')

    frontmatter_lines.append(f'description: "{config["description"]}"')

    if existing_tags:
        tags_str = ", ".join([f'"{tag}"' for tag in existing_tags])
        frontmatter_lines.append(f"tags: [{tags_str}]")

    frontmatter_lines.append(f'priority: "{config["priority"]}"')
    frontmatter_lines.append("---")

    # Replace frontmatter
    new_frontmatter = "\n".join(frontmatter_lines)

    # Remove existing frontmatter
    content_without_frontmatter = re.sub(r"^---.*?---\s*", "", content, flags=re.DOTALL)

    # Write new content
    new_content = new_frontmatter + "\n\n" + content_without_frontmatter

    with open(file_path, "w") as f:
        f.write(new_content)


if __name__ == "__main__":
    update_prompt_frontmatter()
    print("\n🎯 All prompt files updated with standardized frontmatter!")
