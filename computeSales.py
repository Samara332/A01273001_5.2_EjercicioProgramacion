import sys
import time
import json


class computeSales:
    """El siguiente codigo se encarga de calcular las ventas de determinados productos , requiere de dos entradas de archivos JSON para funcionar"""

    def __init__(self):
        """Inicializa la computeSales con listas vacías de warnings y nombres de archivos."""
        self.warnings = {}
        self.nombres_archivos = []

    def leer_archivo(self, ruta: str) -> list:
        """Lee los datos de un archivo JSON.

        Se le pasa como argumento:
            ruta (str): La ubicación del archivo JSON.

        Regresa:
            list: Los datos leídos del archivo JSON.
        """
        try:
            with open(ruta, encoding='utf8') as f:
                datos = json.load(f)
        except FileNotFoundError:
            print(f'Error: No existe ese archivo {ruta}.')
            return []
        return datos

    def encontrar_producto(self, nombre_producto: str, lista_productos: list) -> dict:
        """Encuentra un producto por su nombre en la lista de productos.

        Args:
            nombre_producto (str): El nombre del producto a buscar.
            lista_productos (list): La lista de productos en la que buscar.

        Returns:
            dict: El producto si se encuentra, de lo contrario un diccionario vacío.
        """
        for producto in lista_productos:
            if producto.get('nombre') == nombre_producto:
                return producto
        return {}

    def calcular_ventas(self, lista_productos: list, ventas: list,
                        nombre_archivo: str) -> float:
        """Calcula las ventas totales basadas en la lista de productos y los datos de ventas.

        Args:
            lista_productos (list): La lista de productos.
            ventas (list): Los datos de ventas.
            nombre_archivo (str): El nombre del archivo que se está procesando.

        Returns:
            float: El monto total de ventas.
        """
        total = 0
        self.warnings[nombre_archivo] = []
        for venta in ventas:
            producto = self.encontrar_producto(venta.get('Producto'), lista_productos)
            if not producto:
                self.warnings[nombre_archivo].append(
                    f'Producto "{venta.get("Producto")}" no encontrado')
                continue
            total += venta.get('Cantidad', 0) * producto.get('precio', 0)
        return total

    def escribir_a_archivo(self, resultados: str) -> None:
        """Guarda los resultados en un archivo llamado ResultadosVentas.txt.

        Args:
            resultados (str): Los resultados a escribir en el archivo.
        """
        with open('ResultadosVentas.txt', 'w', encoding='utf8') as f:
            f.write(resultados)

    def leer_archivos_en_pares(self) -> list:
        """Lee pares de archivos de los argumentos de la línea de comandos y devuelve sus datos.

        Returns:
            list: Una lista que contiene pares de listas de productos y datos de ventas.
        """
        datos = []
        for i in range(0, len(sys.argv)-1, 2):
            archivo_lista_productos, archivo_ventas = sys.argv[i+1:i+3]
            if 'ListaProductos' in archivo_ventas:
                archivo_lista_productos, archivo_ventas = archivo_ventas, archivo_lista_productos
            lista_productos = self.leer_archivo(archivo_lista_productos)
            ventas = self.leer_archivo(archivo_ventas)
            self.nombres_archivos.append({'productos': archivo_lista_productos,
                                          'ventas': archivo_ventas})
            datos.append([lista_productos, ventas])
        return datos

    def calcular(self):
        """Calcula las ventas totales a partir de los archivos de entrada y guarda los resultados en un archivo."""
        tiempo_inicio = time.time()
        if (len(sys.argv) - 1) % 2 != 0:
            print('Error: Debes proporcionar las rutas de los archivos en pares.')
            sys.exit()

        datos = self.leer_archivos_en_pares()
        resultados = '\n'

        for i, (lista_productos, ventas) in enumerate(datos):
            nombre_archivo_lista_productos = self.nombres_archivos[i]['productos']
            total = self.calcular_ventas(lista_productos, ventas,
                                         nombre_archivo_lista_productos)
            resultados += f"""- Total de ventas ($):  {self.nombres_archivos[i]
            ["ventas"]}:{total: ,.2f}\n"""
            if self.warnings[nombre_archivo_lista_productos]:
                resultados += f'\nwarnings: No fue posible encontrar los siguientes productos {nombre_archivo_lista_productos}:\n\n'
                resultados += '\n'.join(self.warnings[nombre_archivo_lista_productos])

        tiempo_fin = time.time()
        tiempo_total = tiempo_fin - tiempo_inicio
        resultados += f'\n\nTiempo de compilacion: {tiempo_total: .2f} segundos\n'

        self.escribir_a_archivo(resultados)
        print(resultados)


if __name__ == "__main__":
    calculadora = computeSales()
    calculadora.calcular()
