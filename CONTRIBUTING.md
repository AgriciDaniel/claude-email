# Contributing to Claude Email

Thank you for your interest in contributing to Claude Email!

## Reporting Bugs

Please use [GitHub Issues](https://github.com/AgriciDaniel/claude-email/issues) to report bugs. Include:

- Steps to reproduce the issue
- Expected vs actual behavior
- Claude Code version and OS
- Relevant error messages or output

## Suggesting Features

Use [GitHub Discussions](https://github.com/AgriciDaniel/claude-email/discussions) for feature suggestions and questions. This keeps the Issues tracker focused on bugs.

## Pull Requests

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/your-feature`)
3. Make your changes
4. Test your changes by running the install script and verifying skill activation
5. Commit with a clear message (`git commit -m "feat: add your feature"`)
6. Push to your fork (`git push origin feature/your-feature`)
7. Open a Pull Request against `main`

## Code Style

- **SKILL.md files**: Follow the [Agent Skills open standard](https://agentskills.io) with YAML frontmatter
- **Python scripts**: Include docstrings, CLI interface, and JSON output format
- **Naming**: Use kebab-case for skill directories (e.g., `email-check`)
- **Size limits**: Keep SKILL.md files under 500 lines, reference files under 200 lines

## Commit Messages

Follow [Conventional Commits](https://www.conventionalcommits.org/):

- `feat:` new feature
- `fix:` bug fix
- `docs:` documentation changes
- `refactor:` code restructuring

## License

By contributing, you agree that your contributions will be licensed under the MIT License.
