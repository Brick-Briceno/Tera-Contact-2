"""
Programa para recoger y marcar numeros telefonicos rapidamente
@Brick_briceno 2024
"""

from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem, QShortcut, QHeaderView
from PyQt5.QtGui import QKeySequence
from interfaz_ver import Ui_MainWindow
import csv
import os

class sistema:
    nombre_de_archivo = "Base_datos.tsv"
    def cantidad_celdas(tabla, fila, colum):
        tabla.setRowCount(fila)
        tabla.setColumnCount(colum)
        for i in range(fila):
            for j in range(colum):
                item = QTableWidgetItem()
                tabla.setItem(i, j, item)

    def cambiar_texto_celda(table_widget, texto, fila, columna):
        item = QTableWidgetItem()
        table_widget.setItem(fila, columna, item)
        item.setText(texto)

    def actualizar_celdas():
        if not os.path.exists(sistema.nombre_de_archivo): return
        with open(sistema.nombre_de_archivo, 'r', newline='') as archivo:
            filas = sum(1 for _ in archivo)
        sistema.cantidad_celdas(ventana.tabla_datos, filas+1, 3)
        for fila in range(filas):
            for columna in range(3):
                texto = sistema.leer_celda_en_archivo_tsv(sistema.nombre_de_archivo, fila, columna)
                if texto == None: return
                else: sistema.cambiar_texto_celda(ventana.tabla_datos, texto, fila, columna)

    def leer_celda_en_archivo_tsv(nombre_archivo, fila, columna):
        try:
            with open(nombre_archivo, 'r', newline='') as archivo:
                lector = csv.reader(archivo, delimiter='\t')
                filas = list(lector)

                # Verifica que la fila y columna estén dentro de los límites
                if 0 <= fila < len(filas) and 0 <= columna < len(filas[fila]):
                    return filas[fila][columna]
                else:
                    print("Índices de fila y/o columna fuera de rango.")
                    return None
        except FileNotFoundError:
            print(f"El archivo '{nombre_archivo}' no existe.")
            return None

class MiVentana(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.tabla_datos.cellClicked.connect(self.copy_cell)
        self.tabla_datos.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        QShortcut(QKeySequence("Ctrl+R"), self, lambda: sistema.actualizar_celdas())

    def copy_cell(self, row, column):
        #Esta función copia el contenido de la celda seleccionada al portapapeles
        clipboard = QApplication.clipboard()
        item = self.tabla_datos.item(row, column)
        if item == None: return
        text = item.text()
        if text in [" ", ""]: return
        if column == 2: text = "0034" + text.replace(" ", "")
        clipboard.setText(text)

app = QApplication([])
ventana = MiVentana()
ventana.show()

sistema.actualizar_celdas()

app.exec_()
