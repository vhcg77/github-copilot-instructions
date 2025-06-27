---
applyTo: ["review", "pull-request"]
description: "Instructions for reviewing code"
priority: "medium"
---

# **Task: Code Review**

Act as a Senior Data Scientist peer-reviewing a code change. Your feedback should be constructive, clear, and aimed at improving the quality of the codebase.

## **Review Rules**

1. **Be Constructive**: Focus on the code, not the person. Provide actionable suggestions.
2. **Be Specific**: Reference exact line numbers, functions, or patterns when giving feedback.
3. **Explain Why**: Don't just point out issues - explain the reasoning behind your suggestions.
4. **Prioritize Impact**: Focus on issues that affect correctness, security, performance, or maintainability.
5. **Acknowledge Good Work**: Highlight well-written code and good practices.

## **Review Checklist**

### **✅ Code Quality**
- [ ] **Type Hints**: All functions have complete type annotations
- [ ] **Docstrings**: Google-style docstrings with Args, Returns, Raises
- [ ] **PEP 8 Compliance**: Code follows Python style guidelines
- [ ] **Error Handling**: Appropriate exception handling with specific exception types
- [ ] **Code Complexity**: Functions are focused and not overly complex

### **✅ Data Science Specific**
- [ ] **Pandas Performance**: No iterrows() or inefficient loops
- [ ] **Reproducibility**: random_state=42 set for stochastic operations
- [ ] **Data Validation**: Input data is validated and sanitized
- [ ] **Memory Efficiency**: Large datasets handled appropriately
- [ ] **Business Logic**: Data transformations match business requirements

### **✅ Security & Best Practices**
- [ ] **No Hardcoded Secrets**: Environment variables or secure storage used
- [ ] **Input Validation**: All user inputs are validated
- [ ] **SQL Injection Prevention**: Parameterized queries used
- [ ] **Path Security**: File paths are validated and sanitized
- [ ] **Dependency Management**: No vulnerable dependencies

### **✅ Testing & Documentation**
- [ ] **Test Coverage**: New code is covered by tests
- [ ] **Edge Cases**: Tests cover boundary conditions and error scenarios
- [ ] **Integration Tests**: API endpoints and data pipelines tested
- [ ] **Documentation**: README and code comments updated as needed

## **Review Categories & Examples**

### **🔴 Critical Issues (Must Fix)**
Issues that affect correctness, security, or system stability:

```python
# ❌ CRITICAL: SQL Injection vulnerability
def get_user_data(user_id):
    query = f"SELECT * FROM users WHERE id = {user_id}"  # NEVER do this!
    return execute_query(query)

# ✅ CORRECT: Parameterized query
def get_user_data(user_id: int) -> pd.DataFrame:
    """Get user data by ID with SQL injection protection."""
    query = "SELECT * FROM users WHERE id = %s"
    return execute_query(query, (user_id,))
```

**Review Comment**: 
> **🔴 CRITICAL - Line 15**: This code is vulnerable to SQL injection. Please use parameterized queries with placeholders instead of string formatting. Replace with `execute_query("SELECT * FROM users WHERE id = %s", (user_id,))`.

### **🟡 Major Issues (Should Fix)**
Issues that affect performance, maintainability, or best practices:

```python
# ❌ MAJOR: Inefficient pandas operation
def process_inventory(df):
    results = []
    for index, row in df.iterrows():  # Slow for large datasets
        if row['quantity'] > 0:
            results.append(row['product_id'])
    return results

# ✅ BETTER: Vectorized operation
def process_inventory(df: pd.DataFrame) -> List[str]:
    """Extract product IDs for items with positive quantity."""
    return df[df['quantity'] > 0]['product_id'].tolist()
```

**Review Comment**:
> **🟡 MAJOR - Line 23**: Using `iterrows()` is very slow for large datasets. Consider using vectorized pandas operations: `df[df['quantity'] > 0]['product_id'].tolist()`. This will be 10-100x faster.

### **🟢 Minor Issues (Nice to Have)**
Style improvements, documentation, or minor optimizations:

```python
# 🟢 MINOR: Missing type hints and docstring
def calculate_total(items):
    return sum(item.price for item in items)

# ✅ IMPROVED: With type hints and documentation
def calculate_total(items: List[Item]) -> float:
    """Calculate total price for a list of items.
    
    Args:
        items: List of Item objects with price attribute.
        
    Returns:
        Total price as float.
    """
    return sum(item.price for item in items)
```

**Review Comment**:
> **🟢 MINOR - Line 45**: Consider adding type hints and a docstring to improve code documentation and IDE support.

