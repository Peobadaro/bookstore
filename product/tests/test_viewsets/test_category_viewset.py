import pytest
from rest_framework.test import APIClient

from product.factories import CategoryFactory
from product.models import Category

pytestmark = pytest.mark.django_db
URL = "/bookstore/v1/category/"


def test_lista_categorias():
    CategoryFactory(title="Livros")
    resposta = APIClient().get(URL)

    assert resposta.status_code == 200
    assert resposta.json()["results"][0]["title"] == "Livros"


def test_cria_categoria():
    resposta = APIClient().post(
        URL, {"title": "Romance", "slug": "romance"}, format="json"
    )

    assert resposta.status_code == 201
    assert Category.objects.filter(slug="romance").exists()
