#!/usr/bin/env python3
"""
Research Prompts Auto-Integration Monitor
=========================================

Este script monitorea el uso de GitHub Copilot y sugiere automáticamente
research prompts relevantes basado en el contexto detectado.

Author: GitHub Copilot Integration System
Date: 2025-06-26
"""

import json
import re
from pathlib import Path
from typing import Dict, List, Optional, Tuple


class ResearchPromptsAutoIntegration:
    """Sistema de integración automática de research prompts."""

    def __init__(self, base_path: str = ".github/instructions"):
        """
        Inicializa el sistema de auto-integración.

        Args:
            base_path: Ruta base del sistema de instrucciones
        """
        self.base_path = Path(base_path)
        self.research_path = self.base_path / "research_prompts"

        # Patrones de detección para roles
        self.role_patterns = {
            "data-scientist": [
                r"\b(data scientist|data science|machine learning|ML model|feature engineering)\b",
                r"\b(pandas|sklearn|jupyter|statistical analysis|EDA)\b",
                r"\b(model training|data analysis|visualization)\b",
            ],
            "mlops-engineer": [
                r"\b(mlops|vertex ai|model deployment|ci/cd|pipeline)\b",
                r"\b(docker|kubernetes|monitoring|model registry)\b",
                r"\b(cloud build|terraform|gcp deployment)\b",
            ],
            "data-engineer": [
                r"\b(data engineer|etl|data pipeline|bigquery|dataflow)\b",
                r"\b(data warehouse|data lake|cloud storage|gcs)\b",
                r"\b(apache beam|data processing|batch processing)\b",
            ],
            "cloud-architect": [
                r"\b(cloud architect|gcp architecture|infrastructure|terraform)\b",
                r"\b(cloud functions|cloud run|kubernetes engine)\b",
                r"\b(networking|security|cost optimization)\b",
            ],
            "frontend-developer": [
                r"\b(frontend|react|angular|vue|typescript|javascript)\b",
                r"\b(ui|ux|component|responsive design|css)\b",
                r"\b(web development|browser|dom manipulation)\b",
            ],
        }

        # Patrones de detección para tareas
        self.task_patterns = {
            "code-generation": [
                r"\b(generate code|write function|create class|implement)\b",
                r"\b(function definition|class definition|method)\b",
                r"\b(python code|script|algorithm implementation)\b",
            ],
            "notebook-eda": [
                r"\b(eda|exploratory analysis|data exploration|jupyter notebook)\b",
                r"\b(data visualization|statistical analysis|correlation)\b",
                r"\b(dataset analysis|data profiling|summary statistics)\b",
            ],
            "code-review": [
                r"\b(code review|review code|optimize code|refactor)\b",
                r"\b(code quality|best practices|performance optimization)\b",
                r"\b(security review|code audit|improvement)\b",
            ],
            "test-generation": [
                r"\b(unit test|integration test|pytest|testing)\b",
                r"\b(test case|test coverage|test automation)\b",
                r"\b(mock|assert|test data|validation test)\b",
            ],
            "architecture-design": [
                r"\b(architecture|system design|microservices|design pattern)\b",
                r"\b(scalability|high availability|distributed system)\b",
                r"\b(api design|database design|cloud architecture)\b",
            ],
        }

    def detect_context(self, text: str) -> Tuple[List[str], List[str]]:
        """
        Detecta roles y tareas relevantes en un texto.

        Args:
            text: Texto a analizar

        Returns:
            Tupla con (roles_detectados, tareas_detectadas)
        """
        text_lower = text.lower()
        detected_roles = []
        detected_tasks = []

        # Detectar roles
        for role, patterns in self.role_patterns.items():
            for pattern in patterns:
                if re.search(pattern, text_lower, re.IGNORECASE):
                    if role not in detected_roles:
                        detected_roles.append(role)
                    break

        # Detectar tareas
        for task, patterns in self.task_patterns.items():
            for pattern in patterns:
                if re.search(pattern, text_lower, re.IGNORECASE):
                    if task not in detected_tasks:
                        detected_tasks.append(task)
                    break

        return detected_roles, detected_tasks

    def generate_research_suggestions(
        self, roles: List[str], tasks: List[str]
    ) -> Dict[str, List[str]]:
        """
        Genera sugerencias de research prompts basado en contexto detectado.

        Args:
            roles: Lista de roles detectados
            tasks: Lista de tareas detectadas

        Returns:
            Dictionary con sugerencias organizadas
        """
        suggestions = {
            "role_research": [],
            "task_research": [],
            "combined_prompts": [],
            "mcp_integration": [],
        }

        # Sugerencias por roles
        for role in roles:
            research_file = self.research_path / "roles" / f"{role}_research.md"
            if research_file.exists():
                suggestions["role_research"].append(
                    {
                        "role": role,
                        "prompt": f"@workspace #file:.github/instructions/research_prompts/roles/{role}_research.md",
                        "description": f"Research template for {role.replace('-', ' ').title()} role",
                    }
                )

        # Sugerencias por tareas
        for task in tasks:
            research_file = self.research_path / "tasks" / f"{task}_research.md"
            if research_file.exists():
                suggestions["task_research"].append(
                    {
                        "task": task,
                        "prompt": f"@workspace #file:.github/instructions/research_prompts/tasks/{task}_research.md",
                        "description": f"Research template for {task.replace('-', ' ').title()} task",
                    }
                )

        # Sugerencias combinadas
        if roles and tasks:
            primary_role = roles[0]
            primary_task = tasks[0]
            suggestions["combined_prompts"].append(
                {
                    "type": "combined",
                    "prompt": f"""# Comprehensive research approach
@workspace #file:.github/instructions/research_prompts/roles/{primary_role}_research.md
@workspace #file:.github/instructions/research_prompts/tasks/{primary_task}_research.md

"[Your specific request], use context7\"""",
                    "description": f"Combined research for {primary_role} doing {primary_task}",
                }
            )

        # Sugerencias de integración MCP
        if roles or tasks:
            suggestions["mcp_integration"].append(
                {
                    "type": "context7",
                    "example": '"[Your request], use context7"',
                    "description": "Add context7 for up-to-date library documentation",
                }
            )
            suggestions["mcp_integration"].append(
                {
                    "type": "consult7",
                    "example": "Use Consult7 to analyze existing codebase patterns",
                    "description": "Analyze similar implementations in the project",
                }
            )

        return suggestions

    def create_integration_report(self, input_text: str) -> Dict[str, any]:
        """
        Crea un reporte completo de integración para un texto dado.

        Args:
            input_text: Texto del usuario a analizar

        Returns:
            Reporte de integración con sugerencias
        """
        roles, tasks = self.detect_context(input_text)
        suggestions = self.generate_research_suggestions(roles, tasks)

        report = {
            "timestamp": self._get_timestamp(),
            "input_analysis": {
                "text_length": len(input_text),
                "detected_roles": roles,
                "detected_tasks": tasks,
                "detection_confidence": self._calculate_confidence(
                    input_text, roles, tasks
                ),
            },
            "research_suggestions": suggestions,
            "integration_ready": len(roles) > 0 or len(tasks) > 0,
            "recommended_workflow": self._create_recommended_workflow(roles, tasks),
        }

        return report

    def _calculate_confidence(
        self, text: str, roles: List[str], tasks: List[str]
    ) -> float:
        """Calcula confianza de detección basado en matches."""
        total_matches = 0
        text_lower = text.lower()

        for role in roles:
            for pattern in self.role_patterns.get(role, []):
                total_matches += len(re.findall(pattern, text_lower, re.IGNORECASE))

        for task in tasks:
            for pattern in self.task_patterns.get(task, []):
                total_matches += len(re.findall(pattern, text_lower, re.IGNORECASE))

        # Normalizar por longitud del texto
        words_count = len(text.split())
        if words_count == 0:
            return 0.0

        confidence = min(total_matches / words_count, 1.0)
        return round(confidence, 3)

    def _create_recommended_workflow(
        self, roles: List[str], tasks: List[str]
    ) -> List[str]:
        """Crea workflow recomendado basado en contexto."""
        workflow = []

        if not roles and not tasks:
            workflow.append("No specific context detected - use general best practices")
            return workflow

        if roles:
            primary_role = roles[0]
            workflow.append(
                f"1. Load role research: @workspace #file:.github/instructions/research_prompts/roles/{primary_role}_research.md"
            )

        if tasks:
            primary_task = tasks[0]
            workflow.append(
                f"2. Load task research: @workspace #file:.github/instructions/research_prompts/tasks/{primary_task}_research.md"
            )

        workflow.append(
            "3. Add 'use context7' to your request for current documentation"
        )
        workflow.append("4. Consider using Consult7 for existing pattern analysis")
        workflow.append("5. Apply research insights to your specific implementation")

        return workflow

    def _get_timestamp(self) -> str:
        """Genera timestamp."""
        from datetime import datetime

        return datetime.now().strftime("%Y%m%d_%H%M%S")


