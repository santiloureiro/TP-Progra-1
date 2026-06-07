import json
#elementos que tiene que tener el pedido ?
#Cliente, telefono, direccion, tipo de problema,descripcion,prioridad,estado
#Voy a usar un diccionario para los datos del pedido
#Voy a usar una lista de diccionarios para guardar los pedidos
#agrego pedidos con .append
ARCHIVO_PEDIDOS = "./carpeta_archivos/pedidos.json"

def mostrar_menu(): #muestro el menu de seleccion para el usuario del sistema
    print("1. Registrar nuevo pedido")
    print("2. Ver todos los pedidos")
    print("0. salir")


def main(): #funcion principal
    while True: #bucle 'infinito' para poner la condicion de salida luego
        mostrar_menu()
        opcion = input("Seleccione una opcion: ")

        if opcion == "1":

            registrar_pedido()
        elif opcion == "2":
            ver_todos_los_pedidos()
        elif opcion == "0":
            print("saliendo del sistema...")
            break #Si el usuario elige salir, rompo el bucle para no seguir ejecutandolo
        else:
            print("Opcion invalida. Intente nuevamente.") 


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
    
    print("\n REGISTRAR NUEVO PEDIDO")

    cliente = input("Nombre del cliente: ")
    telefono = input("Telefono: ")
    direccion = input("direccion: ")
    tipo = input("Tipo de problema: ")
    descripcion = input("Descripcion breve del problema: ")

    pedido = {
        "id": contador_id,
        "cliente": cliente,
        "telefono": telefono,
        "direccion": direccion,
        "tipo": tipo,
        "descripcion": descripcion,
        "prioridad": "Normal",
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
            print("\n LISTA DE PEDIDOS")
            if len(datos) == 0:
                print("No hay pedidos registrados.")
                return
            
            for pedido in datos :
                mostrar_pedido(pedido)
    except :
        print("No hay datos")
main()


