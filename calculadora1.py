import ast
import operator
import sys

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QGridLayout,
    QLineEdit,
    QPushButton,
    QLabel,
    QListWidget,
    QHBoxLayout,
)


# ============================================================
# MOTOR DE OPERACIONES
# ============================================================

class MotorCalculo:
    OPERADORES = {
        ast.Add: operator.add,
        ast.Sub: operator.sub,
        ast.Mult: operator.mul,
        ast.Div: operator.truediv,
        ast.USub: operator.neg,
        ast.UAdd: operator.pos,
    }

    @classmethod
    def calcular(cls, expresion):
        # Completar paréntesis que hayan quedado abiertos
        abiertos = expresion.count("(") - expresion.count(")")

        if abiertos > 0:
            expresion += ")" * abiertos

        try:
            arbol = ast.parse(expresion, mode="eval")
            return cls._resolver(arbol.body)

        except ZeroDivisionError:
            raise

        except Exception as error:
            raise ValueError("Operación inválida") from error

    @classmethod
    def _resolver(cls, nodo):

        if isinstance(nodo, ast.Constant):

            if isinstance(nodo.value, (int, float)):
                return nodo.value

            raise ValueError("Número no válido")

        if isinstance(nodo, ast.BinOp):

            izquierda = cls._resolver(nodo.left)
            derecha = cls._resolver(nodo.right)

            operacion = cls.OPERADORES.get(type(nodo.op))

            if operacion is None:
                raise ValueError("Operador no permitido")

            return operacion(izquierda, derecha)

        if isinstance(nodo, ast.UnaryOp):

            valor = cls._resolver(nodo.operand)

            operacion = cls.OPERADORES.get(type(nodo.op))

            if operacion is None:
                raise ValueError("Operador no permitido")

            return operacion(valor)

        raise ValueError("Expresión no permitida")


# ============================================================
# VENTANA PRINCIPAL
# ============================================================

