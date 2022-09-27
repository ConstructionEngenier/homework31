import pytest


@pytest.mark.django_db
def test_selection_create(client, user_token, user, ad):
    expected_response = {
        "id": 1,
        "name": "test_selection_name",
        "owner": user.id,
        "items": [ad.id]
    }

    response = client.post(
        "/selection/create/",
        {
            "name": "test_selection_name",
            "owner": user.id,
            "items": [ad.id]
        },
        content_type="application/json",
        HTTP_AUTHORIZATION="Bearer " + user_token
    )

    assert response.status_code == 201
    assert response.data == expected_response
