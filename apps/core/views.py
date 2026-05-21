from django.shortcuts import render
import requests


def users(request):
    usuarios = []
    try:
        response = requests.get('https://jsonplaceholder.typicode.com/users', timeout=10)
        response.raise_for_status()
        usuarios = response.json()
    except requests.RequestException:
        usuarios = []

    return render(request, 'core/usuarios.html', {'usuarios': usuarios})
