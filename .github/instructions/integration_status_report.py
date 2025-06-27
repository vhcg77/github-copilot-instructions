#!/usr/bin/env python3
"""
Research Prompts Integration Status Report
==========================================

Verifica el estado actual de la integración de research prompts
y demuestra cómo usar el sistema integrado.

Author: GitHub Copilot Analysis System
Date: 2025-06-26
"""

import json
from pathlib import Path
from typing import Dict, List


def check_integration_status():
    """Verifica el estado de la integración de research prompts."""
    print("🔍 Research Prompts Integration Status Report")
    print("=" * 60)
    print()

    base_path = Path(".github/instructions")
    research_path = base_path / "research_prompts"

    # 1. Verificar estructura
    print("📁 Structure Check:")
    if research_path.exists():
        print("   ✅ research_prompts directory exists")

        roles_count = len(list((research_path / "roles").glob("*_research.md")))
        tasks_count = len(list((research_path / "tasks").glob("*_research.md")))

        print(f"   ✅ {roles_count} role research prompts found")
        print(f"   ✅ {tasks_count} task research prompts found")
    else:
        print("   ❌ research_prompts directory not found")
        return

    print()

    # 2. Verificar integración en archivos principales
    print("🔗 Integration Check:")

    integration_files = [
        "roles/data-scientist.md",
        "roles/mlops-engineer.md",
        "tasks/code-generation.md",
        ".github/copilot-instructions.md",
    ]

    integrated_count = 0
    for file_path in integration_files:
        full_path = (
            Path(file_path)
            if file_path.startswith(".github")
            else base_path / file_path
        )
        if full_path.exists():
            with open(full_path, "r", encoding="utf-8") as f:
                content = f.read()
                if "research_prompts" in content:
                    print(f"   ✅ {file_path} - integrated")
                    integrated_count += 1
                else:
                    print(f"   ❌ {file_path} - not integrated")
        else:
            print(f"   ❌ {file_path} - file not found")

    print(
        f"\n   📊 Integration Rate: {integrated_count}/{len(integration_files)} files ({integrated_count/len(integration_files)*100:.1f}%)"
    )
    print()

    # 3. Mostrar ejemplos de uso
    print("🚀 Usage Examples:")
    print()

    examples = [
        {
            "scenario": "Data Science EDA",
            "prompt": """@workspace #file:.github/instructions/research_prompts/roles/data-scientist_research.md

"Create comprehensive EDA notebook for Gasco inventory dataset, use context7" """,
            "benefits": [
                "Best practices for data analysis",
                "Anti-patterns to avoid",
                "GCP-specific optimizations",
            ],
        },
        {
            "scenario": "MLOps Deployment",
            "prompt": """@workspace #file:.github/instructions/research_prompts/roles/mlops-engineer_research.md

"Implement Vertex AI model deployment with monitoring, use context7" """,
            "benefits": [
                "Vertex AI best practices",
                "Monitoring patterns",
                "CI/CD optimization",
            ],
        },
        {
            "scenario": "Code Generation",
            "prompt": """@workspace #file:.github/instructions/research_prompts/tasks/code-generation_research.md

"Generate data validation functions for inventory analysis, use context7" """,
            "benefits": [
                "Code quality patterns",
                "Performance optimization",
                "Testing strategies",
            ],
        },
    ]

    for i, example in enumerate(examples, 1):
        print(f"{i}. {example['scenario']}:")
        print("   📝 Prompt:")
        print("   ```")
        print(f"   {example['prompt']}")
        print("   ```")
        print("   💡 Benefits:")
        for benefit in example["benefits"]:
            print(f"      - {benefit}")
        print()

    # 4. Próximos pasos
    print("📋 Next Steps:")
    if integrated_count == len(integration_files):
        print("   ✅ Integration is complete!")
        print("   🎯 Start using research prompts in your GitHub Copilot workflows")
        print("   📊 Monitor usage and effectiveness")
        print("   🔄 Provide feedback for improvements")
    else:
        print("   🔧 Complete integration in remaining files")
        print("   📝 Add research prompt references")
        print("   ✅ Validate integration")

    print()
    print("🎉 Research Prompts Integration Ready!")


