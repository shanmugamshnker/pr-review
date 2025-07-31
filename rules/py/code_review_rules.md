# 📘 AI Code Review Rules

This markdown document defines code review rules used in the hybrid RAG + FM-based AI code reviewer.
Rules are grouped by pillar and follow a structured format: `Rule ID`, `Pattern`, `Explanation`, and `Comment Prompt`.

---

## 🛡️ Security Rules

### 🔒 SEC005: Sensitive Path or System Command Execution
- **Pattern**: Python scripts using `os.system`, `subprocess.run`, or `shutil.rmtree` to manipulate paths like `/etc/`, `C:\Windows\System32`, or `~/.ssh`
- **Explanation**: Executing destructive or privileged system commands can lead to irreversible changes or security risks, especially on production machines.
- **Comment Prompt**: "This script performs operations on sensitive paths or executes critical system commands. Ensure proper input validation, error handling, and access controls are in place. Consider restricting to safe environments only."

### 🔒 SEC002: URL Injection in Web Apps
- **Pattern**: Dynamic URLs using unsanitized query parameters, e.g., `url = request.args.get('next')`
- **Explanation**: Unvalidated user input in URLs can lead to open redirect or SSRF attacks.
- **Comment Prompt**: "Potential URL injection risk. Validate and sanitize user-controlled URL parameters."

### 🔒 SEC004: Server-Side Code Execution Risks
- **Pattern**: Use of `os.system`, `subprocess.Popen`, `eval`, or `exec` with user input
- **Explanation**: Can lead to remote code execution (RCE) vulnerabilities in Flask and similar apps.
- **Comment Prompt**: "Avoid executing user-supplied input directly in system commands. Use `shlex.quote()` and validate inputs."


### 🔒 SEC001: Hardcoded Secrets or Keys
- **Pattern**: `AKIA[0-9A-Z]{16}`, `password =`, `.env`, `secret =`, `private_key`
- **Explanation**: Hardcoded secrets are a major security risk and should be stored in a secure vault (e.g., AWS Secrets Manager).
- **Comment Prompt**: "Detected a possible hardcoded secret or credential. Consider using AWS Secrets Manager or environment variables."

### 🔒 SEC003: Use of `eval()` or `exec()`
- **Pattern**: `eval(`, `exec(`
- **Explanation**: These functions can be exploited for remote code execution.
- **Comment Prompt**: "Avoid using `eval()` or `exec()` unless absolutely necessary. Consider using `ast.literal_eval()` or safer alternatives."

---

## 📏 Python Best Practices

### 📘 PY011: Extra Blank Lines and Whitespace
- **Pattern**: Multiple consecutive blank lines, trailing spaces at line ends
- **Explanation**: Extra blank lines and trailing spaces clutter the code and create noisy diffs.
- **Comment Prompt**: "Detected unnecessary whitespace or extra blank lines. Remove to keep the code clean and consistent."

### 📘 PY012: Incorrect Spacing Around Operators
- **Pattern**: Missing or excessive spaces around `=`, `+`, `-`, etc.
- **Explanation**: Inconsistent spacing reduces readability and violates PEP8.
- **Comment Prompt**: "Fix spacing around operators to match PEP8 standards. Use a linter like `black` or `flake8` to enforce consistency."

### 📘 PY005: Silent Exception Handling
- **Pattern**: `except Exception as e:` followed by `pass` or only logging
- **Explanation**: Silently swallowing exceptions can hide bugs and delay debugging.
- **Comment Prompt**: "Avoid suppressing exceptions without handling. At least log and re-raise or handle explicitly."

### 📘 PY006: Repeated Imports in Large Files
- **Pattern**: Same import statement repeated in multiple functions
- **Explanation**: Repeated imports reduce clarity and may impact performance in large files.
- **Comment Prompt**: "This module appears to import the same library multiple times. Consolidate imports at the top."

### 📘 PY007: Debug or Dev Tools Left in Production
- **Pattern**: `import pdb`, `pdb.set_trace()`, `debug=True`, `print()` in route handlers
- **Explanation**: Debug statements should not be present in production code.
- **Comment Prompt**: "Remove debug or development tools before pushing to production. Use structured logging where needed."

