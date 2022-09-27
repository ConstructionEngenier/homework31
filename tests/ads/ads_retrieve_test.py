import pytest

from ads.serializers import AdSerializer


@pytest.mark.django_db
def test_retrieve_ads(client, ad, user_token):

    response = client.get(
        f"/ad/{ad.id}/",
        HTTP_AUTHORIZATION="Bearer " + user_token
    )

    assert response.status_code == 200
    assert response.data == AdSerializer(ad).data
