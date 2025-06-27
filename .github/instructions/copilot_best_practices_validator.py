#!/usr/bin/env python3
"""
Validador de Mejores Prácticas para GitHub Copilot
Basado en la guía completa de implementación de instrucciones de GitHub Copilot 2025
"""

import json
import os
import re
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple


class CopilotBestPracticesValidator:
    """Validador completo de mejores prácticas para GitHub Copilot"""
    
    def __init__(self, project_root: str):
        self.project_root = Path(project_root)
        self.github_dir = self.project_root / ".github"
        self.instructions_dir = self.github_dir / "instructions"
        self.vscode_dir = self.project_root / ".vscode"
        self.validation_results = {
            "timestamp": datetime.now().isoformat(),
            "overall_score": 0,
            "critical_issues": [],
            "recommendations": [],
            "strengths": [],
            "detailed_analysis": {}
        }
    
    def validate_all(self) -> Dict[str, Any]:
        """Ejecuta todas las validaciones de mejores prácticas"""
        print("🚀 Iniciando validación de mejores prácticas GitHub Copilot...")
        
        # 1. Configuración VS Code
        self._validate_vscode_configuration()
        
        # 2. Estructura de archivos
        self._validate_file_structure()
        
        # 3. Calidad de instrucciones
        self._validate_instructions_quality()
        
        # 4. Roles y responsabilidades
        self._validate_roles_definition()
        
        # 5. Configuración de seguridad
        self._validate_security_configuration()
        
        # 6. Integración y orquestación
        self._validate_integration_orchestration()
        
        # 7. Contexto y referencias
        self._validate_context_management()
        
        # 8. Prompt files y funcionalidad avanzada
        self._validate_advanced_features()
        
        # Calcular score final
        self._calculate_overall_score()
        
        return self.validation_results
    
    def _validate_vscode_configuration(self):
        """Valida la configuración crítica de VS Code"""
        analysis = {
            "critical_settings": {},
            "security_exclusions": {},
            "prompt_locations": {},
            "python_settings": {},
            "issues": [],
            "strengths": []
        }
        
        settings_file = self.vscode_dir / "settings.json"
        if not settings_file.exists():
            analysis["issues"].append("❌ CRÍTICO: No existe .vscode/settings.json")
            self.validation_results["critical_issues"].append("Archivo .vscode/settings.json no encontrado")
            self.validation_results["detailed_analysis"]["vscode_config"] = analysis
            return
        
        try:
            # Leer y parsear settings.json (maneja comentarios JSON)
            content = settings_file.read_text(encoding='utf-8')
            
            # Improved JSON comment removal
            lines = content.split('\n')
            cleaned_lines = []
            
            for line in lines:
                # Remove comments but preserve strings
                if '//' in line:
                    # Check if // is inside a string
                    in_string = False
                    escaped = False
                    comment_pos = None
                    
                    for i, char in enumerate(line):
                        if escaped:
                            escaped = False
                            continue
                        if char == '\\':
                            escaped = True
                            continue
                        if char == '"':
                            in_string = not in_string
                        elif char == '/' and i + 1 < len(line) and line[i + 1] == '/' and not in_string:
                            comment_pos = i
                            break
                    
                    if comment_pos is not None:
                        line = line[:comment_pos].rstrip()
                
                if line.strip():  # Only add non-empty lines
                    cleaned_lines.append(line)
            
            content_clean = '\n'.join(cleaned_lines)
            
            # Remove block comments
            content_clean = re.sub(r'/\*.*?\*/', '', content_clean, flags=re.DOTALL)
            
            # Remove trailing commas
            content_clean = re.sub(r',(\s*[}\]])', r'\1', content_clean)
            
            settings = json.loads(content_clean)
            
            # 1. Configuraciones críticas
            critical_settings = {
                "github.copilot.chat.codeGeneration.useInstructionFiles": True,
                "chat.promptFiles": True,
                "python.analysis.typeCheckingMode": "strict",
                "editor.formatOnSave": True
            }
            
            for setting, expected_value in critical_settings.items():
                if setting in settings:
                    if settings[setting] == expected_value:
                        analysis["critical_settings"][setting] = "✅ CORRECTO"
                        analysis["strengths"].append(f"✅ {setting} configurado correctamente")
                    else:
                        analysis["critical_settings"][setting] = f"⚠️ INCORRECTO: {settings[setting]} (esperado: {expected_value})"
                        analysis["issues"].append(f"⚠️ {setting}: {settings[setting]} (esperado: {expected_value})")
                else:
                    analysis["critical_settings"][setting] = "❌ FALTANTE"
                    analysis["issues"].append(f"❌ Falta configuración crítica: {setting}")
            
            # 2. Configuraciones de seguridad - Verificación directa del archivo
            security_patterns = [
                "**/secrets/**", "**/.env*", "**/terraform.tfstate*", 
                "**/terraform.tfvars", "**/*.key", "**/*.pem", "**/.git/**"
            ]
            
            # Leer el contenido raw para verificación directa
            raw_content = settings_file.read_text()
            
            if "github.copilot.enable" in settings:
                for pattern in security_patterns:
                    # Verificar si el patrón está en el archivo con valor false
                    pattern_string = f'"{pattern}": false'
                    if pattern_string in raw_content:
                        analysis["security_exclusions"][pattern] = "✅ PROTEGIDO"
                        analysis["strengths"].append(f"✅ Exclusión de seguridad: {pattern}")
                    else:
                        analysis["security_exclusions"][pattern] = "❌ NO PROTEGIDO"
                        analysis["issues"].append(f"❌ Patrón de seguridad no encontrado: {pattern}")
            else:
                analysis["issues"].append("❌ No hay configuraciones de exclusión de seguridad")
            
            # 3. Ubicaciones de prompt files
            if "chat.promptFilesLocations" in settings:
                locations = settings["chat.promptFilesLocations"]
                expected_locations = [
                    ".github/instructions", ".github/instructions/prompts",
                    ".github/instructions/roles", ".github/instructions/tasks"
                ]
                
                for location in expected_locations:
                    if location in locations and locations[location]:
                        analysis["prompt_locations"][location] = "✅ HABILITADO"
                        analysis["strengths"].append(f"✅ Ubicación de prompts: {location}")
                    else:
                        analysis["prompt_locations"][location] = "❌ NO HABILITADO"
                        analysis["issues"].append(f"❌ Ubicación de prompts no habilitada: {location}")
            else:
                analysis["issues"].append("❌ No hay configuración de ubicaciones de prompt files")
            
            # 4. Configuraciones Python/Data Science
            python_settings = {
                "python.formatting.provider": "black",
                "python.linting.enabled": True,
                "python.linting.pylintEnabled": True,
                "python.linting.flake8Enabled": True
            }
            
            for setting, expected_value in python_settings.items():
                if setting in settings:
                    if settings[setting] == expected_value:
                        analysis["python_settings"][setting] = "✅ CORRECTO"
                        analysis["strengths"].append(f"✅ Configuración Python: {setting}")
                    else:
                        analysis["python_settings"][setting] = f"⚠️ INCORRECTO: {settings[setting]}"
                        analysis["issues"].append(f"⚠️ {setting}: {settings[setting]} (esperado: {expected_value})")
                else:
                    analysis["python_settings"][setting] = "❌ FALTANTE"
                    analysis["issues"].append(f"❌ Falta configuración Python: {setting}")
            
            # 5. Instrucciones específicas por tarea
            task_instructions = [
                "github.copilot.chat.testGeneration.instructions",
                "github.copilot.chat.commitMessageGeneration.instructions",
                "github.copilot.chat.codeGeneration.instructions",
                "github.copilot.chat.pullRequestGeneration.instructions"
            ]
            
            for instruction_type in task_instructions:
                if instruction_type in settings:
                    analysis["strengths"].append(f"✅ Instrucciones específicas: {instruction_type}")
                else:
                    analysis["issues"].append(f"⚠️ Falta instrucciones específicas: {instruction_type}")
            
            # 6. Configuraciones avanzadas
            if "github.copilot.advanced" in settings:
                advanced = settings["github.copilot.advanced"]
                if "debug.overrideEngine" in advanced and advanced["debug.overrideEngine"] == "gpt-4o":
                    analysis["strengths"].append("✅ Motor GPT-4o configurado")
                else:
                    analysis["issues"].append("⚠️ Motor GPT-4o no configurado")
            
        except json.JSONDecodeError as e:
            analysis["issues"].append(f"❌ Error al parsear settings.json: {e}")
        except Exception as e:
            analysis["issues"].append(f"❌ Error al validar configuración VS Code: {e}")
        
        self.validation_results["detailed_analysis"]["vscode_config"] = analysis
    
    def _validate_file_structure(self):
        """Valida la estructura de archivos según mejores prácticas"""
        analysis = {
            "required_files": {},
            "directory_structure": {},
            "issues": [],
            "strengths": []
        }
        
        # Archivos requeridos
        required_files = {
            ".github/copilot-instructions.md": "Instrucciones principales",
            ".vscode/settings.json": "Configuración VS Code",
        }
        
        for file_path, description in required_files.items():
            full_path = self.project_root / file_path
            if full_path.exists():
                analysis["required_files"][file_path] = f"✅ {description}"
                analysis["strengths"].append(f"✅ {description}: {file_path}")
            else:
                analysis["required_files"][file_path] = f"❌ FALTANTE: {description}"
                analysis["issues"].append(f"❌ Archivo requerido faltante: {file_path}")
        
        # Estructura de directorios
        required_dirs = {
            ".github/instructions/roles": "Roles especializados",
            ".github/instructions/tasks": "Tareas específicas", 
            ".github/instructions/prompts": "Prompt files ejecutables",
            ".github/instructions/research_prompts": "Plantillas de investigación"
        }
        
        for dir_path, description in required_dirs.items():
            full_path = self.project_root / dir_path
            if full_path.exists() and full_path.is_dir():
                # Contar archivos
                files = list(full_path.glob("*.md"))
                analysis["directory_structure"][dir_path] = f"✅ {description} ({len(files)} archivos)"
                analysis["strengths"].append(f"✅ {description}: {len(files)} archivos en {dir_path}")
            else:
                analysis["directory_structure"][dir_path] = f"❌ FALTANTE: {description}"
                analysis["issues"].append(f"❌ Directorio requerido faltante: {dir_path}")
        
        self.validation_results["detailed_analysis"]["file_structure"] = analysis
    
    def _validate_instructions_quality(self):
        """Valida la calidad de las instrucciones según mejores prácticas"""
        analysis = {
            "main_instructions": {},
            "specificity_score": 0,
            "examples_included": 0,
            "actionable_instructions": 0,
            "issues": [],
            "strengths": []
        }
        
        # Validar instrucciones principales
        main_file = self.github_dir / "copilot-instructions.md"
        if main_file.exists():
            content = main_file.read_text()
            
            # Verificar elementos clave
            key_elements = {
                "Tech Stack": r"##.*[Tt]ech [Ss]tack",
                "Code Standards": r"##.*[Cc]ode [Ss]tandards?|##.*[Mm]andatory.*[Ss]tandards?",
                "Examples": r"```\w+",
                "Anti-patterns": r"❌|Don't|Avoid|Never",
                "Role References": r"\.github/instructions/roles/",
                "Task References": r"\.github/instructions/tasks/"
            }
            
            for element, pattern in key_elements.items():
                if re.search(pattern, content, re.MULTILINE | re.IGNORECASE):
                    analysis["main_instructions"][element] = "✅ PRESENTE"
                    analysis["strengths"].append(f"✅ {element} definido en instrucciones principales")
                    if element == "Examples":
                        analysis["examples_included"] += len(re.findall(pattern, content))
                else:
                    analysis["main_instructions"][element] = "❌ AUSENTE"
                    analysis["issues"].append(f"❌ {element} no encontrado en instrucciones principales")
            
            # Evaluar especificidad (buscar instrucciones específicas vs vagas)
            specific_patterns = [
                r"type hints?", r"docstrings?", r"PEP 8", r"random_state=42",
                r"pandas\.", r"numpy\.", r"ValueError", r"KeyError"
            ]
            
            vague_patterns = [
                r"good practices?", r"best practices?", r"follow standards?",
                r"write clean code", r"be consistent"
            ]
            
            specific_count = sum(len(re.findall(pattern, content, re.IGNORECASE)) for pattern in specific_patterns)
            vague_count = sum(len(re.findall(pattern, content, re.IGNORECASE)) for pattern in vague_patterns)
            
            if specific_count > 0:
                analysis["specificity_score"] = specific_count / (specific_count + vague_count) * 100
                if analysis["specificity_score"] > 70:
                    analysis["strengths"].append(f"✅ Alto nivel de especificidad: {analysis['specificity_score']:.1f}%")
                else:
                    analysis["issues"].append(f"⚠️ Nivel de especificidad bajo: {analysis['specificity_score']:.1f}%")
            
            # Verificar instrucciones accionables
            actionable_patterns = [
                r"MUST", r"always", r"never", r"use", r"avoid", r"include", r"follow"
            ]
            
            analysis["actionable_instructions"] = sum(
                len(re.findall(pattern, content, re.IGNORECASE)) for pattern in actionable_patterns
            )
            
            if analysis["actionable_instructions"] > 10:
                analysis["strengths"].append(f"✅ Instrucciones accionables: {analysis['actionable_instructions']}")
            else:
                analysis["issues"].append(f"⚠️ Pocas instrucciones accionables: {analysis['actionable_instructions']}")
        
        else:
            analysis["issues"].append("❌ No existe archivo de instrucciones principales")
        
        self.validation_results["detailed_analysis"]["instructions_quality"] = analysis
    
    def _validate_roles_definition(self):
        """Valida la definición de roles especializados"""
        analysis = {
            "roles_found": [],
            "role_quality": {},
            "coverage_analysis": {},
            "issues": [],
            "strengths": []
        }
        
        roles_dir = self.instructions_dir / "roles"
        if not roles_dir.exists():
            analysis["issues"].append("❌ Directorio de roles no existe")
            self.validation_results["detailed_analysis"]["roles_definition"] = analysis
            return
        
        role_files = list(roles_dir.glob("*.md"))
        analysis["roles_found"] = [f.stem for f in role_files]
        
        # Roles esperados según mejores prácticas
        expected_roles = [
            "data-scientist", "data-engineer", "cloud-architect", "frontend-developer",
            "mlops-engineer", "qa-engineer", "business-analyst", "project-manager"
        ]
        
        for role in expected_roles:
            if role in analysis["roles_found"]:
                analysis["coverage_analysis"][role] = "✅ DEFINIDO"
                analysis["strengths"].append(f"✅ Rol definido: {role}")
            else:
                analysis["coverage_analysis"][role] = "❌ FALTANTE"
                analysis["issues"].append(f"❌ Rol faltante: {role}")
        
        # Validar calidad de cada rol
        for role_file in role_files:
            role_name = role_file.stem
            content = role_file.read_text()
            
            quality_checks = {
                "Responsibilities": r"##.*[Rr]esponsibilities?",
                "Tech Stack": r"##.*[Tt]ech [Ss]tack",
                "Principles": r"##.*[Pp]rinciples?",
                "Code Examples": r"```\w+",
                "MCP Integration": r"MCP|Context7|Consult7|DuckDuckGo"
            }
            
            role_score = 0
            for check, pattern in quality_checks.items():
                if re.search(pattern, content, re.MULTILINE | re.IGNORECASE):
                    role_score += 1
            
            analysis["role_quality"][role_name] = f"{role_score}/5 elementos"
            
            if role_score >= 4:
                analysis["strengths"].append(f"✅ Rol completo: {role_name} ({role_score}/5)")
            elif role_score >= 2:
                analysis["issues"].append(f"⚠️ Rol incompleto: {role_name} ({role_score}/5)")
            else:
                analysis["issues"].append(f"❌ Rol deficiente: {role_name} ({role_score}/5)")
        
        self.validation_results["detailed_analysis"]["roles_definition"] = analysis
    
    def _validate_security_configuration(self):
        """Valida configuraciones de seguridad - Solo archivos sensibles, exclusiones ya validadas"""
        analysis = {
            "exclusion_patterns": {},
            "sensitive_files_check": {},
            "issues": [],
            "strengths": []
        }
        
        # Solo verificar que no existan archivos sensibles expuestos
        # (Las exclusiones ya se validan en _validate_vscode_configuration)
        sensitive_files = [
            ".env", ".env.local", ".env.production", "config.json",
            "terraform.tfvars", "secrets.json"
        ]
        
        for file_name in sensitive_files:
            file_path = self.project_root / file_name
            if file_path.exists():
                analysis["sensitive_files_check"][file_name] = "⚠️ ARCHIVO SENSIBLE ENCONTRADO"
                analysis["issues"].append(f"⚠️ Archivo sensible en proyecto: {file_name}")
            else:
                analysis["sensitive_files_check"][file_name] = "✅ No encontrado"
                analysis["strengths"].append(f"✅ Archivo sensible ausente: {file_name}")
        
        self.validation_results["detailed_analysis"]["security_configuration"] = analysis
        
        self.validation_results["detailed_analysis"]["security_configuration"] = analysis
    
    def _validate_integration_orchestration(self):
        """Valida la integración y orquestación del sistema"""
        analysis = {
            "cross_references": {},
            "mcp_integration": {},
            "validation_scripts": {},
            "issues": [],
            "strengths": []
        }
        
        # Verificar referencias cruzadas en instrucciones principales
        main_file = self.github_dir / "copilot-instructions.md"
        if main_file.exists():
            content = main_file.read_text()
            
            # Referencias a roles y tareas
            role_refs = len(re.findall(r'\.github/instructions/roles/', content))
            task_refs = len(re.findall(r'\.github/instructions/tasks/', content))
            prompt_refs = len(re.findall(r'@workspace', content))
            
            analysis["cross_references"] = {
                "role_references": role_refs,
                "task_references": task_refs,
                "prompt_references": prompt_refs
            }
            
            if role_refs > 0:
                analysis["strengths"].append(f"✅ Referencias a roles: {role_refs}")
            else:
                analysis["issues"].append("❌ No hay referencias a roles en instrucciones principales")
            
            if task_refs > 0:
                analysis["strengths"].append(f"✅ Referencias a tareas: {task_refs}")
            else:
                analysis["issues"].append("❌ No hay referencias a tareas en instrucciones principales")
        
        # Verificar integración MCP
        mcp_patterns = ["Context7", "Consult7", "DuckDuckGo", "GitHub Tools", "MCP"]
        mcp_files = []
        
        for pattern in ["roles/*.md", "tasks/*.md", "prompts/*.md"]:
            for file_path in self.instructions_dir.glob(pattern):
                if file_path.is_file():
                    content = file_path.read_text()
                    mcp_mentions = sum(1 for p in mcp_patterns if p in content)
                    if mcp_mentions > 0:
                        mcp_files.append(f"{file_path.name} ({mcp_mentions} menciones)")
        
        analysis["mcp_integration"]["files_with_mcp"] = mcp_files
        if len(mcp_files) > 0:
            analysis["strengths"].append(f"✅ Integración MCP en {len(mcp_files)} archivos")
        else:
            analysis["issues"].append("⚠️ Poca integración de herramientas MCP")
        
        # Verificar scripts de validación
        validation_scripts = list(self.instructions_dir.glob("*validator*.py"))
        analysis["validation_scripts"]["scripts_found"] = [s.name for s in validation_scripts]
        
        if len(validation_scripts) > 0:
            analysis["strengths"].append(f"✅ Scripts de validación: {len(validation_scripts)}")
        else:
            analysis["issues"].append("⚠️ No se encontraron scripts de validación")
        
        self.validation_results["detailed_analysis"]["integration_orchestration"] = analysis
    
    def _validate_context_management(self):
        """Valida la gestión de contexto"""
        analysis = {
            "context_instructions": {},
            "file_associations": {},
            "issues": [],
            "strengths": []
        }
        
        # Verificar instrucciones de gestión de contexto
        context_file = self.instructions_dir / "tasks" / "context-management.md"
        if context_file.exists():
            content = context_file.read_text()
            
            context_elements = {
                "File Management": r"open.*file|close.*file|workspace",
                "Reference Patterns": r"@workspace|#file:|#selection",
                "Context Setup": r"context.*setup|relevant.*file",
                "Best Practices": r"best.*practice|pattern|guideline"
            }
            
            for element, pattern in context_elements.items():
                if re.search(pattern, content, re.IGNORECASE):
                    analysis["context_instructions"][element] = "✅ PRESENTE"
                    analysis["strengths"].append(f"✅ Gestión de contexto: {element}")
                else:
                    analysis["context_instructions"][element] = "❌ AUSENTE"
                    analysis["issues"].append(f"❌ Falta elemento de contexto: {element}")
        else:
            analysis["issues"].append("❌ No existe archivo de gestión de contexto")
        
        # Verificar asociaciones de archivos en VS Code
        settings_file = self.vscode_dir / "settings.json"
        if settings_file.exists():
            try:
                content = settings_file.read_text()
                content_clean = re.sub(r'//.*?\n', '\n', content)
                settings = json.loads(content_clean)
                
                if "files.associations" in settings:
                    associations = settings["files.associations"]
                    expected_associations = {
                        "*.md": "markdown",
                        "*.prompt.md": "markdown"
                    }
                    
                    for pattern, expected_type in expected_associations.items():
                        if pattern in associations and associations[pattern] == expected_type:
                            analysis["file_associations"][pattern] = f"✅ {expected_type}"
                            analysis["strengths"].append(f"✅ Asociación de archivo: {pattern}")
                        else:
                            analysis["file_associations"][pattern] = f"❌ Falta {expected_type}"
                            analysis["issues"].append(f"❌ Falta asociación: {pattern}")
                
            except Exception as e:
                analysis["issues"].append(f"❌ Error al validar asociaciones de archivos: {e}")
        
        self.validation_results["detailed_analysis"]["context_management"] = analysis
    
    def _validate_advanced_features(self):
        """Valida características avanzadas y prompt files"""
        analysis = {
            "prompt_files": {},
            "advanced_prompts": {},
            "orchestrator": {},
            "issues": [],
            "strengths": []
        }
        
        # Verificar prompt files
        prompts_dir = self.instructions_dir / "prompts"
        if prompts_dir.exists():
            prompt_files = list(prompts_dir.glob("*.prompt.md"))
            analysis["prompt_files"]["total_files"] = len(prompt_files)
            
            # Verificar prompt files críticos
            critical_prompts = [
                "generate-eda-notebook.prompt.md",
                "create-gcp-architecture.prompt.md",
                "mcp-tools-orchestrator.prompt.md"
            ]
            
            for prompt in critical_prompts:
                prompt_path = prompts_dir / prompt
                if prompt_path.exists():
                    analysis["advanced_prompts"][prompt] = "✅ PRESENTE"
                    analysis["strengths"].append(f"✅ Prompt crítico: {prompt}")
                else:
                    analysis["advanced_prompts"][prompt] = "❌ AUSENTE"
                    analysis["issues"].append(f"❌ Prompt crítico faltante: {prompt}")
            
            # Validar calidad de prompt files
            for prompt_file in prompt_files:
                content = prompt_file.read_text()
                
                # Verificar frontmatter
                if content.startswith("---"):
                    analysis["strengths"].append(f"✅ Frontmatter en: {prompt_file.name}")
                else:
                    analysis["issues"].append(f"⚠️ Sin frontmatter: {prompt_file.name}")
        else:
            analysis["issues"].append("❌ Directorio de prompts no existe")
        
        # Verificar orchestrator específico
        orchestrator_file = prompts_dir / "mcp-tools-orchestrator.prompt.md"
        if orchestrator_file.exists():
            content = orchestrator_file.read_text()
            
            orchestrator_elements = {
                "MCP Tools": r"Context7|Consult7|DuckDuckGo",
                "Workflow": r"workflow|process|step",
                "Examples": r"```|example",
                "Instructions": r"instruction|guide|how to"
            }
            
            for element, pattern in orchestrator_elements.items():
                if re.search(pattern, content, re.IGNORECASE):
                    analysis["orchestrator"][element] = "✅ PRESENTE"
                    analysis["strengths"].append(f"✅ Orchestrator: {element}")
                else:
                    analysis["orchestrator"][element] = "❌ AUSENTE"
                    analysis["issues"].append(f"❌ Orchestrator falta: {element}")
        
        self.validation_results["detailed_analysis"]["advanced_features"] = analysis
    
    def _calculate_overall_score(self):
        """Calcula el score general basado en todos los análisis"""
        total_strengths = len(self.validation_results["strengths"])
        total_issues = len(self.validation_results["critical_issues"])
        
        # Contar elementos específicos
        for analysis in self.validation_results["detailed_analysis"].values():
            if "strengths" in analysis:
                total_strengths += len(analysis["strengths"])
            if "issues" in analysis:
                total_issues += len(analysis["issues"])
        
        # Calcular score (máximo 100)
        if total_strengths + total_issues > 0:
            score = (total_strengths / (total_strengths + total_issues)) * 100
        else:
            score = 0
        
        self.validation_results["overall_score"] = round(score, 1)
        
        # Determinar nivel de calidad
        if score >= 90:
            quality_level = "🏆 EXCELENTE"
        elif score >= 80:
            quality_level = "🥇 MUY BUENO"
        elif score >= 70:
            quality_level = "🥈 BUENO"
        elif score >= 60:
            quality_level = "🥉 ACEPTABLE"
        else:
            quality_level = "⚠️ NECESITA MEJORAS"
        
        self.validation_results["quality_level"] = quality_level
        
        # Compilar fortalezas y issues globales
        for analysis in self.validation_results["detailed_analysis"].values():
            if "strengths" in analysis:
                self.validation_results["strengths"].extend(analysis["strengths"])
            if "issues" in analysis:
                self.validation_results["critical_issues"].extend(analysis["issues"])
    
    def generate_report(self, output_file: Optional[str] = None) -> str:
        """Genera reporte detallado de la validación"""
        report = f"""
# 🚀 Reporte de Validación - GitHub Copilot Best Practices

**Fecha:** {self.validation_results['timestamp']}
**Score General:** {self.validation_results['overall_score']}% - {self.validation_results.get('quality_level', 'N/A')}

## 📊 Resumen Ejecutivo

### ✅ Fortalezas Identificadas ({len(self.validation_results['strengths'])})
"""
        
        for strength in self.validation_results["strengths"][:10]:  # Top 10
            report += f"- {strength}\n"
        
        if len(self.validation_results["strengths"]) > 10:
            report += f"- ... y {len(self.validation_results['strengths']) - 10} más\n"
        
        report += f"""
### ⚠️ Issues Identificados ({len(self.validation_results['critical_issues'])})
"""
        
        for issue in self.validation_results["critical_issues"][:10]:  # Top 10
            report += f"- {issue}\n"
        
        if len(self.validation_results["critical_issues"]) > 10:
            report += f"- ... y {len(self.validation_results['critical_issues']) - 10} más\n"
        
        # Análisis detallado por categoría
        report += "\n## 🔍 Análisis Detallado\n\n"
        
        for category, analysis in self.validation_results["detailed_analysis"].items():
            report += f"### {category.replace('_', ' ').title()}\n\n"
            
            # Mostrar elementos principales del análisis
            for key, value in analysis.items():
                if key not in ["issues", "strengths"]:
                    if isinstance(value, dict):
                        report += f"**{key.replace('_', ' ').title()}:**\n"
                        for sub_key, sub_value in value.items():
                            report += f"  - {sub_key}: {sub_value}\n"
                    elif isinstance(value, list):
                        report += f"**{key.replace('_', ' ').title()}:** {len(value)} elementos\n"
                    else:
                        report += f"**{key.replace('_', ' ').title()}:** {value}\n"
            
            report += "\n"
        
        # Recomendaciones
        report += """
## 🎯 Recomendaciones Prioritarias

### Alta Prioridad
1. **Configuración VS Code**: Verificar todas las configuraciones críticas
2. **Seguridad**: Asegurar exclusiones de archivos sensibles
3. **Integración MCP**: Maximizar uso de herramientas avanzadas

### Media Prioridad
1. **Calidad de Instrucciones**: Aumentar especificidad y ejemplos
2. **Gestión de Contexto**: Mejorar referenciación de archivos
3. **Prompt Files**: Expandir biblioteca de prompts reutilizables

### Baja Prioridad
1. **Documentación**: Completar gaps en documentación
2. **Validación**: Implementar más scripts de validación
3. **Organización**: Optimizar estructura de archivos

## 📈 Métricas de Mejora

Para alcanzar un score de 95%+:
- Resolver issues críticos de configuración
- Añadir más ejemplos específicos en instrucciones
- Completar integración MCP en todos los roles
- Implementar validación automatizada continua

---
*Reporte generado por CopilotBestPracticesValidator*
"""
        
        if output_file:
            output_path = Path(output_file)
            output_path.write_text(report)
            print(f"✅ Reporte guardado en: {output_path.absolute()}")
        
        return report


