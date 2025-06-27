---
applyTo: ["commit", "git", "versioning"]
task: "commit-message"
description: "Prompt examples for generating conventional commit messages"
tags: ["git", "commit", "conventional-commits", "semantic-versioning"]
priority: "medium"
---

# **Task: Commit Message Generation Prompts**

## **1. Conventional Commit for a New Feature**

### **Prompt**

"Generate a Conventional Commit message for the following changes. The changes introduce a new API endpoint for user authentication.

*   **Files changed**: `src/api/auth.py`, `tests/api/test_auth.py`
*   **Description**: Added a `/login` endpoint that accepts a username and password and returns a JWT token. Also added corresponding unit tests.

Follow the format: `feat(api): <subject>` with a descriptive body."

---

## **2. Conventional Commit for a Bug Fix**

### **Prompt**

"Generate a Conventional Commit message for a bug fix. The fix addresses an issue where the application crashed if a configuration file was missing. The change adds a try-except block to handle the `FileNotFoundError` and logs a warning instead.

*   **File changed**: `src/config.py`
*   **Issue reference**: Fixes #123

Follow the format: `fix(config): <subject>` and include the issue reference in the footer."

---

## **3. Commit Message for a Refactor**

### **Prompt**

"I have refactored the `data_processing` function in `src/etl/processing.py` to be more modular and readable. I broke down a large function into three smaller, single-responsibility helper functions. No external behavior has changed.

Generate a Conventional Commit message for this refactoring work. Use the `refactor` type."

---

## **4. Commit Message for Documentation**

### **Prompt**

"Generate a Conventional Commit message for documentation updates. I have added Google-style docstrings to all public functions in the `src/utils/helpers.py` module.

Use the `docs` type."

---

## **5. Commit with a Breaking Change**

### **Prompt**

"Generate a Conventional Commit message for a change that introduces a breaking change. I have renamed the `user_id` column to `customer_uuid` in the main `users` database table. This will require downstream services to update their queries.

Follow the Conventional Commits specification, ensuring you include a `BREAKING CHANGE:` footer that clearly explains the change and its impact."
