# Security Policy

## Supported Versions

We actively support and provide security updates for the following versions:

| Version | Supported          |
| ------- | ------------------ |
| 1.1.x   | :white_check_mark: |
| 1.0.0   | :white_check_mark: |
| < 1.0   | :x:                |

## Reporting a Vulnerability

**Please report security vulnerabilities responsibly.**

To report a security issue, please open an issue in the [Issues](https://github.com/bludrgn311/python-network-testing/issues) tab with the label "security".

### What to Include

When reporting a vulnerability, please include:
- A description of the vulnerability
- Steps to reproduce the issue
- Potential impact
- Any suggested fixes (if available)

### Response Timeline

- **Initial Response**: Within 48 hours
- **Status Update**: Within 7 days
- **Fix Timeline**: Varies based on severity

## Security Features

This project implements several security measures:

- **Input Validation**: All user inputs (hostnames, filenames, ports, counts) are validated
- **Command Injection Prevention**: Hostname sanitization prevents shell command injection
- **Path Traversal Protection**: Output filenames are sanitized to prevent directory traversal attacks
- **Resource Limits**: Ping counts (1-1000) and port numbers (1-65535) are bounded
- **SSL/TLS Verification**: HTTPS connections verify certificates by default
- **Safe Exception Handling**: Specific exception types prevent information leakage

## Known Vulnerabilities

### Code

✅ **No detected vulnerabilities** in the Python code as of the latest version.

### Container Image

The Docker container is based on Amazon Linux 2023. The following known vulnerabilities exist in the base image:

- **[CVE-2023-5752](https://scout.docker.com/vulnerabilities/id/CVE-2023-5752/)** - PIP vulnerability
  - **Status**: Pending upstream fix
  - **Impact**: Low
  - **Details**: Amazon Linux 2023 package repository currently locked to PIP v21.3.1
  - **Mitigation**: Will be addressed when AWS updates their package repository

- **[CVE-2025-8869](https://scout.docker.com/vulnerabilities/id/CVE-2025-8869/)** - PIP vulnerability
  - **Status**: Pending upstream fix
  - **Impact**: Low
  - **Details**: Amazon Linux 2023 package repository currently locked to PIP v21.3.1
  - **Mitigation**: Will be addressed when AWS updates their package repository

**Note**: These vulnerabilities are in the base image's package manager and do not affect the network testing functionality. The tool itself does not use PIP at runtime.

## Security Best Practices

When using this tool:

1. **Validate Targets**: Only test networks and hosts you have permission to test
2. **Review Output**: Check output files for sensitive information before sharing
3. **Container Security**: Run containers with minimal privileges when possible
4. **Keep Updated**: Use the latest version to benefit from security improvements
5. **Network Isolation**: Consider running tests in isolated network environments

## Changelog

### Version 1.1.x
- Added hostname validation and sanitization
- Implemented path traversal protection
- Added resource limits for ping counts and ports
- Enhanced SSL/TLS certificate verification
- Improved error handling with specific exception types

### Version 1.0.0
- Initial release with basic security measures
