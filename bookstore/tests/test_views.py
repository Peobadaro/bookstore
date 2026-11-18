import hashlib
import hmac
from unittest import mock

import pytest
from django.test import Client


def test_hello_world():
    resposta = Client().get("/hello/")

    assert resposta.status_code == 200
    assert "Hello, World!" in resposta.content.decode()


def test_update_server_nao_aceita_get():
    assert Client().get("/update_server/").status_code == 405


@mock.patch("bookstore.views._recarregar_pythonanywhere")
@mock.patch("bookstore.views.git.Repo")
def test_update_server_faz_pull_no_push_da_main(repo, recarregar):
    resposta = Client().post(
        "/update_server/",
        data={"ref": "refs/heads/main"},
        content_type="application/json",
        HTTP_X_GITHUB_EVENT="push",
    )

    assert resposta.status_code == 200
    repo.return_value.remotes.origin.pull.assert_called_once()
    recarregar.assert_called_once()


@mock.patch("bookstore.views.git.Repo")
def test_update_server_ignora_outras_branches(repo):
    resposta = Client().post(
        "/update_server/",
        data={"ref": "refs/heads/feature"},
        content_type="application/json",
    )

    assert resposta.status_code == 200
    repo.assert_not_called()


@pytest.mark.parametrize("assinatura_correta", [True, False])
@mock.patch("bookstore.views._recarregar_pythonanywhere")
@mock.patch("bookstore.views.git.Repo")
def test_update_server_confere_assinatura(repo, recarregar, settings, assinatura_correta):
    settings.WEBHOOK_SECRET = "segredo"
    corpo = b'{"ref": "refs/heads/main"}'
    chave = b"segredo" if assinatura_correta else b"errado"
    assinatura = "sha256=" + hmac.new(chave, corpo, hashlib.sha256).hexdigest()

    resposta = Client().post(
        "/update_server/",
        data=corpo,
        content_type="application/json",
        HTTP_X_HUB_SIGNATURE_256=assinatura,
    )

    assert resposta.status_code == (200 if assinatura_correta else 403)
