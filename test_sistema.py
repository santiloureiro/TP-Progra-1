from constantes import REGEXID
from gestion_pedidos import ingresarTelefono
from gestion_stock import ingresarCantidad, ingresarPrecio, obtenerSubstringSeleccion
from ver_pedidos import buscarOpcionesEnArchivo


def test_ingresar_cantidad_valida_devuelve_entero():
    assert ingresarCantidad("15") == 15


def test_ingresar_precio_entero_valido_devuelve_float():
    assert ingresarPrecio("120") == 120.0


def test_ingresar_telefono_valido_devuelve_mismo_telefono():
    assert ingresarTelefono("111512345678") == "111512345678"


def test_buscar_opciones_en_archivo_devuelve_valores_unicos_en_orden():
    pedidos = [
        {"prioridad": "Alta"},
        {"prioridad": "Media"},
        {"prioridad": "Alta"},
        {"prioridad": "Urgente"},
    ]

    assert list(buscarOpcionesEnArchivo("prioridad", pedidos)) == [
        "Alta",
        "Media",
        "Urgente",
    ]


def test_obtener_substring_seleccion_extrae_id():
    assert obtenerSubstringSeleccion("25 | Cambio de enchufe", REGEXID) == "25"