class CalculadoraPro(QWidget):

    MAX_HISTORIAL = 6

    def __init__(self):
        super().__init__()

        self.operacion_actual = ""
        self.ultimo_resultado = False

        self.configurar_ventana()
        self.crear_interfaz()
        self.aplicar_estilos()

    # ========================================================
    # CONFIGURACIÓN
    # ========================================================

    def configurar_ventana(self):
        self.setWindowTitle("MathBox - Calculadora")
        self.setFixedSize(390, 570)

    # ========================================================
    # INTERFAZ
    # ========================================================

    def crear_interfaz(self):

        principal = QVBoxLayout()
        principal.setContentsMargins(18, 18, 18, 18)
        principal.setSpacing(12)

        # ----------------------------------------------------
        # ENCABEZADO
        # ----------------------------------------------------

        titulo = QLabel("MATHBOX")
        titulo.setObjectName("titulo")

        subtitulo = QLabel("Calculadora matemática")

        principal.addWidget(titulo)
        principal.addWidget(subtitulo)

        # ----------------------------------------------------
        # PANTALLA
        # ----------------------------------------------------

        self.pantalla = QLineEdit()
        self.pantalla.setReadOnly(True)
        self.pantalla.setAlignment(Qt.AlignRight)
        self.pantalla.setPlaceholderText("0")

        principal.addWidget(self.pantalla)

        # ----------------------------------------------------
        # BOTONES
        # ----------------------------------------------------

        teclado = QGridLayout()
        teclado.setSpacing(7)

        botones = [
            ("AC", 0, 0),
            ("⌫", 0, 1),
            ("(", 0, 2),
            (")", 0, 3),

            ("7", 1, 0),
            ("8", 1, 1),
            ("9", 1, 2),
            ("÷", 1, 3),

            ("4", 2, 0),
            ("5", 2, 1),
            ("6", 2, 2),
            ("×", 2, 3),

            ("1", 3, 0),
            ("2", 3, 1),
            ("3", 3, 2),
            ("-", 3, 3),

            ("0", 4, 0),
            (".", 4, 1),
            ("+", 4, 2),
            ("=", 4, 3),
        ]

        for texto, fila, columna in botones:

            boton = QPushButton(texto)
            boton.setMinimumHeight(48)

            if texto in ["+", "-", "×", "÷"]:
                boton.setProperty("categoria", "operador")

            elif texto == "=":
                boton.setProperty("categoria", "igual")

            elif texto in ["AC", "⌫", "(", ")"]:
                boton.setProperty("categoria", "funcion")

            else:
                boton.setProperty("categoria", "numero")

            boton.clicked.connect(
                lambda _, valor=texto:
                self.procesar_boton(valor)
            )

            teclado.addWidget(boton, fila, columna)

        principal.addLayout(teclado)

        # ----------------------------------------------------
        # BOTONES EXTRA
        # ----------------------------------------------------

        fila_extra = QHBoxLayout()
        fila_extra.setSpacing(7)

        self.btn_borrar_historial = QPushButton(
            "🗑 Limpiar historial"
        )
        self.btn_borrar_historial.setObjectName("btnHistorial")

        self.btn_ultimo = QPushButton(
            "↩ Usar resultado"
        )
        self.btn_ultimo.setObjectName("btnResultado")

        self.btn_borrar_historial.clicked.connect(
            self.limpiar_historial
        )

        self.btn_ultimo.clicked.connect(
            self.usar_ultimo_resultado
        )

        fila_extra.addWidget(self.btn_borrar_historial)
        fila_extra.addWidget(self.btn_ultimo)

        principal.addLayout(fila_extra)

        # ----------------------------------------------------
        # HISTORIAL
        # ----------------------------------------------------

        etiqueta_historial = QLabel(
            "Historial reciente"
        )
        etiqueta_historial.setObjectName("historialTitulo")

        principal.addWidget(etiqueta_historial)

        self.lista_historial = QListWidget()
        self.lista_historial.setFocusPolicy(Qt.NoFocus)

        principal.addWidget(self.lista_historial)

        self.setLayout(principal)

    # ========================================================
    # ESTILOS
    # ========================================================

    def aplicar_estilos(self):

        estilo = """

        QWidget {
            background-color: #111827;
            color: #f9fafb;
            font-family: Segoe UI;
        }

        QLabel#titulo {
            color: #22d3ee;
            font-size: 24px;
            font-weight: bold;
        }

        QLabel {
            color: #9ca3af;
            font-size: 12px;
        }

        QLabel#historialTitulo {
            color: #e5e7eb;
            font-size: 13px;
            font-weight: bold;
        }

        QLineEdit {
            background-color: #030712;
            border: 2px solid #374151;
            border-radius: 10px;
            color: #67e8f9;
            font-size: 27px;
            font-weight: bold;
            padding: 12px;
        }

        QLineEdit:focus {
            border: 2px solid #06b6d4;
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
            background-color: #f59e0b;
            color: #111827;
        }

        QPushButton[categoria="operador"]:hover {
            background-color: #fbbf24;
        }

        QPushButton[categoria="funcion"] {
            background-color: #ec4899;
            color: white;
        }

        QPushButton[categoria="funcion"]:hover {
            background-color: #f472b6;
        }

        QPushButton[categoria="igual"] {
            background-color: #06b6d4;
            color: #082f49;
        }

        QPushButton[categoria="igual"]:hover {
            background-color: #22d3ee;
        }

        QPushButton#btnHistorial {
            background-color: #374151;
            color: #e5e7eb;
            font-size: 11px;
            padding: 8px;
        }

        QPushButton#btnResultado {
            background-color: #8b5cf6;
            color: white;
            font-size: 11px;
            padding: 8px;
        }

        QPushButton:pressed {
            background-color: #1f2937;
        }

        QListWidget {
            background-color: #030712;
            border: 1px solid #374151;
            border-radius: 8px;
            color: #d1d5db;
            padding: 5px;
        }

        QListWidget::item {
            padding: 6px;
            border-bottom: 1px solid #1f2937;
        }

        QListWidget::item:selected {
            background-color: #164e63;
        }
        """

        self.setStyleSheet(estilo)

    # ========================================================
    # BOTONES
    # ========================================================

    def procesar_boton(self, valor):

        if valor == "AC":
            self.limpiar()
            return

        if valor == "⌫":
            self.borrar_ultimo()
            return

        if valor == "=":
            self.realizar_calculo()
            return

        # Si acabamos de obtener un resultado y escribimos
        # un número, comenzamos una nueva operación.
        if self.ultimo_resultado and valor.isdigit():
            self.operacion_actual = ""

        self.ultimo_resultado = False

        self.operacion_actual += valor

        self.pantalla.setText(
            self.operacion_actual
        )

    # ========================================================
    # LIMPIAR
    # ========================================================

    def limpiar(self):

        self.operacion_actual = ""
        self.ultimo_resultado = False

        self.pantalla.clear()

    # ========================================================
    # BORRAR ÚLTIMO CARÁCTER
    # ========================================================

    def borrar_ultimo(self):

        if self.operacion_actual:

            self.operacion_actual = (
                self.operacion_actual[:-1]
            )

            self.pantalla.setText(
                self.operacion_actual
            )

    # ========================================================
    # CALCULAR
    # ========================================================

    def realizar_calculo(self):

        if not self.operacion_actual:
            return

        expresion = (
            self.operacion_actual
            .replace("÷", "/")
            .replace("×", "*")
        )

        try:

            resultado = MotorCalculo.calcular(
                expresion
            )

            if (
                isinstance(resultado, float)
                and resultado.is_integer()
            ):
                resultado = int(resultado)

            resultado = str(resultado)

            texto_historial = (
                f"{self.operacion_actual} = {resultado}"
            )

            self.agregar_historial(
                texto_historial
            )

            self.pantalla.setText(
                resultado
            )

            self.operacion_actual = resultado
            self.ultimo_resultado = True

        except ZeroDivisionError:

            self.pantalla.setText(
                "No se puede dividir entre 0"
            )

            self.operacion_actual = ""
            self.ultimo_resultado = False

        except Exception:

            self.pantalla.setText(
                "Operación incorrecta"
            )

            self.operacion_actual = ""
            self.ultimo_resultado = False

    # ========================================================
    # HISTORIAL
    # ========================================================

    def agregar_historial(self, texto):

        self.lista_historial.addItem(texto)

        if (
            self.lista_historial.count()
            > self.MAX_HISTORIAL
        ):
            self.lista_historial.takeItem(0)

        self.lista_historial.scrollToBottom()

    def limpiar_historial(self):

        self.lista_historial.clear()

    # ========================================================
    # USAR ÚLTIMO RESULTADO
    # ========================================================

    def usar_ultimo_resultado(self):

        if not self.operacion_actual:
            return

        self.pantalla.setText(
            self.operacion_actual
        )

    # ========================================================
    # TECLADO
    # ========================================================

    def keyPressEvent(self, evento):

        tecla = evento.key()
        texto = evento.text()

        if tecla in (
            Qt.Key_Return,
            Qt.Key_Enter
        ):
            self.realizar_calculo()

        elif tecla == Qt.Key_Escape:
            self.limpiar()

        elif tecla == Qt.Key_Backspace:
            self.borrar_ultimo()

        elif texto in "0123456789+-./*()":

            conversion = {
                "*": "×",
                "/": "÷"
            }

            valor = conversion.get(
                texto,
                texto
            )

            self.procesar_boton(valor)

        else:
            super().keyPressEvent(evento)


# ============================================================
# EJECUCIÓN
# ============================================================

if __name__ == "__main__":

    app = QApplication(sys.argv)

    ventana = CalculadoraPro()
    ventana.show()

    sys.exit(app.exec())