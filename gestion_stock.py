import json, re, tabulate
from InquirerPy import prompt, inquirer

ARCHIVO_STOCK = "./carpeta_archivos/stock.json"
CATEGORIAS_STOCK = ("Aire acondicionado", "Electricidad", "Soporte tecnico", "General")
REGEXCANTIDAD = r"([0-9]+)"
REGEXPRECIO = r"([0-9]+(\.[0-9]+)?)"

opciones = [
    {
        "type": "list",
        "message": "Que operación vas a realizar en el Stock?",
        "choices": ["Registrar nuevo repuesto", "Salir"],
    },
]

def registrar_repuesto():
    contador_id = 0
    datos = []
    
    try:
        with open(ARCHIVO_STOCK, "r") as stock:
            datos = json.load(stock)
            if len(datos) > 0:
                contador_id = int(datos[-1]["id"]) + 1
    except:
        print("El archivo no existe! Se creara uno nuevo.")
    
    print("\nREGISTRAR NUEVO REPUESTO")

    nombre = input("Nombre del repuesto: ")
    categoria = inquirer.select(message="Seleccione Categoria:", choices=CATEGORIAS_STOCK).execute()
    cantidad = ingresarCantidad(input("Ingrese Cantidad inicial (Ejemplo: 10): "))
    precio = ingresarPrecio(input("Ingrese Precio unitario (Ejemplo: 2500 o 2500.50): "))

    repuesto = {
        "id": contador_id,
        "nombre": nombre,
        "categoria": categoria,
        "cantidad": cantidad,
        "precio": precio
    }

    try:
        with open(ARCHIVO_STOCK, "r") as stock:
            datos = json.load(stock)
    except Exception as error:
        print(f"Ocurrio un problema con el archivo: {error}")
    finally:
        datos.append(repuesto)
        with open(ARCHIVO_STOCK, "w") as stock:
            json.dump(datos, stock, indent=4)

    print("Repuesto registrado correctamente.\n")

def ingresarCantidad(cantidad):
    cantidadIngresada = cantidad
    cantidadInvalida = re.fullmatch(REGEXCANTIDAD, cantidadIngresada)

    while not cantidadInvalida:
        cantidadIngresada = input("Reingrese una cantidad valida! (Ejemplo: 15): ")
        cantidadInvalida = re.fullmatch(REGEXCANTIDAD, cantidadIngresada)

    return int(cantidadIngresada)

def ingresarPrecio(precio):
    precioIngresado = precio
    precioInvalido = re.fullmatch(REGEXPRECIO, precioIngresado)

    while not precioInvalido:
        precioIngresado = input("Reingrese un precio valido! (Ejemplo: 1500 o 1500.50): ")
        precioInvalido = re.fullmatch(REGEXPRECIO, precioIngresado)

    return float(precioIngresado)

def main(): 
    seguirCargando = True
    while seguirCargando: 
        opcion = prompt(opciones)
        if opcion[0] == opciones[0]["choices"][0]:
            registrar_repuesto()
        elif opcion[0] == opciones[0]["choices"][1]:
            print("Saliendo del sistema...")
            seguirCargando = False 
        else:
            print("Opcion invalida. Intente nuevamente.") 

if __name__ == "__main__":
    main()