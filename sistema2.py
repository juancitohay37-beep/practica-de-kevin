import sys

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QApplication,
    QCheckBox,
    QComboBox,
    QDialog,
    QFormLayout,
    QFrame,
    QGridLayout,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QListWidget,
    QListWidgetItem,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QRadioButton,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)


# ==============================================================================
# ESTILOS
# ==============================================================================

ESTILO_GLOBAL = """

QMainWindow {
    background-color: #101827;
}

QWidget {
    color: #e5e7eb;
    font-family: "Segoe UI";
    font-size: 13px;
}


/* TARJETAS */

QFrame#CardFrame {
    background-color: #182335;
    border: 1px solid #29384f;
    border-radius: 14px;
}


/* ENCABEZADO */

QLabel#HeaderTitle {
    font-size: 26px;
    font-weight: bold;
    color: #f59e0b;
}

QLabel#HeaderSubtitle {
    font-size: 13px;
    color: #94a3b8;
}


/* CAMPOS */

QLineEdit,
QComboBox,
QTextEdit,
QListWidget {
    background-color: #0f172a;
    color: #f8fafc;
    border: 1px solid #334155;
    border-radius: 8px;
    padding: 8px;
}

QLineEdit:focus,
QComboBox:focus,
QTextEdit:focus {
    border: 2px solid #f59e0b;
}


/* COMBOBOX */

QComboBox {
    min-height: 22px;
}

QComboBox:hover {
    border: 1px solid #fbbf24;
}

QComboBox QAbstractItemView {
    background-color: #182335;
    color: #f8fafc;
    border: 1px solid #475569;
    selection-background-color: #d97706;
    selection-color: white;
}


/* LISTA */

QListWidget {
    background-color: #0f172a;
    border: 1px solid #334155;
    border-radius: 9px;
    padding: 6px;
}

QListWidget::item {
    padding: 10px;
    margin: 2px;
    border-radius: 6px;
    color: #e2e8f0;
}

QListWidget::item:hover {
    background-color: #263449;
}

QListWidget::item:selected {
    background-color: #b45309;
    color: white;
}


/* BOTONES */

QPushButton {
    background-color: #d97706;
    color: white;
    border: none;
    border-radius: 8px;
    padding: 10px 14px;
    font-weight: bold;
}

QPushButton:hover {
    background-color: #f59e0b;
}

QPushButton:pressed {
    background-color: #b45309;
}


/* BOTÓN ELIMINAR */

QPushButton#BtnEliminar {
    background-color: #be123c;
}

QPushButton#BtnEliminar:hover {
    background-color: #e11d48;
}


/* BOTONES SECUNDARIOS */

QPushButton#BtnSecundario {
    background-color: #334155;
    color: #e2e8f0;
    border: 1px solid #475569;
}

QPushButton#BtnSecundario:hover {
    background-color: #475569;
}


/* BOTÓN FICHA */

QPushButton#BtnFicha {
    background-color: #2563eb;
}

QPushButton#BtnFicha:hover {
    background-color: #3b82f6;
}


/* GROUPBOX */

QGroupBox {
    border: 1px solid #334155;
    border-radius: 9px;
    margin-top: 12px;
    padding-top: 8px;
    font-weight: bold;
    color: #fbbf24;
}

QGroupBox::title {
    subcontrol-origin: margin;
    left: 12px;
    padding: 0 7px;
    background-color: #182335;
    color: #fbbf24;
}


/* CHECKBOX */

QCheckBox {
    color: #e2e8f0;
    spacing: 7px;
}

QCheckBox:hover {
    color: #fbbf24;
}

QCheckBox::indicator {
    width: 17px;
    height: 17px;
}

QCheckBox::indicator:unchecked {
    background-color: #0f172a;
    border: 2px solid #475569;
    border-radius: 4px;
}

QCheckBox::indicator:checked {
    background-color: #d97706;
    border: 2px solid #fbbf24;
    border-radius: 4px;
}


/* RADIO */

QRadioButton {
    color: #e2e8f0;
    spacing: 7px;
}

QRadioButton:hover {
    color: #fbbf24;
}

QRadioButton::indicator {
    width: 16px;
    height: 16px;
    border-radius: 8px;
    border: 2px solid #475569;
    background-color: #0f172a;
}

QRadioButton::indicator:checked {
    background-color: #f59e0b;
    border: 2px solid #fbbf24;
}


/* DIALOGOS */

QDialog {
    background-color: #101827;
}

"""


