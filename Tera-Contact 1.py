"""
Tera-Contact v1.7 [by Brick Briceño]

El objetivo de este programa es facilitar
la recolección de nombres, telefonos y direcciones
"""

from PyQt5.QtCore import QUrl, Qt
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtWidgets import QApplication, QMainWindow, QTabWidget, QWidget, QVBoxLayout, QTableWidget, QShortcut, QTableWidgetItem, QHeaderView, QLineEdit, QMessageBox
from tkinter import filedialog as FileDialog
from PyQt5.QtGui import QKeySequence
from threading import Thread
import qdarkstyle
import xlsxwriter
import pandas as pd
import time

#Funciones

def export_table_to_excel(nombre_archivo):
    # Crear un DataFrame de pandas para almacenar los datos de la tabla
    data = []
    for row in range(table.rowCount()):
        row_data = []
        for column in range(table.columnCount()):
            item = table.item(row, column)
            if item is not None:
                row_data.append(item.text())
            else:
                row_data.append('')
        data.append(row_data)

    df = pd.DataFrame(data)

    # Configurar el archivo de Excel y la hoja de cálculo
    workbook = xlsxwriter.Workbook(nombre_archivo)
    worksheet = workbook.add_worksheet()

    # Escribir los datos de la tabla en el archivo de Excel
    for row in range(df.shape[0]):
        for col in range(df.shape[1]):
            worksheet.write(row, col, df.iat[row, col])

    # Cerrar el archivo de Excel
    workbook.close()

def guardar_como():
    fichero = FileDialog.asksaveasfile(title="Guardar Hoja de Excel", 
            mode="w", defaultextension=".xlsx")
    if fichero != None:
        export_table_to_excel(fichero.name)


guardado_activado = True
def guardado_automatico():
    """Esto crea 2 copias del proyecto en exel cada 2 minutos
    Guarda una y espera 1 segundo para guardar la otra
    """
    n = 0
    while True:
        n += 1
        time.sleep(1)
        if not guardado_activado: break
        elif n == 40:
            n = 0
            export_table_to_excel("Respaldo 1.xlsx")
            time.sleep(1)
            export_table_to_excel("Respaldo 2.xlsx")

Thread(target=guardado_automatico).start()

def filtrar_numeros_y_espacios(cadena):
    numeros_y_espacios = [c for c in cadena if c.isdigit() or c.isspace()]
    return "".join(numeros_y_espacios)

def limpiar_espacios(texto):
    return texto.strip()

index_pestana = 0
def cambiar_pestana():
    global index_pestana
    index_pestana = not(index_pestana)
    tab_widget.setCurrentIndex(index_pestana)

magia_posicion = [0, 0]
def celda_selec(fila, col):
    global magia_posicion
    magia_posicion = [fila, col]
    table.setCurrentCell(magia_posicion[0], magia_posicion[1])
    print(magia_posicion)

def limpiar_celdas_vacias():
    filas = table.rowCount()
    columnas = table.columnCount()
    for fila in range(filas):
        for columna in range(columnas):
            item = table.item(fila, columna)
            if item is not None:
                texto = item.text()
                if texto.isspace() or texto == '\n':
                    table.setItem(fila, columna, None)

"""hay un pequeño bug
que es que si una celda esta vacia
pero si se usó alguna vez el buscador
de coincidencias lo tecta como si hubiera algo,
las causas de este bug... las desconozco aún
"""
def ver_if_hay_repeticion():
    #limpiar_celdas_vacias()
    filas = table.rowCount()
    columnas = table.columnCount()
    encontrada = False
    linea_selec_v = 0
    colum_selec_v = 0
    linea_busc_v = 0
    colum_busc_v = 0
    for linea_selec in range(filas):
        for colum_selec in range(columnas):
            item_selec = table.item(linea_selec, colum_selec)
            if item_selec is not None:
                for linea_busc in range(filas):
                    for colum_busc in range(columnas):
                        item_busc = table.item(linea_busc, colum_busc)
                        if item_busc is not None and item_selec.text() == item_busc.text() and (linea_selec != linea_busc or colum_selec != colum_busc):
                            encontrada = True
                            linea_selec_v = linea_selec
                            colum_selec_v = colum_selec
                            linea_busc_v = linea_busc
                            colum_busc_v = colum_busc
                            break
                    if encontrada:
                        break
                if encontrada:
                    break
            if encontrada:
                break

    if encontrada:
        scrollbar.setValue(linea_selec_v)
        return "Hay una coincidencia en:\nFila: " + str(linea_selec_v+1) + " Columna: " + str(colum_selec_v+1) + "\nCon Fila: " + str(linea_busc_v+1) + " Columna: " + str(colum_busc_v+1)
    else:
        return "No se encontraron coincidencias"

def cantidad_de_contactos():
    n = 0
    for x in range(5000):
        if table.item(x, 0) != None:
            n += 1
    return n


def magia2():
    nom = False
    dire = False
    tele = False
    global magia_posicion
    texto = webview.page().selectedText()
    for x in texto.splitlines():
        print(x)
        if x != "" and not nom:
            nom = True
            table.setItem(magia_posicion[0],
                  0, QTableWidgetItem(
                    limpiar_espacios(x)))

        elif "España" in x and not dire:
            dire = True
            table.setItem(magia_posicion[0],
                  1, QTableWidgetItem(
                    limpiar_espacios(x)))

        elif "+34"  in x and not tele:
            tele = True
            table.setItem(magia_posicion[0],
                  2, QTableWidgetItem(
                    limpiar_espacios(x)[1:]))

    if not(nom * dire * tele):
        mostrar_mensaje("Faltan datos para el contacto")

    scrollbar.setValue(magia_posicion[0]-7)
    magia_posicion[0] += 1

