---
title: "MCP Tools Orchestrator"
description: "Advanced context and research tools for enhanced development"
mode: "assistant"
tools: ["context7", "consult7", "duckduckgo", "github", "google-cloud"]
priority: "high"
applyTo: ["research", "context", "documentation", "analysis"]
---

# MCP Tools Orchestrator

## Objetivo
Proporcionar acceso centralizado a herramientas MCP avanzadas para mejorar la calidad del contexto y las decisiones de desarrollo en el proyecto Gasco.

## Herramientas MCP Disponibles

### 🔍 **Context7 - Documentación Actualizada de Librerías**

**Cuándo usar:**
- Necesitas documentación actualizada y específica por versión de una librería
- Quieres evitar APIs desactualizadas o alucinadas
- Buscas ejemplos de código actuales y funcionales

**Cómo usar:**
```
Agrega "use context7" a tu prompt para activar automáticamente
```

**Ejemplos prácticos:**
- `"Crear validación de DataFrame con pandas, use context7"`
- `"Implementar autenticación JWT con FastAPI, use context7"`
- `"Configurar Terraform para BigQuery, use context7"`

**Herramientas específicas:**
- **resolve-library-id**: Convierte nombre de librería a ID compatible
- **get-library-docs**: Obtiene documentación por ID específico

---

### 🔬 **Consult7 - Análisis de Codebases Extensos**

**Cuándo usar:**
- Necesitas analizar arquitecturas completas de proyectos
- Buscas patrones de implementación específicos en código existente
- Quieres entender flujos complejos across múltiples archivos
- Realizas auditorías de código o análisis de cobertura

**Cómo usar:**
```
Especifica path, patrón regex y consulta específica
```

**Ejemplos prácticos:**
- `"Analiza patrones de autenticación en todo el backend"`
- `"Encuentra todas las funciones de validación de datos"`
- `"Revisa cobertura de tests en el proyecto"`
- `"Identifica dependencias y arquitectura del sistema"`

**Modelos recomendados:**
- **gemini-2.5-flash|thinking**: Para análisis profundo con razonamiento
- **gemini-2.5-pro**: Para análisis complejos e inteligentes
- **claude-sonnet-4|thinking**: Para revisiones críticas de código

---

### 🌐 **DuckDuckGo - Investigación Web Actualizada**

**Cuándo usar:**
- Necesitas mejores prácticas actuales
- Buscas soluciones a errores específicos
- Quieres investigar nuevas tecnologías o enfoques
- Necesitas información de troubleshooting

**Cómo usar:**
```
Busca información específica con queries técnicas
```

**Ejemplos prácticos:**
- `"Mejores prácticas seguridad datos 2025"`
- `"Solución error pandas memory overflow"`
- `"GCP BigQuery optimization techniques"`
- `"Python testing patterns pytest 2025"`

**Herramientas específicas:**
- **search**: Búsquedas con resultados formateados
- **fetch_content**: Obtener contenido completo de páginas específicas

---

### 📂 **GitHub Tools - Análisis de Repositorios**

**Cuándo usar:**
- Investigas implementaciones en proyectos open source
- Buscas ejemplos de código similares a tu caso de uso
- Quieres analizar documentación de proyectos específicos
- Necesitas mapear librerías a repositorios

**Cómo usar:**
```
Especifica owner/repo y tipo de búsqueda
```

**Ejemplos prácticos:**
- `"Buscar implementaciones de data pipelines en Apache Airflow"`
- `"Analizar documentación de FastAPI para patrones de testing"`
- `"Encontrar ejemplos de Terraform para GCP en proyectos reales"`

**Herramientas específicas:**
- **fetch_generic_documentation**: Documentación de cualquier repo
- **search_generic_code**: Búsqueda de código específico
- **search_generic_documentation**: Búsqueda semántica en docs
- **match_common_libs_owner_repo_mapping**: Mapear librería a repo

---

## 🎯 Patrones de Uso por Contexto

### Para **Data Science y Analysis**
```
1. Context7: "pandas data validation patterns, use context7"
2. Consult7: Analizar notebooks existentes para patrones de EDA
3. DuckDuckGo: "latest data quality best practices 2025"
4. GitHub: Buscar implementaciones de pipelines de ML
```

### Para **Testing y QA**
```
1. Context7: "pytest fixtures and parametrization, use context7"
2. Consult7: Analizar cobertura de tests en todo el proyecto
3. DuckDuckGo: "data validation testing strategies Python"
4. GitHub: Buscar ejemplos de test suites en proyectos similares
```

### Para **Infrastructure y Cloud**
```
1. Context7: "Terraform GCP modules, use context7"
2. Consult7: Revisar configuraciones de infraestructura existentes
3. DuckDuckGo: "GCP security best practices 2025"
4. GitHub: Analizar proyectos con arquitecturas GCP similares
```

### Para **API Development**
```
1. Context7: "FastAPI authentication and validation, use context7"
2. Consult7: Analizar estructura de APIs existentes
3. DuckDuckGo: "REST API design patterns 2025"
4. GitHub: Buscar implementaciones de APIs similares
```

## 🔄 Workflow de Investigación Recomendado

### **Fase 1: Contexto Base**
1. **Context7**: Obtener documentación actualizada de librerías principales
2. **Consult7**: Analizar código existente relacionado

### **Fase 2: Investigación Complementaria**
3. **DuckDuckGo**: Buscar mejores prácticas y soluciones actuales
4. **GitHub**: Revisar implementaciones de referencia

