# GitHub Copilot Instructions Organization

This document explains how Copilot instructions are organized in this project to support multi-language scalability and precise context loading.

## Instruction Hierarchy

### 1. High-Level Architecture (Language-Agnostic)
**File:** `../.github/copilot-instructions.md`

Contains universal concepts that apply regardless of programming language:
- Clean Architecture principles
- Layer boundaries and dependency rules
- SOLID principles
- API design principles (RESTful conventions)
- Testing philosophy
- Error handling strategy
- Immutability principles (conceptual)

**When loaded:** Always (root configuration)

---

### 2. Language-Specific Instructions

#### Python Language Patterns
**File:** `python.instructions.md`
**Applies to:** `**/*.py`

Python-specific implementation patterns:
- Python version requirements (3.11+)
- Type system: Protocol vs ABC, type hints
- Immutability: frozen dataclasses, `object.__setattr__()`
- PEP 8 style guidelines
- Google-style docstrings
- Python idioms and standard library usage

**When loaded:** When working with `.py` files

---

#### FastAPI Framework
**File:** `python-fastapi.instructions.md`
**Applies to:** `**/api/**/*.py, **/main.py`

FastAPI-specific patterns:
- FastAPI and Pydantic usage
- Dependency injection with `Depends()`
- Route definitions and decorators
- Request/response validation
- Exception handlers
- ASGI configuration

**When loaded:** When working with API layer or main entry point

---

#### Python Testing
**File:** `python-testing.instructions.md`
**Applies to:** `**/tests/**/*.py`

pytest and testing patterns:
- pytest framework and plugins
- Test structure (AAA pattern)
- Fixtures and factories
- Mocking strategies (prefer in-memory implementations)
- Test coverage goals

**When loaded:** When working with test files

---

### 3. Layer-Specific Instructions (Language-Agnostic)

These define architectural patterns that apply to all languages:

#### Domain Layer
**File:** `domain.instructions.md`
**Applies to:** `**/domain/**/*`

- No external dependencies rule
- Interface definitions
- Business logic encapsulation
- Domain exceptions

---

#### Application Layer
**File:** `application.instructions.md`
**Applies to:** `**/application/**/*`

- Use case orchestration
- DTO patterns
- Dependency management
- Framework independence

---

#### API Layer
**File:** `api.instructions.md`
**Applies to:** `**/api/**/*`

- HTTP concerns only
- Routing conventions
- Error handling
- Response formatting

---

#### Infrastructure Layer
**File:** `infrastructure.instructions.md`
**Applies to:** `**/infrastructure/**/*`

- Repository implementations
- External service integration
- Database access patterns

---

### 4. Technology-Specific Instructions

#### Bicep/Azure
**File:** `azure-verified-modules-bicep.instructions.md`
**Applies to:** `**/*.bicep, **/*.bicepparam`

Azure-specific infrastructure as code patterns

---

## Instruction Composition

When Copilot works on a file, it loads instructions in this order:

1. **copilot-instructions.md** (always loaded)
2. **Language-specific instructions** (e.g., `python.instructions.md` for `.py` files)
3. **Framework-specific instructions** (e.g., `python-fastapi.instructions.md` for API layer)
4. **Layer-specific instructions** (e.g., `domain.instructions.md` for domain layer files)

### Example: Working on `/domain/models.py`
Loaded instructions:
- ✅ copilot-instructions.md (architecture)
- ✅ python.instructions.md (language patterns)
- ✅ domain.instructions.md (layer rules)
- ❌ python-fastapi.instructions.md (not applicable)
- ❌ api.instructions.md (not applicable)

### Example: Working on `/api/routes.py`
Loaded instructions:
- ✅ copilot-instructions.md (architecture)
- ✅ python.instructions.md (language patterns)
- ✅ python-fastapi.instructions.md (framework)
- ✅ api.instructions.md (layer rules)
- ❌ domain.instructions.md (not applicable)

---

## Benefits of This Structure

### 1. **Multi-Language Scalability**
To add a new language (e.g., .NET, Go):
- Create `dotnet.instructions.md` or `golang.instructions.md`
- Create framework-specific files (e.g., `dotnet-aspnet.instructions.md`)
- **No changes** to copilot-instructions.md or layer-specific instructions

### 2. **Precision Loading**
Copilot only loads relevant instructions for the file being edited:
- Reduces noise and token usage
- Improves response accuracy
- Prevents conflicting guidance

### 3. **Maintainability**
Each file has a single responsibility:
- Update FastAPI patterns without touching architecture
- Update architecture without touching language specifics
- Change language patterns independently of framework

### 4. **Composition**
Instructions compose cleanly:
- High-level principles in copilot-instructions.md
- Implementation details in language/framework files
- No duplication or conflicts

---

## Adding New Instructions

### New Programming Language
1. Create `<language>.instructions.md`
2. Define `applyTo` pattern (e.g., `**/*.cs` for C#)
3. Document language-specific patterns:
   - Version requirements
   - Type system
   - Immutability patterns
   - Code style
   - Standard library usage

### New Framework
1. Create `<language>-<framework>.instructions.md`
2. Define `applyTo` pattern for framework-specific files
3. Document framework-specific patterns:
   - Dependency injection
   - Routing/handlers
   - Validation
   - Configuration

### New Layer
1. Create `<layer>.instructions.md`
2. Define `applyTo` pattern (e.g., `**/<layer>/**/*`)
3. Document layer-specific rules (language-agnostic)

---

## Best Practices

1. **Keep copilot-instructions.md language-agnostic**
   - Use pseudo-code for examples
   - Focus on concepts, not syntax

2. **Use specific applyTo patterns**
   - Ensures instructions load only when relevant
   - Prevents conflicts between languages/frameworks

3. **Avoid duplication**
   - If guidance applies to all files, put it in copilot-instructions.md
   - If specific to Python, put it in python.instructions.md
   - If specific to FastAPI, put it in python-fastapi.instructions.md

4. **Single Responsibility Principle**
   - Each instruction file should have one reason to change
   - Architecture changes → copilot-instructions.md
   - Language updates → language-specific files
   - Framework updates → framework-specific files

5. **Test instruction composition**
   - Verify correct instructions load for different file types
   - Ensure no conflicts between instruction files
   - Check that guidance remains consistent across layers