# ==============================================================================
# FICHA DEL ESTUDIANTE
# ==============================================================================

class FichaEstudianteDialog(QDialog):

    def __init__(self, datos, parent=None):

        super().__init__(parent)

        self.setWindowTitle(
            "Ficha del Estudiante"
        )

        self.resize(
            440,
            390
        )

        self.setStyleSheet(
            ESTILO_GLOBAL
        )

        layout = QVBoxLayout()

        layout.setContentsMargins(
            18,
            18,
            18,
            18
        )

        layout.setSpacing(
            15
        )

        # ------------------------------------------------------------------
        # TARJETA
        # ------------------------------------------------------------------

        card = QFrame()

        card.setObjectName(
            "CardFrame"
        )

        card_layout = QVBoxLayout(
            card
        )

        # ------------------------------------------------------------------
        # TÍTULO
        # ------------------------------------------------------------------

        titulo = QLabel(
            "🎓 FICHA DEL ESTUDIANTE"
        )

        titulo.setStyleSheet(
            """
            font-size: 19px;
            font-weight: bold;
            color: #f59e0b;
            padding-bottom: 5px;
            """
        )

        # ------------------------------------------------------------------
        # INFORMACIÓN
        # ------------------------------------------------------------------

        detalles = f"""
        <div style='line-height: 1.8;'>

        <b style='color:#fbbf24;'>Estudiante:</b>
        {datos['nombre']}<br>

        <b style='color:#fbbf24;'>C.I. / DNI:</b>
        {datos['ci']}<br>

        <b style='color:#fbbf24;'>Curso:</b>
        {datos['curso']}<br>

        <b style='color:#fbbf24;'>Horario:</b>
        {datos['horario']}<br>

        <b style='color:#fbbf24;'>Materias favoritas:</b>
        {datos['materias'] or 'Sin registro'}<br><br>

        <b style='color:#fbbf24;'>Rendimiento / Comentarios:</b><br>

        {datos['comentarios'] or 'Sin comentarios'}

        </div>
        """

        lbl_info = QLabel(
            detalles
        )

        lbl_info.setWordWrap(
            True
        )

        card_layout.addWidget(
            titulo
        )

        card_layout.addWidget(
            lbl_info
        )

        # ------------------------------------------------------------------
        # CERRAR
        # ------------------------------------------------------------------

        btn_cerrar = QPushButton(
            "Cerrar"
        )

        btn_cerrar.setObjectName(
            "BtnSecundario"
        )

        btn_cerrar.clicked.connect(
            self.accept
        )

        layout.addWidget(
            card
        )

        layout.addWidget(
            btn_cerrar
        )

        self.setLayout(
            layout
        )


# ==============================================================================
# APLICACIÓN PRINCIPAL
# ==============================================================================

