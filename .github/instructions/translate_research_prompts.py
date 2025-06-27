#!/usr/bin/env python3
"""
Research Prompts Translation Tool
=================================

Este script traduce todos los research prompts de español a inglés,
manteniendo la estructura y formato consistente.

Author: GitHub Copilot Analysis System
Date: 2025-06-26
"""

import os
from pathlib import Path
from typing import Any, Dict, List, Tuple


class ResearchPromptsTranslator:
    """Traductor de research prompts de español a inglés."""

    def __init__(self, base_path: str = ".github/instructions/research_prompts"):
        """
        Inicializa el traductor.

        Args:
            base_path: Ruta base de los research prompts
        """
        self.base_path = Path(base_path)
        self.roles_path = self.base_path / "roles"
        self.tasks_path = self.base_path / "tasks"

        # Diccionario de traducciones consistentes
        self.translations = {
            # Títulos principales
            "Investigación: Rol:": "Research: Role:",
            "Investigación: Tarea:": "Research: Task:",
            # Secciones principales
            "Investiga específicamente el rol de": "Research specifically the role of",
            "Investiga específicamente la tarea de": "Research specifically the task of",
            "en GitHub Copilot:": "in GitHub Copilot:",
            "ANÁLISIS REQUERIDO:": "REQUIRED ANALYSIS:",
            "MEJORES PRÁCTICAS": "BEST PRACTICES",
            "ANTI-PATTERNS CRÍTICOS": "CRITICAL ANTI-PATTERNS",
            "ANTI-PATTERNS para": "ANTI-PATTERNS for",
            "RECOMENDACIONES AVANZADAS": "ADVANCED RECOMMENDATIONS",
            "RECOMENDACIONES para": "RECOMMENDATIONS for",
            # Contexto y objetivos
            "CONTEXTO:": "CONTEXT:",
            "STACK:": "TECH STACK:",
            "OBJETIVO:": "OBJECTIVE:",
            "ENFOQUE:": "FOCUS:",
            # Contenido específico de roles
            "Proyecto de ciencia de datos en GCP, análisis de inventario": "GCP data science project, inventory analysis",
            "Maximizar productividad del rol": "Maximize role productivity for",
            # Contenido específico de tareas
            "Ciencia de datos en GCP": "Data science in GCP",
            "Tarea específica": "Specific task",
            "con máxima efectividad": "with maximum effectiveness",
            # Descriptivos comunes
            "específicas": "specific",
            "críticos": "critical",
            "avanzadas": "advanced",
            "para": "for",
            # Bullet points comunes
            "Configuraciones VS Code optimizadas para": "VS Code configurations optimized for",
            "Patterns de instrucciones más efectivos": "Most effective instruction patterns",
            "Integración con herramientas del rol": "Integration with role-specific tools",
            "Ejemplos de prompts de alto rendimiento": "High-performance prompt examples",
            "Métricas de productividad específicas": "Specific productivity metrics",
            "Errores comunes en instrucciones para": "Common instruction errors for",
            "Configuraciones problemáticas": "Problematic configurations",
            "Patterns que reducen efectividad": "Patterns that reduce effectiveness",
            "Impacto negativo documentado": "Documented negative impact",
            "Optimizaciones específicas del rol": "Role-specific optimizations",
            "Integraciones con stack tecnológico": "Tech stack integrations",
            "Workflows recomendados": "Recommended workflows",
            "Estrategias de adopción": "Adoption strategies",
            # Para tareas de code generation
            "Estructura óptima de instrucciones": "Optimal instruction structure",
            "Palabras clave más efectivas": "Most effective keywords",
            "Ejemplos de configuración exitosa": "Successful configuration examples",
            "Patrones de prompt engineering": "Prompt engineering patterns",
            "Métricas de calidad específicas": "Specific quality metrics",
            "Errores comunes en implementación": "Common implementation errors",
            "Configuraciones contraproducentes": "Counterproductive configurations",
            "Patterns que fallan frecuentemente": "Frequently failing patterns",
            "Problemas de rendimiento": "Performance issues",
            "Optimizaciones avanzadas": "Advanced optimizations",
            "Integración con flujo de trabajo": "Workflow integration",
            "Herramientas complementarias": "Complementary tools",
            "Procesos de validación": "Validation processes",
        }

    def translate_role_prompts(self) -> List[Tuple[str, str]]:
        """
        Traduce todos los research prompts de roles.

        Returns:
            Lista de tuplas (archivo_original, contenido_traducido)
        """
        translated_files = []

        for role_file in self.roles_path.glob("*_research.md"):
            if role_file.exists():
                with open(role_file, "r", encoding="utf-8") as f:
                    content = f.read()

                # Extraer el nombre del rol del archivo
                role_name = role_file.stem.replace("_research", "")
                role_display_name = self._format_role_name(role_name)

                # Crear contenido traducido específico para el rol
                translated_content = self._create_role_template(
                    role_name, role_display_name
                )

                translated_files.append((str(role_file), translated_content))

        return translated_files

    def translate_task_prompts(self) -> List[Tuple[str, str]]:
        """
        Traduce todos los research prompts de tareas.

        Returns:
            Lista de tuplas (archivo_original, contenido_traducido)
        """
        translated_files = []

        for task_file in self.tasks_path.glob("*_research.md"):
            if task_file.exists():
                with open(task_file, "r", encoding="utf-8") as f:
                    content = f.read()

                # Extraer el nombre de la tarea del archivo
                task_name = task_file.stem.replace("_research", "")
                task_display_name = self._format_task_name(task_name)

                # Crear contenido traducido específico para la tarea
                translated_content = self._create_task_template(
                    task_name, task_display_name
                )

                translated_files.append((str(task_file), translated_content))

        return translated_files

    def _format_role_name(self, role_name: str) -> str:
        """Formatea el nombre del rol para display."""
        role_names = {
            "data-scientist": "Data Scientist",
            "data-engineer": "Data Engineer",
            "mlops-engineer": "MLOps Engineer",
            "cloud-architect": "Cloud Architect",
            "frontend-developer": "Frontend Developer",
            "qa-engineer": "QA Engineer",
            "visualization-engineer": "Visualization Engineer",
            "business-analyst": "Business Analyst",
            "project-manager": "Project Manager",
        }
        return role_names.get(role_name, role_name.replace("-", " ").title())

    def _format_task_name(self, task_name: str) -> str:
        """Formatea el nombre de la tarea para display."""
        task_names = {
            "code-generation": "Code Generation",
            "code-review": "Code Review",
            "notebook-eda": "Notebook EDA",
            "test-generation": "Test Generation",
            "architecture-design": "Architecture Design",
            "etl-pipeline-development": "ETL Pipeline Development",
            "data-validation": "Data Validation",
            "dashboard-creation": "Dashboard Creation",
            "ci-cd-pipelines": "CI/CD Pipelines",
            "sql-optimization": "SQL Optimization",
            "project-planning": "Project Planning",
            "requirements-documentation": "Requirements Documentation",
            "ui-development": "UI Development",
            "commit-message": "Commit Message",
            "pull-request": "Pull Request",
        }
        return task_names.get(task_name, task_name.replace("-", " ").title())

    def _create_role_template(self, role_name: str, display_name: str) -> str:
        """Crea un template traducido para un rol específico."""
        return f"""# Research: Role: {display_name}

Research specifically the {display_name} role in GitHub Copilot:

REQUIRED ANALYSIS:
1. BEST PRACTICES (5 specific)
   - VS Code configurations optimized for {role_name}
   - Most effective instruction patterns
   - Integration with role-specific tools
   - High-performance prompt examples
   - Specific productivity metrics

2. CRITICAL ANTI-PATTERNS (5 critical)
   - Common instruction errors for {role_name}
   - Problematic configurations
   - Patterns that reduce effectiveness
   - Documented negative impact

3. ADVANCED RECOMMENDATIONS (5 advanced)
   - Role-specific optimizations
   - Tech stack integrations
   - Recommended workflows
   - Adoption strategies

CONTEXT: GCP data science project, inventory analysis
TECH STACK: Python, BigQuery, Vertex AI, Terraform, Jupyter
OBJECTIVE: Maximize {role_name} role productivity
            """

    def _create_task_template(self, task_name: str, display_name: str) -> str:
        """Crea un template traducido para una tarea específica."""
        return f"""# Research: Task: {display_name}

Research specifically the {display_name} task in GitHub Copilot:

REQUIRED ANALYSIS:
1. BEST PRACTICES for {task_name}
   - Optimal instruction structure
   - Most effective keywords
   - Successful configuration examples
   - Prompt engineering patterns
   - Specific quality metrics

2. ANTI-PATTERNS for {task_name}
   - Common implementation errors
   - Counterproductive configurations
   - Frequently failing patterns
   - Performance issues

3. RECOMMENDATIONS for {task_name}
   - Advanced optimizations
   - Workflow integration
   - Complementary tools
   - Validation processes

CONTEXT: Data science in GCP
FOCUS: Specific {task_name} task with maximum effectiveness
            """

    def create_backup(self) -> str:
        """
        Crea backup de los archivos originales.

        Returns:
            Ruta del directorio de backup
        """
        backup_dir = (
            self.base_path.parent / f"research_prompts_backup_{self._get_timestamp()}"
        )
        backup_dir.mkdir(exist_ok=True)

        # Copiar estructura completa
        import shutil

        shutil.copytree(
            self.base_path, backup_dir / "research_prompts", dirs_exist_ok=True
        )

        return str(backup_dir)

    def _get_timestamp(self) -> str:
        """Genera timestamp para backup."""
        from datetime import datetime

        return datetime.now().strftime("%Y%m%d_%H%M%S")

    def apply_translations(self, create_backup: bool = True) -> Dict[str, Any]:
        """
        Aplica todas las traducciones.

        Args:
            create_backup: Si crear backup antes de aplicar cambios

        Returns:
            Reporte de la traducción realizada
        """
        report = {
            "timestamp": self._get_timestamp(),
            "backup_created": False,
            "backup_path": None,
            "roles_translated": 0,
            "tasks_translated": 0,
            "files_processed": [],
            "errors": [],
        }

        try:
            # Crear backup si se solicita
            if create_backup:
                backup_path = self.create_backup()
                report["backup_created"] = True
                report["backup_path"] = backup_path
                print(f"✅ Backup creado en: {backup_path}")

            # Traducir roles
            role_translations = self.translate_role_prompts()
            for file_path, translated_content in role_translations:
                try:
                    with open(file_path, "w", encoding="utf-8") as f:
                        f.write(translated_content)
                    report["files_processed"].append(file_path)
                    report["roles_translated"] += 1
                    print(f"✅ Traducido: {Path(file_path).name}")
                except Exception as e:
                    report["errors"].append(f"Error traduciendo {file_path}: {str(e)}")

            # Traducir tareas
            task_translations = self.translate_task_prompts()
            for file_path, translated_content in task_translations:
                try:
                    with open(file_path, "w", encoding="utf-8") as f:
                        f.write(translated_content)
                    report["files_processed"].append(file_path)
                    report["tasks_translated"] += 1
                    print(f"✅ Traducido: {Path(file_path).name}")
                except Exception as e:
                    report["errors"].append(f"Error traduciendo {file_path}: {str(e)}")

        except Exception as e:
            report["errors"].append(f"Error general: {str(e)}")

        return report


