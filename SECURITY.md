# Security Policy

## Supported Versions

| Version | Supported          |
| ------- | ------------------ |
| 0.1.x   | :white_check_mark: |

## Reporting a Vulnerability

We take security seriously. If you discover a security vulnerability, please report it responsibly.

### How to Report

1. **Do NOT** open a public issue for security vulnerabilities
2. Email the maintainers directly or use GitHub's private vulnerability reporting
3. Include:
   - Description of the vulnerability
   - Steps to reproduce
   - Potential impact
   - Suggested fix (if any)

### What to Expect

- Acknowledgment within 48 hours
- Regular updates on progress
- Credit in the security advisory (if desired)

## Security Best Practices

When using this software:

1. **Never commit API keys** - Use environment variables or `.env` files
2. **Keep dependencies updated** - Run `pip install --upgrade` regularly
3. **Use virtual environments** - Isolate project dependencies
4. **Review AI-generated actions** - The assistant executes actions on your system
5. **Limit permissions** - Run with minimum required permissions

## Known Security Considerations

- This software controls mouse and keyboard - use in trusted environments
- API keys are sent to OpenAI - ensure compliance with your data policies
- Voice recognition audio is processed by Google Speech Recognition
