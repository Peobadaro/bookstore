import pytest
from rest_framework.test import APIClient

from order.factories import OrderFactory, UserFactory
from order.models import Order
from product.factories import ProductFactory

pytestmark = pytest.mark.django_db
URL = "/bookstore/v1/order/"


def test_lista_pedidos():
    OrderFactory(product=[ProductFactory(price=30)])
    resposta = APIClient().get(URL)

    assert resposta.status_code == 200
    assert resposta.json()["results"][0]["total"] == 30


def test_cria_pedido():
    user = UserFactory()
    product = ProductFactory(price=40)
    resposta = APIClient().post(
        URL, {"user": user.id, "products_id": [product.id]}, format="json"
    )

    assert resposta.status_code == 201
    assert Order.objects.get().product.first() == product