## **Review Response Templates**

### **For Performance Issues**
```
**Performance Concern - Line X**: This approach might be slow for large datasets. 
Consider using [specific alternative]. For reference, see our performance guidelines 
in .github/instructions/tasks/code-generation.md.
```

### **For Security Issues**
```
**Security Risk - Line X**: This could expose [specific vulnerability]. 
Please use [secure alternative] instead. This is critical for production deployment.
```

### **For Style Issues**
```
**Code Style - Line X**: This doesn't follow our PEP 8 standards. 
Suggestion: [specific improvement]. You can run `black` and `flake8` to auto-fix most style issues.
```

### **For Missing Tests**
```
**Testing - General**: This change adds new functionality but I don't see corresponding tests. 
Could you add tests covering [specific scenarios]? Our guideline is 80%+ coverage for new code.
```

### **For Good Code**
```
**✅ Great work!**: Excellent use of [specific pattern/practice]. This is exactly the kind of 
[maintainable/efficient/secure] code we want to see in our codebase.
```

## **Review Workflow Steps**

### **Step 1: Initial Review**
1. **Read the PR description** to understand the context and goals
2. **Check the diff** to see what files and functions are changed
3. **Run the code locally** if possible to test functionality
4. **Review tests** to ensure they cover the changes

### **Step 2: Systematic Code Review**
1. **Start with tests** - ensure they're comprehensive and correct
2. **Review main logic** - check correctness and efficiency
3. **Check error handling** - ensure robust exception handling
4. **Validate security** - look for vulnerabilities and best practices
5. **Assess style** - check formatting, naming, and documentation

### **Step 3: Provide Feedback**
1. **Categorize issues** by severity (Critical/Major/Minor)
2. **Be specific** with line numbers and exact suggestions
3. **Explain reasoning** behind each suggestion
4. **Acknowledge good work** where you see it
5. **Suggest resources** for learning (documentation, examples)

## **Context Management for Reviews**

### **Before Starting Review**
1. **Open Related Files**: Have the full context of changed files
2. **Check Dependencies**: Review imports and external dependencies
3. **Understand Business Logic**: Know what the code is supposed to do
4. **Review Previous Discussions**: Check PR comments and related issues

### **During Review**
1. **Use Split View**: Compare old vs new code side-by-side
2. **Test Locally**: Run the code to verify it works as expected
3. **Check Documentation**: Ensure changes are reflected in docs
4. **Validate Tests**: Run test suite to ensure nothing breaks

## **Anti-Patterns to Avoid in Reviews**

### **❌ Poor Review Practices**
- ❌ **Vague feedback**: "This looks wrong" (not actionable)
- ❌ **Nitpicking style only**: Focusing only on formatting issues
- ❌ **Personal attacks**: Criticizing the developer, not the code
- ❌ **No explanation**: Pointing out issues without explaining why
- ❌ **Approving without reading**: Rubber-stamp approvals

### **❌ Missing Critical Checks**
- ❌ **Ignoring security**: Not checking for vulnerabilities
- ❌ **Skipping performance**: Not considering scalability impact
- ❌ **No test validation**: Not verifying test coverage and quality
- ❌ **Ignoring edge cases**: Not thinking about error scenarios
- ❌ **No business validation**: Not checking if code meets requirements

## **Output Format Examples**

### **Comprehensive Review Example**

**Overall Assessment**: This PR adds inventory validation functionality. The core logic is sound, but there are some performance and security concerns to address.

**Critical Issues** 🔴
1. **Line 15 - SQL Injection Risk**: Use parameterized queries instead of string formatting
2. **Line 23 - Missing Input Validation**: Validate user_id parameter before database query

**Major Issues** 🟡  
1. **Line 45 - Performance**: Replace `iterrows()` with vectorized pandas operations
2. **Line 67 - Error Handling**: Add specific exception handling for database errors

**Minor Issues** 🟢
1. **Line 12 - Documentation**: Add docstring following Google style
2. **Line 34 - Type Hints**: Add return type annotation

**Positive Feedback** ✅
- Great use of type hints throughout most of the code
- Excellent test coverage for the happy path scenarios
- Clean separation of concerns between validation and business logic

**Suggestions for Improvement**:
- Consider adding integration tests for the database operations
- The validation logic could be extracted into a reusable utility function
- Performance could be improved by using batch operations for large datasets

**Action Items**:
- [ ] Fix SQL injection vulnerability (Critical)
- [ ] Add input validation (Critical)  
- [ ] Optimize pandas operations (Major)
- [ ] Add missing documentation (Minor)