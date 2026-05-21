from django.conf import settings
import requests


class ExchangeRateServiceError(Exception):
    def __init__(self, code, message):
        super().__init__(message)
        self.code = code
        self.message = message


def get_exchange_rate(target_currency):
    api_key = settings.EXCHANGERATE_API_KEY
    base_url = settings.EXCHANGERATE_BASE_URL.rstrip('/')
    source_currency = settings.EXCHANGERATE_SOURCE_CURRENCY
    currency = (target_currency or settings.EXCHANGERATE_TARGET_CURRENCY).upper()

    if not api_key:
        raise ExchangeRateServiceError(
            code='missing_api_key',
            message='No se configuro EXCHANGERATE_API_KEY.',
        )

    url = f'{base_url}/{api_key}/latest/{source_currency}'

    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
    except requests.exceptions.HTTPError as exc:
        status_code = getattr(response, 'status_code', None)
        if status_code in [401, 403]:
            raise ExchangeRateServiceError(
                code='authentication_error',
                message='La API de tipo de cambio rechazo la autenticacion.',
            ) from exc
        raise ExchangeRateServiceError(
            code='upstream_http_error',
            message='La API de tipo de cambio devolvio un error HTTP.',
        ) from exc
    except requests.exceptions.ConnectionError as exc:
        raise ExchangeRateServiceError(
            code='connection_error',
            message='No se pudo conectar con la API de tipo de cambio.',
        ) from exc
    except requests.exceptions.Timeout as exc:
        raise ExchangeRateServiceError(
            code='timeout_error',
            message='La API de tipo de cambio tardo demasiado en responder.',
        ) from exc
    except requests.exceptions.RequestException as exc:
        raise ExchangeRateServiceError(
            code='request_error',
            message='Error inesperado al consultar la API de tipo de cambio.',
        ) from exc

    try:
        data = response.json()
    except ValueError as exc:
        raise ExchangeRateServiceError(
            code='invalid_json',
            message='La API de tipo de cambio devolvio una respuesta invalida.',
        ) from exc

    if data.get('result') == 'error':
        provider_error = (data.get('error-type') or 'unknown_error').lower()
        if provider_error == 'invalid-key':
            raise ExchangeRateServiceError(
                code='authentication_error',
                message='La API key de tipo de cambio no es valida.',
            )
        raise ExchangeRateServiceError(
            code=f'provider_{provider_error.replace("-", "_")}',
            message=f'La API de tipo de cambio reporto el error: {provider_error}.',
        )

    conversion_rates = data.get('conversion_rates', {})
    rate = conversion_rates.get(currency)
    if rate is None:
        raise ExchangeRateServiceError(
            code='target_currency_not_found',
            message=f'No se encontro tasa de conversion para {currency}.',
        )

    return rate, currency
