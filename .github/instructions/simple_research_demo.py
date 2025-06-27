#!/usr/bin/env python3
"""
Simplified Research Prompts Integration Demo
===========================================

Una versión más simple y directa para demostrar la integración
de research prompts con contextos de ejemplo predefinidos.

Author: GitHub Copilot Analysis System
Date: 2025-06-26
"""

import json
from pathlib import Path
from typing import Dict, List, Tuple


class SimpleResearchIntegrationDemo:
    """Demo simplificado de integración de research prompts."""

    def __init__(self):
        """Inicializa el demo con ejemplos predefinidos."""
        self.research_path = Path(".github/instructions/research_prompts")

        # Ejemplos predefinidos para testing rápido
        self.demo_scenarios = {
            "1": {
                "description": "Data Science EDA Analysis",
                "input": "I need to create an exploratory data analysis notebook for the Gasco inventory dataset using pandas and plotly",
                "expected_roles": ["data-scientist"],
                "expected_tasks": ["notebook-eda"],
            },
            "2": {
                "description": "MLOps Model Deployment",
                "input": "Help me implement a Vertex AI model deployment pipeline with monitoring and CI/CD",
                "expected_roles": ["mlops-engineer"],
                "expected_tasks": ["code-generation", "ci-cd-pipelines"],
            },
            "3": {
                "description": "Code Generation for Data Validation",
                "input": "Generate a Python function for data validation that checks missing values and outliers",
                "expected_roles": ["data-scientist", "data-engineer"],
                "expected_tasks": ["code-generation", "data-validation"],
            },
            "4": {
                "description": "Architecture Design for GCP",
                "input": "Design a scalable architecture for real-time data processing using BigQuery and Cloud Functions",
                "expected_roles": ["cloud-architect", "data-engineer"],
                "expected_tasks": ["architecture-design", "etl-pipeline-development"],
            },
            "5": {
                "description": "Test Generation for ML Models",
                "input": "Create unit tests for my machine learning model training pipeline including validation tests",
                "expected_roles": ["data-scientist", "qa-engineer"],
                "expected_tasks": ["test-generation", "data-validation"],
            },
        }

        # Patrones simples para detección
        self.simple_patterns = {
            "roles": {
                "data-scientist": [
                    "data scientist",
                    "eda",
                    "analysis",
                    "modeling",
                    "pandas",
                    "plotly",
                    "statistics",
                    "machine learning",
                ],
                "data-engineer": [
                    "data engineer",
                    "etl",
                    "pipeline",
                    "bigquery",
                    "sql",
                    "data processing",
                ],
                "mlops-engineer": [
                    "mlops",
                    "deployment",
                    "vertex ai",
                    "ci/cd",
                    "monitoring",
                    "production",
                ],
                "cloud-architect": [
                    "architecture",
                    "gcp",
                    "cloud",
                    "scalable",
                    "design",
                    "infrastructure",
                ],
                "qa-engineer": ["test", "testing", "qa", "unit test", "validation"],
                "frontend-developer": [
                    "frontend",
                    "ui",
                    "dashboard",
                    "react",
                    "javascript",
                ],
            },
            "tasks": {
                "code-generation": [
                    "generate",
                    "create",
                    "write",
                    "implement",
                    "function",
                    "code",
                ],
                "notebook-eda": [
                    "notebook",
                    "eda",
                    "exploratory",
                    "analysis",
                    "jupyter",
                ],
                "test-generation": ["test", "testing", "unit test", "pytest"],
                "data-validation": ["validation", "validate", "check", "quality"],
                "architecture-design": ["architecture", "design", "system", "scalable"],
                "ci-cd-pipelines": ["ci/cd", "pipeline", "deployment", "automation"],
            },
        }

    def detect_simple_context(self, text: str) -> Dict[str, any]:
        """
        Detección simple de contexto basada en palabras clave.

        Args:
            text: Texto a analizar

        Returns:
            Dictionary con roles, tareas y confianza detectados
        """
        text_lower = text.lower()
        detected_roles = []
        detected_tasks = []

        # Detectar roles
        for role, keywords in self.simple_patterns["roles"].items():
            matches = sum(1 for keyword in keywords if keyword in text_lower)
            if matches > 0:
                detected_roles.append(role)

        # Detectar tareas
        for task, keywords in self.simple_patterns["tasks"].items():
            matches = sum(1 for keyword in keywords if keyword in text_lower)
            if matches > 0:
                detected_tasks.append(task)

        # Calcular confianza simple
        total_matches = len(detected_roles) + len(detected_tasks)
        confidence = min(
            total_matches * 0.2, 1.0
        )  # Confianza basada en número de matches

        return {
            "roles": detected_roles,
            "tasks": detected_tasks,
            "confidence": confidence,
            "integration_ready": len(detected_roles) > 0 or len(detected_tasks) > 0,
        }

    def generate_integration_commands(
        self, roles: List[str], tasks: List[str]
    ) -> List[str]:
        """
        Genera comandos de integración para los roles y tareas detectados.

        Args:
            roles: Lista de roles detectados
            tasks: Lista de tareas detectadas

        Returns:
            Lista de comandos a ejecutar
        """
        commands = []

        # Comandos para roles
        for role in roles:
            research_file = self.research_path / "roles" / f"{role}_research.md"
            if research_file.exists():
                commands.append(
                    f"@workspace #file:.github/instructions/research_prompts/roles/{role}_research.md"
                )

        # Comandos para tareas
        for task in tasks:
            research_file = self.research_path / "tasks" / f"{task}_research.md"
            if research_file.exists():
                commands.append(
                    f"@workspace #file:.github/instructions/research_prompts/tasks/{task}_research.md"
                )

        return commands

    def show_integration_example(self, scenario_key: str) -> None:
        """
        Muestra un ejemplo completo de integración.

        Args:
            scenario_key: Clave del scenario (1-5)
        """
        if scenario_key not in self.demo_scenarios:
            print(f"❌ Scenario '{scenario_key}' no encontrado. Use 1-5.")
            return

        scenario = self.demo_scenarios[scenario_key]

        print(f"\n🎯 Scenario {scenario_key}: {scenario['description']}")
        print("=" * 60)
        print(f"📝 Input: {scenario['input']}")
        print()

        # Detectar contexto
        context = self.detect_simple_context(scenario["input"])

        print(f"🔍 Detected Context:")
        print(f"   Roles: {context['roles']}")
        print(f"   Tasks: {context['tasks']}")
        print(f"   Confidence: {context['confidence']:.2f}")
        print(f"   Integration Ready: {'✅' if context['integration_ready'] else '❌'}")
        print()

        if context["integration_ready"]:
            # Generar comandos de integración
            commands = self.generate_integration_commands(
                context["roles"], context["tasks"]
            )

            print("🚀 Integration Commands:")
            for i, command in enumerate(commands, 1):
                print(f"   {i}. {command}")
            print()

            print("💡 Complete Integration Example:")
            print("```markdown")
            for command in commands:
                print(command)
            print()
            print(f'"{scenario["input"]}, use context7"')
            print("```")
            print()

            print("📋 What this provides:")
            for role in context["roles"]:
                print(
                    f"   ✅ {role.replace('-', ' ').title()} best practices and anti-patterns"
                )
            for task in context["tasks"]:
                print(f"   ✅ {task.replace('-', ' ').title()} optimization guidelines")
            print("   ✅ Context7 integration for up-to-date documentation")
        else:
            print("❌ No sufficient context detected for integration")

    def run_interactive_demo(self) -> None:
        """Ejecuta el demo interactivo."""
        print("🎯 Simple Research Prompts Integration Demo")
        print("=" * 50)
        print()
        print("Available scenarios:")
        for key, scenario in self.demo_scenarios.items():
            print(f"  {key}. {scenario['description']}")
        print("  'custom' - Enter your own text")
        print("  'all' - Show all scenarios")
        print("  'quit' - Exit")
        print()

        while True:
            choice = (
                input("Select scenario (1-5, 'custom', 'all', 'quit'): ")
                .strip()
                .lower()
            )

            if choice == "quit":
                print("👋 Demo finished!")
                break
            elif choice == "all":
                for key in self.demo_scenarios.keys():
                    self.show_integration_example(key)
                    print()
            elif choice == "custom":
                custom_input = input("Enter your custom text: ").strip()
                if custom_input:
                    context = self.detect_simple_context(custom_input)
                    print(f"\n🔍 Analysis Results:")
                    print(f"   Roles: {context['roles']}")
                    print(f"   Tasks: {context['tasks']}")
                    print(f"   Confidence: {context['confidence']:.2f}")

                    if context["integration_ready"]:
                        commands = self.generate_integration_commands(
                            context["roles"], context["tasks"]
                        )
                        print(f"\n🚀 Suggested Commands:")
                        for command in commands:
                            print(f"   {command}")
                    else:
                        print(
                            "   💡 Try including more specific keywords about your task or role"
                        )
                    print()
            elif choice in self.demo_scenarios:
                self.show_integration_example(choice)
            else:
                print(
                    "❌ Invalid choice. Please select 1-5, 'custom', 'all', or 'quit'"
                )
                print()


def main():
    """Función principal."""
    demo = SimpleResearchIntegrationDemo()
    demo.run_interactive_demo()


if __name__ == "__main__":
    main()
