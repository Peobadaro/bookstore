# Bookstore API

Projeto final do curso **Desenvolvedor Full Stack Python (EBAC)**: API REST de uma livraria feita com **Django REST Framework**, publicada no **PythonAnywhere** com **deploy automático pelo GitHub Actions** a cada commit/merge na `main`.

- API no ar: https://pedrobada.pythonanywhere.com/bookstore/v1/product/
- Página de teste: https://pedrobada.pythonanywhere.com/hello/

## Endpoints

| Método | Rota | Descrição |
|---|---|---|
| GET/POST | `/bookstore/v1/category/` | Categorias |
| GET/POST | `/bookstore/v1/product/` | Produtos (livros) |
| GET/POST | `/bookstore/v1/order/` | Pedidos (com total calculado) |
| POST | `/api-token-auth/` | Gera token de autenticação |
| POST | `/update_server/` | Webhook de deploy (git pull + reload no PythonAnywhere) |
| GET | `/hello/` | Página de verificação do deploy |

## Rodando localmente

```bash
poetry install --no-root          # ou: pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
pytest                            # testes
```

## CI/CD

- `.github/workflows/ci.yml`: lint (flake8) e testes (pytest) em todo push e pull request.
- `.github/workflows/deploy-pythonanywhere.yml`: em todo push/merge na `main`, roda os testes e, se passarem, chama `/update_server/` no PythonAnywhere, que faz `git pull` e recarrega a aplicação.

## Deploy no PythonAnywhere (resumo)

1. Console Bash: `git clone https://github.com/Peobadaro/bookstore.git`
2. `python3.10 -m venv ~/env && source ~/env/bin/activate && pip install -r ~/bookstore/requirements.txt`
3. `cd ~/bookstore && python manage.py migrate && python manage.py collectstatic --noinput`
4. Aba **Web**: *Manual configuration* → Python 3.10, *Source code* `~/bookstore`, *Virtualenv* `~/env`, e no arquivo WSGI apontar para `bookstore.settings`.
5. *Static files*: URL `/static/` → `/home/pedrobada/bookstore/staticfiles`.
