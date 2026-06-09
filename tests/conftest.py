from copy import deepcopy

import pytest
from fastapi.testclient import TestClient

import src.app as app_module


@pytest.fixture(scope="session")
def client():
    return TestClient(app_module.app)


@pytest.fixture(scope="session")
def activities_snapshot():
    return deepcopy(app_module.activities)


@pytest.fixture(autouse=True)
def reset_activities(activities_snapshot):
    app_module.activities.clear()
    app_module.activities.update(deepcopy(activities_snapshot))
    yield
    app_module.activities.clear()
    app_module.activities.update(deepcopy(activities_snapshot))
