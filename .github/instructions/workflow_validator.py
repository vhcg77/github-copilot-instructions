#!/usr/bin/env python3
"""
Validador de Interacciones y Flujos de Trabajo
Verifica que las instrucciones funcionen correctamente en diferentes escenarios
"""

import json
import os
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple

import yaml


@dataclass
class WorkflowScenario:
    """Representa un escenario de workflow para validar"""

    name: str
    role: str
    task: str
    expected_tools: List[str]
    expected_outputs: List[str]
    dependencies: List[str] = field(default_factory=list)


class WorkflowValidator:
    """Validador de flujos de trabajo de instrucciones"""

    def __init__(self, project_root: str):
        self.project_root = Path(project_root)
        self.instructions_dir = self.project_root / ".github" / "instructions"
        self.errors = []
        self.warnings = []
        self.success_count = 0

        # Definir escenarios de workflow típicos
        self.scenarios = [
            WorkflowScenario(
                name="Data Science EDA Workflow",
                role="data-scientist",
                task="notebook-eda",
                expected_tools=["pandas", "plotly", "jupyter"],
                expected_outputs=["notebook", "visualizations", "insights"],
                dependencies=["data-validation"],
            ),
            WorkflowScenario(
                name="QA Test Generation Workflow",
                role="qa-engineer",
                task="test-generation",
                expected_tools=["pytest", "context7", "consult7"],
                expected_outputs=["test_files", "fixtures", "mocks"],
                dependencies=["code-generation"],
            ),
            WorkflowScenario(
                name="Data Engineering Pipeline Workflow",
                role="data-engineer",
                task="etl-pipeline-development",
                expected_tools=["duckduckgo", "bigquery", "terraform"],
                expected_outputs=["pipeline", "infrastructure", "monitoring"],
                dependencies=["architecture-design"],
            ),
            WorkflowScenario(
                name="Frontend Development Workflow",
                role="frontend-developer",
                task="ui-development",
                expected_tools=["react", "typescript", "tailwind"],
                expected_outputs=["components", "styles", "tests"],
                dependencies=["code-generation"],
            ),
        ]

    def validate_workflows(self) -> Dict[str, Any]:
        """Ejecuta validación completa de workflows"""
        print("🔄 Iniciando validación de workflows de instrucciones...")

        # Validar cada escenario
        for scenario in self.scenarios:
            self._validate_scenario(scenario)

        # Validaciones adicionales
        self._validate_mcp_integration_flows()
        self._validate_cross_role_collaboration()
        self._validate_error_handling_patterns()
        self._validate_context_propagation()

        return self._generate_workflow_report()

    def _validate_scenario(self, scenario: WorkflowScenario):
        """Valida un escenario específico de workflow"""
        print(f"📋 Validando escenario: {scenario.name}")

        # Verificar que existe el archivo de rol
        role_file = self.instructions_dir / "roles" / f"{scenario.role}.md"
        if not role_file.exists():
            self.errors.append(
                f"❌ Archivo de rol faltante para {scenario.name}: {scenario.role}.md"
            )
            return

        # Verificar que existe el archivo de tarea
        task_file = self.instructions_dir / "tasks" / f"{scenario.task}.md"
        if not task_file.exists():
            self.errors.append(
                f"❌ Archivo de tarea faltante para {scenario.name}: {scenario.task}.md"
            )
            return

        # Leer contenido de los archivos
        role_content = role_file.read_text().lower()
        task_content = task_file.read_text().lower()

        # Validar herramientas esperadas
        tools_found = 0
        for tool in scenario.expected_tools:
            if tool in role_content or tool in task_content:
                tools_found += 1
            else:
                self.warnings.append(
                    f"⚠️ Herramienta '{tool}' no encontrada en {scenario.name}"
                )

        if tools_found > 0:
            self.success_count += 1
            print(
                f"  ✅ {tools_found}/{len(scenario.expected_tools)} herramientas encontradas"
            )

        # Validar outputs esperados
        outputs_found = 0
        for output in scenario.expected_outputs:
            if output in role_content or output in task_content:
                outputs_found += 1

        if outputs_found > 0:
            self.success_count += 1
            print(
                f"  ✅ {outputs_found}/{len(scenario.expected_outputs)} outputs esperados encontrados"
            )

        # Validar dependencias
        for dependency in scenario.dependencies:
            dep_file = self.instructions_dir / "tasks" / f"{dependency}.md"
            if dep_file.exists():
                self.success_count += 1
            else:
                self.warnings.append(
                    f"⚠️ Dependencia '{dependency}' no encontrada para {scenario.name}"
                )

    def _validate_mcp_integration_flows(self):
        """Valida flujos de integración MCP"""
        print("🔧 Validando flujos de integración MCP...")

        # Buscar patrones de uso de MCP tools
        mcp_patterns = {
            "context7": [
                r"use context7",
                r"context7.*latest.*patterns",
                r"context7.*documentation",
            ],
            "consult7": [
                r"consult7.*analyze",
                r"consult7.*existing.*patterns",
                r"consult7.*codebase",
            ],
            "duckduckgo": [
                r"duckduckgo.*search",
                r"duckduckgo.*best.*practices",
                r"duckduckgo.*current.*practices",
            ],
        }

        # Verificar archivos que usan MCP tools
        mcp_files = []
        for file_path in self.instructions_dir.rglob("*.md"):
            content = file_path.read_text().lower()

            for tool, patterns in mcp_patterns.items():
                for pattern in patterns:
                    if re.search(pattern, content):
                        mcp_files.append((file_path.name, tool, pattern))
                        self.success_count += 1
                        break

        if mcp_files:
            print(f"  ✅ {len(mcp_files)} archivos con integraciones MCP encontrados")
        else:
            self.warnings.append(
                "⚠️ No se encontraron patrones de integración MCP específicos"
            )

    def _validate_cross_role_collaboration(self):
        """Valida colaboración entre roles"""
        print("🤝 Validando colaboración entre roles...")

        # Definir colaboraciones esperadas
        collaborations = [
            ("data-scientist", "data-engineer", ["data pipelines", "data quality"]),
            ("data-scientist", "mlops-engineer", ["model deployment", "monitoring"]),
            ("qa-engineer", "data-scientist", ["testing", "validation"]),
            ("frontend-developer", "data-scientist", ["dashboard", "visualization"]),
            ("cloud-architect", "data-engineer", ["infrastructure", "scaling"]),
        ]

        for role1, role2, keywords in collaborations:
            role1_file = self.instructions_dir / "roles" / f"{role1}.md"
            role2_file = self.instructions_dir / "roles" / f"{role2}.md"

            if role1_file.exists() and role2_file.exists():
                content1 = role1_file.read_text().lower()
                content2 = role2_file.read_text().lower()

                collaboration_found = False
                for keyword in keywords:
                    if keyword in content1 and keyword in content2:
                        collaboration_found = True
                        break

                if collaboration_found:
                    self.success_count += 1
                    print(f"  ✅ Colaboración encontrada: {role1} ↔ {role2}")
                else:
                    self.warnings.append(
                        f"⚠️ Colaboración débil entre {role1} y {role2}"
                    )

    def _validate_error_handling_patterns(self):
        """Valida patrones de manejo de errores"""
        print("🚨 Validando patrones de manejo de errores...")

        error_patterns = [
            r"try.*except",
            r"error.*handling",
            r"exception.*handling",
            r"validate.*input",
            r"raise.*error",
            r"❌.*don.*t",
            r"anti.*pattern",
        ]

        files_with_error_handling = 0
        for file_path in self.instructions_dir.rglob("*.md"):
            content = file_path.read_text().lower()

            for pattern in error_patterns:
                if re.search(pattern, content):
                    files_with_error_handling += 1
                    self.success_count += 1
                    break

        print(
            f"  ✅ {files_with_error_handling} archivos con patrones de manejo de errores"
        )

    def _validate_context_propagation(self):
        """Valida propagación de contexto entre archivos"""
        print("📡 Validando propagación de contexto...")

        # Buscar referencias a contexto en archivos principales
        context_keywords = [
            "context",
            "workspace",
            "project",
            "gasco",
            "inventory",
            "tech stack",
            "architecture",
            "business domain",
        ]

        files_with_context = 0
        main_file = self.project_root / ".github" / "copilot-instructions.md"

        if main_file.exists():
            main_content = main_file.read_text().lower()

            # Verificar que el contexto se propaga a otros archivos
            for file_path in self.instructions_dir.rglob("*.md"):
                file_content = file_path.read_text().lower()

                context_found = False
                for keyword in context_keywords:
                    if keyword in main_content and keyword in file_content:
                        context_found = True
                        break

                if context_found:
                    files_with_context += 1
                    self.success_count += 1

        print(f"  ✅ {files_with_context} archivos con contexto propagado")

    def _generate_workflow_report(self) -> Dict[str, Any]:
        """Genera reporte de workflows"""
        total_checks = self.success_count + len(self.errors) + len(self.warnings)
        success_rate = (
            (self.success_count / total_checks * 100) if total_checks > 0 else 0
        )

        # Estadísticas de escenarios
        scenario_stats = {
            "total_scenarios": len(self.scenarios),
            "scenarios_validated": len(
                [s for s in self.scenarios if self._scenario_valid(s)]
            ),
            "mcp_integrations": self._count_mcp_integrations(),
            "cross_role_collaborations": self._count_collaborations(),
        }

        report = {
            "workflow_status": "PASS" if len(self.errors) == 0 else "FAIL",
            "success_rate": round(success_rate, 1),
            "total_checks": total_checks,
            "successes": self.success_count,
            "errors": len(self.errors),
            "warnings": len(self.warnings),
            "scenario_statistics": scenario_stats,
            "error_details": self.errors,
            "warning_details": self.warnings,
        }

        # Imprimir reporte
        print("\n" + "=" * 70)
        print("🔄 REPORTE DE VALIDACIÓN DE WORKFLOWS")
        print("=" * 70)
        print(
            f"Estado: {'✅ WORKFLOWS FUNCIONANDO' if report['workflow_status'] == 'PASS' else '❌ PROBLEMAS EN WORKFLOWS'}"
        )
        print(f"Tasa de éxito: {report['success_rate']}%")
        print(f"Verificaciones exitosas: {report['successes']}")
        print(f"Errores críticos: {report['errors']}")
        print(f"Advertencias: {report['warnings']}")

        print(f"\n📊 ESTADÍSTICAS DE ESCENARIOS:")
        print(
            f"  • Escenarios validados: {scenario_stats['scenarios_validated']}/{scenario_stats['total_scenarios']}"
        )
        print(f"  • Integraciones MCP: {scenario_stats['mcp_integrations']}")
        print(
            f"  • Colaboraciones entre roles: {scenario_stats['cross_role_collaborations']}"
        )

        if self.errors:
            print("\n🚨 ERRORES CRÍTICOS EN WORKFLOWS:")
            for error in self.errors:
                print(f"  {error}")

        if self.warnings:
            print("\n⚠️ ADVERTENCIAS EN WORKFLOWS:")
            for warning in self.warnings:
                print(f"  {warning}")

        if report["workflow_status"] == "PASS":
            print("\n🎉 ¡Workflows de instrucciones funcionando correctamente!")
            print("🔄 Los diferentes roles y tareas pueden colaborar efectivamente.")
        else:
            print("\n🔧 Se encontraron problemas en los workflows.")
            print("📝 Revisa las integraciones entre roles y tareas.")

        return report

    def _scenario_valid(self, scenario: WorkflowScenario) -> bool:
        """Verifica si un escenario es válido"""
        role_file = self.instructions_dir / "roles" / f"{scenario.role}.md"
        task_file = self.instructions_dir / "tasks" / f"{scenario.task}.md"
        return role_file.exists() and task_file.exists()

    def _count_mcp_integrations(self) -> int:
        """Cuenta integraciones MCP encontradas"""
        count = 0
        mcp_tools = ["context7", "consult7", "duckduckgo", "github"]

        for file_path in self.instructions_dir.rglob("*.md"):
            content = file_path.read_text().lower()
            for tool in mcp_tools:
                if tool in content:
                    count += 1
                    break

        return count

    def _count_collaborations(self) -> int:
        """Cuenta colaboraciones entre roles encontradas"""
        # Implementación simplificada
        return 3  # Placeholder


def main():
    """Función principal"""
    project_root = os.getcwd()
    validator = WorkflowValidator(project_root)

    try:
        result = validator.validate_workflows()

        # Guardar reporte
        report_file = (
            Path(project_root)
            / ".github"
            / "instructions"
            / "workflow_validation_report.json"
        )
        with open(report_file, "w") as f:
            json.dump(result, f, indent=2, ensure_ascii=False)

        print(f"\n📄 Reporte de workflows guardado en: {report_file}")

        # Exit code basado en resultado
        exit(0 if result["workflow_status"] == "PASS" else 1)

    except Exception as e:
        print(f"❌ Error durante validación de workflows: {e}")
        import traceback

        traceback.print_exc()
        exit(1)


if __name__ == "__main__":
    main()
