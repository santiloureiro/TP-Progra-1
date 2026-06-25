import json, re, tabulate
from InquirerPy import prompt, inquirer
from constantes import ARCHIVO_STOCK, CATEGORIAS_STOCK, REGEXPRECIO, REGEXID

opciones = [
    {
        "type": "list",
        "message": "Que operación vas a realizar en el Stock?",
        "choices": ["Registrar nuevo repuesto", "Ver todo el stock", "Modificar repuesto", "Eliminar repuesto", "Salir"],
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
        print("El archivo no existe! Se creara uno nuevo al guardar.")
    
    print("\n--- REGISTRAR NUEVO REPUESTO ---")

    nombre = input("Nombre del repuesto: ")
    categoria = inquirer.select(message="Seleccione Categoria:", choices=CATEGORIAS_STOCK).execute()
    cantidad = ingresarCantidad(input("Ingrese Cantidad inicial: "))
    precio = ingresarPrecio(input("Ingrese Precio unitario: "))

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
    except Exception:
        pass
    finally:
        datos.append(repuesto)
        with open(ARCHIVO_STOCK, "w") as stock:
            json.dump(datos, stock, indent=4)

    print("✅ Repuesto registrado correctamente.\n")

def ingresarCantidad(cantidad):
    cantidadIngresada = cantidad
    cantidadInvalida = re.fullmatch(REGEXID, cantidadIngresada)

    while not cantidadInvalida:
        cantidadIngresada = input("Reingrese una cantidad valida!: ")
        cantidadInvalida = re.fullmatch(REGEXID, cantidadIngresada)

    return int(cantidadIngresada)


def ingresarPrecio(precio):
    precioIngresado = precio
    precioInvalido = re.fullmatch(REGEXPRECIO, precioIngresado)

    while not precioInvalido:
        precioIngresado = input("Reingrese un precio valido!: ")
        precioInvalido = re.fullmatch(REGEXPRECIO, precioIngresado)

    return float(precioIngresado)

def ver_todo_el_stock():
    try:
        with open(ARCHIVO_STOCK, "r") as stock:
            datos = json.load(stock)
            print("\n--- INVENTARIO DE STOCK ---\n")
            if len(datos) == 0:
                print("No hay repuestos registrados en el stock.")
                return

            print(tabulate.tabulate(datos, headers="keys"))
            print()

    except Exception as e:
        print(f"No hay datos o el archivo no existe: {e}\n")


def modificar_repuesto():
    try:
        with open(ARCHIVO_STOCK, "r") as stock:
            datos = json.load(stock)
            
        if len(datos) == 0:
            print("No hay repuestos registrados para modificar.")
            return

        lista_repuestos = []
        for item in datos:
            lista_repuestos.append(f"{item['id']} | {item['nombre']} (Stock: {item['cantidad']})")
            
        lista_repuestos.append("Volver atrás")
            
        seleccion = inquirer.select(
            message="Seleccione el repuesto a modificar:", 
            choices=lista_repuestos
        ).execute()
        
        if seleccion == "Volver atrás":
            print("Operación cancelada.\n")
            return
        
        id_str = obtenerSubstringSeleccion(seleccion, REGEXID)
        id_seleccionado = int(id_str)
        
        indice = 0
        for i, repuesto in enumerate(datos):
            if repuesto["id"] == id_seleccionado:
                indice = i
                break
                
        campos = ["Cantidad", "Precio", "Nombre", "Categoria", "Cancelar"]
        campo_elegido = inquirer.select(
            message=f"¿Qué deseas modificar de '{datos[indice]['nombre']}'?", 
            choices=campos
        ).execute()
        
        if campo_elegido == "Cantidad":
            nueva_cant = ingresarCantidad(input(f"Nueva cantidad (Actual: {datos[indice]['cantidad']}): "))
            datos[indice]["cantidad"] = nueva_cant
            
        elif campo_elegido == "Precio":
            nuevo_precio = ingresarPrecio(input(f"Nuevo precio (Actual: {datos[indice]['precio']}): "))
            datos[indice]["precio"] = nuevo_precio
            
        elif campo_elegido == "Nombre":
            nuevo_nombre = input(f"Nuevo nombre (Actual: {datos[indice]['nombre']}): ")
            datos[indice]["nombre"] = nuevo_nombre
            
        elif campo_elegido == "Categoria":
            nueva_categoria = inquirer.select(message="Nueva categoría:", choices=CATEGORIAS_STOCK).execute()
            datos[indice]["categoria"] = nueva_categoria
            
        elif campo_elegido == "Cancelar":
            print("Modificación cancelada.\n")
            return

        with open(ARCHIVO_STOCK, "w") as stock:
            json.dump(datos, stock, indent=4)
            
        print("✅ Repuesto modificado correctamente.\n")

    except Exception as e:
        print(f"Ocurrió un error al modificar: {e}\n")


def eliminar_repuesto():
    try:
        with open(ARCHIVO_STOCK, "r") as stock:
            datos = json.load(stock)
            
        if len(datos) == 0:
            print("No hay repuestos registrados para eliminar.")
            return

        lista_repuestos = []
        for item in datos:
            lista_repuestos.append(f"{item['id']} | {item['nombre']} (Stock: {item['cantidad']})")
            
        lista_repuestos.append("Volver atrás")
            
        seleccion = inquirer.select(
            message="Seleccione el repuesto a ELIMINAR:", 
            choices=lista_repuestos
        ).execute()
        
        if seleccion == "Volver atrás":
            print("Operación cancelada.\n")
            return
        
        id_str = obtenerSubstringSeleccion(seleccion, REGEXID)
        id_seleccionado = int(id_str)
        
        indice = 0
        for i, repuesto in enumerate(datos):
            if repuesto["id"] == id_seleccionado:
                indice = i
                break
        
        repuesto_a_eliminar = datos[indice]

        if repuesto_a_eliminar["cantidad"] > 0:
            print(f"\n⚠️ ¡ATENCIÓN! Todavía hay {repuesto_a_eliminar['cantidad']} unidades de este repuesto en stock.")
            
        confirmacion = inquirer.confirm(
            message=f"¿Estás completamente seguro de eliminar '{repuesto_a_eliminar['nombre']}' del sistema?",
            default=False
        ).execute()

        if confirmacion:
            datos.pop(indice) 
            
            with open(ARCHIVO_STOCK, "w") as stock:
                json.dump(datos, stock, indent=4)
            print("🗑️ Repuesto eliminado correctamente.\n")
        else:
            print("Eliminación cancelada. El repuesto está a salvo.\n")

    except Exception as e:
        print(f"Ocurrió un error al eliminar: {e}\n")

def obtenerSubstringSeleccion(seleccion, patron):
    item = re.search(patron, seleccion)
    return item.group()


def mainStock(): 
    seguirCargando = True
    while seguirCargando: 
        opcion = prompt(opciones)
        
        if opcion[0] == opciones[0]["choices"][0]:
            registrar_repuesto()
            
        elif opcion[0] == opciones[0]["choices"][1]:
            ver_todo_el_stock()

        elif opcion[0] == opciones[0]["choices"][2]:
            modificar_repuesto()
            
        elif opcion[0] == opciones[0]["choices"][3]:
            eliminar_repuesto()
            
        elif opcion[0] == opciones[0]["choices"][4]:
            print("Saliendo del sistema de stock...")
            seguirCargando = False 
            
        else:
            print("Opcion invalida. Intente nuevamente.") 