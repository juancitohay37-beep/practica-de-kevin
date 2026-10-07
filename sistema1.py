import sys

from PySide6.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QTextEdit,
    QPushButton,
    QCheckBox,
    QRadioButton,
    QComboBox,
    QButtonGroup,
)


class AnalizadorTextoPySide6(QWidget):

    def __init__(self):

        super().__init__()

        self.setWindowTitle(
            "Sistema 1 - Analizador de Texto"
        )

        self.setFixedSize(
            520,
            500
        )

        # ====================================================
        # DISEÑO PRINCIPAL
        # ====================================================

        layout = QVBoxLayout()

        layout.setContentsMargins(
            25,
            20,
            25,
            20
        )

        layout.setSpacing(
            12
        )

        # ====================================================
        # TÍTULO
        # ====================================================

        titulo = QLabel(
            "◆ ANALIZADOR DE TEXTO"
        )

        titulo.setProperty(
            "rol",
            "titulo"
        )

        layout.addWidget(
            titulo
        )

        subtitulo = QLabel(
            "Analiza, transforma y guarda tus textos"
        )

        subtitulo.setProperty(
            "rol",
            "subtitulo"
        )

        layout.addWidget(
            subtitulo
        )

        # ====================================================
        # TEXTO
        # ====================================================

        etiqueta_texto = QLabel(
            "Ingrese una frase o texto:"
        )

        etiqueta_texto.setProperty(
            "rol",
            "etiqueta"
        )

        layout.addWidget(
            etiqueta_texto
        )

        self.input_texto = QLineEdit()

        self.input_texto.setPlaceholderText(
            "Escriba aquí su texto..."
        )

        layout.addWidget(
            self.input_texto
        )

        # ====================================================
        # OPERACIÓN
        # ====================================================

        etiqueta_operacion = QLabel(
            "Seleccione una operación:"
        )

        etiqueta_operacion.setProperty(
            "rol",
            "etiqueta"
        )

        layout.addWidget(
            etiqueta_operacion
        )

        self.combo_op = QComboBox()

        self.combo_op.addItems([
            "Contar Caracteres",
            "Contar Palabras",
            "Convertir a Mayúsculas",
            "Invertir Texto"
        ])

        layout.addWidget(
            self.combo_op
        )

        # ====================================================
        # OPCIÓN ESPACIOS
        # ====================================================

        self.chk_espacios = QCheckBox(
            "Incluir espacios en el conteo"
        )

        layout.addWidget(
            self.chk_espacios
        )

        # ====================================================
        # HISTORIAL
        # ====================================================

        etiqueta_historial = QLabel(
            "¿Guardar resultado en el historial?"
        )

        etiqueta_historial.setProperty(
            "rol",
            "etiqueta"
        )

        layout.addWidget(
            etiqueta_historial
        )

        row_radio = QHBoxLayout()

        self.radio_si = QRadioButton(
            "Sí"
        )

        self.radio_no = QRadioButton(
            "No"
        )

        self.radio_si.setChecked(
            True
        )

        self.bg_historial = QButtonGroup(
            self
        )

        self.bg_historial.addButton(
            self.radio_si
        )

        self.bg_historial.addButton(
            self.radio_no
        )

        row_radio.addWidget(
            self.radio_si
        )

        row_radio.addWidget(
            self.radio_no
        )

        row_radio.addStretch()

        layout.addLayout(
            row_radio
        )

        # ====================================================
        # BOTÓN PROCESAR
        # ====================================================

        self.btn_procesar = QPushButton(
            "ANALIZAR / PROCESAR"
        )

        self.btn_procesar.setProperty(
            "rol",
            "procesar"
        )

        self.btn_procesar.clicked.connect(
            self.procesar
        )

        layout.addWidget(
            self.btn_procesar
        )

        # ====================================================
        # RESULTADO
        # ====================================================

        self.lbl_resultado = QLabel(
            "Resultado: -"
        )

        self.lbl_resultado.setProperty(
            "rol",
            "resultado"
        )

        self.lbl_resultado.setWordWrap(
            True
        )

        layout.addWidget(
            self.lbl_resultado
        )

        # ====================================================
        # HISTORIAL
        # ====================================================

        etiqueta_historial_lista = QLabel(
            "Historial de operaciones"
        )

        etiqueta_historial_lista.setProperty(
            "rol",
            "etiqueta"
        )

        layout.addWidget(
            etiqueta_historial_lista
        )

        self.txt_historial = QTextEdit()

        self.txt_historial.setReadOnly(
            True
        )

        self.txt_historial.setPlaceholderText(
            "Aquí aparecerán las operaciones realizadas..."
        )

        layout.addWidget(
            self.txt_historial
        )

        # ====================================================
        # APLICAR LAYOUT
        # ====================================================

        self.setLayout(
            layout
        )

        # ====================================================
        # ESTILOS
        # ====================================================

        self.aplicar_estilos()

    # ========================================================
    # PROCESAR TEXTO
    # ========================================================

    def procesar(self):

        texto = self.input_texto.text()

        opcion = self.combo_op.currentText()

        res = ""

        if opcion == "Contar Caracteres":

            if self.chk_espacios.isChecked():

                cant = len(texto)

            else:

                cant = len(
                    texto.replace(" ", "")
                )

            res = (
                f"Cantidad de caracteres: {cant}"
            )

        elif opcion == "Contar Palabras":

            palabras = texto.split()

            res = (
                f"Cantidad de palabras: "
                f"{len(palabras)}"
            )

        elif opcion == "Convertir a Mayúsculas":

            res = (
                f"Texto: {texto.upper()}"
            )

        elif opcion == "Invertir Texto":

            res = (
                f"Texto invertido: "
                f"{texto[::-1]}"
            )

        # ====================================================
        # MOSTRAR RESULTADO
        # ====================================================

        self.lbl_resultado.setText(
            f"Resultado: {res}"
        )

        # ====================================================
        # GUARDAR HISTORIAL
        # ====================================================

        if self.radio_si.isChecked():

            self.txt_historial.append(
                f"[{opcion}] "
                f"{texto} → {res}"
            )

    # ========================================================
    # ESTILOS
    # ========================================================

    def aplicar_estilos(self):

        qss = """

        /* =================================================
           VENTANA
           ================================================= */

        QWidget {
            background-color: #0f1020;
            color: #f1f5f9;
            font-family: "Segoe UI";
            font-size: 13px;
        }

        /* =================================================
           TÍTULO
           ================================================= */

        QLabel[rol="titulo"] {
            color: #c084fc;
            font-size: 22px;
            font-weight: bold;
            padding-bottom: 2px;
        }

        QLabel[rol="subtitulo"] {
            color: #94a3b8;
            font-size: 11px;
            padding-bottom: 8px;
        }

        /* =================================================
           ETIQUETAS
           ================================================= */

        QLabel[rol="etiqueta"] {
            color: #ddd6fe;
            font-size: 12px;
            font-weight: bold;
        }

        /* =================================================
           CAMPO DE TEXTO
           ================================================= */

        QLineEdit {
            background-color: #191a2f;
            color: #f8fafc;
            border: 2px solid #373060;
            border-radius: 8px;
            padding: 9px;
            font-size: 14px;
        }

        QLineEdit:focus {
            border: 2px solid #a855f7;
            background-color: #1d1b35;
        }

        /* =================================================
           COMBOBOX
           ================================================= */

        QComboBox {
            background-color: #191a2f;
            color: #f8fafc;
            border: 2px solid #373060;
            border-radius: 8px;
            padding: 8px;
            min-height: 20px;
        }

        QComboBox:hover {
            border: 2px solid #7c3aed;
        }

        QComboBox:focus {
            border: 2px solid #a855f7;
        }

        QComboBox QAbstractItemView {
            background-color: #191a2f;
            color: #f8fafc;
            selection-background-color: #7c3aed;
            selection-color: white;
            border: 1px solid #6d28d9;
        }

        /* =================================================
           CHECKBOX
           ================================================= */

        QCheckBox {
            color: #cbd5e1;
            spacing: 8px;
        }

        QCheckBox:hover {
            color: #e9d5ff;
        }

        QCheckBox::indicator {
            width: 17px;
            height: 17px;
        }

        QCheckBox::indicator:unchecked {
            background-color: #191a2f;
            border: 2px solid #51457a;
            border-radius: 4px;
        }

        QCheckBox::indicator:checked {
            background-color: #9333ea;
            border: 2px solid #c084fc;
            border-radius: 4px;
        }

        /* =================================================
           RADIO BUTTONS
           ================================================= */

        QRadioButton {
            color: #cbd5e1;
            spacing: 8px;
        }

        QRadioButton::indicator {
            width: 16px;
            height: 16px;
            border-radius: 8px;
            border: 2px solid #51457a;
            background-color: #191a2f;
        }

        QRadioButton::indicator:checked {
            background-color: #a855f7;
            border: 2px solid #d8b4fe;
        }

        /* =================================================
           BOTÓN PRINCIPAL
           ================================================= */

        QPushButton[rol="procesar"] {
            background-color: #7c3aed;
            color: white;
            border: none;
            border-radius: 8px;
            padding: 11px;
            font-size: 13px;
            font-weight: bold;
        }

        QPushButton[rol="procesar"]:hover {
            background-color: #9333ea;
        }

        QPushButton[rol="procesar"]:pressed {
            background-color: #6d28d9;
        }

        /* =================================================
           RESULTADO
           ================================================= */

        QLabel[rol="resultado"] {
            background-color: #17152a;
            color: #f0abfc;
            border-left: 4px solid #d946ef;
            border-radius: 6px;
            padding: 10px;
            font-size: 14px;
            font-weight: bold;
        }

        /* =================================================
           HISTORIAL
           ================================================= */

        QTextEdit {
            background-color: #141525;
            color: #c4b5fd;
            border: 2px solid #302653;
            border-radius: 8px;
            padding: 8px;
            font-size: 12px;
        }

        QTextEdit:focus {
            border: 2px solid #7c3aed;
        }

        """

        self.setStyleSheet(
            qss
        )


# ============================================================
# EJECUCIÓN
# ============================================================

if __name__ == "__main__":

    app = QApplication(
        sys.argv
    )

    window = AnalizadorTextoPySide6()

    window.show()

    sys.exit(
        app.exec()
    )