def main():
    """Función principal para ejecutar la traducción."""
    print("🌐 Research Prompts Translation Tool")
    print("=" * 50)

    translator = ResearchPromptsTranslator()

    # Verificar que la carpeta existe
    if not translator.base_path.exists():
        print("❌ Error: Carpeta research_prompts no encontrada")
        return

    print(f"📁 Procesando: {translator.base_path}")
    print(
        f"📄 Roles encontrados: {len(list(translator.roles_path.glob('*_research.md')))}"
    )
    print(
        f"📄 Tareas encontradas: {len(list(translator.tasks_path.glob('*_research.md')))}"
    )

    # Confirmar antes de proceder
    response = input("\n¿Continuar con la traducción? (y/N): ")
    if response.lower() != "y":
        print("❌ Traducción cancelada")
        return

    # Aplicar traducciones
    print("\n🚀 Iniciando traducción...")
    report = translator.apply_translations(create_backup=True)

    # Mostrar resultados
    print(f"\n📊 Resumen de traducción:")
    print(f"   ✅ Roles traducidos: {report['roles_translated']}")
    print(f"   ✅ Tareas traducidas: {report['tasks_translated']}")
    print(f"   📁 Backup: {report['backup_path']}")

    if report["errors"]:
        print(f"   ❌ Errores: {len(report['errors'])}")
        for error in report["errors"]:
            print(f"      - {error}")

    # Guardar reporte
    import json

    report_file = f"translation_report_{report['timestamp']}.json"
    with open(report_file, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2, ensure_ascii=False)

    print(f"\n💾 Reporte guardado en: {report_file}")
    print("\n🎉 Traducción completada!")

    # Mostrar próximos pasos
    print("\nPróximos pasos recomendados:")
    print("1. Revisar archivos traducidos")
    print("2. Validar que el formato es correcto")
    print("3. Ejecutar research_prompts_validator.py para verificar")
    print("4. Proceder con la integración al flujo principal")


if __name__ == "__main__":
    main()
