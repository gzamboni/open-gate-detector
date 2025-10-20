# Contributing to Open Gate Detector

Thank you for considering contributing to the Open Gate Detector project! This document provides guidelines and instructions for contributing.

## Code of Conduct

By participating in this project, you agree to abide by our [Code of Conduct](CODE_OF_CONDUCT.md).

## How Can I Contribute?

### Reporting Bugs

Bug reports help us improve the project. To report a bug:

1. Check if the bug has already been reported in the [Issues](https://github.com/gzamboni/open-gate-detector/issues)
2. If not, create a new issue using the bug report template
3. Provide as much detail as possible, including steps to reproduce, expected behavior, and your environment

### Suggesting Features

We welcome feature suggestions:

1. Check if the feature has already been suggested in the [Issues](https://github.com/gzamboni/open-gate-detector/issues)
2. If not, create a new issue using the feature request template
3. Clearly describe the feature and its potential benefits

### Pull Requests

We actively welcome pull requests:

1. Fork the repository
2. Create a new branch for your feature or bugfix (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Run the tests to ensure they pass (`pytest`)
5. Commit your changes (`git commit -m 'Add amazing feature'`)
6. Push to the branch (`git push origin feature/amazing-feature`)
7. Open a Pull Request

## Development Setup

1. Clone the repository:
   ```
   git clone https://github.com/gzamboni/open-gate-detector.git
   cd open-gate-detector
   ```

2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Run tests to ensure everything is working:
   ```
   pytest
   ```

## Coding Guidelines

### Python Style

- Follow [PEP 8](https://www.python.org/dev/peps/pep-0008/) style guidelines
- Use meaningful variable and function names
- Write docstrings for all functions, classes, and modules
- Keep functions small and focused on a single task

### Testing

- Write tests for all new features and bug fixes
- Aim for high test coverage
- Tests should be in the `tests/` directory and follow the naming convention `test_*.py`

### Commit Messages

- Use clear, descriptive commit messages
- Start with a short summary line (50 chars or less)
- Optionally followed by a blank line and a more detailed explanation
- Reference issues and pull requests where appropriate

## Review Process

All submissions require review:

1. A maintainer will review your PR
2. Changes may be requested before a PR can be merged
3. Once approved, a maintainer will merge your PR

## License

By contributing to Open Gate Detector, you agree that your contributions will be licensed under the project's [MIT License](LICENSE).
