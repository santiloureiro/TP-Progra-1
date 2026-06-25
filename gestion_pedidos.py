import json, re
from InquirerPy import inquirer
from constantes import ARCHIVO_PEDIDOS, PRIORIDADES, TIPOSDETRABAJOS, REGEXID, REGEXTELEFONO, ESTADOS
from asignar_trabajos import obtenerSubstringSeleccion

def registrar_pedido():
    contador_id = 0
    datos = []
    try:
        with open(ARCHIVO_PEDIDOS, "r") as pedidos:
            datos = json.load(pedidos)
            contador_id = int(datos[-1]["id"]) + 1
    except:
        print("El archivo no existe!")
    
    print("\nREGISTRAR NUEVO PEDIDO")

    cliente = input("Nombre del cliente: ")
    telefono = ingresarTelefono(input("Ingrese Telefono (Ejemplo: 11-15-1234-5678):"))
    direccion = input("Direccion: ")
    tipo = inquirer.select(message="Seleccione Tipo de trabajo:",choices=TIPOSDETRABAJOS).execute()
    descripcion = input("Descripcion breve del problema: ")
    prioridad = inquirer.select(message="Seleccione Prioridad del trabajo: ",choices=PRIORIDADES).execute()

    pedido = {
        "id": contador_id,
        "cliente": cliente,
        "telefono": telefono,
        "direccion": direccion,
        "tipo": tipo,
        "descripcion": descripcion,
        "prioridad": prioridad,
        "estado": "Pendiente",
        "presupuesto": 0,
        "detalle_presupuesto": "Sin presupuesto cargado" #agregue dos caracteristicas nuevas ("presupuesto" y "detalle_presupuesto")
    }

    try:
        with open(ARCHIVO_PEDIDOS, "r") as pedidos:
            datos = json.load(pedidos)
    except Exception as error:
        print(f"Ocurrio un problema con el archivo: {error}")
    finally:
        datos.append(pedido)
        with open(ARCHIVO_PEDIDOS, "w") as pedidos:
            json.dump(datos, pedidos)

    print("Pedido registrado correctamente.")



def ingresarTelefono(telefono):

    telefonoIngresado = telefono
    
    telefonoInvalido = re.fullmatch(REGEXTELEFONO, telefonoIngresado)

    while not telefonoInvalido:
        telefonoIngresado = input("Reingrese un telefono valido! (Ejemplo: 11-15-1234-5678): ")
        telefonoInvalido = re.fullmatch(REGEXTELEFONO, telefonoIngresado)

    return(telefonoIngresado)

def seleccionarPedido(): #agregue esta nueva funcion para seleccionar un pedido y posteriormente usarla para cambiar estados.
    listaDePedidos = []  #la funcion seleccionartarea la usamos para asignar tecnico a los pedidos pendientes,con esta nueva funcion accedemos a cualquier pedido en cualquier estado.

    try:
        with open(ARCHIVO_PEDIDOS, "r") as pedidos:
            datos = json.load(pedidos)

            for pedido in datos:
                listaDePedidos.append(f"{pedido['id']} | {pedido['cliente']} | {pedido['descripcion']} | Estado: {pedido['estado']}")

        if len(listaDePedidos) == 0:
            print("No hay pedidos cargados.")
            return None
        
        pedidoSeleccionado = inquirer.select(
            message="Seleccione un pedido: ",
            choices=listaDePedidos
        ).execute()

        return pedidoSeleccionado
    
    except Exception as error:
        print(f"Ocurrio un problema al seleccionar el pedido: {error}")


def cambiarEstadoPedido(): #Cambiamos el estado del pedido 
    pedidoSeleccionado = seleccionarPedido()

    if pedidoSeleccionado == None:
        return
    
    idPedido = obtenerSubstringSeleccion(pedidoSeleccionado, REGEXID)

    nuevoEstado = inquirer.select(
        message="Seleccione el nuevo estado del pedido: ",
        choices=ESTADOS
    ).execute()

    try:
        with open(ARCHIVO_PEDIDOS, "r") as pedidos:
            datos = json.load(pedidos)

        pedidoEncontrado = False

        for pedido in datos:
            if str(pedido["id"]) == idPedido:
                pedido["estado"] = nuevoEstado
                pedidoEncontrado = True

        if pedidoEncontrado:
            with open(ARCHIVO_PEDIDOS, "w") as pedidos:
                json.dump(datos, pedidos)

            print(f"El pedido {idPedido} cambio su estado a: {nuevoEstado}")
        else:
            print("No se encontro el pedido.")

    except Exception as error:
        print(f"Ocurrio un problema al cambiar el estado: {error}")


def ingresarPresupuesto(): #ingresamos presupuesto
    presupuesto = input("Ingrese el monto del presupuesto: ")

    while not presupuesto.isdigit():
        presupuesto = input("Reingrese un monto valido, solo numeros: ")

    return int(presupuesto)

def agregarPresupuestoPedido(): #agregamos presupuesto
    pedidoSeleccionado = seleccionarPedido()

    if pedidoSeleccionado == None:
        return
    
    idPedido = obtenerSubstringSeleccion(pedidoSeleccionado, REGEXID)

    presupuesto = ingresarPresupuesto()
    detallePresupuesto = input("Ingrese detalle del presupuesto: ")

    try:
        with open(ARCHIVO_PEDIDOS, "r") as pedidos:
            datos = json.load(pedidos)

        pedidoEncontrado = False

        for pedido in datos:
            if str(pedido["id"]) == idPedido:
                pedido["presupuesto"] = presupuesto
                pedido["detalle_presupuesto"] = detallePresupuesto
                pedidoEncontrado = True

        if pedidoEncontrado:
            with open(ARCHIVO_PEDIDOS, "w") as pedidos:
                json.dump(datos, pedidos)

            print(f"Presupuesto agregado al pedido {idPedido}.")
        else:
            print("No se encontró el pedido.")

    except Exception as error:
        print(f"Ocurrio un problema al agregar el presupuesto: {error}")
