import pytest

from order.factories import OrderFactory
from order.serializers import OrderSerializer
from product.factories import ProductFactory

pytestmark = pytest.mark.django_db


def test_order_serializer_calcula_total():
    p1 = ProductFactory(price=100)
    p2 = ProductFactory(price=50)
    order = OrderFactory(product=[p1, p2])
    data = OrderSerializer(order).data

    assert data["total"] == 150
    assert len(data["product"]) == 2
