import pytest

from tests.factories import AdFactory
from ads.serializers import AdSerializer


@pytest.mark.django_db
def test_ads_list(client):
    ads_factories = AdFactory.create_batch(10)

    response = client.get("/ad/")

    ads = []
    for ad in ads_factories:
        ads.append({
            "id": ad.id,
            "name": ad.name,
            "author": "",
            "author_id": ad.author_id,
            "price": ad.price,
            "description": ad.description,
            "is_published": False,
            "category_id": ad.category_id,
            "image": ad.image.url if ad.image else None
        })

    expected_response = {
        "items": ads,
        "num_page": 1,
        "total": 10
    }

    assert response.status_code == 200
    assert response.json() == expected_response
