import pytest

def pytest_configure(config):
    """Konfiguracja pytest"""
    config.addinivalue_line(
        "markers", "slow: marks tests as slow (deselect with '-m \"not slow\"')"
    )

@pytest.fixture(scope="session")
def test_database_path():
    """Ścieżka do bazy testowej"""
    import os
    return os.path.join(os.path.dirname(__file__), '..', 'data', 'test_database.db')