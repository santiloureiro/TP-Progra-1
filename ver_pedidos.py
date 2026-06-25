import json, tabulate
from InquirerPy import inquirer
from InquirerPy.base.control import Choice

FILTROS = (
    Choice("prioridad", name="Por prioridad >"),
    Choice("tecnico", name="Por tecnico asignado >"),
    Choice("tipo", name="Por tipo >"),
    Choice("estado", name="Por estado >"),
)

def buscarOpcionesEnArchivo(operacion, pedidos):
    agregado = set()
    opciones = (pedido[operacion] for pedido in pedidos if not (pedido[operacion] in agregado or agregado.add(pedido[operacion])))
    return opciones

def filtrar_pedidos(pedidos):
    operacion = inquirer.select(message="Filtrar por:",choices=FILTROS).execute()

    opcionesDeFiltro = buscarOpcionesEnArchivo(operacion, pedidos)

    filtro = inquirer.select(message="Filtrar por:",choices=opcionesDeFiltro).execute()

    pedidosFiltrados = []

    for pedido in pedidos:
        if pedido[operacion] == filtro:
            pedidosFiltrados.append(pedido)
    print(tabulate.tabulate(pedidosFiltrados,headers="keys"))


def ver_todos_los_pedidos(archivo):
    try:
        with open(archivo, "r") as pedidos:
            datos = json.load(pedidos)
            print("\nLISTA DE PEDIDOS:\n")
            if len(datos) == 0:
                print("No hay pedidos registrados.")
                return

            print(tabulate.tabulate(datos,headers="keys"))
            print()

    except Exception as e :
        print(f"No hay datos: {e}")

def ver_pedidos_filtrados(archivo):
    with open(archivo, "r") as pedidos:
        datos = json.load(pedidos)
        filtrar_pedidos(datos)