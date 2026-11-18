import pytest

from product.factories import CategoryFactory
from product.serializers import CategorySerializer

pytestmark = pytest.mark.django_db


def test_category_serializer():
    category = CategoryFactory(title="Livros", slug="livros")
    data = CategorySerializer(category).data

    assert data["title"] == "Livros"
    assert data["slug"] == "livros"
