from requests import get, post, put, delete, HTTPError


def test_api():
    """
    An automated version of the manual testing I've been doing,
    testing the lifecycle of an inserted document.
    """
    student_root = "http://localhost:8000/students/"

    initial_doc = {
        "course": "Test Course",
        "email": "jdoe_test@example.com",
        "gpa": "3.0",
        "name": "Jane Doe",
    }

    try:
        # Insert a student
        response = post(student_root, json=initial_doc)
        response.raise_for_status()
        doc = response.json()
        inserted_id = doc["id"]
        print(f"Inserted document with id: {inserted_id}")
        print(
            "If the test fails in the middle you may want to manually remove the document."
        )
        assert doc["course"] == "Test Course"
        assert doc["email"] == "jdoe_test@example.com"
        assert doc["gpa"] == 3.0
        assert doc["name"] == "Jane Doe"

        # List students and ensure it's present
        response = get(student_root)
        response.raise_for_status()
        student_ids = {s["id"] for s in response.json()["students"]}
        assert inserted_id in student_ids

        # Get individual student doc
        response = get(student_root + inserted_id)
        response.raise_for_status()
        doc = response.json()
        assert doc["id"] == inserted_id
        assert doc["course"] == "Test Course"
        assert doc["email"] == "jdoe_test@example.com"
        assert doc["gpa"] == 3.0
        assert doc["name"] == "Jane Doe"

        # Update the student doc
        response = put(
            student_root + inserted_id,
            json={
                "email": "updated_email@example.com",
            },
        )
        response.raise_for_status()
        doc = response.json()
        assert doc["id"] == inserted_id
        assert doc["course"] == "Test Course"
        assert doc["email"] == "updated_email@example.com"
        assert doc["gpa"] == 3.0
        assert doc["name"] == "Jane Doe"

        # Get the student doc and check for change
        response = get(student_root + inserted_id)
        response.raise_for_status()
        doc = response.json()
        assert doc["id"] == inserted_id
        assert doc["course"] == "Test Course"
        assert doc["email"] == "updated_email@example.com"
        assert doc["gpa"] == 3.0
        assert doc["name"] == "Jane Doe"

        # Delete the doc
        response = delete(student_root + inserted_id)
        response.raise_for_status()

        # Get the doc and ensure it's been deleted
        response = get(student_root + inserted_id)
        assert response.status_code == 404
    except HTTPError as he:
        print(he.response.json())
        raise
