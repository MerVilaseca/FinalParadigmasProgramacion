# -*- coding: utf-8 -*-
# Librerias
import re
import os
import csv
import logging
from datetime import datetime

# Definicion constantes
PATH_CLIENTES = './src/clientes.csv'
PATH_VIAJES = './src/viajes.csv'
LISTA_OPCIONES = ['1','2','3','4','5']
LOG_FILENAME = datetime.now().strftime('./log/logfile_%H_%M_%S_%d_%m_%Y.log')

# inicializo log file 
logging.basicConfig(filename=LOG_FILENAME, level=logging.INFO)

# Funciones y clases

def load_csv(filename):
    """
    Realiza la carga y validación de un archivo csv

    Parameters
    ----------
    filename : str

    Returns
    ----------
    data : lista de diccionarios
    """
    if os.path.isfile(filename):
        with open(filename, mode='r', encoding='latin-1') as csvfile:
            file_reader = csv.DictReader(csvfile)
            data = list()
            for row in file_reader:
                if 'monto' in row.keys():
                    # convierto columna 'monto' a float
                    row['monto'] = float(row['monto'].replace(',',''))
                data.append(row)
            return data
    else:
        print('Nombre de archivo no encontrado')
        

def menu_principal():
    """
    Menu princiapal del programa

    Returns
    ----------
    opcion : str
    """

    print("""
        BIENVENIDO AL SISTEMA DE BÚSQUEDA
        -------------------------------------------
        Qué acción desea realizar?

        1) Búsqueda de cliente por nombre.
        2) Búsqueda total de usuarios por empresa.
        3) Total de ingreso por empresa.
        4) Total de viajes realizados y gasto total por n° documento.
        5) Salir del programa
        """)
    opcion = input('Ingrese la opción a realizar: ')

    if opcion in LISTA_OPCIONES:
        return opcion
    else:
        print('Opción no válida, vuelva a intentar')
        return menu_principal()

def mostrar(cadena):
    print("""
        ------------------------------------------------------------------------------
        {}
        ------------------------------------------------------------------------------
        """.format(cadena))

class Acciones:
    data_clientes = load_csv(PATH_CLIENTES)
    data_viajes = load_csv(PATH_VIAJES)
    
    def busqueda_nombre(self, nombre):
        """
        docstring
        """
        nombre = nombre.lower()
        names_filter = self.filtrar_data(self.data_clientes, 'Nombre', 'Nombre', nombre)

        if names_filter:
            print(f'Se encontraron las siguientes personas que cumplen el patron ingresado "{nombre}"')
            print(names_filter)

            data = [list(self.data_clientes[0].keys())]
            for row in self.data_clientes:
                if row['Nombre'] in names_filter:
                    data.append(list(row.values()))
            return data

    def total_usuario_empresa(self, empresa):
        """
        docstring
        """
        empresa = empresa.lower()
        clientes = self.data_clientes.copy()

        data = [list(clientes[0].keys())]
        for row in clientes:
            if empresa in row['Empresa'].lower():
                data.append(list(row.values()))
        return data
    
    def total_ganancia_empresa(self, empresa):
        """
        docstring
        """
        data_clientes = self.data_clientes.copy()
        data_viajes = self.data_viajes.copy()

        consolidado = {
            'Empresa': empresa,
            'Clientes': self.filtrar_data(data_clientes, 'Empresa', 'Documento',empresa),
            'Montos': []
        }

        for documento in consolidado['Clientes']:
            s = sum(self.filtrar_data(data_viajes, 'Documento', 'monto',documento))
            consolidado['Montos'].append(s)
        return consolidado
        

    def viajes_monto_documento(self, documento):
        """
        docstring
        """
        c = [list(self.data_clientes[0].keys())]
        for cliente in self.data_clientes:
            if cliente['Documento'] == documento:
                c.append(list(cliente.values()))
                break
        
        s = sum(self.filtrar_data(self.data_viajes, 'Documento', 'monto',documento))

        busqueda_viajes = [list(self.data_viajes[0].keys())]
        for viaje in self.data_viajes:
            if viaje['Documento'] == documento:
                busqueda_viajes.append(list(viaje.values()))
        
        return c, s, busqueda_viajes

    def filtrar_data(self, data, key, column,filtro=''):
        """
        docstring
        """
        set_filtro = set()
        for row in data:
            if filtro.lower() in row[key].lower():
                set_filtro.add(row[column])
        return list(set_filtro)

# Programa principal
if __name__ == "__main__":
    logging.info('Inicializando programa ...')
    # inicializo clase
    acc = Acciones()
    # filtro data clientes según empresas
    empresas = acc.filtrar_data(acc.data_clientes, 'Empresa', 'Empresa')

    # muestro menu de opciones
    opcion = menu_principal()
    logging.info(f'Accion: {opcion}')

    # según opción recopilada realiza acción
    if opcion == '1':
        logging.info('Búsqueda de cliente por nombre')
        nombre = input('Ingrese el nombre de la persona a buscar: ')

        clientes = acc.busqueda_nombre(nombre)
        # imprimiendo resultado en pantalla
        print('Mostrando los datos .. ')
        for cliente in clientes:
            print(cliente)
    
    elif opcion == '2':
        logging.info('Búsqueda total de usuarios por empresa')
        print('Mostrando listado de empresas en archivo : ')
        for i,empresa in enumerate(empresas):
            print(i,empresa)
        num = int(input('Ingrese el número de empresa a buscar: '))

        data = acc.total_usuario_empresa(empresas[num])
        
        # imprimiendo resultado en pantalla
        n = len(data) - 1
        cadena = f"Empresa: {empresas[num]}\n        Total Usuarios: {n}"
        mostrar(cadena)
        
        for d in data:
            print(d)

    elif opcion == '3':
        logging.info('Total de ingreso por empresa')
        print('Mostrando listado de empresas en archivo : ')
        for i,empresa in enumerate(empresas):
            print(i,empresa)

        num = int(input('Ingrese el número de empresa a buscar: '))
        consolidado = acc.total_ganancia_empresa(empresas[num])
        
        # imprimiendo resultado en pantalla 
        cadena = f"Empresa: {empresas[num]} ${round(sum(consolidado['Montos']),2)}"
        mostrar(cadena)
    
    elif opcion == '4':
        logging.info('Total de viajes realizados y gasto total por n° documento')
        documento = input('Ingrese el número de documento a buscar: ')

        c, s, viajes = acc.viajes_monto_documento(documento)

        # imprimiendo resultado en pantalla
        cadena = f"Documento: {documento}"
        mostrar(cadena)

        for x in c:
            print(x)
        
        cadena = f"Total viajes: {len(viajes)-1}, Monto: {round(s,2)}"
        mostrar(cadena)

        for viaje in viajes:
            print(viaje)
    
    elif opcion == '5':
        logging.info('Salir')
        print('Adios')
    
    logging.info('salir')