#!/usr/bin/env python3
"""
Research Prompts Integration Example
====================================

Este script demuestra cómo se podrían integrar los research prompts
con el sistema principal de instrucciones de GitHub Copilot.

Author: GitHub Copilot Analysis System
Date: 2025-06-26
"""

import json
from pathlib import Path
from typing import Any, Dict, List, Tuple


class ResearchPromptsIntegrator:
    """Integrador de research prompts con el sistema principal de instrucciones."""

    def __init__(self, base_path: str = ".github/instructions"):
        """
        Inicializa el integrador de research prompts.

        Args:
            base_path: Ruta base del sistema de instrucciones
        """
        self.base_path = Path(base_path)
        self.research_path = self.base_path / "research_prompts"
        self.roles_path = self.base_path / "roles"
        self.tasks_path = self.base_path / "tasks"

    def create_integration_references(self) -> Dict[str, List[str]]:
        """
        Crea referencias de integración entre archivos principales y research prompts.

        Returns:
            Dictionary con las referencias a añadir a cada archivo

        Example:
            {
                "roles/data-scientist.md": [
                    "## Research Templates",
                    "Use specialized research: `@workspace #file:.github/instructions/research_prompts/roles/data-scientist_research.md`"
                ]
            }
        """
        integrations: Dict[str, List[str]] = {}

        # Integración para roles
        for role_file in self.roles_path.glob("*.md"):
            role_name = role_file.stem
            research_file = self.research_path / "roles" / f"{role_name}_research.md"

            if research_file.exists():
                integrations[f"roles/{role_file.name}"] = [
                    "",
                    "## 🔬 Research Templates",
                    "",
                    f"Para investigación especializada de este rol, use:",
                    f"`@workspace #file:.github/instructions/research_prompts/roles/{role_name}_research.md`",
                    "",
                    "Este template incluye:",
                    "- ✅ Mejores prácticas específicas del rol",
                    "- ❌ Anti-patterns críticos a evitar",
                    "- 💡 Recomendaciones avanzadas",
                    "- 🎯 Contexto específico del proyecto Gasco",
                    "",
                ]

        # Integración para tareas
        for task_file in self.tasks_path.glob("*.md"):
            task_name = task_file.stem
            research_file = self.research_path / "tasks" / f"{task_name}_research.md"

            if research_file.exists():
                integrations[f"tasks/{task_file.name}"] = [
                    "",
                    "## 🔬 Research Templates",
                    "",
                    f"Para investigación especializada de esta tarea, use:",
                    f"`@workspace #file:.github/instructions/research_prompts/tasks/{task_name}_research.md`",
                    "",
                    "Este template proporciona:",
                    "- 📋 Mejores prácticas para la tarea",
                    "- 🚫 Anti-patterns que reducen efectividad",
                    "- 🚀 Recomendaciones de optimización",
                    "- 💼 Contexto de aplicación en GCP",
                    "",
                ]

        return integrations

    def create_mcp_integration_config(self) -> Dict[str, Any]:
        """
        Crea configuración para integrar research prompts con MCP Tools.

        Returns:
            Configuración de integración MCP
        """
        return {
            "research_prompts_integration": {
                "enabled": True,
                "auto_suggest": True,
                "triggers": {
                    "role_detection": {
                        "enabled": True,
                        "patterns": [
                            "data-scientist",
                            "data-engineer",
                            "mlops-engineer",
                            "cloud-architect",
                            "frontend-developer",
                            "qa-engineer",
                        ],
                    },
                    "task_detection": {
                        "enabled": True,
                        "patterns": [
                            "code-generation",
                            "code-review",
                            "notebook-eda",
                            "test-generation",
                            "architecture-design",
                        ],
                    },
                },
                "mcp_tools_integration": {
                    "context7": {
                        "use_research_templates": True,
                        "auto_resolve_libraries": True,
                    },
                    "consult7": {
                        "analyze_with_research_context": True,
                        "pattern_matching": True,
                    },
                    "duckduckgo": {
                        "guided_search": True,
                        "research_prompt_context": True,
                    },
                },
            }
        }

    def generate_integration_commands(self) -> List[str]:
        """
        Genera comandos para aplicar la integración automáticamente.

        Returns:
            Lista de comandos bash para aplicar la integración
        """
        commands = [
            "#!/bin/bash",
            "# Research Prompts Integration Script",
            "# Generated automatically by ResearchPromptsIntegrator",
            "",
            "echo '🔧 Iniciando integración de research prompts...'",
            "",
        ]

        integrations = self.create_integration_references()

        for file_path, content_lines in integrations.items():
            commands.extend(
                [
                    f"echo '📝 Integrando {file_path}...'",
                    f"# Backup original file",
                    f"cp .github/instructions/{file_path} .github/instructions/{file_path}.bak",
                    "",
                    f"# Add research prompt reference",
                    "cat << 'EOF' >> .github/instructions/" + file_path,
                ]
            )

            commands.extend(content_lines)
            commands.append("EOF")
            commands.append("")

        commands.extend(
            [
                "echo '✅ Integración completada'",
                "echo '📊 Archivos modificados:'",
                f"echo '   - {len(integrations)} archivos principales'",
                "echo '   - Referencias a research prompts añadidas'",
                "echo '   - Backups creados (.bak)'",
                "",
            ]
        )

        return commands

    def validate_integration(self) -> Tuple[bool, List[str]]:
        """
        Valida que la integración sea correcta y completa.

        Returns:
            Tuple con (éxito, lista de issues encontrados)
        """
        issues: List[str] = []

        # Verificar que research_prompts existe
        if not self.research_path.exists():
            issues.append("❌ Carpeta research_prompts no encontrada")
            return False, issues

        # Verificar archivos de research por rol
        roles_count = 0
        for role_file in self.roles_path.glob("*.md"):
            role_name = role_file.stem
            research_file = self.research_path / "roles" / f"{role_name}_research.md"
            if research_file.exists():
                roles_count += 1
            else:
                issues.append(f"⚠️  Research prompt faltante para rol: {role_name}")

        # Verificar archivos de research por tarea
        tasks_count = 0
        for task_file in self.tasks_path.glob("*.md"):
            task_name = task_file.stem
            research_file = self.research_path / "tasks" / f"{task_name}_research.md"
            if research_file.exists():
                tasks_count += 1
            else:
                issues.append(f"⚠️  Research prompt faltante para tarea: {task_name}")

        # Verificar referencias en archivos principales
        reference_count = 0
        for file_path in [self.roles_path, self.tasks_path]:
            for md_file in file_path.glob("*.md"):
                with open(md_file, "r", encoding="utf-8") as f:
                    content = f.read()
                    if "research_prompts" in content:
                        reference_count += 1

        # Generar resumen
        success = len(issues) == 0
        if success:
            issues.append(f"✅ {roles_count} roles con research prompts")
            issues.append(f"✅ {tasks_count} tareas con research prompts")
            issues.append(f"✅ {reference_count} referencias encontradas")

        return success, issues


