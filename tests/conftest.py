import copy

import pytest
from fastapi.testclient import TestClient

from src.app import app, activities as activities_dict

_original_activities = copy.deepcopy(activities_dict)


@pytest.fixture(scope="session")
def client():
    return TestClient(app)


@pytest.fixture(autouse=True)
def reset_activities():
    activities_dict.clear()
    activities_dict.update(copy.deepcopy(_original_activities))
    yield
    activities_dict.clear()
    activities_dict.update(copy.deepcopy(_original_activities))
