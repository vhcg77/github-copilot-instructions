---
applyTo: ["pull-request", "code-review", "collaboration"]
task: "pull-request"
description: "Prompt examples for pull request tasks"
tags: ["pr", "pull-request-description", "review-guidance", "testing-summary"]
priority: "medium"
---

# **Task: Pull Request Description Prompts**

## **1. PR Description for a New Feature**

### **Prompt**

"Generate a pull request description for a new feature that adds user profile pages to the application. The PR includes changes to the backend (a new API endpoint) and the frontend (a new React component).

The description should include:
*   A clear title.
*   A summary of the changes.
*   A link to the relevant Jira ticket (e.g., MDIJ-456).
*   A section on 'How to Test' with manual testing steps.
*   A screenshot of the new UI."

---

## **2. PR Description for a Bug Fix**

### **Prompt**

"Generate a pull request description for a bug fix. The bug caused incorrect calculations in the monthly sales report. The fix corrects the SQL query logic.

The description should include:
*   A title that clearly states the fix.
*   A 'Before' and 'After' section explaining the bug and the fix.
*   A link to the bug report issue (e.g., #241).
*   A note confirming that existing unit tests were updated and a new test was added."

---

## **3. PR Description for a Technical Debt Refactor**

### **Prompt**

"I have a pull request that refactors the legacy `AuthService` class. The goal was to improve maintainability and add no new functionality. Generate a PR description that explains this.

The description should cover:
*   The motivation for the refactor (e.g., reducing complexity, improving testability).
*   A summary of the key changes (e.g., breaking down large methods, removing dead code).
*   A confirmation that all existing tests pass and that code coverage has not decreased."

---

## **4. Draft/WIP Pull Request**

### **Prompt**

"Generate a pull request description for a draft/work-in-progress (WIP) PR. I am working on a new data pipeline and want to get early feedback on my approach. The code is not complete or fully tested.

The description should:
*   Clearly state that it is a **[WIP]** in the title.
*   Explain the overall goal of the feature.
*   Ask for specific feedback on certain parts of the implementation (e.g., 'Is this the most efficient way to join these two DataFrames?').
*   List the remaining to-do items in a checklist."
