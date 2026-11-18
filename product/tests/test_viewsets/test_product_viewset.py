import pytest
from rest_framework.test import APIClient

from product.factories import CategoryFactory, ProductFactory
from product.models import Product

pytestmark = pytest.mark.django_db
URL = "/bookstore/v1/product/"


def test_lista_produtos():
    ProductFactory(title="Clean Code", price=120)
    resposta = APIClient().get(URL)

    assert resposta.status_code == 200
    assert resposta.json()["results"][0]["title"] == "Clean Code"


def test_cria_produto():
    category = CategoryFactory()
    resposta = APIClient().post(
        URL,
        {"title": "Django for APIs", "price": 80, "categories_id": [category.id]},
        format="json",
    )

    assert resposta.status_code == 201
    assert Product.objects.get(title="Django for APIs").category.count() == 1


def test_remove_produto():
    product = ProductFactory()
    resposta = APIClient().delete(f"{URL}{product.id}/")

    assert resposta.status_code == 204
    assert not Product.objects.filter(id=product.id).exists()