### **Fase 3: Síntesis**
5. Combinar información de todas las fuentes
6. Generar solución optimizada y actualizada

## ⚡ Activadores Automáticos

### **Para Roles Específicos**
- **QA Engineer**: Activar Context7 para frameworks de testing
- **Data Scientist**: Activar Consult7 para análisis de notebooks
- **Cloud Architect**: Activar DuckDuckGo para mejores prácticas GCP
- **Frontend Developer**: Activar GitHub para patrones de UI/UX

### **Para Tareas Específicas**
- **Code Generation**: Context7 + Consult7 para patrones existentes
- **Architecture Design**: DuckDuckGo + GitHub para referencias
- **Test Generation**: Context7 + Consult7 para cobertura completa
- **Documentation**: GitHub + DuckDuckGo para estándares actuales

## 🎨 Prompts de Ejemplo Completos

### **Ejemplo 1: Desarrollo de API**
```
"Necesito crear un endpoint FastAPI para validación de inventario que:
1. Valide formato de product_id
2. Verifique stock disponible
3. Registre transacciones

use context7 para FastAPI patterns
Analiza con consult7 endpoints similares en /src/
Busca con duckduckgo: 'FastAPI validation best practices 2025'"
```

### **Ejemplo 2: Pipeline de Datos**
```
"Crear pipeline ETL para procesar datos de inventario que:
1. Extraiga de BigQuery
2. Transforme con pandas
3. Cargue a Cloud Storage

use context7 para pandas y google-cloud-bigquery
Analiza con consult7 pipelines existentes en /src/data/
Investiga con github: implementaciones ETL similares"
```

### **Ejemplo 3: Suite de Testing**
```
"Generar tests comprehensivos para módulo de validación que:
1. Cubra todos los casos edge
2. Use fixtures apropiados  
3. Incluya tests de performance

use context7 para pytest patterns
Analiza con consult7 cobertura actual de tests
Busca con duckduckgo: 'Python testing strategies 2025'"
```

## 📈 Métricas de Efectividad

### **Indicadores de Éxito**
- ✅ **Precisión**: Código generado funciona al primer intento
- ✅ **Actualización**: APIs y patrones están actualizados
- ✅ **Consistencia**: Sigue patrones establecidos en el proyecto
- ✅ **Completitud**: Incluye documentación, tests y error handling

### **Señales de Mejora Necesaria**
- ❌ Código que requiere múltiples iteraciones
- ❌ Uso de APIs desactualizadas o deprecadas
- ❌ Inconsistencia con patrones del proyecto
- ❌ Falta de contexto business-specific

## 🔧 Troubleshooting

### **Problema: Context7 no encuentra la librería**
```
Solución: Usar resolve-library-id primero
Ejemplo: "Resolve pandas to context7 ID, then get validation docs"
```

### **Problema: Consult7 respuesta demasiado genérica**
```
Solución: Especificar query más específica y usar thinking mode
Ejemplo: "Analiza autenticación patterns usando gemini-2.5-flash|thinking"
```

### **Problema: DuckDuckGo resultados irrelevantes**
```
Solución: Usar queries más específicas con contexto técnico
Ejemplo: "Python pandas DataFrame memory optimization 2025" vs "pandas memory"
```

---

## � Instructions for Use

### **Step-by-Step Guide**

1. **Identify Your Need**: Determine what type of research or context you need
   - Current library documentation → Use Context7
   - Existing code patterns → Use Consult7  
   - Best practices research → Use DuckDuckGo
   - Reference implementations → Use GitHub Tools

2. **Activate the Tool**: Add the activation phrase to your prompt
   - Context7: Add `"use context7"` to any request
   - Consult7: Specify path and analysis query
   - DuckDuckGo: Use specific technical search terms
   - GitHub: Provide owner/repo and search criteria

3. **Combine Sources**: Use multiple tools for comprehensive analysis
   - Start with Context7 for official docs
   - Use Consult7 for internal patterns
   - Research with DuckDuckGo for current practices
   - Validate with GitHub examples

4. **Apply Results**: Integrate findings into your implementation
   - Follow official documentation patterns (Context7)
   - Maintain consistency with existing code (Consult7)
   - Apply current best practices (DuckDuckGo)
   - Reference proven implementations (GitHub)

### **Quick Commands**

- **Full Research**: `"[your request], use context7, analyze with consult7, research best practices"`
- **Context Only**: `"[your request], use context7"`
- **Pattern Analysis**: `"Analyze [pattern] with consult7 in /src/ directory"`
- **Best Practices**: `"Research [topic] best practices 2025"`
- **Reference Search**: `"Find [implementation] examples in similar projects"`

### **Quality Checklist**

Before implementing any solution, ensure:
- [ ] Used Context7 for current API documentation
- [ ] Analyzed existing patterns with Consult7
- [ ] Researched current best practices with DuckDuckGo
- [ ] Reviewed reference implementations when needed
- [ ] Solution follows project conventions
- [ ] Code includes proper error handling
- [ ] Documentation and tests are included

---

## �📝 Notas de Implementación

- Este prompt puede ser invocado desde cualquier rol o tarea
- Las herramientas MCP se activarán automáticamente cuando se detecten los patrones
- Siempre combinar múltiples fuentes para obtener la mejor solución
- Priorizar Context7 para documentación oficial, Consult7 para análisis interno

**Última actualización**: Junio 2025 - Proyecto Gasco Utilities
