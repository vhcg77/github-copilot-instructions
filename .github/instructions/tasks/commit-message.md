---
applyTo: ["commit", "git"]
description: "Instructions for writing commit messages"
priority: "medium"
---

# Task: Commit Message Generation

Your task is to generate a git commit message for the staged changes. The message MUST follow the Conventional Commits specification.

## Format

():

## **Rules**

1. **Type**: Must be one of the following:  
   * feat: A new feature.  
   * fix: A bug fix.  
   * docs: Documentation only changes.  
   * style: Changes that do not affect the meaning of the code (white-space, formatting, etc).  
   * refactor: A code change that neither fixes a bug nor adds a feature.  
   * perf: A code change that improves performance.  
   * test: Adding missing tests or correcting existing tests.  
   * build: Changes that affect the build system or external dependencies.  
   * ci: Changes to our CI configuration files and scripts.  
   * chore: Other changes that don't modify src or test files.  
2. **Scope** (optional): A noun describing the section of the codebase affected (e.g., data-cleaning, modeling, eda-notebook).  
3. **Subject**:  
   * Use the imperative, present tense: "add" not "added" nor "adds".  
   * No capitalization at the beginning.  
   * No dot (.) at the end.  
   * Maximum 50 characters.  
4. **Body** (optional):  
   * Use the imperative, present tense.  
   * Explain the "what" and "why" of the change, not the "how".  
   * Separate from the subject with a blank line.

## **Example**

feat(auth): add user login functionality

- Implement the /login API endpoint using JWT for authentication.  
- Create a new service to handle password hashing and comparison.  
- This change allows users to securely access protected routes.