app = QApplication([])
app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())

window = QMainWindow()
window.setWindowTitle("Tera-Contact v1.7 [by Brick Briceño]")

central_widget = QWidget(window)
layout = QVBoxLayout(central_widget)

# Creamos el QTabWidget
tab_widget = QTabWidget(window)
tab_widget.setStyleSheet("QTabBar::tab { font-size: 16px; width: 100px; height: 20px;}")

# Creamos la primera pestaña "Web"
web_tab = QWidget()

web_layout = QVBoxLayout(web_tab)
webview = QWebEngineView()

try:#Revisar y cargar la ultima url
    f = open("ultima Url.txt", "r")
    ultima_url = f.read()
    f.close()
except:
    ultima_url = "https://www.google.com"

webview.load(QUrl(ultima_url))

def cargar_url():
    url = line_edit.text()
    for x in [".com", ".ve", ".ar", ".es", ".net"]:
        if x in url:
            if not "www." in url:
                url = "www." + url

            if not "https://" in url or "http://" in url:
                url = "http://" + url
            webview.load(QUrl(url))
            return
    url = "https://google.es/maps?search&q=" + url.replace(" ", "+")
    webview.load(QUrl(url))

def cambiar_url_y_guardar(url: QUrl):
    url = url.toString()
    if "https://" in url:
        line_edit.setText(url[8:])
    elif "http://" in url:
        line_edit.setText(url[7:])
    else:
        line_edit.setText(url)

    g = open("ultima Url.txt", "w+")
    g.write(url)
    g.close()

def mostrar_mensaje(texto):
    mensaje = QMessageBox()
    mensaje.setWindowFlag(Qt.FramelessWindowHint)
    mensaje.setText(texto)
    mensaje.exec_()

def mostrar_tiempo(tiempo_pasado):
    segundos = int(tiempo_pasado % 60)
    minutos = int(tiempo_pasado/60)
    horas = int(tiempo_pasado/3600)

    if horas:
        if minutos == 0 and segundos == 0:
            return f"{horas}H"
        elif minutos == 0:
            return f"{horas}H {segundos}S"
        else:
            return f"{horas}H {minutos}M"
    elif minutos:
        if segundos == 0:
            return f"{minutos}M"
        else:
            return f"{minutos}M {segundos}S"
    else:
        return f"{segundos}S"

start_time = time.time()
def mostrar_cronometro():
    tiempo_pasado = time.time() - start_time
    segundos = int(tiempo_pasado)
    minutos = int(tiempo_pasado/60)
    horas = int(tiempo_pasado/3600)

    tiempo = mostrar_tiempo(tiempo_pasado)

    cts = cantidad_de_contactos()
    mostrar_mensaje(f"Tiempo transcurrido: {tiempo}\nHay {cts} Contactos\nHaces " +
                    f"{cts/segundos*60:.{2}f} contactos por minuto\n{int(cts/segundos*3600)} por Hora")


line_edit = QLineEdit()
line_edit.setPlaceholderText("Pon la Url :D")
line_edit.returnPressed.connect(lambda: cargar_url())
webview.urlChanged.connect(cambiar_url_y_guardar)
line_edit.setStyleSheet("QLineEdit {font-size: 17px; height: 28px; }")

web_layout.addWidget(line_edit)
web_layout.addWidget(webview)

#Creamos la segunda pestaña "Datos"
data_tab = QWidget()
data_layout = QVBoxLayout(data_tab)
table = QTableWidget()
table.setColumnCount(3)# Número de columnas
table.setRowCount(5000)# Número de filas
table.setHorizontalHeaderLabels(["Nombre", "Dirección", "Numero"])
table.cellClicked.connect(celda_selec)
data_layout.addWidget(table)
header = table.horizontalHeader()
header.setSectionResizeMode(QHeaderView.Stretch)

scrollbar = table.verticalScrollBar()

# Agregamos las pestañas al QTabWidget
tab_widget.addTab(web_tab, "Web")
tab_widget.addTab(data_tab, "Datos")
window.setCentralWidget(tab_widget)

def copiar_tabla():
    clipboard = QApplication.clipboard()
    texto = ""
    for linea in range(5000):
        for colum in range(3):
            dato_ob = table.item(linea, colum)
            if dato_ob != None:
                dato = dato_ob.text()
                texto += dato+"\t"
        texto += "\n"

    clipboard.setText(texto)


"Atajos de teclado"

QShortcut(QKeySequence("A"), window).activated.connect(magia2)
QShortcut(QKeySequence("Ctrl+Q"), window).activated.connect(cambiar_pestana)
QShortcut(QKeySequence("Ctrl+O"), window).activated.connect(lambda: webview.back())
QShortcut(QKeySequence("Ctrl+P"), window).activated.connect(lambda: webview.forward())
QShortcut(QKeySequence("Ctrl+C"), window).activated.connect(copiar_tabla)
QShortcut(QKeySequence("Ctrl+T"), window).activated.connect(mostrar_cronometro)
QShortcut(QKeySequence("Ctrl+R"), window).activated.connect(lambda: mostrar_mensaje(ver_if_hay_repeticion()))
QShortcut(QKeySequence("Ctrl+S"), window).activated.connect(guardar_como)


window.showMaximized()
window.show()
app.exec_()
guardado_activado = False
