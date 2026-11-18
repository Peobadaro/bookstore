import glob
import hashlib
import hmac
import json
from pathlib import Path

import git
from django.conf import settings
from django.http import HttpResponse, HttpResponseForbidden
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST


def _assinatura_valida(request):
    """Confere a assinatura do GitHub quando WEBHOOK_SECRET estiver configurado."""
    if not settings.WEBHOOK_SECRET:
        return True
    assinatura = request.headers.get("X-Hub-Signature-256", "")
    esperado = "sha256=" + hmac.new(
        settings.WEBHOOK_SECRET.encode(), request.body, hashlib.sha256
    ).hexdigest()
    return hmac.compare_digest(assinatura, esperado)


def _recarregar_pythonanywhere():
    """No PythonAnywhere, alterar o arquivo WSGI recarrega a aplicação."""
    arquivos = (
        [settings.PYTHONANYWHERE_WSGI_FILE]
        if settings.PYTHONANYWHERE_WSGI_FILE
        else glob.glob("/var/www/*_pythonanywhere_com_wsgi.py")
    )
    for arquivo in arquivos:
        Path(arquivo).touch()


@csrf_exempt
@require_POST
def update(request):
    """Recebe o webhook do GitHub e atualiza o código no PythonAnywhere."""
    if not _assinatura_valida(request):
        return HttpResponseForbidden("Assinatura inválida")

    if request.headers.get("X-GitHub-Event") == "ping":
        return HttpResponse("pong")

    try:
        payload = json.loads(request.body or b"{}")
    except json.JSONDecodeError:
        payload = {}
    ref = payload.get("ref")
    if ref and ref != "refs/heads/main":
        return HttpResponse(f"Ignorado: push em {ref}")

    repo = git.Repo(settings.BASE_DIR)
    repo.remotes.origin.pull()
    _recarregar_pythonanywhere()
    return HttpResponse("Código atualizado no PythonAnywhere")


def hello_world(request):
    return render(request, "hello_world.html")