class AulaGestionApp(QMainWindow):

    def __init__(self):

        super().__init__()

        self.setWindowTitle(
            "AulaGestión - Registro Académico"
        )

        self.resize(
            1000,
            680
        )

        self.registros = []

        self.id_edicion = None

        self.init_ui()

        self.setStyleSheet(
            ESTILO_GLOBAL
        )


    # ==========================================================================
    # INTERFAZ
    # ==========================================================================

    def init_ui(self):

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
            15
        )


        # ======================================================================
        # ENCABEZADO
        # ======================================================================

        header = QHBoxLayout()

        titulo = QLabel(
            "◆ AulaGestión"
        )

        titulo.setObjectName(
            "HeaderTitle"
        )

        subtitulo = QLabel(
            "Sistema de Registro Académico"
        )

        subtitulo.setObjectName(
            "HeaderSubtitle"
        )

        header.addWidget(
            titulo
        )

        header.addStretch()

        header.addWidget(
            subtitulo
        )

        layout_principal.addLayout(
            header
        )


        # ======================================================================
        # CONTENIDO
        # ======================================================================

        contenido = QHBoxLayout()


        # ======================================================================
        # FORMULARIO
        # ======================================================================

        frame_form = QFrame()

        frame_form.setObjectName(
            "CardFrame"
        )

        layout_form = QVBoxLayout(
            frame_form
        )

        layout_form.setSpacing(
            10
        )


        # ======================================================================
        # DATOS DEL ESTUDIANTE
        # ======================================================================

        formulario = QFormLayout()

        formulario.setSpacing(
            10
        )

        self.txt_nombre = QLineEdit()

        self.txt_nombre.setPlaceholderText(
            "Nombre completo"
        )

        self.txt_ci = QLineEdit()

        self.txt_ci.setPlaceholderText(
            "Número de documento"
        )

        self.cmb_curso = QComboBox()

        self.cmb_curso.addItems(
            [
                "1º Secundaria",
                "2º Secundaria",
                "3º Secundaria",
                "4º Secundaria",
                "5º Secundaria",
                "6º Secundaria",
            ]
        )

        formulario.addRow(
            "Estudiante:",
            self.txt_nombre
        )

        formulario.addRow(
            "C.I.:",
            self.txt_ci
        )

        formulario.addRow(
            "Curso:",
            self.cmb_curso
        )

        layout_form.addLayout(
            formulario
        )


        # ======================================================================
        # HORARIO
        # ======================================================================

        box_horario = QGroupBox(
            "Horario de Clases"
        )

        layout_horario = QHBoxLayout(
            box_horario
        )

        self.rad_manana = QRadioButton(
            "Mañana"
        )

        self.rad_tarde = QRadioButton(
            "Tarde"
        )

        self.rad_noche = QRadioButton(
            "Noche"
        )

        self.rad_manana.setChecked(
            True
        )

        layout_horario.addWidget(
            self.rad_manana
        )

        layout_horario.addWidget(
            self.rad_tarde
        )

        layout_horario.addWidget(
            self.rad_noche
        )

        layout_form.addWidget(
            box_horario
        )


        # ======================================================================
        # MATERIAS FAVORITAS
        # ======================================================================

        box_materias = QGroupBox(
            "Materias Favoritas"
        )

        grid_materias = QGridLayout(
            box_materias
        )

        self.chk_matematica = QCheckBox(
            "Matemática"
        )

        self.chk_fisica = QCheckBox(
            "Física"
        )

        self.chk_quimica = QCheckBox(
            "Química"
        )

        self.chk_historia = QCheckBox(
            "Historia"
        )

        grid_materias.addWidget(
            self.chk_matematica,
            0,
            0
        )

        grid_materias.addWidget(
            self.chk_fisica,
            0,
            1
        )

        grid_materias.addWidget(
            self.chk_quimica,
            1,
            0
        )

        grid_materias.addWidget(
            self.chk_historia,
            1,
            1
        )

        layout_form.addWidget(
            box_materias
        )


        # ======================================================================
        # COMENTARIOS
        # ======================================================================

        lbl_comentarios = QLabel(
            "Rendimiento / Comentarios:"
        )

        lbl_comentarios.setStyleSheet(
            """
            color: #fbbf24;
            font-weight: bold;
            """
        )

        layout_form.addWidget(
            lbl_comentarios
        )

        self.txt_comentarios = QTextEdit()

        self.txt_comentarios.setPlaceholderText(
            "Escriba observaciones sobre el rendimiento del estudiante..."
        )

        layout_form.addWidget(
            self.txt_comentarios
        )


        # ======================================================================
        # BOTONES
        # ======================================================================

        botones = QHBoxLayout()

        self.btn_guardar = QPushButton(
            "Guardar"
        )

        self.btn_editar = QPushButton(
            "Editar"
        )

        self.btn_editar.setObjectName(
            "BtnSecundario"
        )

        self.btn_eliminar = QPushButton(
            "Eliminar"
        )

        self.btn_eliminar.setObjectName(
            "BtnEliminar"
        )

        self.btn_limpiar = QPushButton(
            "Limpiar"
        )

        self.btn_limpiar.setObjectName(
            "BtnSecundario"
        )

        botones.addWidget(
            self.btn_guardar
        )

        botones.addWidget(
            self.btn_editar
        )

        botones.addWidget(
            self.btn_eliminar
        )

        botones.addWidget(
            self.btn_limpiar
        )

        layout_form.addLayout(
            botones
        )


        # ======================================================================
        # PANEL DERECHO
        # ======================================================================

        frame_lista = QFrame()

        frame_lista.setObjectName(
            "CardFrame"
        )

        layout_lista = QVBoxLayout(
            frame_lista
        )

        layout_lista.setSpacing(
            10
        )

        lbl_busqueda = QLabel(
            "🔎 Buscar estudiante"
        )

        lbl_busqueda.setStyleSheet(
            """
            color: #fbbf24;
            font-weight: bold;
            """
        )

        layout_lista.addWidget(
            lbl_busqueda
        )

        self.txt_buscar = QLineEdit()

        self.txt_buscar.setPlaceholderText(
            "Nombre o número de documento..."
        )

        layout_lista.addWidget(
            self.txt_buscar
        )

        self.lst_estudiantes = QListWidget()

        layout_lista.addWidget(
            self.lst_estudiantes
        )

        self.btn_ver_ficha = QPushButton(
            "📄 Ver Ficha"
        )

        self.btn_ver_ficha.setObjectName(
            "BtnFicha"
        )

        layout_lista.addWidget(
            self.btn_ver_ficha
        )


        # ======================================================================
        # ENSAMBLAR
        # ======================================================================

        contenido.addWidget(
            frame_form,
            3
        )

        contenido.addWidget(
            frame_lista,
            2
        )

        layout_principal.addLayout(
            contenido
        )


        # ======================================================================
        # EVENTOS
        # ======================================================================

        self.btn_guardar.clicked.connect(
            self.guardar_estudiante
        )

        self.btn_editar.clicked.connect(
            self.cargar_para_editar
        )

        self.btn_eliminar.clicked.connect(
            self.eliminar_estudiante
        )

        self.btn_limpiar.clicked.connect(
            self.limpiar_formulario
        )

        self.btn_ver_ficha.clicked.connect(
            self.abrir_ficha
        )

        self.txt_buscar.textChanged.connect(
            self.refrescar_lista
        )


    # ==========================================================================
    # CAPTURAR DATOS
    # ==========================================================================

    def capturar_datos(self):

        materias = []

        if self.chk_matematica.isChecked():
            materias.append(
                "Matemática"
            )

        if self.chk_fisica.isChecked():
            materias.append(
                "Física"
            )

        if self.chk_quimica.isChecked():
            materias.append(
                "Química"
            )

        if self.chk_historia.isChecked():
            materias.append(
                "Historia"
            )


        if self.rad_manana.isChecked():

            horario = "Mañana"

        elif self.rad_tarde.isChecked():

            horario = "Tarde"

        else:

            horario = "Noche"


        return {

            "nombre":
                self.txt_nombre.text().strip(),

            "ci":
                self.txt_ci.text().strip(),

            "curso":
                self.cmb_curso.currentText(),

            "horario":
                horario,

            "materias":
                ", ".join(materias),

            "comentarios":
                self.txt_comentarios.toPlainText().strip()
        }


    # ==========================================================================
    # VALIDACIÓN
    # ==========================================================================

    def es_valido(self, datos):

        if len(datos["nombre"]) < 3:

            QMessageBox.warning(
                self,
                "Datos incorrectos",
                "El nombre debe tener al menos 3 caracteres."
            )

            return False


        if not datos["ci"].isdigit():

            QMessageBox.warning(
                self,
                "Datos incorrectos",
                "El C.I. debe contener únicamente números."
            )

            return False


        return True


    # ==========================================================================
    # GUARDAR
    # ==========================================================================

    def guardar_estudiante(self):

        datos = self.capturar_datos()

        if not self.es_valido(datos):
            return


        if self.id_edicion is not None:

            self.registros[
                self.id_edicion
            ] = datos

            self.id_edicion = None

            QMessageBox.information(
                self,
                "Registro actualizado",
                "Los datos del estudiante fueron actualizados."
            )

        else:

            self.registros.append(
                datos
            )

            QMessageBox.information(
                self,
                "Registro guardado",
                "El estudiante fue registrado correctamente."
            )


        self.refrescar_lista()

        self.limpiar_formulario()


    # ==========================================================================
    # REFRESCAR LISTA
    # ==========================================================================

    def refrescar_lista(self):

        filtro = (
            self.txt_buscar.text().lower()
        )

        self.lst_estudiantes.clear()


        for indice, estudiante in enumerate(
            self.registros
        ):

            nombre = estudiante[
                "nombre"
            ].lower()

            ci = estudiante[
                "ci"
            ].lower()


            if (
                filtro in nombre
                or filtro in ci
            ):

                item = QListWidgetItem(
                    f"{estudiante['nombre']}  |  "
                    f"CI: {estudiante['ci']}  |  "
                    f"{estudiante['curso']}"
                )

                item.setData(
                    Qt.UserRole,
                    indice
                )

                self.lst_estudiantes.addItem(
                    item
                )


    # ==========================================================================
    # OBTENER SELECCIÓN
    # ==========================================================================

    def obtener_indice(self):

        item = (
            self.lst_estudiantes.currentItem()
        )

        if item:

            return item.data(
                Qt.UserRole
            )

        return None


    # ==========================================================================
    # EDITAR
    # ==========================================================================

    def cargar_para_editar(self):

        indice = self.obtener_indice()

        if indice is None:

            QMessageBox.warning(
                self,
                "Atención",
                "Selecciona un estudiante de la lista."
            )

            return


        estudiante = self.registros[
            indice
        ]


        self.txt_nombre.setText(
            estudiante["nombre"]
        )

        self.txt_ci.setText(
            estudiante["ci"]
        )

        self.cmb_curso.setCurrentText(
            estudiante["curso"]
        )


        # HORARIO

        if estudiante["horario"] == "Mañana":

            self.rad_manana.setChecked(
                True
            )

        elif estudiante["horario"] == "Tarde":

            self.rad_tarde.setChecked(
                True
            )

        else:

            self.rad_noche.setChecked(
                True
            )


        # MATERIAS

        materias = estudiante[
            "materias"
        ]

        self.chk_matematica.setChecked(
            "Matemática" in materias
        )

        self.chk_fisica.setChecked(
            "Física" in materias
        )

        self.chk_quimica.setChecked(
            "Química" in materias
        )

        self.chk_historia.setChecked(
            "Historia" in materias
        )


        self.txt_comentarios.setPlainText(
            estudiante["comentarios"]
        )


        self.id_edicion = indice


    # ==========================================================================
    # ELIMINAR
    # ==========================================================================

    def eliminar_estudiante(self):

        indice = self.obtener_indice()

        if indice is None:

            QMessageBox.warning(
                self,
                "Atención",
                "Selecciona un estudiante para eliminar."
            )

            return


        confirmacion = QMessageBox.question(
            self,
            "Confirmar eliminación",
            "¿Deseas eliminar este registro?",
            QMessageBox.Yes | QMessageBox.No
        )


        if confirmacion == QMessageBox.Yes:

            self.registros.pop(
                indice
            )

            self.refrescar_lista()

            self.limpiar_formulario()


    # ==========================================================================
    # LIMPIAR
    # ==========================================================================

    def limpiar_formulario(self):

        self.txt_nombre.clear()

        self.txt_ci.clear()

        self.txt_comentarios.clear()


        self.cmb_curso.setCurrentIndex(
            0
        )


        self.rad_manana.setChecked(
            True
        )


        self.chk_matematica.setChecked(
            False
        )

        self.chk_fisica.setChecked(
            False
        )

        self.chk_quimica.setChecked(
            False
        )

        self.chk_historia.setChecked(
            False
        )


        self.id_edicion = None


    # ==========================================================================
    # ABRIR FICHA
    # ==========================================================================

    def abrir_ficha(self):

        indice = self.obtener_indice()

        if indice is None:

            QMessageBox.warning(
                self,
                "Atención",
                "Selecciona un estudiante para ver su ficha."
            )

            return


        dialogo = FichaEstudianteDialog(
            self.registros[indice],
            self
        )

        dialogo.exec()


# ==============================================================================
# EJECUCIÓN
# ==============================================================================

if __name__ == "__main__":

    app = QApplication(
        sys.argv
    )

    ventana = AulaGestionApp()

    ventana.show()

    sys.exit(
        app.exec()
    )