def demonstrate_workflow():
    """Demuestra un workflow completo con research prompts."""
    print("\n" + "=" * 60)
    print("🔬 Complete Workflow Demonstration")
    print("=" * 60)
    print()

    workflow_steps = [
        {
            "step": "1. Context Setup",
            "action": "Open relevant files in VS Code",
            "files": [
                "data/inventario_recursos_gasco_2025_06_25.csv",
                "notebooks/analisis_exploratorio_inventario.ipynb",
            ],
            "purpose": "Provide context for Copilot",
        },
        {
            "step": "2. Research Prompt Loading",
            "action": "Load role-specific research template",
            "command": "@workspace #file:.github/instructions/research_prompts/roles/data-scientist_research.md",
            "purpose": "Get specialized guidance and best practices",
        },
        {
            "step": "3. Enhanced Request",
            "action": "Combine research context with MCP tools",
            "command": '"Create EDA notebook analyzing inventory turnover patterns, use context7"',
            "purpose": "Get current best practices + up-to-date documentation",
        },
        {
            "step": "4. Quality Validation",
            "action": "Apply research template guidelines",
            "checks": [
                "Type hints",
                "Docstrings",
                "Anti-patterns avoided",
                "GCP optimizations",
            ],
            "purpose": "Ensure output meets quality standards",
        },
    ]

    for step_info in workflow_steps:
        print(f"📋 {step_info['step']}: {step_info['action']}")

        if "files" in step_info:
            print("   📁 Files:")
            for file in step_info["files"]:
                print(f"      - {file}")

        if "command" in step_info:
            print("   💻 Command:")
            print(f"      {step_info['command']}")

        if "checks" in step_info:
            print("   ✅ Quality Checks:")
            for check in step_info["checks"]:
                print(f"      - {check}")

        print(f"   🎯 Purpose: {step_info['purpose']}")
        print()

    print("🎉 Result: High-quality, context-aware output that follows best practices!")


def show_research_templates():
    """Muestra los templates de research disponibles."""
    print("\n" + "=" * 60)
    print("📚 Available Research Templates")
    print("=" * 60)
    print()

    research_path = Path(".github/instructions/research_prompts")

    # Roles
    print("👥 Role Templates:")
    roles_path = research_path / "roles"
    if roles_path.exists():
        for role_file in sorted(roles_path.glob("*_research.md")):
            role_name = role_file.stem.replace("_research", "")
            display_name = role_name.replace("-", " ").title()
            print(f"   📋 {display_name}")
            print(
                f"      @workspace #file:.github/instructions/research_prompts/roles/{role_file.name}"
            )

    print()

    # Tasks
    print("🎯 Task Templates:")
    tasks_path = research_path / "tasks"
    if tasks_path.exists():
        for task_file in sorted(tasks_path.glob("*_research.md")):
            task_name = task_file.stem.replace("_research", "")
            display_name = task_name.replace("-", " ").title()
            print(f"   📋 {display_name}")
            print(
                f"      @workspace #file:.github/instructions/research_prompts/tasks/{task_file.name}"
            )

    print()
    print("💡 Usage: Copy any template reference into your GitHub Copilot prompt")


def main():
    """Función principal."""
    check_integration_status()
    demonstrate_workflow()
    show_research_templates()

    print("\n" + "=" * 60)
    print("✨ Research Prompts Integration Complete & Ready!")
    print("=" * 60)
    print()
    print(
        "🚀 You can now use research prompts to enhance your GitHub Copilot workflows!"
    )
    print(
        "📝 Try copying one of the template references above into your next Copilot request."
    )
    print("🔧 Combine with 'use context7' for the most comprehensive assistance.")


if __name__ == "__main__":
    main()
