"""
Unittests für CSRF-Schutz auf PDF/Page-Endpunkten.
"""
import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.models import User, Role, UserRole, Record, Page, Restriction, WorkStatus, WorkStatusArea
from app.utils import hash_password, create_access_token
import uuid

@pytest.fixture
def client(db):
    # Dependency override for shared session
    def override_get_db():
        yield db
    app.dependency_overrides = { }
    app.dependency_overrides[__import__('app.database').database.get_db] = override_get_db
    with TestClient(app, base_url="http://localhost", headers={"Host": "localhost"}) as c:
        yield c
    app.dependency_overrides = { }

@pytest.fixture
def test_user_with_role(db):
    role = Role(name="admin", description="admin role")
    db.add(role)
    db.flush()
    user = User(
        username="csrfuser",
        email="csrfuser@example.com",
        hashed_password=hash_password("TestPassword123!"),
        active=True,
    )
    db.add(user)
    db.flush()
    db.add(UserRole(user_id=user.id, role_id=role.id, active=True))
    db.commit()
    db.refresh(user)
    return user

def _auth_headers_for_user(user: User) -> dict:
    token = create_access_token(str(user.id))
    return {
        "Authorization": f"Bearer {token}",
        "Host": "localhost",
    }

def _create_record_and_page(db, user_id):
    restriction = Restriction(name=f"none-{uuid.uuid4()}")
    area = WorkStatusArea(area=f"page-{uuid.uuid4()}")
    db.add_all([restriction, area])
    db.flush()
    workstatus = WorkStatus(status=f"running-{uuid.uuid4()}", workstatus_area_id=area.id)
    db.add(workstatus)
    db.flush()
    record = Record(
        title="CSRF Test Record",
        description="record description",
        signature="CSRFSignature",
        comment="comment",
        restriction_id=restriction.id,
        workstatus_id=workstatus.id,
        created_by=user_id,
    )
    db.add(record)
    db.flush()
    page = Page(
        name="CSRF Test Page",
        record_id=record.id,
        restriction_id=restriction.id,
        workstatus_id=workstatus.id,
        orgin_file="CSRFSignature/origin/test.pdf",
        current_file="CSRFSignature/current/test_current.pdf",
        active=True,
        order_by=1,
    )
    db.add(page)
    db.commit()
    db.refresh(page)
    return record, page

def test_pdf_endpoint_rejects_without_csrf(client, db, test_user_with_role):
    user = test_user_with_role
    record, page = _create_record_and_page(db, user.id)
    headers = _auth_headers_for_user(user)
    # Kein CSRF-Token im Header
    response = client.get(f"/api/v1/pages/{page.id}/pdf", headers=headers)
    assert response.status_code == 403
    assert "CSRF" in response.text

def test_pdf_endpoint_accepts_with_csrf(client, db, test_user_with_role):
    user = test_user_with_role
    record, page = _create_record_and_page(db, user.id)
    headers = _auth_headers_for_user(user)
    # Simuliere CSRF-Token im Header (Name ggf. anpassen)
    headers["X-CSRF-Token"] = "testtoken"
    # Setze Cookie direkt auf Client
    client.cookies.set("csrf_token", "testtoken")
    response = client.get(f"/api/v1/pages/{page.id}/pdf", headers=headers)
    # 404 ist ok, wenn Datei nicht existiert, aber kein 403 wegen CSRF
    assert response.status_code in (200, 404)
    if response.status_code == 403:
        assert False, "CSRF-Token wurde trotz Header/Cookie nicht akzeptiert"

def test_pdf_endpoint_rejects_with_invalid_csrf(client, db, test_user_with_role):
    user = test_user_with_role
    record, page = _create_record_and_page(db, user.id)
    headers = _auth_headers_for_user(user)
    headers["X-CSRF-Token"] = "falschtoken"
    client.cookies.set("csrf_token", "andertoken")
    response = client.get(f"/api/v1/pages/{page.id}/pdf", headers=headers)
    assert response.status_code == 403
    assert "CSRF" in response.text

def test_pdf_endpoint_rejects_without_auth(client, db):
    # Kein Auth, kein CSRF
    response = client.get("/api/v1/pages/00000000-0000-0000-0000-000000000000/pdf")
    assert response.status_code == 401 or response.status_code == 403
