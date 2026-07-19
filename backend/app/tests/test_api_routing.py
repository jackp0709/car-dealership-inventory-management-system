from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_versioned_health_check_returns_ok() -> None:
    response = client.get("/api/v1/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_sales_routes_and_openapi_documentation_are_registered() -> None:
    schema = app.openapi()

    assert "/api/v1/sales" in schema["paths"]
    assert "/api/v1/sales/{sale_id}" in schema["paths"]
    assert set(schema["paths"]["/api/v1/sales"]) == {"get", "post"}
    assert set(schema["paths"]["/api/v1/sales/{sale_id}"]) == {"get", "put", "delete"}
    assert schema["paths"]["/api/v1/sales"]["post"]["security"]
