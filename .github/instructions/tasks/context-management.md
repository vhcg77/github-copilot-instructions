---
title: "Context Management for Copilot"
description: "Instructions for managing context when working with GitHub Copilot"
mode: "guidance"
tools: ["vscode", "copilot", "context"]
priority: "high"
---

# Context Management for GitHub Copilot

## Objective
Maximize GitHub Copilot effectiveness by providing optimal context through file management and workspace organization.

## Pre-Task Context Setup

### Before Starting Any Development Task

1. **Open Relevant Files in VS Code**
   ```
   Essential files to have open:
   - Target file you're working on
   - Related modules/utilities
   - Configuration files (config.py, settings.json)
   - Data schema files or examples
   - Existing similar implementations for pattern reference
   ```

2. **Close Irrelevant Files**
   ```
   Files to close to avoid context pollution:
   - Unrelated project files
   - Large data files (open sample instead)
   - Generated/compiled files
   - Files from different domains/contexts
   ```

3. **Workspace Organization**
   ```
   Recommended VS Code layout:
   - Explorer panel: Show project structure
   - Terminal: Open to project root
   - Problems panel: Check for existing issues
   - Copilot Chat: Ready for specific queries
   ```

## Context-Specific Workflows

### For Data Analysis Tasks
```
Required Context Files:
✅ Target dataset (or sample if large)
✅ Data dictionary/schema documentation
✅ Existing analysis notebooks for patterns
✅ Configuration files with data sources
✅ Utility functions from /src directory

Example VS Code tabs for EDA:
- data/sample_data.csv (first 1000 rows)
- notebooks/existing_analysis.ipynb
- src/data/cleaning.py
- docs/data_dictionary.md
- .env or config.py (for data sources)
```

### For Model Development
```
Required Context Files:
✅ Training dataset samples
✅ Feature engineering utilities
✅ Model configuration files
✅ Evaluation metrics definitions
✅ Similar model implementations

Example VS Code tabs:
- src/models/base_model.py
- src/features/feature_engineering.py
- config/model_config.yaml
- notebooks/model_comparison.ipynb
- tests/test_model.py
```

### For API Development
```
Required Context Files:
✅ API schema/OpenAPI definitions
✅ Database models
✅ Authentication utilities
✅ Similar endpoint implementations
✅ Error handling patterns

Example VS Code tabs:
- api/schemas.py
- models/database.py
- auth/security.py
- routers/similar_endpoint.py
- tests/test_api.py
```

## Effective Copilot Chat Usage

### Reference Specific Files
```
Instead of: "Help me analyze data"
Use: "@workspace #file:data/inventory.csv Help me create EDA for this inventory dataset"

Instead of: "Create a function"
Use: "@workspace #file:src/utils/helpers.py Create a data validation function following the patterns in this file"
```

### Provide Context in Prompts
```
Good context prompt:
"Looking at the pandas DataFrame in #file:notebooks/analysis.ipynb, 
create a function that follows the same cleaning pattern but for 
the new dataset structure shown in #file:data/new_format.csv"

Poor context prompt:
"Create a data cleaning function"
```

### Use Selection References
```
When you have code selected:
"#selection Refactor this function to use type hints and proper error handling"

"#selection Optimize this pandas operation for better performance"

"#selection Add comprehensive unit tests for this function"
```

## Context Validation Checklist

Before using Copilot for a task, verify:

- [ ] **Relevant Files Open**: All necessary files are in VS Code tabs
- [ ] **Clean Workspace**: Irrelevant files are closed
- [ ] **Current Directory**: Terminal is in correct project directory
- [ ] **File References**: You can reference specific files in prompts
- [ ] **Pattern Examples**: Similar code is available for reference
- [ ] **Configuration Access**: Settings and config files are accessible

## Advanced Context Techniques

### Schema Context for Data Tasks
```python
# Include schema context in comments at top of file
"""
DATA SCHEMA CONTEXT:
- inventory_data.csv: product_id(str), quantity(int), price(float), location(str)
- sales_data.csv: transaction_id(str), product_id(str), quantity(int), date(datetime)
- Expected output: aggregated_sales with columns [product_id, total_sales, avg_price]
"""
```

### Business Context for Analysis
```markdown
<!-- Include business context in markdown cells -->
## Business Context
- Analyzing inventory turnover for Q4 optimization
- Key metrics: turnover rate, stockout frequency, carrying costs
- Stakeholders: Supply chain team, Finance team
- Decision timeline: Results needed by month-end
```

### Technical Context for Development
```python
# Technical context in docstrings and comments
"""
TECHNICAL CONTEXT:
- Using pandas 2.0+ with PyArrow backend
- Data sources: BigQuery tables updated daily at 6 AM UTC
- Performance requirement: Process 1M+ rows in <5 minutes
- Integration: Results feed into existing dashboard API
"""
```

## Troubleshooting Context Issues

### When Copilot Suggestions Are Poor
1. **Check file context**: Are the right files open?
2. **Review prompt specificity**: Is your request clear and specific?
3. **Verify workspace state**: Are you in the correct directory?
4. **Clean context**: Close unrelated files and try again

### When References Don't Work
1. **File path format**: Use `#file:relative/path/to/file.py`
2. **Workspace scope**: Use `@workspace` for multi-file queries
3. **Selection scope**: Use `#selection` for highlighted code

### When Patterns Aren't Followed
1. **Open pattern examples**: Have reference implementations visible
2. **Include style guides**: Keep style/convention files open
3. **Use configuration files**: Ensure linting/formatting configs are accessible

## Success Metrics

Track your context management effectiveness:
- **Suggestion Acceptance Rate**: Aim for >30% acceptance rate
- **First-Try Success**: How often first suggestion is usable
- **Context Setup Time**: Time to prepare optimal context
- **Iteration Reduction**: Fewer back-and-forth refinements needed

Monitor these in your development workflow and adjust context management practices accordingly.
