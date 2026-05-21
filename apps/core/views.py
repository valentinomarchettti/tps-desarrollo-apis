from django.shortcuts import render
import requests


def users(request):
    usuarios = []
    mensaje_error = None
    url = 'https://jsonplaceholder.typicode.com/users'

    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        usuarios = response.json()
    except requests.exceptions.HTTPError:
        mensaje_error = 'La API externa devolvio un error HTTP.'
        usuarios = []
    except requests.exceptions.ConnectionError:
        mensaje_error = 'No se pudo conectar con la API externa.'
        usuarios = []
    except requests.exceptions.Timeout:
        mensaje_error = 'La API externa tardo demasiado en responder.'
        usuarios = []
    except requests.exceptions.RequestException:
        mensaje_error = 'Ocurrio un error al consultar la API externa.'
        usuarios = []

    return render(
        request,
        'core/usuarios.html',
        {
            'usuarios': usuarios,
            'mensaje_error': mensaje_error,
        },
    )
