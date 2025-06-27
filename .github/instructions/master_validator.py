#!/usr/bin/env python3
"""
Orchestrador Maestro de Validación GitHub Copilot
Ejecuta todas las validaciones en secuencia y genera reporte consolidado
"""

import json
import os
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List


class MasterOrchestrationValidator:
    """Orchestrador maestro de todas las validaciones"""

    def __init__(self, project_root: str):
        self.project_root = Path(project_root)
        self.instructions_dir = self.project_root / ".github" / "instructions"
        self.reports_dir = self.instructions_dir
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        # Scripts de validación disponibles
        self.validators = [
            {
                "name": "Estructura Básica",
                "script": "comprehensive_validator.py",
                "description": "Valida estructura de archivos y configuración básica",
                "weight": 3,
            },
            {
                "name": "Orquestación Completa",
                "script": "orchestration_validator.py",
                "description": "Valida orquestación entre componentes",
                "weight": 4,
            },
            {
                "name": "Workflows de Trabajo",
                "script": "workflow_validator.py",
                "description": "Valida flujos de trabajo entre roles y tareas",
                "weight": 3,
            },
            {
                "name": "Validación Práctica",
                "script": "practical_validator.py",
                "description": "Simula escenarios reales de uso",
                "weight": 4,
            },
        ]

    def run_complete_validation(self) -> Dict[str, Any]:
        """Ejecuta validación completa en secuencia"""
        print("🎭" + "=" * 70)
        print("   VALIDACIÓN MAESTRA DE ORQUESTACIÓN GITHUB COPILOT")
        print("=" * 74)
        print(
            f"📅 Iniciando validación completa: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        )
        print(f"📂 Directorio del proyecto: {self.project_root}")
        print("=" * 74)

        validation_results = {
            "timestamp": self.timestamp,
            "project_root": str(self.project_root),
            "overall_status": "PASS",
            "total_score": 0,
            "max_score": 0,
            "validator_results": {},
            "summary": {},
            "recommendations": [],
        }

        # Ejecutar cada validador
        for i, validator in enumerate(self.validators, 1):
            print(f"\n🔹 [{i}/{len(self.validators)}] Ejecutando: {validator['name']}")
            print(f"   📝 {validator['description']}")
            print("-" * 70)

            result = self._run_single_validator(validator)
            validation_results["validator_results"][validator["name"]] = result

            # Actualizar puntajes
            validation_results["max_score"] += validator["weight"] * 100
            validation_results["total_score"] += (
                result.get("score", 0) * validator["weight"]
            )

            # Verificar si hay errores críticos
            if result.get("status") == "FAIL":
                validation_results["overall_status"] = "FAIL"

            print(
                f"   📊 Resultado: {result.get('status', 'UNKNOWN')} ({result.get('success_rate', 0)}%)"
            )

        # Calcular puntaje general
        overall_percentage = (
            (validation_results["total_score"] / validation_results["max_score"] * 100)
            if validation_results["max_score"] > 0
            else 0
        )
        validation_results["overall_percentage"] = round(overall_percentage, 1)

        # Generar recomendaciones
        validation_results["recommendations"] = self._generate_recommendations(
            validation_results
        )

        # Generar resumen
        validation_results["summary"] = self._generate_summary(validation_results)

        # Guardar reporte consolidado
        self._save_consolidated_report(validation_results)

        # Mostrar reporte final
        self._display_final_report(validation_results)

        return validation_results

    def _run_single_validator(self, validator: Dict[str, Any]) -> Dict[str, Any]:
        """Ejecuta un validador individual"""
        script_path = self.instructions_dir / validator["script"]

        if not script_path.exists():
            return {
                "status": "ERROR",
                "success_rate": 0,
                "score": 0,
                "error": f"Script {validator['script']} no encontrado",
            }

        try:
            # Ejecutar script
            result = subprocess.run(
                [sys.executable, str(script_path)],
                cwd=self.project_root,
                capture_output=True,
                text=True,
                timeout=60,
            )

            # Buscar reporte JSON correspondiente
            report_files = {
                "comprehensive_validator.py": "validation_report.json",
                "orchestration_validator.py": "orchestration_report.json",
                "workflow_validator.py": "workflow_validation_report.json",
                "practical_validator.py": "practical_validation_report.json",
            }

            report_file = self.reports_dir / report_files.get(
                validator["script"], "unknown_report.json"
            )

            if report_file.exists():
                with open(report_file, "r") as f:
                    report_data = json.load(f)

                # Extraer información relevante
                status_keys = [
                    "status",
                    "orchestration_status",
                    "workflow_status",
                    "practical_status",
                ]
                success_rate_keys = ["success_rate"]

                status = "UNKNOWN"
                for key in status_keys:
                    if key in report_data:
                        status = report_data[key]
                        break

                success_rate = 0
                for key in success_rate_keys:
                    if key in report_data:
                        success_rate = report_data[key]
                        break

                return {
                    "status": status,
                    "success_rate": success_rate,
                    "score": success_rate,
                    "details": report_data,
                    "stdout": result.stdout,
                    "stderr": result.stderr,
                    "return_code": result.returncode,
                }
            else:
                return {
                    "status": "COMPLETED" if result.returncode == 0 else "FAIL",
                    "success_rate": 100 if result.returncode == 0 else 0,
                    "score": 100 if result.returncode == 0 else 0,
                    "stdout": result.stdout,
                    "stderr": result.stderr,
                    "return_code": result.returncode,
                }

        except subprocess.TimeoutExpired:
            return {
                "status": "TIMEOUT",
                "success_rate": 0,
                "score": 0,
                "error": "Script ejecutado por más de 60 segundos",
            }
        except Exception as e:
            return {"status": "ERROR", "success_rate": 0, "score": 0, "error": str(e)}

    def _generate_recommendations(self, results: Dict[str, Any]) -> List[str]:
        """Genera recomendaciones basadas en los resultados"""
        recommendations = []

        overall_percentage = results.get("overall_percentage", 0)

        if overall_percentage >= 95:
            recommendations.append(
                "🏆 ¡Excelente! Tu configuración de GitHub Copilot es de clase mundial."
            )
            recommendations.append(
                "📚 Considera documentar tu configuración como ejemplo para otros proyectos."
            )

        elif overall_percentage >= 85:
            recommendations.append(
                "✅ Muy buena configuración. Pequeños ajustes pueden optimizar aún más."
            )
            recommendations.append(
                "🔍 Revisa las advertencias menores para alcanzar la perfección."
            )

        elif overall_percentage >= 70:
            recommendations.append(
                "⚡ Configuración sólida con algunas áreas de mejora."
            )
            recommendations.append("🎯 Enfócate en resolver errores críticos primero.")

        else:
            recommendations.append(
                "🔧 Se necesitan mejoras significativas en la orquestación."
            )
            recommendations.append(
                "📖 Revisa la documentación de mejores prácticas de GitHub Copilot."
            )

        # Recomendaciones específicas por validador
        for validator_name, result in results["validator_results"].items():
            if result.get("success_rate", 0) < 80:
                recommendations.append(f"🎭 Mejorar configuración de: {validator_name}")

        return recommendations

    def _generate_summary(self, results: Dict[str, Any]) -> Dict[str, Any]:
        """Genera resumen ejecutivo"""
        summary = {
            "validation_date": datetime.now().isoformat(),
            "project_status": results["overall_status"],
            "overall_score": f"{results['overall_percentage']}%",
            "validators_executed": len(self.validators),
            "validators_passed": len(
                [
                    r
                    for r in results["validator_results"].values()
                    if r.get("status") == "PASS"
                ]
            ),
            "critical_issues": len(
                [
                    r
                    for r in results["validator_results"].values()
                    if r.get("status") == "FAIL"
                ]
            ),
            "performance_grade": self._calculate_grade(results["overall_percentage"]),
        }

        return summary

    def _calculate_grade(self, percentage: float) -> str:
        """Calcula calificación basada en porcentaje"""
        if percentage >= 95:
            return "A+ (Excelente)"
        elif percentage >= 90:
            return "A (Muy Bueno)"
        elif percentage >= 85:
            return "B+ (Bueno)"
        elif percentage >= 80:
            return "B (Satisfactorio)"
        elif percentage >= 70:
            return "C+ (Necesita Mejoras)"
        elif percentage >= 60:
            return "C (Problemas Significativos)"
        else:
            return "D (Requiere Atención Urgente)"

    def _save_consolidated_report(self, results: Dict[str, Any]):
        """Guarda reporte consolidado"""
        report_file = (
            self.reports_dir / f"master_validation_report_{self.timestamp}.json"
        )

        with open(report_file, "w") as f:
            json.dump(results, f, indent=2, ensure_ascii=False)

        # También guardar como reporte más reciente
        latest_report = self.reports_dir / "latest_master_validation_report.json"
        with open(latest_report, "w") as f:
            json.dump(results, f, indent=2, ensure_ascii=False)

        results["report_file"] = str(report_file)
        results["latest_report_file"] = str(latest_report)

    def _display_final_report(self, results: Dict[str, Any]):
        """Muestra reporte final consolidado"""
        print("\n" + "🎭" + "=" * 70)
        print("               REPORTE FINAL DE VALIDACIÓN MAESTRA")
        print("=" * 74)

        summary = results["summary"]

        print(f"📊 CALIFICACIÓN GENERAL: {summary['performance_grade']}")
        print(f"🎯 PUNTAJE TOTAL: {summary['overall_score']}")
        print(
            f"📈 ESTADO: {'✅ APROBADO' if results['overall_status'] == 'PASS' else '❌ NECESITA ATENCIÓN'}"
        )

        print(f"\n📋 RESUMEN EJECUTIVO:")
        print(f"   • Validadores ejecutados: {summary['validators_executed']}")
        print(f"   • Validadores aprobados: {summary['validators_passed']}")
        print(f"   • Problemas críticos: {summary['critical_issues']}")

        print(f"\n📈 RESULTADOS POR VALIDADOR:")
        for validator_name, result in results["validator_results"].items():
            status_icon = (
                "✅"
                if result.get("status") == "PASS"
                else "❌" if result.get("status") == "FAIL" else "⚠️"
            )
            print(
                f"   {status_icon} {validator_name}: {result.get('success_rate', 0)}%"
            )

        print(f"\n🎯 RECOMENDACIONES:")
        for rec in results["recommendations"][:5]:  # Top 5 recomendaciones
            print(f"   {rec}")

        if results["overall_status"] == "PASS":
            print(f"\n🚀 ¡FELICITACIONES!")
            print(f"   Tu configuración de GitHub Copilot está optimizada y lista para")
            print(f"   maximizar la productividad del equipo. La orquestación funciona")
            print(f"   correctamente en todos los escenarios validados.")
        else:
            print(f"\n🔧 ACCIÓN REQUERIDA:")
            print(f"   Hay problemas críticos que necesitan atención para optimizar")
            print(f"   GitHub Copilot. Revisa los errores específicos y aplica las")
            print(f"   recomendaciones proporcionadas.")

        print(f"\n📄 Reportes guardados en:")
        print(f"   • Detallado: {results['report_file']}")
        print(f"   • Más reciente: {results['latest_report_file']}")

        print("=" * 74)


def main():
    """Función principal"""
    project_root = os.getcwd()
    master_validator = MasterOrchestrationValidator(project_root)

    try:
        results = master_validator.run_complete_validation()

        # Exit code basado en resultado general
        exit(0 if results["overall_status"] == "PASS" else 1)

    except KeyboardInterrupt:
        print("\n❌ Validación interrumpida por el usuario")
        exit(130)
    except Exception as e:
        print(f"❌ Error durante validación maestra: {e}")
        import traceback

        traceback.print_exc()
        exit(1)


if __name__ == "__main__":
    main()
