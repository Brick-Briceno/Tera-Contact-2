from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem, QShortcut, QMessageBox, QHeaderView
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QUrl, Qt
from PyQt5.QtGui import QKeySequence
from interfaz import Ui_MainWindow
import time
import csv
import os

#pip install PyQtWebEngine

class sistema:
    nombre_de_archivo = "Base_datos.tsv"
    def mostrar_mensaje(texto):
        mensaje = QMessageBox()
        mensaje.setWindowFlag(Qt.FramelessWindowHint)
        mensaje.setText(texto)
        mensaje.setStyleSheet("* {background-color: black; color: white; font-size: 15px; height: 28px; }")
        mensaje.exec_()

    temas = [""]
    n_tema = 0
    def cambiar_tema():
        tema = sistema.temas[sistema.n_tema]
        t = open(f"temas/{tema}", "r")
        ventana.setStyleSheet(t.read())
        t.close()
        sistema.n_tema += 1
        if sistema.n_tema > len(sistema.temas)-1: sistema.n_tema = 0
        ventana.statusbar.showMessage(f"Se cambió el tema a {tema[:-4]}")

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

    def cuantas_celdas_hay():
        with open(sistema.nombre_de_archivo, 'r', newline='') as archivo:
            return sum(1 for _ in archivo)

    def actualizar_celdas():
        if not os.path.exists(sistema.nombre_de_archivo): sistema.crear_base()
        filas = sistema.cuantas_celdas_hay()
        sistema.cantidad_celdas(ventana.tabla_contactos, filas+1, 5)
        sistema.cantidad_celdas(ventana.tabla_contactos_2, filas+1, 7)
        for fila in range(filas):
            for columna in range(7):
                texto = sistema.leer_celda_en_archivo_tsv(sistema.nombre_de_archivo, fila, columna)
                if texto == None: texto = ""
                else:
                    #Orden de datos: 0 Nombre, 1 Telefono, 2 Interes,
                    #3 Dueño Nombre, 4 Horario, 5 Pagina Web, 6 Direción
                    sistema.cambiar_texto_celda(ventana.tabla_contactos_2, texto, fila, columna)
                    #Ordenar 1ra tabla
                    if columna == 0: sistema.cambiar_texto_celda(ventana.tabla_contactos, texto, fila, 0)
                    elif columna == 1: sistema.cambiar_texto_celda(ventana.tabla_contactos, texto, fila, 1)
                    elif columna == 6: sistema.cambiar_texto_celda(ventana.tabla_contactos, texto, fila, 2)
                    elif columna == 4: sistema.cambiar_texto_celda(ventana.tabla_contactos, texto, fila, 3)
                    elif columna == 5: sistema.cambiar_texto_celda(ventana.tabla_contactos, texto, fila, 4)

    def escribir_en_celda(nombre_archivo, fila, columna, valor):
        # Verifica si el archivo existe
        if not os.path.exists(nombre_archivo):
            # Si no existe, crea el archivo y escribe una fila vacía
            with open(nombre_archivo, 'w', newline='') as archivo:
                escritor = csv.writer(archivo, delimiter='\t')
                escritor.writerow([])

        # Lee el archivo existente
        with open(nombre_archivo, 'r', newline='') as archivo:
            lector = csv.reader(archivo, delimiter='\t')
            filas = list(lector)

        # Asegúrate de que haya suficientes filas
        while len(filas) <= fila:
            filas.append([])

        # Asegúrate de que haya suficientes columnas en la fila específica
        while len(filas[fila]) <= columna:
            filas[fila].append('')

        # Modifica el valor en la fila y columna especificadas
        filas[fila][columna] = valor

        # Escribe los cambios de vuelta al archivo
        with open(nombre_archivo, 'w', newline='') as archivo:
            escritor = csv.writer(archivo, delimiter='\t')
            escritor.writerows(filas)

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

    def celda_editada(item):
        fila = item.row()
        columna = item.column()
        texto = item.text()
        if sistema.magia_posicion != "vacio":
            sistema.magia_posicion = "vacio"
            ventana.statusbar.showMessage("Ningún contacto selecionado")
            sistema.escribir_en_celda(sistema.nombre_de_archivo, fila, columna, texto.strip())
            sistema.actualizar_celdas()

    def buscar_datos():
        t = open(sistema.nombre_de_archivo, "r")
        txt = t.read()
        t.close()
        eureca = ventana.buscador_datos.text().strip().upper()
        si = False
        lugar = 0
        resultados = 0
        for x in enumerate(txt.split("\n")):
            if eureca in x[1].strip().upper():
                resultados += 1
                if not si:
                    lugar = x[0]
                    si = True
        if si:
            ventana.tabla_contactos_2.verticalScrollBar().setValue(lugar)
            if not resultados-1: ventana.statusbar.showMessage(f"{resultados} resultado encontrado")
            else: ventana.statusbar.showMessage(f"{resultados} resultados encontrados")
        else: ventana.statusbar.showMessage("No se ha encontrado ningun resultado")

    def interes_n(f, c):
        if sistema.magia_posicion == "vacio":
            sistema.mostrar_mensaje("Seleciona un contacto para definir el interes")
            return
        interes = ("Interesado", "Nah", "Contestadora",
                   "Llamar por la mañana", "El jefe no viene regularmete")
        sistema.escribir_en_celda(sistema.nombre_de_archivo,
                                  sistema.magia_posicion, 2, interes[c])
        sistema.actualizar_celdas()
        sistema.magia_posicion = "vacio"

    def definir_fecha(fecha):
        if not fecha.isValid(): return
        #fecha.toPyDate()
        #ano = fecha.year()
        mes = str(fecha.month())
        dia = fecha.day()
        meses = {1:"Enero", 2:"Febrero", 3:"Marzo", 4:"Abril",
                 5:"Mayo", 6:"Jinio", 7:"Julio", 8:"Agosto", 9:"Septiembre",
                 10:"Octubre", 11:"Noviembre", 12:"Diciembre"}
        mes = mes.replace(mes, meses[int(mes)])
        dato = f"Llamar el {dia} de {mes}"
        ventana.crear_dato_fecha.setText(dato)

    def llamar_el_dia():
        if sistema.magia_posicion == "vacio":
            ventana.pestana_ver.setCurrentIndex(0)
            sistema.mostrar_mensaje("Seleciona un Contacto para agregar esta fecha de llamada")
            return
        
        sistema.escribir_en_celda(sistema.nombre_de_archivo,
                                  sistema.magia_posicion, 2,
                                  ventana.crear_dato_fecha.text())
        ventana.pestana_ver.setCurrentIndex(0)
        sistema.actualizar_celdas()
        sistema.magia_posicion = "vacio"

    def eliminar_fila(nombre_archivo, fila):
        # Verifica si el archivo existe
        if not os.path.exists(nombre_archivo):
            print(f"El archivo '{nombre_archivo}' no existe.")
            return

        # Lee el archivo existente
        with open(nombre_archivo, 'r', newline='') as archivo:
            lector = csv.reader(archivo, delimiter='\t')
            filas = list(lector)

        # Verifica si la fila está dentro del rango de filas del archivo
        if 0 <= fila < len(filas):
            # Elimina la fila específica del archivo
            filas.pop(fila)

            # Escribe los cambios de vuelta al archivo
            with open(nombre_archivo, 'w', newline='') as archivo:
                escritor = csv.writer(archivo, delimiter='\t')
                escritor.writerows(filas)
        else:
            print("Índice de fila fuera de rango.")

    def ir_atras(): ventana.browser.back()

    def ir_adelante(): ventana.browser.forward()

    def recargar(): ventana.browser.reload()

    def crear_base():
        with open(sistema.nombre_de_archivo, "w") as file:
            file.write("")

    def eliminar_todo():
        sistema.crear_base()
        sistema.actualizar_celdas()

    def crear_base():
        with open(sistema.nombre_de_archivo, "w") as file:
            file.write("")

    def eliminar_todo():
        sistema.crear_base()
        sistema.actualizar_celdas()

    def eliminar_contacto():
        if sistema.magia_posicion == "vacio":
            sistema.mostrar_mensaje("Seleciona un contacto para eliminarlo")
            return

        n = sistema.magia_posicion
        sistema.magia_posicion = "vacio"
        ventana.statusbar.showMessage(f"Ningún contacto selecionado")

        nombre = sistema.leer_celda_en_archivo_tsv(sistema.nombre_de_archivo, n, 0)
        tlfn = sistema.leer_celda_en_archivo_tsv(sistema.nombre_de_archivo, n, 1)
        sistema.eliminar_fila(sistema.nombre_de_archivo, n)
        sistema.actualizar_celdas()
        if not(nombre == None or tlfn == None):
            sistema.mostrar_mensaje(f"Se Eliminó:\n {nombre}\n" + tlfn)
            return

    index_pestana = 0
    def cambiar_pestana():
        sistema.index_pestana += 1
        if sistema.index_pestana > 2: sistema.index_pestana = 0
        ventana.pestanas.setCurrentIndex(sistema.index_pestana)

    def copy_cell(row, column):
        #Esta función copia el contenido de la celda seleccionada al portapapeles
        clipboard = QApplication.clipboard()
        item = ventana.tabla_contactos_2.item(row, column)
        if item == None: return
        text = item.text()
        if text in [" ", ""]: return
        if column == 1: text = "0034" + text.replace(" ", "")
        clipboard.setText(text)


    invertido = False
    def invetir_color():
        sistema.invertido = not(sistema.invertido)
        code = "var style = document.createElement(\"style\"); document.head.appendChild(style); style.sheet.insertRule(\"body { filter: invert("+str(sistema.invertido*100)+"%); }\", 0);"
        ventana.browser.page().runJavaScript(code)

    def copiar_link():
        clipboard = QApplication.clipboard()
        clipboard.setText(ventana.buscador.text())

    def resolucion(n):
        ventana.browser.setZoomFactor(n/100)
        g = open("r.ini", "w+")
        g.write(str(n))
        g.close()

    def cargar_url():
        url = ventana.buscador.text()
        for x in [".com", ".ve", ".ar", ".es", ".net"]:
            if x in url:
                if not "www." in url:
                    url = "www." + url

                if not "https://" in url or "http://" in url:
                    url = "http://" + url
                ventana.browser.load(QUrl(url))
                return

        url = "https://google.es/maps?search&q=" + url.replace(" ", "+")
        ventana.browser.load(QUrl(url))

    def cambiar_url_y_guardar(url: QUrl):
        url = url.toString()
        if "https://" in url:
            ventana.buscador.setText(url[8:])
        elif "http://" in url:
            ventana.buscador.setText(url[7:])
        else:
            ventana.buscador.setText(url)
        try:
            g = open("ultima Url.txt", "w+")
            g.write(url)
            g.close()
        except: None

    "Funciones Magia"

    franquicias = ("Papa John", "Burger King", "McDonald",
                   "Domino", "Subway", "KFC", "Pizza Hut", "Wendy"
                   )

    def numero_34(texto):
        while len(texto):
            if texto[0] == "3" and texto[1] == "4":
                return texto[3:]
            texto = texto[1:]

    def hay_horario(texto):
        if texto == "Abierto las 24 horas": return True, texto
        lista = ("Abierto", "Cierra pronto", "Cerrado")
        for x in lista:
            if x in texto: return True, texto.replace(x, "").replace("\u202f", "").replace(".", "").replace("\u22c5", "").strip()
        return False, ""

    def limpiar_texto(texto):
        texto = texto.replace("+", " ")
        texto = texto.replace("%60", "`")
        texto = texto.replace("%2F", "/")
        texto = texto.replace("%26", "&")
        texto = texto.replace("%7C", "|")
        texto = texto.replace("\u2013", "")
        texto = texto.replace("\u22c5", ".")
        texto = texto.replace("\u202f", "")
        return texto.strip()

    magia_posicion = "vacio"
    def magia2():
        sistema.magia_posicion = "vacio"
        posicion = ventana.tabla_contactos.rowCount()
        dire = False
        tele = False
        #Orden de datos: 0 Nombre, 1 Telefono, 2 Interes,
        #3 Dueño Nombre, 4 Horario, 5 Pagina Web, 6 Direción
        data = [""]*7
        texto = ventana.browser.page().selectedText()
        #texto = sistema.limpiar_texto(texto)
        nombre = ""
        for x in ventana.buscador.text()[25:]:
            if x == "/": break
            nombre += x

        data[0] = sistema.limpiar_texto(nombre)
        for x in sistema.franquicias:
            if x in data[0]:
                sistema.mostrar_mensaje("¡Esto es una Franquicia!")
                return

        for x in texto.splitlines():
            hay_h = sistema.hay_horario(x)#función para el horario, arroja un bool->

            #Direción
            if "España" in x and "+" in x and not dire:
                dire = True
                data[6] = x

            #Telefono
            elif "+34"  in x and not tele:
                tele = True
                data[1] = sistema.numero_34(x)
                t = open(sistema.nombre_de_archivo, "r")
                if data[1] in t.read():
                    sistema.mostrar_mensaje("Telefono repetido")
                    t.close()
                    return

            #Horario
            elif hay_h[0]:
                data[4] = hay_h[1]

            #Pagina Web
            elif ".com" in x or ".net" in x: data[5] = x

        if not(dire * tele):
            sistema.mostrar_mensaje("Faltan datos para el contacto")
            return

        #Orden de datos: 0 Nombre, 1 Telefono, 2 Interes,
        #3 Dueño Nombre, 4 Horario, 5 Pagina Web, 6 Direción
        for x in enumerate(data):
            sistema.escribir_en_celda(sistema.nombre_de_archivo,
                                      posicion-1, x[0], sistema.limpiar_texto(x[1]))

        sistema.actualizar_celdas()

        ventana.tabla_contactos.verticalScrollBar().setValue(sistema.cuantas_celdas_hay()-10)
        sistema.actualizar_status_bar()

    promedio_list = []
    def promedio():
        #Esta función toma cuando se agrega un contacto y saca un promedio de cuanto tiempo se saca uno con respecto a los 10 ultimos
        sistema.promedio_list.append(time.time())
        if len(sistema.promedio_list) >= 10: sistema.promedio_list.pop(0)
        if (sistema.promedio_list[-1:][0] - time.time()) > 60*5: sistema.promedio_list = [time.time()]
        return ((sum(sistema.promedio_list)/len(sistema.promedio_list))-sistema.promedio_list[0])/4

    def mostrar_tiempo(tiempo_pasado):
        segundos = int(tiempo_pasado % 60)
        minutos = int(tiempo_pasado/60)
        horas = int(tiempo_pasado/3600)

        if horas:
            if minutos == 0 and segundos == 0:
                return f"{horas}h"
            elif minutos == 0:
                return f"{horas}h {segundos}s"
            else:
                return f"{horas}h {minutos}m"
        elif minutos:
            if segundos == 0:
                return f"{minutos}m"
            else:
                return f"{minutos}m {segundos}s"
        else:
            return f"{segundos}s"
    
    start_time = time.time()
    def actualizar_status_bar():
        tiempo_pasado = time.time() - sistema.start_time
        tiempo = sistema.mostrar_tiempo(tiempo_pasado)
        promedio_s = sistema.promedio()
        cts = ventana.tabla_contactos.rowCount()-1
        ventana.statusbar.showMessage(f"Hay {cts} Contactos, haces {promedio_s:.{2}f} contactos por minuto, {int(promedio_s*60)} por Hora, tiempo transcurrido: {tiempo}")

    def celda_selec(fila, col):
        sistema.magia_posicion = fila
        sistema.copy_cell(fila, col)
        ventana.statusbar.showMessage(f"Contacto {fila+1} selecionado")

    def copiar_tabla():
        try:
            a = open(sistema.nombre_de_archivo, encoding="utf-8").read() + "\n"
        except UnicodeDecodeError:
            a = open(sistema.nombre_de_archivo, encoding="ansi").read() + "\n"

        QApplication.clipboard().setText(a)

    def tutorial():
        ventana.browser.load(QUrl("file:///Tutorial/index.html"))
        ventana.browser.setZoomFactor(1)
        ventana.buscador.setText("El mejor tutorial de TODOS! 😎🔥")
        ventana.statusbar.showMessage("¿Como usar Tera Contact 2? 🤔")

