---
applyTo: ["pull-request", "git"]
description: "Instructions for creating pull requests"
priority: "medium"
---

# **Task: Pull Request Title and Description Generation**

Your task is to generate a title and description for a new Pull Request based on the committed changes.

## **Title**

The title should be concise and follow the same rules as a Conventional Commit subject line.  
Format: \<type\>(\<scope\>): \<description\>  
Example: feat(visualization): add interactive churn analysis dashboard

## **Description**

Use the following markdown template for the PR description. Fill in the sections based on the changes in the PR.

### **Description**

*A clear and concise summary of the changes included in this PR. Explain the problem being solved and the approach taken.*

### **Related Issue**

*Link to the relevant issue or ticket, if one exists. (e.g., Closes \#123)*

### **Type of Change**

*Please delete options that are not relevant.*

* \[ \] Bug fix (non-breaking change which fixes an issue)  
* \[ \] New feature (non-breaking change which adds functionality)  
* \[ \] Breaking change (fix or feature that would cause existing functionality to not work as expected)  
* \[ \] Documentation update  
* \[ \] Refactor or performance improvement

### **How Has This Been Tested?**

*Please describe the tests that you ran to verify your changes. Provide instructions so we can reproduce.*

* \[ \] New unit tests have been added.  
* \[ \] Existing tests pass with these changes.  
* \[ \] I have manually tested the following scenarios:  
  1. ...  
  2. ...

### **Checklist**

* \[ \] My code follows the style guidelines of this project (PEP 8, type hints, docstrings).  
* \[ \] I have performed a self-review of my own code.  
* \[ \] I have commented my code, particularly in hard-to-understand areas.  
* \[ \] I have made corresponding changes to the documentation.  
* \[ \] My changes generate no new warnings.  
* \[ \] New and existing unit tests pass locally with my changes.