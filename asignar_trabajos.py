import json, re
from InquirerPy import inquirer
from constantes import ARCHIVO_PEDIDOS, ARCHIVO_TECNICOS, REGEXTECNICOS, REGEXID

def obtenerSubstringSeleccion(seleccion, patron):

    item = re.search(patron, seleccion)

    return item.group()

def seleccionarTarea():
    listaDePendientes = []

    with open(ARCHIVO_PEDIDOS, "r") as pedidos:
        datos = json.load(pedidos)
        
        for tarea in datos:
            if tarea["estado"] == "Pendiente":
                listaDePendientes.append(f"{tarea['id']} | {tarea['descripcion']}")
    
    tarea = inquirer.select(message="Seleccione tarea a asignar: ",choices=listaDePendientes).execute()

    return tarea

def seleccionarTecnico(tarea):

    listaDeTecnicos = []

    with open(ARCHIVO_TECNICOS, "r") as tecnicos:
        datos = json.load(tecnicos)
        
        for tecnico in datos:
            listaDeTecnicos.append(f"{tecnico['nombre']} | {tecnico['trabajos']}")

    tecnicoAsignado = inquirer.select(message="Seleccione tecnico: ",choices=listaDeTecnicos).execute()
    
    asignarTecnico(tecnicoAsignado, tarea)


def marcarPedidoComoAgignado(idPedido): #esta funcion va a cambiar el estado de un "pendiente" a "asignado" automaticamente cuando le asignemos un tecnico a un pedido
    try:
        with open(ARCHIVO_PEDIDOS, "r") as pedidos:
            datos = json.load(pedidos)

        for pedido in datos:
            if str(pedido["id"]) == str(idPedido):
                pedido["estado"] = "Asignado"

        with open(ARCHIVO_PEDIDOS, "w") as pedidos:
            json.dump(datos, pedidos)

    except Exception as error:
        print(f"No se pudo actualizar el estado del pedido: {error}")
    
def asignarTecnico(tecnico, tarea):

    tecnicoFiltrado = obtenerSubstringSeleccion(tecnico, REGEXTECNICOS)

    tarea = obtenerSubstringSeleccion(tarea, REGEXID)

    try:
        datos = []
        with open(ARCHIVO_TECNICOS, "r") as tecnicos:
            datos = json.load(tecnicos)
    
            for tecnico in datos:
                if tecnicoFiltrado in tecnico["nombre"]:
                    tecnico["trabajos"].append(tarea)

        print(datos)

        with open(ARCHIVO_TECNICOS, "w") as tecnicos:
            json.dump(datos,tecnicos)

        marcarPedidoComoAgignado(tarea)  # llamo a "marcarPedidoComoAsignado" para cambiar el estado a asignado
    except:
            print("Hubo un error en la asignacion.")
    
    print(f"El tecnico {tecnicoFiltrado} ha sido asignado a la tarea {tarea}")

