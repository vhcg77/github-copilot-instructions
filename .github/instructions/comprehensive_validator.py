#!/usr/bin/env python3
"""
Validador de estructura de instrucciones GitHub Copilot
Basado en mejores prácticas 2025
"""

import json
import os
import re
from pathlib import Path
from typing import Any, Dict, List, Optional

import yaml


class CopilotInstructionsValidator:
    """Validador completo de instrucciones GitHub Copilot"""

    def __init__(self, project_root: str):
        self.project_root = Path(project_root)
        self.errors = []
        self.warnings = []
        self.success_count = 0

    def validate_all(self) -> Dict[str, Any]:
        """Ejecuta todas las validaciones"""
        print("🔍 Iniciando validación de instrucciones GitHub Copilot...")

        # Validaciones principales
        self._validate_main_instruction_file()
        self._validate_vscode_settings()
        self._validate_directory_structure()
        self._validate_role_files()
        self._validate_task_files()
        self._validate_prompt_files()
        self._validate_metadata_consistency()

        return self._generate_report()

    def _validate_main_instruction_file(self):
        """Valida archivo principal .github/copilot-instructions.md"""
        main_file = self.project_root / ".github" / "copilot-instructions.md"

        if not main_file.exists():
            self.errors.append(
                "❌ Archivo principal .github/copilot-instructions.md no encontrado"
            )
            return

        content = main_file.read_text()

        # Validar secciones requeridas
        required_sections = [
            "About Me",
            "About This Project",
            "Tech Stack",
            "General Principles",
            "Mandatory Code Standards",
        ]

        for section in required_sections:
            if section not in content:
                self.errors.append(
                    f"❌ Sección requerida '{section}' faltante en archivo principal"
                )
            else:
                self.success_count += 1

        # Validar referencias a archivos de roles
        if ".github/instructions/roles/" in content:
            self.success_count += 1
        else:
            self.warnings.append("⚠️ No se encontraron referencias a archivos de roles")

    def _validate_vscode_settings(self):
        """Valida configuración VS Code"""
        settings_file = self.project_root / ".vscode" / "settings.json"

        if not settings_file.exists():
            self.errors.append("❌ Archivo .vscode/settings.json no encontrado")
            return

        try:
            # Leer JSON con comentarios
            content = settings_file.read_text()
            # Remover comentarios para parsing
            content_clean = re.sub(r"//.*$", "", content, flags=re.MULTILINE)
            settings = json.loads(content_clean)

            # Validar configuraciones críticas
            if settings.get("github.copilot.chat.codeGeneration.useInstructionFiles"):
                self.success_count += 1
            else:
                self.errors.append("❌ useInstructionFiles no habilitado en VS Code")

            if "chat.promptFiles" in settings and settings["chat.promptFiles"]:
                self.success_count += 1
            else:
                self.warnings.append("⚠️ Prompt files no habilitados en VS Code")

        except json.JSONDecodeError as e:
            self.errors.append(f"❌ Error en formato JSON de settings.json: {e}")

    def _validate_directory_structure(self):
        """Valida estructura de directorios"""
        expected_dirs = [
            ".github/instructions/roles",
            ".github/instructions/tasks",
            ".github/instructions/prompts",
        ]

        for dir_path in expected_dirs:
            full_path = self.project_root / dir_path
            if full_path.exists():
                self.success_count += 1
            else:
                self.errors.append(f"❌ Directorio faltante: {dir_path}")

    def _validate_role_files(self):
        """Valida archivos de roles"""
        roles_dir = self.project_root / ".github" / "instructions" / "roles"

        if not roles_dir.exists():
            return

        expected_roles = [
            "data-scientist.md",
            "data-engineer.md",
            "mlops-engineer.md",
            "frontend-developer.md",
            "cloud-architect.md",
            "qa-engineer.md",
            "business-analyst.md",
            "project-manager.md",
            "visualization-engineer.md",
        ]

        for role_file in expected_roles:
            file_path = roles_dir / role_file
            if file_path.exists():
                self._validate_role_file_content(file_path)
                self.success_count += 1
            else:
                self.warnings.append(f"⚠️ Archivo de rol faltante: {role_file}")

    def _validate_role_file_content(self, file_path: Path):
        """Valida contenido de archivo de rol"""
        content = file_path.read_text()

        # Validar frontmatter YAML
        if content.startswith("---"):
            try:
                yaml_end = content.find("---", 3)
                if yaml_end > 0:
                    yaml_content = content[3:yaml_end]
                    metadata = yaml.safe_load(yaml_content)

                    # Validar campos requeridos
                    required_fields = ["applyTo", "description", "priority"]
                    for field in required_fields:
                        if field not in metadata:
                            self.warnings.append(
                                f"⚠️ Campo '{field}' faltante en metadata de {file_path.name}"
                            )

            except yaml.YAMLError:
                self.errors.append(f"❌ Error en YAML frontmatter de {file_path.name}")

    def _validate_task_files(self):
        """Valida archivos de tareas"""
        tasks_dir = self.project_root / ".github" / "instructions" / "tasks"

        if not tasks_dir.exists():
            return

        # Validar que existan archivos de tareas clave
        key_tasks = [
            "code-generation.md",
            "test-generation.md",
            "code-review.md",
            "notebook-eda.md",
            "data-validation.md",
        ]

        for task_file in key_tasks:
            file_path = tasks_dir / task_file
            if file_path.exists():
                self.success_count += 1
            else:
                self.warnings.append(f"⚠️ Archivo de tarea clave faltante: {task_file}")

    def _validate_prompt_files(self):
        """Valida archivos de prompts"""
        prompts_dir = self.project_root / ".github" / "instructions" / "prompts"

        if not prompts_dir.exists():
            return

        # Validar archivos .prompt.md
        prompt_files = list(prompts_dir.glob("*.prompt.md"))

        for prompt_file in prompt_files:
            self._validate_prompt_file_content(prompt_file)

    def _validate_prompt_file_content(self, file_path: Path):
        """Valida contenido de archivo de prompt"""
        content = file_path.read_text()

        if content.startswith("---"):
            try:
                yaml_end = content.find("---", 3)
                if yaml_end > 0:
                    yaml_content = content[3:yaml_end]
                    metadata = yaml.safe_load(yaml_content)

                    # Validar campos recomendados para prompts
                    recommended_fields = [
                        "title",
                        "description",
                        "mode",
                        "tools",
                        "role",
                    ]
                    for field in recommended_fields:
                        if field in metadata:
                            self.success_count += 1
                        else:
                            self.warnings.append(
                                f"⚠️ Campo recomendado '{field}' faltante en {file_path.name}"
                            )

            except yaml.YAMLError:
                self.errors.append(f"❌ Error en YAML frontmatter de {file_path.name}")

    def _validate_metadata_consistency(self):
        """Valida consistencia entre metadatos"""
        # Esta validación se puede expandir para verificar que los roles
        # referenciados en prompts existen, etc.
        pass

    def _generate_report(self) -> Dict[str, Any]:
        """Genera reporte final de validación"""
        total_checks = self.success_count + len(self.errors) + len(self.warnings)
        success_rate = (
            (self.success_count / total_checks * 100) if total_checks > 0 else 0
        )

        report = {
            "status": "PASS" if len(self.errors) == 0 else "FAIL",
            "success_rate": round(success_rate, 1),
            "total_checks": total_checks,
            "successes": self.success_count,
            "errors": len(self.errors),
            "warnings": len(self.warnings),
            "error_details": self.errors,
            "warning_details": self.warnings,
        }

        # Imprimir reporte
        print("\n" + "=" * 60)
        print("📊 REPORTE DE VALIDACIÓN")
        print("=" * 60)
        print(
            f"Estado: {'✅ APROBADO' if report['status'] == 'PASS' else '❌ FALLIDO'}"
        )
        print(f"Tasa de éxito: {report['success_rate']}%")
        print(f"Verificaciones exitosas: {report['successes']}")
        print(f"Errores: {report['errors']}")
        print(f"Advertencias: {report['warnings']}")

        if self.errors:
            print("\n🚨 ERRORES CRÍTICOS:")
            for error in self.errors:
                print(f"  {error}")

        if self.warnings:
            print("\n⚠️ ADVERTENCIAS:")
            for warning in self.warnings:
                print(f"  {warning}")

        if report["status"] == "PASS":
            print("\n🎉 ¡Estructura de instrucciones validada exitosamente!")
        else:
            print("\n🔧 Corrige los errores críticos para completar la validación.")

        return report


def main():
    """Función principal"""
    project_root = os.getcwd()
    validator = CopilotInstructionsValidator(project_root)

    try:
        result = validator.validate_all()

        # Guardar reporte
        report_file = (
            Path(project_root) / ".github" / "instructions" / "validation_report.json"
        )
        with open(report_file, "w") as f:
            json.dump(result, f, indent=2)

        print(f"\n📄 Reporte guardado en: {report_file}")

        # Exit code basado en resultado
        exit(0 if result["status"] == "PASS" else 1)

    except Exception as e:
        print(f"❌ Error durante validación: {e}")
        exit(1)


if __name__ == "__main__":
    main()
