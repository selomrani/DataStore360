---
sessionId: session-260915-141627-l24d
---

# Requirements

### Overview & Goals
When importing `ydata_profiling` in `notebooks/profiling/ydata-profiling.ipynb`, execution fails with `ModuleNotFoundError: No module named 'pkg_resources'`. The goal is to resolve this dependency issue so that data profiling reports can be generated in Jupyter notebooks and scripts without runtime errors.

### Scope
- **In Scope:**
  - Add `setuptools` (which provides `pkg_resources`) to `pyproject.toml` dependencies.
  - Update `uv.lock` and the project virtual environment.
  - Verify that `from ydata_profiling import ProfileReport` executes cleanly in `notebooks/profiling/ydata-profiling.ipynb`.
- **Out of Scope:**
  - Modifying the underlying ETL pipeline or Airflow DAG configurations.
  - Major version migrations for `ydata-profiling` or Python.

### User Stories
- As a data engineer / analyst, I want to import `ydata_profiling` inside Jupyter notebooks so that I can generate automated exploratory profiling reports for datasets.

### Functional Requirements
- `from ydata_profiling import ProfileReport` must succeed without `ModuleNotFoundError: No module named 'pkg_resources'`.
- Running the profiling notebook `notebooks/profiling/ydata-profiling.ipynb` must execute cleanly without import failures.

### Non-Functional Requirements
- Maintain compatibility with `uv` dependency management and Python `>=3.10`.

# Technical Design

### Current Implementation
- `pyproject.toml` defines project dependencies including `ydata-profiling>=4.6.0`, `pandas>=2.0.0`, etc.
- In modern Python environments created by `uv` or virtual environments lacking legacy packaging tools by default, `setuptools` is not installed by default.
- `ydata-profiling` relies internally on `pkg_resources` (a component of `setuptools`), resulting in `ModuleNotFoundError: No module named 'pkg_resources'` when imported.

### Key Decisions
- **Add `setuptools` as an explicit runtime dependency**: Rather than pinning or modifying `ydata-profiling` internals, explicitly adding `setuptools` to `dependencies` in `pyproject.toml` is the standard and cleanest resolution for packages relying on `pkg_resources`.

### Proposed Changes
- Update `pyproject.toml`:
  - Add `"setuptools"` to `[project.dependencies]`.
- Synchronize environment via `uv sync`.
- Verify notebook execution in `notebooks/profiling/ydata-profiling.ipynb`.

### File Structure
- `pyproject.toml` — Modified to include `setuptools`.
- `uv.lock` — Updated dependency lockfile.
- `notebooks/profiling/ydata-profiling.ipynb` — Verified execution.

### Risks & Mitigations
- **Risk:** Version conflicts between `setuptools` and existing packages.
  - **Mitigation:** Allow `uv` solver to pick a compatible modern version of `setuptools`.

# Testing

### Validation Approach
- Verify via command-line execution and notebook kernel execution that `pkg_resources` and `ydata_profiling` can be imported without errors.

### Key Scenarios
1. **Import Test via CLI/Python**:
   - Run `python -c "import pandas as pd; from ydata_profiling import ProfileReport; print('ydata_profiling successfully imported')"` in the virtual environment.
   - Expected result: Clean exit with status code 0 and successful output.
2. **Notebook Execution**:
   - Run cell 1 of `notebooks/profiling/ydata-profiling.ipynb`.
   - Expected result: Cell executes successfully without throwing `ModuleNotFoundError`.

### Edge Cases
- Fresh environment installation using `uv sync` properly brings in `setuptools` alongside `ydata-profiling`.

# Delivery Steps

###   Step 1: Add setuptools dependency to pyproject.toml and sync lockfile
`setuptools` is declared in `pyproject.toml` dependencies and resolved in `uv.lock`.

- Add `setuptools` to the `dependencies` list in `pyproject.toml`.
- Run `uv sync` or `uv lock` to update `uv.lock` and sync the virtual environment.

###   Step 2: Validate ydata-profiling execution in the notebook environment
The profiling notebook imports `ydata_profiling` and instantiates `ProfileReport` without `ModuleNotFoundError`.

- Clear previous error output from `notebooks/profiling/ydata-profiling.ipynb`.
- Test importing `pandas` and `from ydata_profiling import ProfileReport` in Python to verify `pkg_resources` resolves correctly.
- Execute the notebook cell to confirm clean execution.