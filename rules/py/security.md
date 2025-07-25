Avoid using eval() or exec() — dangerous with untrusted input.
Never hardcode secrets like passwords, API keys, tokens.
Use subprocess.run() with shell=False for external calls.
Validate file paths to prevent path traversal attacks.
Use secrets or hashlib with SHA-256+ for cryptographic needs.