### 📘 PY008: Unused Variables or Imports
- **Pattern**: Declared but unused variables or imports
- **Explanation**: Adds clutter and increases cognitive load.
- **Comment Prompt**: "Detected unused import or variable. Clean up to improve readability."

### 📘 PY009: Inconsistent Indentation or Mixed Tabs/Spaces
- **Pattern**: Mix of tabs and spaces, or inconsistent indent size
- **Explanation**: Can cause runtime errors and readability issues.
- **Comment Prompt**: "Detected inconsistent indentation. Use either tabs or spaces consistently."

### 📘 PY010: Poor Function or Variable Naming
- **Pattern**: Generic names like `temp`, `data`, `flag`, `my_func`
- **Explanation**: Poor naming reduces code clarity and hinders maintainability.
- **Comment Prompt**: "Use meaningful variable and function names to improve clarity."

### 📘 PY001: Use Logging Instead of Print Statements
- **Pattern**: `print(` used in production code
- **Explanation**: `print()` is not suitable for production diagnostics. Use the `logging` module with appropriate log levels.
- **Comment Prompt**: "Avoid using `print()` in production code. Use the `logging` module for structured logging."

### 📘 PY002: Avoid Bare Except Blocks
- **Pattern**: `except:` without specifying exception types
- **Explanation**: Bare `except` can catch unexpected errors and hide real issues.
- **Comment Prompt**: "Avoid using bare `except:`. Catch specific exceptions instead."

### 📘 PY003: Use Context Managers for File and Resource Handling
- **Pattern**: Manual open/close of files without `with` statement
- **Explanation**: Context managers ensure proper resource cleanup even in case of errors.
- **Comment Prompt**: "Use `with` statements for file operations to ensure proper resource handling."

### 📘 PY004: Avoid Mutable Default Arguments
- **Pattern**: Function signatures like `def foo(bar=[])`
- **Explanation**: Mutable default arguments retain state across function calls.
- **Comment Prompt**: "Avoid using mutable default arguments like lists or dicts. Use `None` and initialize inside the function."

---

## 🧹 Readability & Maintainability

### 🧼 READ001: Deep Nesting (>3 levels)
- **Pattern**: Nesting of control structures beyond 3 levels
- **Explanation**: Deeply nested code is harder to understand and maintain.
- **Comment Prompt**: "This block is deeply nested. Consider refactoring with early returns or helper functions."

### 🧼 READ002: Generic Variable Names
- **Pattern**: Single-letter variables (`a`, `b`, `x`) outside of math/loop context
- **Explanation**: Reduces code readability.
- **Comment Prompt**: "Use descriptive variable names to improve maintainability."

### 🧼 READ003: Missing Type Hints
- **Pattern**: Python functions without return type or param types
- **Explanation**: Type hints improve clarity and tooling support.
- **Comment Prompt**: "Consider adding type hints for this function."

### 🧼 READ004: Long Functions (>50 LOC)
- **Pattern**: Functions exceeding 50 lines
- **Explanation**: Large functions are harder to test and reason about.
- **Comment Prompt**: "This function is quite long. Consider splitting it into smaller units."

---

## ⚡ Performance & Efficiency

### 🚀 PERF001: N+1 Query Problem
- **Pattern**: DB/API calls inside loops
- **Explanation**: Inefficient and non-scalable pattern.
- **Comment Prompt**: "Detected repeated DB/API calls in a loop. Consider batching."

### 🚀 PERF002: Unnecessary Object Creation
- **Pattern**: Object creation inside hot loop
- **Explanation**: Wastes memory and CPU cycles.
- **Comment Prompt**: "Consider creating this object outside the loop and reusing it."

### 🚀 PERF003: Inefficient List Operations
- **Pattern**: Using `+=` on lists in a loop
- **Explanation**: Causes repeated memory allocation.
- **Comment Prompt**: "Prefer using `.append()` or list comprehensions over `+=` in loops."

### 🚀 PERF004: Redundant Sorting
- **Pattern**: Sorting same list multiple times
- **Explanation**: Wastes CPU.
- **Comment Prompt**: "Avoid redundant sorting. Cache the result if used multiple times."

---


