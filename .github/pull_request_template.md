## Description
<!-- Provide a clear and concise description of your changes -->

## Type of Change
<!-- Check all that apply -->
- [ ] `feat`: New feature
- [ ] `fix`: Bug fix
- [ ] `docs`: Documentation update
- [ ] `refactor`: Code refactoring (no functional changes)
- [ ] `test`: Test updates or additions
- [ ] `chore`: Maintenance tasks (dependencies, build, config)
- [ ] `style`: Code style/formatting changes

## Scope
<!-- Which service(s) or area(s) are affected? -->
- [ ] airline-service
- [ ] shared utilities
- [ ] infrastructure (Bicep)
- [ ] CI/CD workflows
- [ ] Documentation
- [ ] Other: _________________

## Clean Architecture Compliance
<!-- Verify architectural principles are maintained -->
- [ ] Domain layer has no external dependencies (pure Python)
- [ ] Application layer depends only on domain interfaces
- [ ] Infrastructure implements domain protocols correctly
- [ ] API layer properly wires dependencies via DI
- [ ] Entities are immutable (frozen dataclasses)
- [ ] Dependencies flow inward (API → Application → Domain)

## Testing
<!-- Describe the tests you've added or updated -->
- [ ] Unit tests added/updated for domain logic
- [ ] Integration tests added/updated for API endpoints
- [ ] All tests pass locally
- [ ] Test coverage maintained or improved
- [ ] Immutability validated in entity tests

## Documentation
<!-- Ensure documentation is up-to-date -->
- [ ] Code comments added where necessary
- [ ] README updated (if applicable)
- [ ] API documentation updated (if applicable)
- [ ] Architecture diagrams updated (if applicable)

## Checklist
<!-- Complete before requesting review -->
- [ ] Code follows Clean Architecture principles
- [ ] Code follows project coding standards
- [ ] Commit messages follow Conventional Commits format
- [ ] No console.log or debug prints left in code
- [ ] No commented-out code blocks
- [ ] Branch is up-to-date with main
- [ ] CI pipeline passes

## Related Issues
<!-- Link related issues or tickets -->
Closes #
Relates to #

## Screenshots/Demo
<!-- If applicable, add screenshots or demo of the feature -->

## Additional Notes
<!-- Any additional context, concerns, or deployment notes -->
