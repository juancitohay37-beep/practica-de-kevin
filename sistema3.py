import tkinter as tk
from tkinter import messagebox, ttk


class SistemaBiblioteca:

    def __init__(self, ventana):
        self.ventana = ventana
        self.ventana.title("Nova Biblioteca - Gestión de Libros")
        self.ventana.geometry("1150x730")
        self.ventana.configure(bg="#17121f")

        self.libros = []
        self.indice_edicion = None

        self.crear_interfaz()

    # =================================================
    # INTERFAZ
    # =================================================

    def crear_interfaz(self):

        contenedor_principal = tk.Frame(
            self.ventana,
            bg="#17121f"
        )
        contenedor_principal.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=20
        )

        # ---------------------------------
        # ENCABEZADO
        # ---------------------------------

        header_frame = tk.Frame(
            contenedor_principal,
            bg="#17121f"
        )
        header_frame.pack(
            fill="x",
            pady=(0, 15)
        )

        tk.Label(
            header_frame,
            text="📚 NOVA BIBLIOTECA",
            font=("Segoe UI", 24, "bold"),
            bg="#17121f",
            fg="#c084fc",
        ).pack(anchor="w")

        tk.Label(
            header_frame,
            text="Sistema de administración y control de libros",
            font=("Segoe UI", 11),
            bg="#17121f",
            fg="#a8a0b8",
        ).pack(anchor="w")

        # ---------------------------------
        # CONTENEDOR PRINCIPAL
        # ---------------------------------

        cuerpo = tk.Frame(
            contenedor_principal,
            bg="#17121f"
        )

        cuerpo.pack(
            fill="both",
            expand=True
        )

        cuerpo.grid_columnconfigure(
            0,
            weight=4
        )

        cuerpo.grid_columnconfigure(
            1,
            weight=6
        )

        cuerpo.grid_rowconfigure(
            0,
            weight=1
        )

        # =================================================
        # PANEL IZQUIERDO
        # =================================================

        panel_izquierdo = tk.Frame(
            cuerpo,
            bg="#241b30"
        )

        panel_izquierdo.grid(
            row=0,
            column=0,
            sticky="nsew",
            padx=(0, 12)
        )

        canvas_izq = tk.Canvas(
            panel_izquierdo,
            bg="#241b30",
            bd=0,
            highlightthickness=0
        )

        scrollbar_izq = ttk.Scrollbar(
            panel_izquierdo,
            orient="vertical",
            command=canvas_izq.yview
        )

        self.scroll_frame_izq = tk.Frame(
            canvas_izq,
            bg="#241b30"
        )

        self.scroll_frame_izq.bind(
            "<Configure>",
            lambda e: canvas_izq.configure(
                scrollregion=canvas_izq.bbox("all")
            )
        )

        window_id = canvas_izq.create_window(
            (0, 0),
            window=self.scroll_frame_izq,
            anchor="nw"
        )

        canvas_izq.bind(
            "<Configure>",
            lambda e: canvas_izq.itemconfig(
                window_id,
                width=e.width
            )
        )

        canvas_izq.configure(
            yscrollcommand=scrollbar_izq.set
        )

        def _on_mousewheel(event):
            canvas_izq.yview_scroll(
                int(-1 * (event.delta / 120)),
                "units"
            )

        canvas_izq.bind_all(
            "<MouseWheel>",
            _on_mousewheel
        )

        canvas_izq.pack(
            side="left",
            fill="both",
            expand=True,
            padx=15,
            pady=15
        )

        scrollbar_izq.pack(
            side="right",
            fill="y"
        )

        # Título

        tk.Label(
            self.scroll_frame_izq,
            text="📖 Datos del Libro",
            font=("Segoe UI", 14, "bold"),
            bg="#241b30",
            fg="#f5f3ff",
        ).pack(
            anchor="w",
            pady=(5, 15)
        )

        formulario = tk.Frame(
            self.scroll_frame_izq,
            bg="#241b30"
        )

        formulario.pack(
            fill="x",
            expand=True
        )

        # ---------------------------------
        # CAMPOS
        # ---------------------------------

        def crear_campo(
            parent,
            texto_label,
            row
        ):

            tk.Label(
                parent,
                text=texto_label,
                font=("Segoe UI", 10, "bold"),
                bg="#241b30",
                fg="#d8d0e5",
            ).grid(
                row=row,
                column=0,
                sticky="w",
                pady=6
            )

            entry = tk.Entry(
                parent,
                font=("Segoe UI", 10),
                bg="#392c48",
                fg="white",
                insertbackground="white",
                relief="flat",
            )

            entry.grid(
                row=row,
                column=1,
                sticky="ew",
                padx=(10, 0),
                pady=6,
                ipady=4
            )

            parent.grid_columnconfigure(
                1,
                weight=1
            )

            return entry

        self.titulo = crear_campo(
            formulario,
            "Título:",
            0
        )

        self.codigo = crear_campo(
            formulario,
            "Código:",
            1
        )

        self.autor = crear_campo(
            formulario,
            "Autor:",
            2
        )

        # ---------------------------------
        # CATEGORÍA
        # ---------------------------------

        tk.Label(
            formulario,
            text="Categoría:",
            font=("Segoe UI", 10, "bold"),
            bg="#241b30",
            fg="#d8d0e5",
        ).grid(
            row=3,
            column=0,
            sticky="w",
            pady=6
        )

        self.categoria = ttk.Combobox(
            formulario,
            values=[
                "Novela",
                "Ciencia",
                "Historia",
                "Tecnología",
                "Educación",
                "Fantasía",
                "Biografía"
            ],
            state="readonly",
            font=("Segoe UI", 10)
        )

        self.categoria.grid(
            row=3,
            column=1,
            sticky="ew",
            padx=(10, 0),
            pady=6
        )

        self.categoria.current(0)

        # ---------------------------------
        # ESTADO
        # ---------------------------------

        tk.Label(
            self.scroll_frame_izq,
            text="Estado del libro",
            font=("Segoe UI", 11, "bold"),
            bg="#241b30",
            fg="#f5f3ff",
        ).pack(
            anchor="w",
            pady=(15, 5)
        )

        self.estado = tk.StringVar(
            value="Disponible"
        )

        estados_frame = tk.Frame(
            self.scroll_frame_izq,
            bg="#241b30"
        )

        estados_frame.pack(
            anchor="w",
            pady=5
        )

        for est in [
            "Disponible",
            "Prestado",
            "Reservado"
        ]:

            tk.Radiobutton(
                estados_frame,
                text=est,
                variable=self.estado,
                value=est,
                bg="#241b30",
                fg="#eee8f5",
                font=("Segoe UI", 9),
                selectcolor="#392c48",
                activebackground="#241b30",
                activeforeground="white",
            ).pack(
                side="left",
                padx=(0, 12)
            )

        # ---------------------------------
        # CARACTERÍSTICAS
        # ---------------------------------

        tk.Label(
            self.scroll_frame_izq,
            text="Características",
            font=("Segoe UI", 11, "bold"),
            bg="#241b30",
            fg="#f5f3ff",
        ).pack(
            anchor="w",
            pady=(15, 5)
        )

        carac_frame = tk.Frame(
            self.scroll_frame_izq,
            bg="#241b30"
        )

        carac_frame.pack(
            anchor="w",
            pady=5
        )

        self.nuevo = tk.BooleanVar()
        self.recomendado = tk.BooleanVar()
        self.digital = tk.BooleanVar()
        self.ilustrado = tk.BooleanVar()

        checks = [
            ("✨ Nuevo", self.nuevo, 0, 0),
            ("⭐ Recomendado", self.recomendado, 0, 1),
            ("💻 Digital", self.digital, 1, 0),
            ("🎨 Ilustrado", self.ilustrado, 1, 1),
        ]

        for texto, var, r, c in checks:

            tk.Checkbutton(
                carac_frame,
                text=texto,
                variable=var,
                bg="#241b30",
                fg="#eee8f5",
                font=("Segoe UI", 9),
                selectcolor="#392c48",
                activebackground="#241b30",
                activeforeground="white",
            ).grid(
                row=r,
                column=c,
                sticky="w",
                padx=(0, 15),
                pady=3
            )

        # ---------------------------------
        # DESCRIPCIÓN
        # ---------------------------------

        tk.Label(
            self.scroll_frame_izq,
            text="Descripción:",
            font=("Segoe UI", 11, "bold"),
            bg="#241b30",
            fg="#f5f3ff",
        ).pack(
            anchor="w",
            pady=(15, 5)
        )

        self.descripcion = tk.Text(
            self.scroll_frame_izq,
            height=4,
            font=("Segoe UI", 10),
            fg="white",
            bg="#392c48",
            insertbackground="white",
            relief="flat",
        )

        self.descripcion.pack(
            fill="x",
            pady=5
        )

        # ---------------------------------
        # BOTONES
        # ---------------------------------

        botones_frame = tk.Frame(
            self.scroll_frame_izq,
            bg="#241b30"
        )

        botones_frame.pack(
            fill="x",
            pady=(20, 10)
        )

        def crear_boton(
            parent,
            texto,
            comando,
            color_bg
        ):

            return tk.Button(
                parent,
                text=texto,
                command=comando,
                bg=color_bg,
                fg="white",
                font=("Segoe UI", 9, "bold"),
                relief="flat",
                padx=8,
                pady=8,
                cursor="hand2",
                activebackground=color_bg,
                activeforeground="white"
            )

        self.btn_registrar = crear_boton(
            botones_frame,
            "💾 Guardar",
            self.registrar,
            "#a855f7"
        )

        self.btn_registrar.pack(
            side="left",
            expand=True,
            fill="x",
            padx=2
        )

        crear_boton(
            botones_frame,
            "✏ Editar",
            self.cargar_para_editar,
            "#6366f1"
        ).pack(
            side="left",
            expand=True,
            fill="x",
            padx=2
        )

        crear_boton(
            botones_frame,
            "🗑 Eliminar",
            self.eliminar,
            "#e11d48"
        ).pack(
            side="left",
            expand=True,
            fill="x",
            padx=2
        )

        crear_boton(
            botones_frame,
            "🧹 Limpiar",
            self.limpiar,
            "#64748b"
        ).pack(
            side="left",
            expand=True,
            fill="x",
            padx=2
        )

        # =================================================
        # PANEL DERECHO
        # =================================================

        panel_derecho = tk.Frame(
            cuerpo,
            bg="#241b30"
        )

        panel_derecho.grid(
            row=0,
            column=1,
            sticky="nsew"
        )

        header_der = tk.Frame(
            panel_derecho,
            bg="#241b30"
        )

        header_der.pack(
            fill="x",
            padx=20,
            pady=20
        )

        tk.Label(
            header_der,
            text="🔎 Catálogo de Biblioteca",
            font=("Segoe UI", 14, "bold"),
            bg="#241b30",
            fg="#f5f3ff",
        ).pack(
            anchor="w",
            pady=(0, 10)
        )

        self.buscar = tk.Entry(
            header_der,
            font=("Segoe UI", 11),
            fg="white",
            bg="#392c48",
            insertbackground="white",
            relief="flat",
        )

        self.buscar.pack(
            fill="x",
            ipady=5
        )

        self.buscar.insert(
            0,
            "🔍 Buscar por título o código..."
        )

        self.buscar.bind(
            "<FocusIn>",
            lambda e:
            self.buscar.delete(0, tk.END)
            if self.buscar.get() ==
            "🔍 Buscar por título o código..."
            else None,
        )

        self.buscar.bind(
            "<KeyRelease>",
            lambda evento:
            self.mostrar_libros()
        )

        # ---------------------------------
        # TABLA
        # ---------------------------------

        style = ttk.Style()

        style.theme_use("clam")

        style.configure(
            "Treeview",
            background="#392c48",
            foreground="white",
            rowheight=32,
            fieldbackground="#392c48",
            font=("Segoe UI", 10),
            borderwidth=0
        )

        style.configure(
            "Treeview.Heading",
            background="#7c3aed",
            foreground="white",
            font=("Segoe UI", 10, "bold")
        )

        style.map(
            "Treeview",
            background=[
                ("selected", "#9333ea")
            ]
        )

        tabla_frame = tk.Frame(
            panel_derecho,
            bg="#241b30"
        )

        tabla_frame.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=10
        )

        columnas = (
            "titulo",
            "codigo",
            "autor",
            "categoria",
            "estado"
        )

        self.tabla = ttk.Treeview(
            tabla_frame,
            columns=columnas,
            show="headings",
            selectmode="browse"
        )

        self.tabla.heading(
            "titulo",
            text="Título"
        )

        self.tabla.heading(
            "codigo",
            text="Código"
        )

        self.tabla.heading(
            "autor",
            text="Autor"
        )

        self.tabla.heading(
            "categoria",
            text="Categoría"
        )

        self.tabla.heading(
            "estado",
            text="Estado"
        )

        self.tabla.column(
            "titulo",
            width=160,
            anchor="w"
        )

        self.tabla.column(
            "codigo",
            width=90,
            anchor="center"
        )

        self.tabla.column(
            "autor",
            width=130,
            anchor="w"
        )

        self.tabla.column(
            "categoria",
            width=110,
            anchor="center"
        )

        self.tabla.column(
            "estado",
            width=100,
            anchor="center"
        )

        scrollbar_tabla = ttk.Scrollbar(
            tabla_frame,
            orient="vertical",
            command=self.tabla.yview
        )

        self.tabla.configure(
            yscrollcommand=scrollbar_tabla.set
        )

        self.tabla.pack(
            side="left",
            fill="both",
            expand=True
        )

        scrollbar_tabla.pack(
            side="right",
            fill="y"
        )

        self.tabla.bind(
            "<Double-1>",
            lambda evento:
            self.cargar_para_editar()
        )

        tk.Button(
            panel_derecho,
            text="📋 Ver información completa",
            command=self.ver_libro,
            bg="#8b5cf6",
            fg="white",
            font=("Segoe UI", 10, "bold"),
            relief="flat",
            pady=10,
            cursor="hand2",
            activebackground="#7c3aed",
            activeforeground="white"
        ).pack(
            fill="x",
            padx=20,
            pady=20
        )

    # =================================================
    # REGISTRAR LIBRO
    # =================================================

    def registrar(self):

        titulo = self.titulo.get().strip()
        codigo = self.codigo.get().strip()
        autor = self.autor.get().strip()

        if titulo == "":
            messagebox.showwarning(
                "Validación",
                "Escribe el título del libro."
            )
            return

        if codigo == "":
            messagebox.showwarning(
                "Validación",
                "Escribe el código del libro."
            )
            return

        if autor == "":
            messagebox.showwarning(
                "Validación",
                "Escribe el nombre del autor."
            )
            return

        # Comprobar código repetido

        for i, libro in enumerate(self.libros):

            if (
                libro["codigo"].lower() ==
                codigo.lower()
                and i != self.indice_edicion
            ):

                messagebox.showwarning(
                    "Código repetido",
                    "Ya existe un libro con ese código."
                )

                return

        # Características

        caracteristicas = []

        if self.nuevo.get():
            caracteristicas.append(
                "Nuevo"
            )

        if self.recomendado.get():
            caracteristicas.append(
                "Recomendado"
            )

        if self.digital.get():
            caracteristicas.append(
                "Digital"
            )

        if self.ilustrado.get():
            caracteristicas.append(
                "Ilustrado"
            )

        libro = {

            "titulo": titulo,

            "codigo": codigo,

            "autor": autor,

            "categoria":
                self.categoria.get(),

            "estado":
                self.estado.get(),

            "caracteristicas":
                ", ".join(caracteristicas),

            "descripcion":
                self.descripcion.get(
                    "1.0",
                    tk.END
                ).strip()
        }

        if self.indice_edicion is not None:

            self.libros[
                self.indice_edicion
            ] = libro

            messagebox.showinfo(
                "Actualizado",
                "Libro actualizado correctamente."
            )

        else:

            self.libros.append(
                libro
            )

            messagebox.showinfo(
                "Registrado",
                "Libro registrado correctamente."
            )

        self.mostrar_libros()

        self.limpiar()

    # =================================================
    # MOSTRAR LIBROS
    # =================================================

    def mostrar_libros(self):

        for elemento in self.tabla.get_children():

            self.tabla.delete(
                elemento
            )

        texto = self.buscar.get().lower()

        if (
            "buscar por título" in texto
            or "buscar por titulo" in texto
        ):

            texto = ""

        for indice, libro in enumerate(
            self.libros
        ):

            if (
                texto in
                libro["titulo"].lower()
                or texto in
                libro["codigo"].lower()
            ):

                self.tabla.insert(

                    "",

                    tk.END,

                    iid=str(indice),

                    values=(

                        libro["titulo"],

                        libro["codigo"],

                        libro["autor"],

                        libro["categoria"],

                        libro["estado"]
                    )
                )

    # =================================================
    # OBTENER SELECCIÓN
    # =================================================

    def obtener_indice(self):

        seleccion = self.tabla.selection()

        if not seleccion:
            return None

        return int(
            seleccion[0]
        )

    # =================================================
    # EDITAR
    # =================================================

    def cargar_para_editar(self):

        indice = self.obtener_indice()

        if indice is None:

            messagebox.showinfo(
                "Aviso",
                "Selecciona un libro de la tabla para editar."
            )

            return

        libro = self.libros[indice]

        self.titulo.delete(
            0,
            tk.END
        )

        self.titulo.insert(
            0,
            libro["titulo"]
        )

        self.codigo.delete(
            0,
            tk.END
        )

        self.codigo.insert(
            0,
            libro["codigo"]
        )

        self.autor.delete(
            0,
            tk.END
        )

        self.autor.insert(
            0,
            libro["autor"]
        )

        self.categoria.set(
            libro["categoria"]
        )

        self.estado.set(
            libro["estado"]
        )

        self.nuevo.set(
            "Nuevo" in
            libro["caracteristicas"]
        )

        self.recomendado.set(
            "Recomendado" in
            libro["caracteristicas"]
        )

        self.digital.set(
            "Digital" in
            libro["caracteristicas"]
        )

        self.ilustrado.set(
            "Ilustrado" in
            libro["caracteristicas"]
        )

        self.descripcion.delete(
            "1.0",
            tk.END
        )

        self.descripcion.insert(
            "1.0",
            libro["descripcion"]
        )

        self.indice_edicion = indice

        self.btn_registrar.config(
            text="💾 Actualizar",
            bg="#6366f1"
        )

    # =================================================
    # ELIMINAR
    # =================================================

    def eliminar(self):

        indice = self.obtener_indice()

        if indice is None:

            messagebox.showinfo(
                "Aviso",
                "Selecciona un libro."
            )

            return

        respuesta = messagebox.askyesno(
            "Confirmar eliminación",
            "¿Seguro que deseas eliminar este libro?"
        )

        if respuesta:

            self.libros.pop(
                indice
            )

            self.mostrar_libros()

            self.limpiar()

    # =================================================
    # VER INFORMACIÓN
    # =================================================

    def ver_libro(self):

        indice = self.obtener_indice()

        if indice is None:

            messagebox.showinfo(
                "Aviso",
                "Selecciona un libro."
            )

            return

        libro = self.libros[indice]

        informacion = (

            f"LIBRO\n\n"

            f"Título: "
            f"{libro['titulo']}\n"

            f"Código: "
            f"{libro['codigo']}\n"

            f"Autor: "
            f"{libro['autor']}\n"

            f"Categoría: "
            f"{libro['categoria']}\n"

            f"Estado: "
            f"{libro['estado']}\n"

            f"Características: "
            f"{libro['caracteristicas'] or 'Ninguna'}\n\n"

            f"Descripción:\n"
            f"{libro['descripcion'] or 'Sin descripción'}"
        )

        messagebox.showinfo(
            "Información del libro",
            informacion
        )

    # =================================================
    # LIMPIAR
    # =================================================

    def limpiar(self):

        self.titulo.delete(
            0,
            tk.END
        )

        self.codigo.delete(
            0,
            tk.END
        )

        self.autor.delete(
            0,
            tk.END
        )

        self.categoria.current(
            0
        )

        self.estado.set(
            "Disponible"
        )

        self.nuevo.set(
            False
        )

        self.recomendado.set(
            False
        )

        self.digital.set(
            False
        )

        self.ilustrado.set(
            False
        )

        self.descripcion.delete(
            "1.0",
            tk.END
        )

        self.indice_edicion = None

        self.btn_registrar.config(
            text="💾 Guardar",
            bg="#a855f7"
        )


# =================================================
# EJECUCIÓN
# =================================================

if __name__ == "__main__":

    ventana = tk.Tk()

    app = SistemaBiblioteca(
        ventana
    )

    ventana.mainloop()