def main():
    """Función principal para ejecutar la validación"""
    import sys
    
    # Determinar directorio del proyecto
    if len(sys.argv) > 1:
        project_root = sys.argv[1]
    else:
        # Default to the root of the repository (where .github and .vscode are)
        project_root = Path(__file__).parent.parent.parent
    
    # Ejecutar validación
    validator = CopilotBestPracticesValidator(str(project_root))
    results = validator.validate_all()
    
    # Generar reporte
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_file = f"copilot_best_practices_report_{timestamp}.md"
    report_path = Path(__file__).parent / report_file
    
    # Generate and save report
    validator.generate_report(str(report_path))
    
    # Guardar resultados JSON
    json_file = report_path.with_suffix('.json')
    with open(json_file, 'w') as f:
        json.dump(results, f, indent=2)
    
    # Mostrar resumen en consola
    print(f"\n🎯 VALIDACIÓN COMPLETADA")
    print(f"Score: {results['overall_score']}% - {results.get('quality_level', 'N/A')}")
    print(f"Fortalezas: {len(results['strengths'])}")
    print(f"Issues: {len(results['critical_issues'])}")
    print(f"Reporte: {report_path.absolute()}")
    print(f"Datos: {json_file.absolute()}")


if __name__ == "__main__":
    main()
