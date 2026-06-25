from InquirerPy import prompt
from constantes import ARCHIVO_PEDIDOS
from ver_pedidos import ver_todos_los_pedidos, ver_pedidos_filtrados
from gestion_pedidos import registrar_pedido, cambiarEstadoPedido, agregarPresupuestoPedido, agregarRepuestosEncargados
from asignar_trabajos import seleccionarTecnico, seleccionarTarea
from gestion_stock import mainStock

opciones = [
    {
        "type": "list",
        "message": "Que operación vas a realizar?",
        "choices": ["Registrar nuevo pedido", "Ver Todos Los Pedidos","Ver Pedidos Filtrados","Asignar Pedido","Cambiar estado de pedido","Agregar presupuesto", "Agregar repuestos encargados", "Gestionar Stock", "Salir"],
    },
]

def menu():
    opcion = prompt(opciones)[0]

    if opcion == "Registrar nuevo pedido":
        registrar_pedido()

    elif opcion == "Ver Todos Los Pedidos":
        ver_todos_los_pedidos(ARCHIVO_PEDIDOS)

    elif opcion == "Ver Pedidos Filtrados":
        ver_pedidos_filtrados(ARCHIVO_PEDIDOS)

    elif opcion == "Asignar Pedido":
        seleccionarTecnico(seleccionarTarea())

    elif opcion == "Cambiar estado de pedido":
        cambiarEstadoPedido()

    elif opcion == "Agregar presupuesto":
        agregarPresupuestoPedido()

    elif opcion == "Agregar repuestos encargados":
        agregarRepuestosEncargados()

    elif opcion == "Gestionar Stock":
        mainStock()

    elif opcion == "Salir":
        print("Saliendo del sistema...")
        return

    else:
        print("Opción inválida.")

    menu() 

menu()