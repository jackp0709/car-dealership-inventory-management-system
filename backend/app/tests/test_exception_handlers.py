from fastapi import FastAPI, HTTPException
from fastapi.testclient import TestClient

from app.core.exception_handlers import register_exception_handlers


def create_test_application() -> FastAPI:
    application = FastAPI()
    register_exception_handlers(application)

    @application.get("/missing")
    def raise_not_found() -> None:
        raise HTTPException(status_code=404, detail="Resource not found.")

    @application.get("/items/{item_id}")
    def get_item(item_id: int) -> dict[str, int]:
        return {"id": item_id}

    @application.get("/unexpected")
    def raise_unexpected_error() -> None:
        raise RuntimeError("Sensitive implementation detail")

    return application


client = TestClient(create_test_application(), raise_server_exceptions=False)


def test_http_exception_uses_standard_error_response() -> None:
    response = client.get("/missing")

    assert response.status_code == 404
    assert response.json() == {
        "success": False,
        "message": "Resource not found.",
        "errors": [],
    }


def test_validation_error_uses_standard_error_response() -> None:
    response = client.get("/items/not-an-integer")

    assert response.status_code == 422
    assert response.json()["success"] is False
    assert response.json()["message"] == "Validation failed."
    assert response.json()["errors"] == [
        {"field": "path.item_id", "message": "Input should be a valid integer, unable to parse string as an integer"}
    ]


def test_unexpected_error_hides_internal_details() -> None:
    response = client.get("/unexpected")

    assert response.status_code == 500
    assert response.json() == {
        "success": False,
        "message": "Internal server error.",
        "errors": [],
    }
