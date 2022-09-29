from datetime import date

import pytest


@pytest.mark.django_db
def test_create_ads(client, user, category, ad):
    expected_response = {
        "id": ad.id+1,
        "name": ad.name,
        "author": user.username,
        "price": 10,
        "description": "test description",
        "is_published": False,
        "category": category.name,
        "image": None
    }

    data = {
        "name": ad.name,
        "author": user.id,
        "price": 10,
        "description": "test description",
        "is_published": False,
        "category": category.id
    }

    response = client.post(
        "/ad/create/",
        data,
        content_type="application/json"
    )

    assert response.status_code == 201
    assert response.data == expected_response