def main():
    """Función principal para demostrar el uso del integrador."""
    print("🔬 Research Prompts Integration Demo")
    print("=" * 50)

    integrator = ResearchPromptsIntegrator()

    # 1. Crear referencias de integración
    print("\n1. 📋 Generando referencias de integración...")
    integrations = integrator.create_integration_references()
    print(f"   ✅ {len(integrations)} archivos para integrar")

    # 2. Crear configuración MCP
    print("\n2. ⚙️  Generando configuración MCP...")
    mcp_config = integrator.create_mcp_integration_config()
    print("   ✅ Configuración MCP generada")

    # 3. Generar comandos de integración
    print("\n3. 🔧 Generando comandos de integración...")
    commands = integrator.generate_integration_commands()
    print(f"   ✅ {len(commands)} comandos generados")

    # 4. Validar estado actual
    print("\n4. ✅ Validando estado actual...")
    success, issues = integrator.validate_integration()
    for issue in issues:
        print(f"   {issue}")

    # 5. Guardar resultados
    print("\n5. 💾 Guardando resultados...")

    # Guardar configuración MCP
    with open("research_prompts_mcp_config.json", "w") as f:
        json.dump(mcp_config, f, indent=2)
    print("   ✅ research_prompts_mcp_config.json")

    # Guardar script de integración
    with open("integrate_research_prompts.sh", "w") as f:
        f.write("\n".join(commands))
    print("   ✅ integrate_research_prompts.sh")

    # Guardar ejemplo de referencia
    example_integration = """
# Ejemplo de integración en data-scientist.md

## 🔬 Research Templates

Para investigación especializada de este rol, use:
`@workspace #file:.github/instructions/research_prompts/roles/data-scientist_research.md`

Este template incluye:
- ✅ Mejores prácticas específicas del rol
- ❌ Anti-patterns críticos a evitar
- 💡 Recomendaciones avanzadas
- 🎯 Contexto específico del proyecto Gasco

### Uso combinado con MCP Tools

```markdown
# Investigación completa con Context7 y Research Prompts
@workspace #file:.github/instructions/research_prompts/roles/data-scientist_research.md

"Implementar validación de datos para inventario Gasco, use context7"
```

### Triggers automáticos
- Al detectar rol "data-scientist", sugerir research prompt
- Al usar MCP tools, incluir contexto de research
- Al generar código, aplicar best practices del research
"""

    with open("research_integration_example.md", "w") as f:
        f.write(example_integration)
    print("   ✅ research_integration_example.md")

    print(f"\n🎉 Demo completado - {3} archivos generados")
    print("\nPróximos pasos:")
    print("1. Revisar archivos generados")
    print("2. Ejecutar integrate_research_prompts.sh (si se desea aplicar)")
    print("3. Testear integración con GitHub Copilot")
    print("4. Medir impacto en productividad")


if __name__ == "__main__":
    main()
