## Plan: Add backend FastAPI tests in separate tests directory

TL;DR: Create a new `tests/` directory at the repository root with pytest fixtures and FastAPI endpoint coverage for `src/app.py`. Use `TestClient` and restore the in-memory activity state between tests.

**Steps**
1. Create `tests/` directory at project root.
2. Add `tests/conftest.py` with a `TestClient` fixture that imports `app` from `src.app` and a fixture to reset the `activities` dictionary before each test.
3. Add `tests/test_app.py` covering the main FastAPI behaviors using the Arrange-Act-Assert pattern:
   - root redirect behavior for `/`
   - `GET /activities` returns the activity listing
   - successful signup for an existing activity
   - duplicate signup returns HTTP 400
   - signup for missing activity returns HTTP 404
   - successful removal of a participant
   - removing a missing participant returns HTTP 404
4. Ensure tests import `src.app` correctly using the existing `pytest.ini` `pythonpath = .` configuration.
5. Optionally validate with `pytest` from the repo root.

**Relevant files**
- `/workspaces/skills-getting-started-with-github-copilot/src/app.py` — existing FastAPI app and in-memory activity state
- `/workspaces/skills-getting-started-with-github-copilot/pytest.ini` — existing pytest path config

**Verification**
1. Confirm `tests/conftest.py` fixture can import `src.app` and create `TestClient(app)`.
2. Confirm `tests/test_app.py` resets `src.app.activities` before each test to avoid cross-test state leakage.
3. Run `pytest` from the repository root and verify all new tests pass.

**Decisions**
- Use `tests/` at the repo root, separate from `src/`.
- Keep the existing `pytest.ini` configuration and do not change app import paths.
- Use the current in-memory `activities` store and reset it in tests rather than changing app implementation.
