import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data

def test_signup_and_unregister():
    # 정상 등록
    email = "testuser@mergington.edu"
    activity = "Chess Club"
    # 이미 등록되어 있으면 먼저 삭제
    client.delete(f"/activities/{activity}/unregister", params={"email": email})
    response = client.post(f"/activities/{activity}/signup", params={"email": email})
    assert response.status_code == 200
    assert f"Signed up {email}" in response.json()["message"]
    # 중복 등록 방지
    response_dup = client.post(f"/activities/{activity}/signup", params={"email": email})
    assert response_dup.status_code == 400
    # 삭제
    response_del = client.delete(f"/activities/{activity}/unregister", params={"email": email})
    assert response_del.status_code == 200
    assert f"Unregistered {email}" in response_del.json()["message"]
    # 없는 참가자 삭제 시도
    response_del2 = client.delete(f"/activities/{activity}/unregister", params={"email": email})
    assert response_del2.status_code == 404

def test_signup_invalid_activity():
    response = client.post("/activities/NonexistentActivity/signup", params={"email": "nobody@mergington.edu"})
    assert response.status_code == 404

def test_unregister_invalid_activity():
    response = client.delete("/activities/NonexistentActivity/unregister", params={"email": "nobody@mergington.edu"})
    assert response.status_code == 404
