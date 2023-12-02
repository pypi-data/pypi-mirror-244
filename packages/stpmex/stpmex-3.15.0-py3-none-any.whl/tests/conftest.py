import datetime as dt

import pytest
import requests_mock
from clabe import generate_new_clabes

from stpmex import Client
from stpmex.resources import CuentaFisica, Orden
from stpmex.types import Pais
from tests.config import EMPRESA, PKEY, PKEY_PASSPHRASE


@pytest.fixture
def client():
    yield Client(EMPRESA, PKEY, PKEY_PASSPHRASE, demo=True)


@pytest.fixture
def client_mock(request):
    with requests_mock.mock() as m:
        m.put(requests_mock.ANY, json=request.param)
        m.post(requests_mock.ANY, json=request.param)
        yield Client(EMPRESA, PKEY, PKEY_PASSPHRASE, demo=True)


@pytest.fixture
def orden_dict():
    yield dict(
        institucionContraparte='40072',
        claveRastreo='CR1564969083',
        monto=1.2,
        tipoPago=1,
        nombreOrdenante=None,
        cuentaOrdenante='646180110400000007',
        rfcCurpOrdenante=None,
        nombreBeneficiario='Ricardo Sanchez',
        cuentaBeneficiario='072691004495711499',
        rfcCurpBeneficiario='ND',
        conceptoPago='Prueba',
        referenciaNumerica=5273144,
        topologia='T',
        medioEntrega=3,
        iva=None,
    )


@pytest.fixture
def orden(client, orden_dict):
    yield Orden(**orden_dict)


@pytest.fixture
def persona_fisica_dict():
    yield dict(
        cuenta=generate_new_clabes(1, '6461801570')[0],
        nombre='Eduardo,Marco',
        apellidoPaterno='Salvador',
        apellidoMaterno='Hernandez-Muñoz',
        rfcCurp='SAHE800416HDFABC01',
        fechaNacimiento=dt.date(1980, 4, 14),
        genero='H',
        entidadFederativa=1,
        actividadEconomica='30',
        calle='mi calle',
        numeroExterior='2',
        numeroInterior='1',
        colonia='mi colonia',
        alcaldiaMunicipio='mi alcaldia',
        cp='12345',
        paisNacimiento=Pais.MX,
        email='asdasd@domain.com',
        idIdentificacion='123123123',
    )


@pytest.fixture
def persona_moral_dict():
    yield dict(
        nombre='Tarjetas Cuenca',
        cuenta='646180157036325892',
        pais=Pais.MX,
        fechaConstitucion=dt.date(2021, 1, 1),
        rfcCurp='TCU200828RX8',
    )


@pytest.fixture
def cuenta_persona_fisica(client, persona_fisica_dict):
    yield CuentaFisica(**persona_fisica_dict)