class MiVentana(QMainWindow, Ui_MainWindow):
    valor = False
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowOpacity(0.97)
        self.showMaximized()

        def pantalla_completa():
            if ventana.valor: self.showMaximized()
            else: self.showFullScreen()
            ventana.valor = not ventana.valor

        "Botones"
        self.ir.clicked.connect(sistema.cargar_url)
        self.atras.clicked.connect(sistema.ir_atras)
        self.adelante.clicked.connect(sistema.ir_adelante)
        self.copiar_link.clicked.connect(sistema.copiar_link)
        self.invertir.clicked.connect(sistema.invetir_color)
        self.anadir_calendario.clicked.connect(sistema.llamar_el_dia)
        self.buscar.clicked.connect(sistema.buscar_datos)

        "Sliders"
        self.resolucion.valueChanged.connect(sistema.resolucion)

        "Navegador"
        self.browser = QWebEngineView()
        self.browser.load(QUrl("https://www.google.com/maps"))
        self.browser.urlChanged.connect(sistema.cambiar_url_y_guardar)
        self.frame_web.layout().addWidget(self.browser)

        "Line Edits"
        self.buscador.returnPressed.connect(sistema.cargar_url)
        self.buscador.setPlaceholderText("Introduzca la URL")
        self.buscador_datos.returnPressed.connect(sistema.buscar_datos)
        self.buscador_datos.setPlaceholderText("¿Qué quieres buscar? 🤔")

        "Tablas"
        self.tabla_contactos.cellClicked.connect(sistema.celda_selec)
        self.tabla_contactos_2.cellClicked.connect(sistema.celda_selec)
        self.tabla_contactos_2.itemChanged.connect(sistema.celda_editada)
        self.tabla_contactos_2.itemChanged.connect(sistema.celda_editada)
        self.tabla_contactos_2.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.interes_llamada.cellClicked.connect(sistema.interes_n)

        "Calendario"
        self.calendario.clicked.connect(sistema.definir_fecha)
        #self.calendario.setSelectedDate(QDate.currentDate())

        "Atajos"
        QShortcut(QKeySequence("F1"), self, sistema.tutorial)
        QShortcut(QKeySequence("F11"), self, pantalla_completa)
        QShortcut(QKeySequence("A"), self, sistema.magia2)
        QShortcut(QKeySequence("Ctrl+R"), self, sistema.recargar)
        QShortcut(QKeySequence("Ctrl+I"), self, sistema.invetir_color)
        QShortcut(QKeySequence("Ctrl+Shift+D"), self, sistema.eliminar_contacto)
        QShortcut(QKeySequence("Ctrl+Shift+C"), self, sistema.copiar_tabla)
        QShortcut(QKeySequence("Ctrl+Shift+T"), self, sistema.cambiar_tema)
        QShortcut(QKeySequence("Ctrl+P"), self, sistema.cambiar_pestana)

        "Menu bars"
        #Tera Contact 2
        self.exportar_datos.triggered.connect(sistema.copiar_tabla)
        self.copiar.triggered.connect(sistema.copiar_tabla)
        self.eliminar.triggered.connect(sistema.eliminar_contacto)
        self.borrar_todos.triggered.connect(sistema.eliminar_todo)
        self.full.triggered.connect(pantalla_completa)
        self.salir.triggered.connect(self.close)

        #Como usar
        self.actionTutorial.triggered.connect(sistema.tutorial)

app = QApplication([])
ventana = MiVentana()
ventana.show()

"Funciones de inicio"

#Verificar si el archivo existe
if not os.path.exists(sistema.nombre_de_archivo): sistema.crear_base()

try:#Revisar y cargar la ultima url
    f = open("ultima Url.txt", "r")
    ultima_url = f.read()
    f.close()
except:
    ultima_url = "https://www.google.es/maps"

ventana.browser.load(QUrl(ultima_url))

try:#Revisar y cargar resolucion
    v = open("r.ini", "r").read()
    valor = int(float(v))
    ventana.browser.setZoomFactor(int(valor)/100)
    ventana.resolucion.setProperty("value", int(valor))
    v.close()

except: None

try:#Cargar temas
    sistema.temas = os.listdir("temas")
except: None

#Un saludo, tienes que ser cordial Hdp!
ventana.statusbar.showMessage("Bienvenido a Tera Contact 2! 😎✨")

sistema.actualizar_celdas()

app.exec_()#iniciar
