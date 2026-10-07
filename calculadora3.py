import ast
import operator
import sys

from PySide6.QtCore import Qt
from PySide6.QtGui import QAction, QKeySequence
from PySide6.QtWidgets import (
    QApplication,
    QGridLayout,
    QLabel,
    QLineEdit,
    QListWidget,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QVBoxLayout,
    QWidget,
)


# =============================================================
# MOTOR MATEMÁTICO
# =============================================================

class MotorMatematico:
    """Procesa expresiones matemáticas de forma controlada."""

    OPERADORES = {
        ast.Add: operator.add,
        ast.Sub: operator.sub,
        ast.Mult: operator.mul,
        ast.Div: operator.truediv,
        ast.UAdd: operator.pos,
        ast.USub: operator.neg,
    }

    @classmethod
    def resolver(cls, expresion):
        # Completar paréntesis que hayan quedado abiertos
        abiertos = expresion.count("(")
        cerrados = expresion.count(")")

        if abiertos > cerrados:
            expresion += ")" * (abiertos - cerrados)

        try:
            arbol = ast.parse(expresion, mode="eval")
            return cls.evaluar(arbol.body)

        except ZeroDivisionError:
            raise

        except Exception as error:
            raise ValueError("Operación no válida") from error

    @classmethod
    def evaluar(cls, nodo):

        # Números
        if isinstance(nodo, ast.Constant):

            if isinstance(nodo.value, (int, float)):
                return nodo.value

            raise ValueError("Número no permitido")

        # Operaciones binarias
        if isinstance(nodo, ast.BinOp):

            izquierda = cls.evaluar(nodo.left)
            derecha = cls.evaluar(nodo.right)

            funcion = cls.OPERADORES.get(type(nodo.op))

            if funcion is None:
                raise ValueError("Operador desconocido")

            return funcion(izquierda, derecha)

        # Números negativos o positivos
        if isinstance(nodo, ast.UnaryOp):

            valor = cls.evaluar(nodo.operand)

            funcion = cls.OPERADORES.get(type(nodo.op))

            if funcion is None:
                raise ValueError("Operador desconocido")

            return funcion(valor)

        raise ValueError("Expresión no permitida")


# =============================================================
# VENTANA PRINCIPAL
# =============================================================

