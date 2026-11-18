import pytest

from product.factories import CategoryFactory, ProductFactory
from product.serializers import ProductSerializer

pytestmark = pytest.mark.django_db


def test_product_serializer_mostra_categorias():
    category = CategoryFactory(title="Tecnologia")
    product = ProductFactory(title="Python Fluente", price=150, category=[category])
    data = ProductSerializer(product).data

    assert data["title"] == "Python Fluente"
    assert data["price"] == 150
    assert data["category"][0]["title"] == "Tecnologia"


def test_product_serializer_cria_produto_com_categorias():
    category = CategoryFactory()
    serializer = ProductSerializer(
        data={"title": "Django", "price": 90, "categories_id": [category.id]}
    )
    assert serializer.is_valid(), serializer.errors
    product = serializer.save()

    assert list(product.category.all()) == [category]
