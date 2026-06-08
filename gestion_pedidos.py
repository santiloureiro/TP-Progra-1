import json, re, tabulate
from InquirerPy import prompt, inquirer
#elementos que tiene que tener el pedido ?
#Cliente, telefono, direccion, tipo de problema,descripcion,prioridad,estado
#Voy a usar un diccionario para los datos del pedido
#Voy a usar una lista de diccionarios para guardar los pedidos
#agrego pedidos con .append

ARCHIVO_PEDIDOS = "./carpeta_archivos/pedidos.json"
ARCHIVO_TECNICOS = "./carpeta_archivos/tecnicos.json"
PRIORIDADES = ("Baja", "Media", "Alta", "Urgente")
TIPOSDETRABAJOS = ("Aire acondicionado", "Electricidad", "Soporte tecnico")
REGEXTELEFONO = r"([0-9]{2,4})(15)([0-9]{6,8})"
REGEXPEDIDOS = r"([0-9]*)"
REGEXTECNICOS = r"([A-Za-z]*)"


opciones = [
    {
        "type": "list",
        "message": "Que operación vas a realizar?",
        "choices": ["Registrar nuevo pedido", "Ver todos los pedidos", "Asignar Pedido", "Salir"],
    },
]

def registrar_pedido():
    contador_id = 0
    datos = []
    try:
        with open(ARCHIVO_PEDIDOS, "r") as pedidos:
            datos = json.load(pedidos)
            print(datos)
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
        "estado": "Pendiente"
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



def mostrar_pedido(pedido): #traigo cada seccion desde "pedido"
    print(f"ID: {pedido["id"]}")
    print(f"Cliente: {pedido["cliente"]}")
    print(f"Telefono: {pedido["telefono"]}")
    print(f"Direccion: {pedido["direccion"]}")
    print(f"Tipo: {pedido["tipo"]}")
    print(f"Descripcion: {pedido["descripcion"]}")
    print(f"Prioridad: {pedido["prioridad"]}")
    print(f"Estado: {pedido["estado"]}")


def ver_todos_los_pedidos():
    try:
        with open(ARCHIVO_PEDIDOS, "r") as pedidos:
            datos = json.load(pedidos)
            print("\nLISTA DE PEDIDOS:\n")
            if len(datos) == 0:
                print("No hay pedidos registrados.")
                return

            print(tabulate.tabulate(datos,headers="keys"))
            print()

    except Exception as e :
        print(f"No hay datos: {e}")

def ingresarTelefono(telefono):

    telefonoIngresado = telefono
    
    telefonoInvalido = re.fullmatch(REGEXTELEFONO, telefonoIngresado)

    while not telefonoInvalido:
        telefonoIngresado = input("Reingrese un telefono valido! (Ejemplo: 11-15-1234-5678): ")
        telefonoInvalido = re.fullmatch(REGEXTELEFONO, telefonoIngresado)

    return(telefonoIngresado)

def obtenerSubstringSeleccion(seleccion, patron):

    item = re.search(patron, seleccion)

    return item.group()

def seleccionarTarea():
    listaDePendientes = []

    with open(ARCHIVO_PEDIDOS, "r") as pedidos:
        datos = json.load(pedidos)
        
        for tarea in datos:
            if tarea["estado"] == "Pendiente":
                listaDePendientes.append(f"{tarea["id"]} | {tarea["descripcion"]}")
    
    tarea = inquirer.select(message="Seleccione tarea a asignar: ",choices=listaDePendientes).execute()

    return tarea

def seleccionarTecnico(tarea):

    listaDeTecnicos = []

    with open(ARCHIVO_TECNICOS, "r") as tecnicos:
        datos = json.load(tecnicos)
        
        for tecnico in datos:
            listaDeTecnicos.append(f"{tecnico["nombre"]} | {tecnico["trabajos"]}")

    tecnicoAsignado = inquirer.select(message="Seleccione tecnico: ",choices=listaDeTecnicos).execute()
    
    asignarTecnico(tecnicoAsignado, tarea)

def asignarTecnico(tecnico, tarea):

    tecnicoFiltrado = obtenerSubstringSeleccion(tecnico, REGEXTECNICOS)

    tarea = obtenerSubstringSeleccion(tarea, REGEXPEDIDOS)

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
    except:
            print("Hubo un error en la asignacion.")
    
    print(f"El tecnico {tecnicoFiltrado} ha sido asignado a la tarea {tarea}")




def main(): #funcion principal
    seguirCargando = True
    while seguirCargando: #bucle 'infinito' para poner la condicion de salida luego
        opcion = prompt(opciones)
        if opcion[0] == opciones[0]["choices"][0]:
            registrar_pedido()
        elif opcion[0] == opciones[0]["choices"][1]:
            ver_todos_los_pedidos()
        elif opcion[0] == opciones[0]["choices"][2]:
            seleccionarTecnico(seleccionarTarea())
            
        elif opcion[0] == opciones[0]["choices"][3]:
            print("Saliendo del sistema...")
            seguirCargando = False #Si el usuario elige salir, rompo el bucle para no seguir ejecutandolo
        else:
            print("Opcion invalida. Intente nuevamente.") 

main()


