# Python - Security Rules

These rules guide secure Python programming and must be enforced in all PRs.

1. **Avoid `eval()` or `exec()`**
   - These functions allow arbitrary code execution. Only use if absolutely safe and sandboxed.

2. **No hardcoded credentials**
   - Use environment variables, AWS Secrets Manager, or encrypted configs.

3. **Use subprocess safely**
   - Always prefer `subprocess.run()` with `shell=False`.
   - Avoid `os.system()` or `shell=True` unless sanitized.

4. **Hashing and cryptography**
   - Avoid `md5` and `sha1`.
   - Use `secrets.token_hex()` for randomness.
   - Use `bcrypt` or `hashlib.sha256()` for hashing passwords.
