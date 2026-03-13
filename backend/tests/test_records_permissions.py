"""
Tests for record read/write permissions.
"""

import uuid

from app.models import Record, Restriction, Role, User, UserRole, WorkStatus, WorkStatusArea
from app.utils import create_access_token, hash_password


def _create_user_with_role(db, username: str, role_name: str) -> User:
    role = db.query(Role).filter(Role.name == role_name).first()
    if role is None:
        role = Role(name=role_name, description=f"{role_name} role")
        db.add(role)
        db.flush()

    user = User(
        username=username,
        email=f"{username}@example.com",
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


def _create_record_fixture(db, created_by) -> Record:
    restriction = Restriction(name=f"none-{uuid.uuid4()}")
    area = WorkStatusArea(area=f"record-{uuid.uuid4()}")
    db.add_all([restriction, area])
    db.flush()

    workstatus = WorkStatus(status=f"running-{uuid.uuid4()}", workstatus_area_id=area.id)
    db.add(workstatus)
    db.flush()

    record = Record(
        title="Read only test record",
        description="record description",
        signature="REC-001",
        comment="comment",
        restriction_id=restriction.id,
        workstatus_id=workstatus.id,
        created_by=created_by,
    )
    db.add(record)
    db.commit()
    db.refresh(record)
    return record


def test_regular_user_can_read_record_by_id(client, db):
    regular_user = _create_user_with_role(db, "reader_user", "user")
    record = _create_record_fixture(db, regular_user.id)

    response = client.get(
        f"/api/v1/records/{record.id}",
        headers=_auth_headers_for_user(regular_user),
    )

    assert response.status_code == 200
    payload = response.json()
    assert payload["id"] == str(record.id)


def test_regular_user_is_read_only_for_records(client, db):
    regular_user = _create_user_with_role(db, "readonly_user", "user")
    record = _create_record_fixture(db, regular_user.id)
    headers = _auth_headers_for_user(regular_user)

    create_response = client.post(
        "/api/v1/records",
        headers=headers,
        json={
            "title": "Should fail",
            "restriction_id": str(record.restriction_id),
            "workstatus_id": str(record.workstatus_id),
        },
    )
    assert create_response.status_code == 403

    update_response = client.put(
        f"/api/v1/records/{record.id}",
        headers=headers,
        json={"title": "Updated"},
    )
    assert update_response.status_code == 403

    delete_response = client.delete(
        f"/api/v1/records/{record.id}",
        headers=headers,
    )
    assert delete_response.status_code == 403


def test_user_record_role_can_modify_records(client, db):
    power_user = _create_user_with_role(db, "editor_user", "user_record")
    base_record = _create_record_fixture(db, power_user.id)
    headers = _auth_headers_for_user(power_user)

    create_response = client.post(
        "/api/v1/records",
        headers=headers,
        json={
            "title": "Allowed create",
            "restriction_id": str(base_record.restriction_id),
            "workstatus_id": str(base_record.workstatus_id),
        },
    )
    assert create_response.status_code == 200
    created_id = create_response.json()["id"]

    update_response = client.put(
        f"/api/v1/records/{created_id}",
        headers=headers,
        json={"title": "Allowed update"},
    )
    assert update_response.status_code == 200

    delete_response = client.delete(
        f"/api/v1/records/{created_id}",
        headers=headers,
    )
    assert delete_response.status_code == 200
