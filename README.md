# TP Programacion 1

Sistema de gestion de pedidos tecnicos desarrollado en Python para administrar solicitudes de trabajo, asignacion de tecnicos, presupuestos y stock de repuestos.

## Integrantes

- Santiago Loureiro
- Juan Bautista Allegrino
- Tomas Dominguez

## Descripcion general

La aplicacion funciona desde consola mediante menus interactivos. Permite registrar pedidos de clientes, consultar pedidos cargados, filtrarlos por distintos criterios, asignar tecnicos, cambiar estados, agregar presupuestos y administrar un inventario de repuestos.

Los datos se guardan en archivos JSON dentro de la carpeta `carpeta_archivos`, por lo que la informacion persiste entre ejecuciones del programa.

## Librerias utilizadas

- `json`: lectura y escritura de datos en formato JSON.
- `re`:  Herramientas para el uso de Expresiones regulares.
- `InquirerPy`: menus interactivos en consola.
- `tabulate`: visualizacion de tablas en consola.

Para instalar las dependencias externas:

```
pip install InquirerPy tabulate
```

## Como ejecutar el sistema

Desde la raiz del proyecto:

```
python main.py
```

El archivo `main.py` abre el menu principal y permite acceder a todas las funcionalidades del sistema.

## Modulos del sistema

### `main.py`

Es el punto de entrada de la aplicacion.

Responsabilidades:

- Muestra el menu principal.
- Conecta las opciones del usuario con los modulos correspondientes.
- Permite acceder a:
  - Registro de nuevos pedidos.
  - Visualizacion de pedidos.
  - Filtros de pedidos.
  - Asignacion de pedidos a tecnicos.
  - Cambio de estado de pedidos.
  - Carga de presupuestos.
  - Gestion de stock.
  - Salida del sistema.

Posibilidades:

- Centralizar nuevas opciones del sistema.
- Agregar nuevos modulos sin modificar demasiado la logica interna de cada funcionalidad.
- Funcionar como menu general para futuras areas, por ejemplo reportes, gestion de clientes o gestion de tecnicos.

### `gestion_pedidos.py`

Administra la carga y modificacion de pedidos.

Responsabilidades:

- Registrar nuevos pedidos.
- Validar telefonos ingresados.
- Seleccionar pedidos existentes.
- Cambiar el estado de un pedido.
- Agregar presupuesto y detalle de presupuesto a un pedido.
- Guardar los cambios en `pedidos.json`.

Datos principales de un pedido:

- `id`: identificador numerico.
- `cliente`: nombre del cliente.
- `telefono`: telefono de contacto.
- `direccion`: domicilio del trabajo.
- `tipo`: rubro del trabajo.
- `descripcion`: descripcion breve del problema.
- `prioridad`: nivel de urgencia.
- `estado`: estado actual del pedido.
- `presupuesto`: monto presupuestado.
- `detalle_presupuesto`: descripcion del presupuesto.

Posibilidades:

- Registrar solicitudes nuevas con estado inicial `Pendiente`.
- Actualizar el ciclo de vida del pedido mediante estados.
- Cargar informacion economica asociada al trabajo.
- Extender la informacion del pedido con fechas, observaciones, materiales usados o historial de cambios.

### `ver_pedidos.py`

Se encarga de mostrar pedidos cargados.

Responsabilidades:

- Mostrar todos los pedidos en formato de tabla.
- Filtrar pedidos por:
  - Prioridad.
  - Tipo.
  - Estado.
- Obtener automaticamente las opciones disponibles para cada filtro segun los datos existentes.

Posibilidades:

- Consultar rapidamente el estado general del trabajo.
- Ver solo los pedidos relevantes segun prioridad, tipo o estado.
- Agregar nuevos filtros, por ejemplo por cliente, tecnico, direccion o rango de presupuesto.
- Generar reportes a partir de los pedidos ya cargados.

### `asignar_trabajos.py`

Gestiona la asignacion de tareas pendientes a tecnicos.

Responsabilidades:

- Buscar pedidos con estado `Pendiente`.
- Mostrar una lista de tareas pendientes.
- Mostrar tecnicos disponibles desde `tecnicos.json`.
- Asignar el ID del pedido seleccionado al listado de trabajos del tecnico.
- Cambiar automaticamente el estado del pedido asignado.
- Extraer IDs y nombres desde las opciones seleccionadas en consola.

Datos principales de un tecnico:

- `nombre`: nombre del tecnico.
- `telefono`: telefono de contacto.
- `tipoDeTrabajos`: especialidad o rubro.
- `trabajos`: lista de IDs de pedidos asignados.
- `vehiculoAsignado`: vehiculo disponible para realizar trabajos.

Posibilidades:

- Distribuir tareas entre tecnicos.
- Mantener un registro de trabajos asignados por tecnico.
- Mejorar la asignacion segun especialidad, carga de trabajo o vehiculo disponible.
- Agregar validaciones para evitar asignaciones duplicadas.

### `gestion_stock.py`

Administra el inventario de repuestos.

Responsabilidades:

- Registrar nuevos repuestos.
- Ver todo el stock en formato de tabla.
- Modificar repuestos existentes.
- Eliminar repuestos.
- Validar cantidades y precios.
- Guardar los cambios en `stock.json`.

Datos principales de un repuesto:

- `id`: identificador numerico.
- `nombre`: nombre del repuesto.
- `categoria`: categoria del repuesto.
- `cantidad`: unidades disponibles.
- `precio`: precio unitario.

Acciones disponibles:

- Registrar nuevo repuesto.
- Ver todo el stock.
- Modificar:
  - Cantidad.
  - Precio.
  - Nombre.
  - Categoria.
- Eliminar repuesto con confirmacion previa.

Posibilidades:

- Llevar control basico de inventario.
- Consultar materiales disponibles antes de realizar trabajos.
- Ampliar el modulo para descontar stock al finalizar pedidos.
- Agregar alertas de stock bajo.
- Calcular costos de repuestos para presupuestos.

## Archivos de datos

### `carpeta_archivos/pedidos.json`

Almacena todos los pedidos registrados. Es utilizado por:

- `gestion_pedidos.py`
- `ver_pedidos.py`
- `asignar_trabajos.py`

### `carpeta_archivos/tecnicos.json`

Almacena los tecnicos disponibles y sus trabajos asignados. Es utilizado por:

- `asignar_trabajos.py`

### `carpeta_archivos/stock.json`

Almacena los repuestos disponibles. Es utilizado por:

- `gestion_stock.py`

## Flujo de uso sugerido

1. Ejecutar `python main.py`.
2. Registrar un nuevo pedido con los datos del cliente.
3. Consultar pedidos para revisar la carga.
4. Asignar un pedido pendiente a un tecnico.
5. Cambiar el estado del pedido segun avance el trabajo.
6. Agregar presupuesto si corresponde.
7. Gestionar el stock de repuestos cuando se necesite registrar, modificar o eliminar materiales.

## Posibles mejoras/Limitaciones

- Agregar gestion completa de tecnicos desde el menu.
- Evitar que un mismo pedido se asigne dos veces al mismo tecnico.
- Relacionar stock con pedidos para descontar repuestos utilizados.
- Agregar fechas de creacion, asignacion y finalizacion.
- Crear reportes por prioridad, estado, tecnico o tipo de trabajo.
