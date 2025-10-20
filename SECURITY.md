# Security Policy

## Supported Versions

Currently, we support security updates for the following versions:

| Version | Supported          |
| ------- | ------------------ |
| 1.x.x   | :white_check_mark: |

## Reporting a Vulnerability

We take the security of Open Gate Detector seriously. If you believe you've found a security vulnerability, please follow these steps:

1. **Do not disclose the vulnerability publicly**
2. **Email the details to security@example.com** (replace with your actual security contact)
   - Provide a detailed description of the vulnerability
   - Include steps to reproduce the issue
   - Attach any proof-of-concept code if applicable
   - Let us know how you'd like to be credited (if desired)

## What to Expect

- We will acknowledge receipt of your vulnerability report within 48 hours
- We will provide an initial assessment of the report within 5 business days
- We aim to release a fix for verified vulnerabilities within 30 days
- We will keep you informed of our progress throughout the process

## Security Measures

The Open Gate Detector implements several security measures:

1. **API Authentication**: All API endpoints are protected with Bearer token authentication
2. **Input Validation**: All user inputs are validated before processing
3. **Dependency Scanning**: Regular automated scanning for vulnerabilities in dependencies
4. **Code Reviews**: All code changes undergo security-focused code reviews

## Security Best Practices for Users

When deploying Open Gate Detector:

1. **Use Strong API Tokens**: Set a strong, unique API token using the `API_TOKEN` environment variable
2. **Secure Network Access**: Restrict network access to the API service
3. **Regular Updates**: Keep the application and its dependencies up to date
4. **Monitor Logs**: Regularly review logs for suspicious activity

## Disclosure Policy

- We follow responsible disclosure principles
- Security issues will be disclosed after a fix has been released
- Credit will be given to the reporter (unless anonymity is requested)
