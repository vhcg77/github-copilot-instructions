#!/usr/bin/env python3
"""
Validador específico para la carpeta research_prompts
Analiza el valor, propósito e integración de los prompts de investigación
"""

import json
import os
from pathlib import Path
from typing import Any, Dict, List, Tuple


class ResearchPromptsValidator:
    def __init__(self, project_root: str):
        self.project_root = Path(project_root)
        self.research_prompts_dir = (
            self.project_root / ".github" / "instructions" / "research_prompts"
        )
        self.instructions_dir = self.project_root / ".github" / "instructions"
        self.roles_dir = self.instructions_dir / "roles"
        self.tasks_dir = self.instructions_dir / "tasks"
        self.prompts_dir = self.instructions_dir / "prompts"

        self.report = {
            "timestamp": "",
            "validation_type": "research_prompts_analysis",
            "overall_status": "PENDING",
            "analysis_results": {},
            "integration_assessment": {},
            "value_proposition": {},
            "recommendations": [],
        }

    def validate_structure(self) -> Dict[str, Any]:
        """Valida la estructura de la carpeta research_prompts"""
        results = {"status": "PASS", "checks": [], "issues": []}

        # Verificar existencia de carpetas principales
        if not self.research_prompts_dir.exists():
            results["issues"].append("❌ Carpeta research_prompts no existe")
            results["status"] = "FAIL"
            return results

        results["checks"].append("✅ Carpeta research_prompts existe")

        # Verificar subcarpetas
        roles_research = self.research_prompts_dir / "roles"
        tasks_research = self.research_prompts_dir / "tasks"
        index_file = self.research_prompts_dir / "research_index.json"

        if roles_research.exists():
            results["checks"].append("✅ Subcarpeta roles existe")
        else:
            results["issues"].append("❌ Subcarpeta roles no existe")
            results["status"] = "FAIL"

        if tasks_research.exists():
            results["checks"].append("✅ Subcarpeta tasks existe")
        else:
            results["issues"].append("❌ Subcarpeta tasks no existe")
            results["status"] = "FAIL"

        if index_file.exists():
            results["checks"].append("✅ Archivo research_index.json existe")
        else:
            results["issues"].append("❌ Archivo research_index.json no existe")
            results["status"] = "FAIL"

        return results

    def analyze_index_file(self) -> Dict[str, Any]:
        """Analiza el archivo research_index.json"""
        results = {
            "status": "PASS",
            "content_analysis": {},
            "issues": [],
            "insights": [],
        }

        index_file = self.research_prompts_dir / "research_index.json"

        try:
            with open(index_file, "r", encoding="utf-8") as f:
                index_data = json.load(f)

            # Analizar estructura
            results["content_analysis"]["roles_count"] = len(
                index_data.get("roles", {})
            )
            results["content_analysis"]["tasks_count"] = len(
                index_data.get("tasks", {})
            )
            results["content_analysis"]["combinations_count"] = len(
                index_data.get("combinations", [])
            )

            # Analizar prompts de roles
            roles_analysis = {}
            for role_name, role_data in index_data.get("roles", {}).items():
                roles_analysis[role_name] = {
                    "has_component": "component" in role_data,
                    "has_prompt": "prompt" in role_data,
                    "prompt_length": len(role_data.get("prompt", "")),
                    "mentions_best_practices": "MEJORES PRÁCTICAS"
                    in role_data.get("prompt", ""),
                    "mentions_anti_patterns": "ANTI-PATTERNS"
                    in role_data.get("prompt", ""),
                    "mentions_recommendations": "RECOMENDACIONES"
                    in role_data.get("prompt", ""),
                }

            results["content_analysis"]["roles_analysis"] = roles_analysis

            # Analizar prompts de tareas
            tasks_analysis = {}
            for task_name, task_data in index_data.get("tasks", {}).items():
                tasks_analysis[task_name] = {
                    "has_component": "component" in task_data,
                    "has_prompt": "prompt" in task_data,
                    "prompt_length": len(task_data.get("prompt", "")),
                    "mentions_best_practices": "MEJORES PRÁCTICAS"
                    in task_data.get("prompt", ""),
                    "mentions_anti_patterns": "ANTI-PATTERNS"
                    in task_data.get("prompt", ""),
                    "mentions_recommendations": "RECOMENDACIONES"
                    in task_data.get("prompt", ""),
                }

            results["content_analysis"]["tasks_analysis"] = tasks_analysis

            results["insights"].append(
                f"📊 {results['content_analysis']['roles_count']} roles definidos"
            )
            results["insights"].append(
                f"📊 {results['content_analysis']['tasks_count']} tareas definidas"
            )

        except Exception as e:
            results["issues"].append(f"❌ Error leyendo research_index.json: {str(e)}")
            results["status"] = "FAIL"

        return results

    def analyze_coverage(self) -> Dict[str, Any]:
        """Analiza la cobertura entre research_prompts y las instrucciones principales"""
        results = {
            "status": "PASS",
            "coverage_analysis": {},
            "gaps": [],
            "overlaps": [],
        }

        # Obtener roles de las instrucciones principales
        main_roles = set()
        if self.roles_dir.exists():
            for role_file in self.roles_dir.glob("*.md"):
                role_name = role_file.stem
                main_roles.add(role_name)

        # Obtener tareas de las instrucciones principales
        main_tasks = set()
        if self.tasks_dir.exists():
            for task_file in self.tasks_dir.glob("*.md"):
                task_name = task_file.stem
                main_tasks.add(task_name)

        # Obtener roles de research_prompts
        research_roles = set()
        index_file = self.research_prompts_dir / "research_index.json"
        if index_file.exists():
            try:
                with open(index_file, "r", encoding="utf-8") as f:
                    index_data = json.load(f)
                research_roles = set(index_data.get("roles", {}).keys())
            except:
                pass

        # Obtener tareas de research_prompts
        research_tasks = set()
        if index_file.exists():
            try:
                with open(index_file, "r", encoding="utf-8") as f:
                    index_data = json.load(f)
                research_tasks = set(index_data.get("tasks", {}).keys())
            except:
                pass

        # Análizar cobertura de roles
        roles_coverage = {
            "main_roles": len(main_roles),
            "research_roles": len(research_roles),
            "overlap": len(main_roles.intersection(research_roles)),
            "missing_in_research": list(main_roles - research_roles),
            "extra_in_research": list(research_roles - main_roles),
        }

        # Análizar cobertura de tareas
        tasks_coverage = {
            "main_tasks": len(main_tasks),
            "research_tasks": len(research_tasks),
            "overlap": len(main_tasks.intersection(research_tasks)),
            "missing_in_research": list(main_tasks - research_tasks),
            "extra_in_research": list(research_tasks - main_tasks),
        }

        results["coverage_analysis"]["roles"] = roles_coverage
        results["coverage_analysis"]["tasks"] = tasks_coverage

        # Identificar gaps
        if roles_coverage["missing_in_research"]:
            results["gaps"].append(
                f"🔍 Roles faltantes en research: {', '.join(roles_coverage['missing_in_research'])}"
            )

        if tasks_coverage["missing_in_research"]:
            results["gaps"].append(
                f"🔍 Tareas faltantes en research: {', '.join(tasks_coverage['missing_in_research'])}"
            )

        # Identificar overlaps
        roles_overlap_pct = (
            roles_coverage["overlap"] / max(roles_coverage["main_roles"], 1)
        ) * 100
        tasks_overlap_pct = (
            tasks_coverage["overlap"] / max(tasks_coverage["main_tasks"], 1)
        ) * 100

        results["overlaps"].append(
            f"📊 Cobertura de roles: {roles_overlap_pct:.1f}% ({roles_coverage['overlap']}/{roles_coverage['main_roles']})"
        )
        results["overlaps"].append(
            f"📊 Cobertura de tareas: {tasks_overlap_pct:.1f}% ({tasks_coverage['overlap']}/{tasks_coverage['main_tasks']})"
        )

        return results

    def assess_integration_with_main_system(self) -> Dict[str, Any]:
        """Evalúa cómo se integra research_prompts con el sistema principal"""
        results = {
            "status": "ANALYSIS",
            "integration_points": [],
            "usage_patterns": [],
            "accessibility": {},
            "value_assessment": {},
        }

        # Verificar referencias en archivos principales
        main_copilot_file = self.project_root / ".github" / "copilot-instructions.md"
        references_found = []

        if main_copilot_file.exists():
            try:
                with open(main_copilot_file, "r", encoding="utf-8") as f:
                    content = f.read()
                    if "research_prompts" in content:
                        references_found.append("copilot-instructions.md")
                    if "research" in content.lower():
                        results["integration_points"].append(
                            "🔗 Menciones de 'research' en instrucciones principales"
                        )
            except:
                pass

        # Verificar si hay llamadas o referencias en otros archivos
        for prompt_file in self.prompts_dir.glob("*.md"):
            try:
                with open(prompt_file, "r", encoding="utf-8") as f:
                    content = f.read()
                    if "research_prompts" in content:
                        references_found.append(prompt_file.name)
            except:
                pass

        results["accessibility"]["direct_references"] = references_found
        results["accessibility"]["reference_count"] = len(references_found)

        # Analizar patrones de uso potenciales
        results["usage_patterns"] = [
            "🎯 Investigación dirigida por roles específicos",
            "🎯 Research templates para mejores prácticas",
            "🎯 Anti-patterns y recomendaciones estructuradas",
            "🎯 Prompts de investigación especializados",
        ]

        # Evaluación de valor
        results["value_assessment"] = {
            "purpose": "Provides structured research templates for role and task-specific best practices",
            "strengths": [
                "Comprehensive coverage of roles and tasks",
                "Structured approach to research (best practices, anti-patterns, recommendations)",
                "Consistent format across all research prompts",
                "Specific to project context (GCP, data science, inventory analysis)",
            ],
            "potential_issues": [
                "Not directly integrated into main instruction flow",
                "No apparent usage or invocation mechanism",
                "May be redundant with existing MCP tools integration",
                "Static content that may become outdated",
            ],
        }

        return results

    def generate_recommendations(self) -> List[str]:
        """Genera recomendaciones basadas en el análisis"""
        recommendations = []

        # Recomendaciones de integración
        recommendations.extend(
            [
                "🔧 INTEGRACIÓN: Conectar research_prompts con el sistema principal de instrucciones",
                "🔧 ACTIVACIÓN: Crear mecanismo para invocar research prompts desde roles/tareas",
                "🔧 REFERENCIAS: Añadir referencias a research_prompts en archivos principales",
                "🔧 DOCUMENTACIÓN: Documentar cómo usar los research prompts en la práctica",
            ]
        )

        # Recomendaciones de optimización
        recommendations.extend(
            [
                "⚡ OPTIMIZACIÓN: Evaluar si research_prompts duplica funcionalidad de MCP tools",
                "⚡ CONSOLIDACIÓN: Considerar fusionar con mcp-tools-orchestrator si es redundante",
                "⚡ AUTOMATIZACIÓN: Crear scripts para actualizar research prompts automáticamente",
                "⚡ VALIDACIÓN: Implementar validación de que research prompts están actualizados",
            ]
        )

        # Recomendaciones de valor
        recommendations.extend(
            [
                "💡 VALOR: Usar research_prompts como templates para entrenar/configurar MCP tools",
                "💡 EVOLUCIÓN: Convertir prompts estáticos en prompts dinámicos con MCP",
                "💡 FEEDBACK: Implementar métricas para medir efectividad de research prompts",
                "💡 MANTENIMIENTO: Crear proceso de actualización basado en feedback del equipo",
            ]
        )

        return recommendations

    def run_validation(self) -> Dict[str, Any]:
        """Ejecuta la validación completa"""
        from datetime import datetime

        self.report["timestamp"] = datetime.now().strftime("%Y%m%d_%H%M%S")

        print("🔍 Iniciando análisis de research_prompts...")

        # Validar estructura
        print("\n📁 Validando estructura...")
        structure_results = self.validate_structure()
        self.report["analysis_results"]["structure"] = structure_results

        if structure_results["status"] == "FAIL":
            self.report["overall_status"] = "FAIL"
            return self.report

        # Analizar archivo índice
        print("\n📊 Analizando research_index.json...")
        index_results = self.analyze_index_file()
        self.report["analysis_results"]["index_analysis"] = index_results

        # Analizar cobertura
        print("\n🎯 Analizando cobertura...")
        coverage_results = self.analyze_coverage()
        self.report["analysis_results"]["coverage"] = coverage_results

        # Evaluar integración
        print("\n🔗 Evaluando integración con sistema principal...")
        integration_results = self.assess_integration_with_main_system()
        self.report["integration_assessment"] = integration_results

        # Generar recomendaciones
        print("\n💡 Generando recomendaciones...")
        recommendations = self.generate_recommendations()
        self.report["recommendations"] = recommendations

        # Determinar estado general
        if structure_results["status"] == "PASS" and index_results["status"] == "PASS":
            self.report["overall_status"] = "ANALYSIS_COMPLETE"
        else:
            self.report["overall_status"] = "ISSUES_FOUND"

        return self.report

    def print_report(self):
        """Imprime el reporte de análisis"""
        print("\n" + "=" * 80)
        print("📊 REPORTE DE ANÁLISIS: RESEARCH_PROMPTS")
        print("=" * 80)

        print(f"Estado general: {self.report['overall_status']}")
        print(f"Timestamp: {self.report['timestamp']}")

        # Estructura
        if "structure" in self.report["analysis_results"]:
            structure = self.report["analysis_results"]["structure"]
            print(f"\n📁 ESTRUCTURA: {structure['status']}")
            for check in structure["checks"]:
                print(f"  {check}")
            for issue in structure["issues"]:
                print(f"  {issue}")

        # Análisis del índice
        if "index_analysis" in self.report["analysis_results"]:
            index = self.report["analysis_results"]["index_analysis"]
            print(f"\n📊 ANÁLISIS DEL ÍNDICE:")
            for insight in index.get("insights", []):
                print(f"  {insight}")

            if "content_analysis" in index:
                ca = index["content_analysis"]
                print(f"  📈 Roles analizados: {ca.get('roles_count', 0)}")
                print(f"  📈 Tareas analizadas: {ca.get('tasks_count', 0)}")

        # Cobertura
        if "coverage" in self.report["analysis_results"]:
            coverage = self.report["analysis_results"]["coverage"]
            print(f"\n🎯 COBERTURA:")
            for overlap in coverage.get("overlaps", []):
                print(f"  {overlap}")
            for gap in coverage.get("gaps", []):
                print(f"  {gap}")

        # Integración
        if "integration_assessment" in self.report:
            integration = self.report["integration_assessment"]
            print(f"\n🔗 INTEGRACIÓN:")
            print(
                f"  Referencias directas: {integration['accessibility']['reference_count']}"
            )
            for pattern in integration.get("usage_patterns", []):
                print(f"  {pattern}")

        # Evaluación de valor
        if "value_assessment" in self.report.get("integration_assessment", {}):
            value = self.report["integration_assessment"]["value_assessment"]
            print(f"\n💡 EVALUACIÓN DE VALOR:")
            print(f"  Propósito: {value.get('purpose', 'N/A')}")
            print(f"  Fortalezas: {len(value.get('strengths', []))}")
            print(f"  Problemas potenciales: {len(value.get('potential_issues', []))}")

        # Recomendaciones
        if self.report["recommendations"]:
            print(f"\n🎯 RECOMENDACIONES ({len(self.report['recommendations'])}):")
            for rec in self.report["recommendations"]:
                print(f"  {rec}")

        print("\n" + "=" * 80)

    def save_report(self, filename: str = None):
        """Guarda el reporte en un archivo JSON"""
        if not filename:
            filename = f"research_prompts_analysis_{self.report['timestamp']}.json"

        report_path = self.instructions_dir / filename

        with open(report_path, "w", encoding="utf-8") as f:
            json.dump(self.report, f, indent=2, ensure_ascii=False)

        print(f"\n📄 Reporte guardado en: {report_path}")
        return report_path


def main():
    """Función principal"""
    import sys

    # Determinar directorio del proyecto
    if len(sys.argv) > 1:
        project_root = sys.argv[1]
    else:
        project_root = os.getcwd()

    # Crear y ejecutar validador
    validator = ResearchPromptsValidator(project_root)
    report = validator.run_validation()

    # Mostrar resultados
    validator.print_report()

    # Guardar reporte
    validator.save_report()

    # Código de salida
    if report["overall_status"] in ["ANALYSIS_COMPLETE"]:
        return 0
    else:
        return 1


if __name__ == "__main__":
    exit(main())