class NovaMath(QMainWindow):

    LIMITE_REGISTROS = 6

    def __init__(self):
        super().__init__()

        self.operacion_actual = ""
        self.resultado_reciente = False

        self.configurar_ventana()
        self.crear_menu()
        self.crear_interfaz()
        self.aplicar_estilo()

    # =========================================================
    # CONFIGURACIÓN
    # =========================================================

    def configurar_ventana(self):

        self.setWindowTitle("NovaMath - Calculadora")
        self.setFixedSize(410, 640)

    # =========================================================
    # MENÚ
    # =========================================================

    def crear_menu(self):

        barra_menu = self.menuBar()

        # -------------------------
        # OPERACIONES
        # -------------------------

        menu_operaciones = barra_menu.addMenu("Operaciones")

        nueva_operacion = QAction(
            "Nueva operación",
            self
        )

        nueva_operacion.setShortcut(
            QKeySequence("Ctrl+N")
        )

        nueva_operacion.triggered.connect(
            self.nueva_operacion
        )

        menu_operaciones.addAction(
            nueva_operacion
        )

        borrar_historial = QAction(
            "Borrar historial",
            self
        )

        borrar_historial.triggered.connect(
            self.borrar_historial
        )

        menu_operaciones.addAction(
            borrar_historial
        )

        menu_operaciones.addSeparator()

        cerrar = QAction(
            "Cerrar programa",
            self
        )

        cerrar.setShortcut(
            QKeySequence("Ctrl+Q")
        )

        cerrar.triggered.connect(
            self.close
        )

        menu_operaciones.addAction(
            cerrar
        )

        # -------------------------
        # HERRAMIENTAS
        # -------------------------

        menu_herramientas = barra_menu.addMenu(
            "Herramientas"
        )

        copiar_resultado = QAction(
            "Copiar resultado",
            self
        )

        copiar_resultado.setShortcut(
            QKeySequence("Ctrl+C")
        )

        copiar_resultado.triggered.connect(
            self.copiar_resultado
        )

        menu_herramientas.addAction(
            copiar_resultado
        )

        limpiar_pantalla = QAction(
            "Limpiar pantalla",
            self
        )

        limpiar_pantalla.triggered.connect(
            self.limpiar_pantalla
        )

        menu_herramientas.addAction(
            limpiar_pantalla
        )

        # -------------------------
        # AYUDA
        # -------------------------

        menu_ayuda = barra_menu.addMenu(
            "Ayuda"
        )

        acerca = QAction(
            "Acerca de NovaMath",
            self
        )

        acerca.triggered.connect(
            self.mostrar_acerca
        )

        menu_ayuda.addAction(
            acerca
        )

        instrucciones = QAction(
            "Instrucciones",
            self
        )

        instrucciones.triggered.connect(
            self.mostrar_instrucciones
        )

        menu_ayuda.addAction(
            instrucciones
        )

    # =========================================================
    # INTERFAZ
    # =========================================================

    def crear_interfaz(self):

        central = QWidget()

        self.setCentralWidget(
            central
        )

        layout_principal = QVBoxLayout(
            central
        )

        layout_principal.setContentsMargins(
            20,
            20,
            20,
            20
        )

        layout_principal.setSpacing(
            12
        )

        # Título

        titulo = QLabel(
            "✦ NOVAMATH"
        )

        titulo.setObjectName(
            "titulo"
        )

        layout_principal.addWidget(
            titulo
        )

        subtitulo = QLabel(
            "Calculadora matemática"
        )

        subtitulo.setObjectName(
            "subtitulo"
        )

        layout_principal.addWidget(
            subtitulo
        )

        # Pantalla

        self.pantalla = QLineEdit()

        self.pantalla.setReadOnly(
            True
        )

        self.pantalla.setAlignment(
            Qt.AlignRight
        )

        self.pantalla.setPlaceholderText(
            "0"
        )

        layout_principal.addWidget(
            self.pantalla
        )

        # Teclado

        self.crear_teclado(
            layout_principal
        )

        # Historial

        etiqueta_historial = QLabel(
            "Historial reciente"
        )

        etiqueta_historial.setObjectName(
            "historialTitulo"
        )

        layout_principal.addWidget(
            etiqueta_historial
        )

        self.historial = QListWidget()

        self.historial.setFocusPolicy(
            Qt.NoFocus
        )

        layout_principal.addWidget(
            self.historial
        )

    # =========================================================
    # TECLADO
    # =========================================================

    def crear_teclado(self, layout_principal):

        teclado = QGridLayout()

        teclado.setSpacing(
            7
        )

        botones = [
            ("AC", 0, 0),
            ("(", 0, 1),
            (")", 0, 2),
            ("÷", 0, 3),

            ("7", 1, 0),
            ("8", 1, 1),
            ("9", 1, 2),
            ("×", 1, 3),

            ("4", 2, 0),
            ("5", 2, 1),
            ("6", 2, 2),
            ("-", 2, 3),

            ("1", 3, 0),
            ("2", 3, 1),
            ("3", 3, 2),
            ("+", 3, 3),

            ("0", 4, 0),
            (".", 4, 1),
            ("=", 4, 2),
        ]

        for texto, fila, columna in botones:

            boton = QPushButton(
                texto
            )

            boton.setMinimumHeight(
                48
            )

            boton.setProperty(
                "categoria",
                self.clasificar_boton(texto)
            )

            boton.clicked.connect(
                lambda _, valor=texto:
                self.recibir_boton(valor)
            )

            if texto == "=":

                teclado.addWidget(
                    boton,
                    fila,
                    columna,
                    1,
                    2
                )

            else:

                teclado.addWidget(
                    boton,
                    fila,
                    columna
                )

        layout_principal.addLayout(
            teclado
        )

    def clasificar_boton(self, texto):

        if texto in ["+", "-", "×", "÷"]:
            return "operador"

        if texto == "=":
            return "resultado"

        if texto in ["AC", "(", ")"]:
            return "especial"

        return "numero"

    # =========================================================
    # DISEÑO
    # =========================================================

    def aplicar_estilo(self):

        estilo = """
        QMainWindow {
            background-color: #111827;
        }

        QWidget {
            color: #e5e7eb;
            font-family: Segoe UI;
        }

        QMenuBar {
            background-color: #1f2937;
            color: #f9fafb;
            padding: 3px;
        }

        QMenuBar::item {
            padding: 6px 12px;
            border-radius: 5px;
        }

        QMenuBar::item:selected {
            background-color: #374151;
        }

        QMenu {
            background-color: #1f2937;
            color: #f9fafb;
            border: 1px solid #4b5563;
        }

        QMenu::item {
            padding: 7px 25px;
        }

        QMenu::item:selected {
            background-color: #7c3aed;
        }

        QLabel#titulo {
            color: #a78bfa;
            font-size: 23px;
            font-weight: bold;
        }

        QLabel#subtitulo {
            color: #9ca3af;
            font-size: 12px;
        }

        QLabel#historialTitulo {
            color: #c4b5fd;
            font-size: 12px;
            font-weight: bold;
        }

        QLineEdit {
            background-color: #1f2937;
            border: 2px solid #374151;
            border-radius: 10px;
            color: #f9fafb;
            font-size: 27px;
            font-weight: bold;
            padding: 10px;
        }

        QLineEdit:focus {
            border: 2px solid #8b5cf6;
        }

        QListWidget {
            background-color: #1f2937;
            border: 1px solid #374151;
            border-radius: 8px;
            color: #d1d5db;
            padding: 5px;
        }

        QListWidget::item {
            padding: 6px;
            border-bottom: 1px solid #374151;
        }

        QListWidget::item:selected {
            background-color: #6d28d9;
        }

        QPushButton {
            border: none;
            border-radius: 8px;
            font-size: 16px;
            font-weight: bold;
        }

        QPushButton[categoria="numero"] {
            background-color: #374151;
            color: #f9fafb;
        }

        QPushButton[categoria="numero"]:hover {
            background-color: #4b5563;
        }

        QPushButton[categoria="operador"] {
            background-color: #7c3aed;
            color: white;
        }

        QPushButton[categoria="operador"]:hover {
            background-color: #6d28d9;
        }

        QPushButton[categoria="especial"] {
            background-color: #db2777;
            color: white;
        }

        QPushButton[categoria="especial"]:hover {
            background-color: #be185d;
        }

        QPushButton[categoria="resultado"] {
            background-color: #059669;
            color: white;
        }

        QPushButton[categoria="resultado"]:hover {
            background-color: #047857;
        }

        QPushButton:pressed {
            background-color: #111827;
        }
        """

        self.setStyleSheet(
            estilo
        )

    # =========================================================
    # BOTONES
    # =========================================================

    def recibir_boton(self, valor):

        if valor == "AC":
            self.limpiar_pantalla()
            return

        if valor == "=":
            self.obtener_resultado()
            return

        # Si acabamos de obtener un resultado y se pulsa un número,
        # comienza una operación nueva.
        if (
            self.resultado_reciente
            and valor.isdigit()
        ):
            self.operacion_actual = ""

        self.resultado_reciente = False

        self.operacion_actual += valor

        self.pantalla.setText(
            self.operacion_actual
        )

    # =========================================================
    # CÁLCULO
    # =========================================================

    def obtener_resultado(self):

        if not self.operacion_actual:
            return

        expresion = (
            self.operacion_actual
            .replace("÷", "/")
            .replace("×", "*")
        )

        try:

            resultado = MotorMatematico.resolver(
                expresion
            )

            if (
                isinstance(resultado, float)
                and resultado.is_integer()
            ):
                resultado = int(resultado)

            resultado = str(
                resultado
            )

            self.registrar_historial(
                self.operacion_actual,
                resultado
            )

            self.pantalla.setText(
                resultado
            )

            self.operacion_actual = resultado

            self.resultado_reciente = True

        except ZeroDivisionError:

            QMessageBox.warning(
                self,
                "Operación incorrecta",
                "No es posible dividir un número entre cero."
            )

            self.limpiar_pantalla()

        except Exception:

            QMessageBox.warning(
                self,
                "Error",
                "La expresión ingresada no es válida."
            )

            self.limpiar_pantalla()

    # =========================================================
    # HISTORIAL
    # =========================================================

    def registrar_historial(
        self,
        expresion,
        resultado
    ):

        registro = (
            f"{expresion}  →  {resultado}"
        )

        self.historial.addItem(
            registro
        )

        if (
            self.historial.count()
            > self.LIMITE_REGISTROS
        ):
            self.historial.takeItem(0)

        self.historial.scrollToBottom()

    # =========================================================
    # FUNCIONES GENERALES
    # =========================================================

    def limpiar_pantalla(self):

        self.operacion_actual = ""

        self.pantalla.clear()

        self.resultado_reciente = False

    def nueva_operacion(self):

        self.limpiar_pantalla()

    def borrar_historial(self):

        self.historial.clear()

    def copiar_resultado(self):

        valor = self.pantalla.text()

        if not valor:
            return

        if valor in [
            "Error",
            "Error de Sintaxis"
        ]:
            return

        QApplication.clipboard().setText(
            valor
        )

    # =========================================================
    # INFORMACIÓN
    # =========================================================

    def mostrar_acerca(self):

        QMessageBox.information(
            self,
            "Acerca de NovaMath",
            "NovaMath v1.0\n\n"
            "Calculadora matemática desarrollada "
            "con PySide6.\n\n"
            "Incluye operaciones básicas, historial "
            "y evaluación segura de expresiones."
        )

    def mostrar_instrucciones(self):

        QMessageBox.information(
            self,
            "Instrucciones",
            "Puedes utilizar:\n\n"
            "• Suma\n"
            "• Resta\n"
            "• Multiplicación\n"
            "• División\n"
            "• Paréntesis\n"
            "• Números decimales\n"
            "• Historial de operaciones\n\n"
            "También puedes utilizar el teclado físico."
        )

    # =========================================================
    # TECLADO FÍSICO
    # =========================================================

    def keyPressEvent(self, evento):

        tecla = evento.key()
        caracter = evento.text()

        if tecla in (
            Qt.Key_Return,
            Qt.Key_Enter
        ):

            self.recibir_boton("=")

        elif tecla == Qt.Key_Escape:

            self.recibir_boton("AC")

        elif tecla == Qt.Key_Backspace:

            if self.operacion_actual:

                self.operacion_actual = (
                    self.operacion_actual[:-1]
                )

                self.pantalla.setText(
                    self.operacion_actual
                )

        elif caracter in "0123456789+-./*()":

            equivalencias = {
                "*": "×",
                "/": "÷"
            }

            valor = equivalencias.get(
                caracter,
                caracter
            )

            self.recibir_boton(
                valor
            )

        else:

            super().keyPressEvent(
                evento
            )


# =============================================================
# EJECUCIÓN DEL PROGRAMA
# =============================================================

if __name__ == "__main__":

    app = QApplication(
        sys.argv
    )

    ventana = NovaMath()

    ventana.show()

    sys.exit(
        app.exec()
    )