def main():
    """Función principal para demostrar el sistema."""
    print("🤖 Research Prompts Auto-Integration Monitor")
    print("=" * 50)

    integrator = ResearchPromptsAutoIntegration()

    # Ejemplos de detección de contexto
    test_cases = [
        {
            "name": "Data Science EDA Request",
            "text": "I need to create a comprehensive EDA notebook for the Gasco inventory dataset using pandas and plotly for visualizations. Include statistical analysis and feature engineering recommendations.",
        },
        {
            "name": "MLOps Deployment Request",
            "text": "Help me implement a Vertex AI model deployment pipeline with monitoring and CI/CD using Cloud Build and Terraform infrastructure.",
        },
        {
            "name": "Code Generation Request",
            "text": "Generate a Python function for data validation that checks for missing values, outliers, and data quality issues in our inventory data.",
        },
        {
            "name": "Mixed Context Request",
            "text": "As a data scientist, I need to generate unit tests for my machine learning model training pipeline and set up code review practices.",
        },
    ]

    print("\n🔍 Testing Context Detection:")
    print("-" * 40)

    for i, test_case in enumerate(test_cases, 1):
        print(f"\n{i}. {test_case['name']}")
        print(f"Input: {test_case['text'][:100]}...")

        report = integrator.create_integration_report(test_case["text"])

        print(f"Detected Roles: {report['input_analysis']['detected_roles']}")
        print(f"Detected Tasks: {report['input_analysis']['detected_tasks']}")
        print(f"Confidence: {report['input_analysis']['detection_confidence']}")
        print(f"Integration Ready: {'✅' if report['integration_ready'] else '❌'}")

        if report["integration_ready"]:
            print("Recommended Workflow:")
            for step in report["recommended_workflow"][:3]:  # Show first 3 steps
                print(f"  {step}")

    # Demostración interactiva
    print(f"\n🎯 Interactive Demo:")
    print("-" * 40)

    while True:
        user_input = input("\nEnter your request (or 'quit' to exit): ")
        if user_input.lower() == "quit":
            break

        if not user_input.strip():
            continue

        report = integrator.create_integration_report(user_input)

        print(f"\n📊 Analysis Results:")
        print(f"Roles: {report['input_analysis']['detected_roles']}")
        print(f"Tasks: {report['input_analysis']['detected_tasks']}")
        print(f"Confidence: {report['input_analysis']['detection_confidence']}")

        if report["integration_ready"]:
            print(f"\n💡 Suggested Research Prompts:")
            suggestions = report["research_suggestions"]

            for role_suggestion in suggestions["role_research"][:1]:
                print(f"Role: {role_suggestion['prompt']}")

            for task_suggestion in suggestions["task_research"][:1]:
                print(f"Task: {task_suggestion['prompt']}")

            if suggestions["combined_prompts"]:
                print(f"\n🔗 Combined Approach:")
                print(suggestions["combined_prompts"][0]["prompt"])
        else:
            print("No specific research prompts detected for this context.")

    print("\n🎉 Demo completed!")


if __name__ == "__main__":
    main()
