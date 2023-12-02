import datetime as dt
from unittest.mock import patch

import pytest
from requests import HTTPError

from stpmex.client import Client
from stpmex.exc import (
    AccountDoesNotExist,
    BankCodeClabeMismatch,
    ClaveRastreoAlreadyInUse,
    DuplicatedAccount,
    InvalidAccountType,
    InvalidAmount,
    InvalidField,
    InvalidFutureDateError,
    InvalidInstitution,
    InvalidPassphrase,
    InvalidRfcOrCurp,
    InvalidTrackingKey,
    MandatoryField,
    NoEntityFound,
    NoServiceResponse,
    PldRejected,
    SameAccount,
    SignatureValidationError,
    StpmexException,
)
from tests.config import EMPRESA, PKEY, PKEY_PASSPHRASE

ORDEN_PAGO_ENDPOINT = '/ordenPago/registra'
CUENTA_ENDPOINT = '/cuentaModule/fisica'


def _desc_error(desc, id):
    return dict(resultado=dict(descripcionError=desc, id=id))


@pytest.mark.vcr
def test_forbidden_without_vpn(client):
    client = Client('TAMIZI', PKEY, '12345678', demo=False)
    with pytest.raises(HTTPError) as exc_info:
        client.request('get', '/application.wadl', {})
    assert exc_info.value.response.status_code == 403


def test_incorrect_passphrase():
    with pytest.raises(InvalidPassphrase):
        Client('TAMIZI', PKEY, 'incorrect')


@pytest.mark.parametrize(
    'client_mock,endpoint,expected_exc',
    [
        (
            _desc_error('No se recibió respuesta del servicio', 0),
            ORDEN_PAGO_ENDPOINT,
            NoServiceResponse,
        ),
        (
            _desc_error('Error validando la firma', 0),
            ORDEN_PAGO_ENDPOINT,
            SignatureValidationError,
        ),
        (
            _desc_error('El campo &lt;CONCEPTO PAGO> es obligatorio', 0),
            ORDEN_PAGO_ENDPOINT,
            MandatoryField,
        ),
        (
            _desc_error(
                'La clave de rastreo {foo123} para la fecha {20200314} de '
                'la institucion {123} ya fue utilizada',
                -1,
            ),
            ORDEN_PAGO_ENDPOINT,
            ClaveRastreoAlreadyInUse,
        ),
        (
            _desc_error('La cuenta {646180257067226640} no existe ', -7),
            ORDEN_PAGO_ENDPOINT,
            AccountDoesNotExist,
        ),
        (
            _desc_error('La Institucion 90679 no es valida', -9),
            ORDEN_PAGO_ENDPOINT,
            InvalidInstitution,
        ),
        (
            _desc_error('El tipo de cuenta 3 es invalido', -11),
            ORDEN_PAGO_ENDPOINT,
            InvalidAccountType,
        ),
        (
            _desc_error('El monto {500.0} no es válido', -20),
            ORDEN_PAGO_ENDPOINT,
            InvalidAmount,
        ),
        (
            _desc_error(
                'La cuenta CLABE {6461801570} no coincide para la '
                'institucion operante {40072}',
                -22,
            ),
            ORDEN_PAGO_ENDPOINT,
            BankCodeClabeMismatch,
        ),
        (
            _desc_error('Cuenta {646180157000000000} - {MISMA_CUENTA}', -24),
            ORDEN_PAGO_ENDPOINT,
            SameAccount,
        ),
        (
            _desc_error('Clave rastreo invalida : ABC123', -34),
            ORDEN_PAGO_ENDPOINT,
            InvalidTrackingKey,
        ),
        (
            _desc_error(
                'Orden sin cuenta ordenante. Se rechaza por PLD', -200
            ),
            ORDEN_PAGO_ENDPOINT,
            PldRejected,
        ),
        (
            _desc_error('unknown code', 9999999),
            ORDEN_PAGO_ENDPOINT,
            StpmexException,
        ),
        (
            dict(descripcion='Cuenta Duplicada', id=3),
            CUENTA_ENDPOINT,
            DuplicatedAccount,
        ),
        (
            dict(descripcion='El campo NOMBRE es invalido', id=1),
            CUENTA_ENDPOINT,
            InvalidField,
        ),
        (
            dict(descripcion='rfc/curp invalido', id=1),
            CUENTA_ENDPOINT,
            InvalidRfcOrCurp,
        ),
        (
            dict(descripcion='unknown code', id=999999),
            CUENTA_ENDPOINT,
            StpmexException,
        ),
        (
            dict(
                descripcion='El campo Apellido materno '
                'obligatorio 6461801500000000',
                id=5,
            ),
            CUENTA_ENDPOINT,
            MandatoryField,
        ),
        (
            _desc_error('Firma invalida No entity found for query', 0),
            ORDEN_PAGO_ENDPOINT,
            NoEntityFound,
        ),
    ],
    indirect=['client_mock'],
)
def test_errors(
    client_mock: Client, endpoint: str, expected_exc: type
) -> None:
    with pytest.raises(expected_exc) as exc_info:
        client_mock.put(endpoint, dict(firma='{hola}'))
    exc = exc_info.value
    assert repr(exc)
    assert str(exc)


@pytest.mark.parametrize(
    'client_mock,endpoint,expected_exc',
    [
        (
            dict(mensaje='unknown code', estado=999999),
            '/efws/API/consultaOrden',
            StpmexException,
        ),
        (
            dict(
                mensaje='La fecha no puede ser mayor a la fecha actual',
                estado=8,
            ),
            '/efws/API/consultaOrden',
            InvalidFutureDateError,
        ),
    ],
    indirect=['client_mock'],
)
def test_client_efws_errors(
    client_mock: Client, endpoint: str, expected_exc: type
):
    with pytest.raises(expected_exc) as exc_info:
        client_mock.post(endpoint, dict(firma='foo'))

    exc = exc_info.value
    assert repr(exc)
    assert str(exc)


@pytest.mark.vcr
def test_account_registration(client) -> None:
    client = Client(EMPRESA, PKEY, PKEY_PASSPHRASE)
    response = client.put(CUENTA_ENDPOINT, dict(firma='{hola}'))
    assert response['id'] == 0
    assert response['descripcion'] == 'Cuenta en revisión.'


def test_prod_efws_url() -> None:
    with patch('stpmex.client.Session.request') as mock_request:
        client = Client(EMPRESA, PKEY, PKEY_PASSPHRASE)
        client.ordenes_v2.consulta_clave_rastreo_recibida(
            'foo', dt.date(2023, 10, 10)
        )

    assert mock_request.call_args[0] == (
        'post',
        'https://prod.stpmex.com/efws/API/consultaOrden',
    )
