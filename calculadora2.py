import ast
import operator
import tkinter as tk
from tkinter import messagebox, ttk


# ============================================================
# MOTOR DE OPERACIONES
# ============================================================

class OperadorMatematico:

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

        # Completar paréntesis abiertos
        abiertos = expresion.count("(") - expresion.count(")")

        if abiertos > 0:
            expresion += ")" * abiertos

        try:
            arbol = ast.parse(
                expresion,
                mode="eval"
            )

            return cls.evaluar(arbol.body)

        except ZeroDivisionError:
            raise

        except Exception as error:
            raise ValueError(
                "Operación no válida"
            ) from error

    @classmethod
    def evaluar(cls, nodo):

        if isinstance(nodo, ast.Constant):

            if isinstance(
                nodo.value,
                (int, float)
            ):
                return nodo.value

            raise ValueError("Número inválido")

        if isinstance(nodo, ast.BinOp):

            izquierda = cls.evaluar(
                nodo.left
            )

            derecha = cls.evaluar(
                nodo.right
            )

            funcion = cls.OPERADORES.get(
                type(nodo.op)
            )

            if funcion is None:
                raise ValueError(
                    "Operador no permitido"
                )

            return funcion(
                izquierda,
                derecha
            )

        if isinstance(nodo, ast.UnaryOp):

            valor = cls.evaluar(
                nodo.operand
            )

            funcion = cls.OPERADORES.get(
                type(nodo.op)
            )

            if funcion is None:
                raise ValueError(
                    "Operador no permitido"
                )

            return funcion(valor)

        raise ValueError(
            "Expresión no permitida"
        )


# ============================================================
# APLICACIÓN PRINCIPAL
# ============================================================

class CalculadoraDigital:

    LIMITE_HISTORIAL = 6

    def __init__(self, ventana):

        self.ventana = ventana

        self.operacion_actual = ""
        self.resultado_anterior = False

        self.configurar_ventana()
        self.crear_interfaz()
        self.configurar_teclas()

    # ========================================================
    # VENTANA
    # ========================================================

    def configurar_ventana(self):

        self.ventana.title(
            "NovaCalc - Calculadora"
        )

        self.ventana.geometry(
            "390x590"
        )

        self.ventana.resizable(
            False,
            False
        )

        self.ventana.configure(
            bg="#101827"
        )

    # ========================================================
    # INTERFAZ
    # ========================================================

    def crear_interfaz(self):

        contenedor = tk.Frame(
            self.ventana,
            bg="#101827"
        )

        contenedor.pack(
            fill="both",
            expand=True,
            padx=18,
            pady=18
        )

        # ----------------------------------------------------
        # ENCABEZADO
        # ----------------------------------------------------

        tk.Label(
            contenedor,
            text="NOVA CALC",
            font=("Segoe UI", 22, "bold"),
            bg="#101827",
            fg="#22d3ee"
        ).pack(
            anchor="w"
        )

        tk.Label(
            contenedor,
            text="Calculadora matemática",
            font=("Segoe UI", 10),
            bg="#101827",
            fg="#94a3b8"
        ).pack(
            anchor="w",
            pady=(0, 12)
        )

        # ----------------------------------------------------
        # PANTALLA
        # ----------------------------------------------------

        pantalla_frame = tk.Frame(
            contenedor,
            bg="#020617"
        )

        pantalla_frame.pack(
            fill="x",
            pady=(0, 14)
        )

        self.pantalla = tk.StringVar(
            value="0"
        )

        self.display = tk.Entry(
            pantalla_frame,
            textvariable=self.pantalla,
            font=("Consolas", 25, "bold"),
            justify="right",
            bd=0,
            relief="flat",
            bg="#020617",
            fg="#67e8f9",
            insertbackground="#67e8f9"
        )

        self.display.pack(
            fill="x",
            ipady=14,
            padx=12,
            pady=8
        )

        # ----------------------------------------------------
        # TECLADO
        # ----------------------------------------------------

        self.crear_teclado(
            contenedor
        )

        # ----------------------------------------------------
        # OPCIONES
        # ----------------------------------------------------

        opciones = tk.Frame(
            contenedor,
            bg="#101827"
        )

        opciones.pack(
            fill="x",
            pady=(12, 8)
        )

        btn_borrar = tk.Button(
            opciones,
            text="⌫ Borrar",
            command=self.borrar_ultimo,
            bg="#475569",
            fg="white",
            activebackground="#64748b",
            activeforeground="white",
            font=("Segoe UI", 9, "bold"),
            relief="flat",
            bd=0,
            cursor="hand2"
        )

        btn_borrar.pack(
            side="left",
            expand=True,
            fill="x",
            padx=(0, 4),
            ipady=5
        )

        btn_historial = tk.Button(
            opciones,
            text="🗑 Vaciar historial",
            command=self.vaciar_historial,
            bg="#7c3aed",
            fg="white",
            activebackground="#8b5cf6",
            activeforeground="white",
            font=("Segoe UI", 9, "bold"),
            relief="flat",
            bd=0,
            cursor="hand2"
        )

        btn_historial.pack(
            side="left",
            expand=True,
            fill="x",
            padx=(4, 0),
            ipady=5
        )

        # ----------------------------------------------------
        # HISTORIAL
        # ----------------------------------------------------

        tk.Label(
            contenedor,
            text="Operaciones recientes",
            font=("Segoe UI", 10, "bold"),
            bg="#101827",
            fg="#cbd5e1"
        ).pack(
            anchor="w",
            pady=(8, 5)
        )

        self.lista_historial = tk.Listbox(
            contenedor,
            height=5,
            font=("Consolas", 9),
            bg="#020617",
            fg="#cbd5e1",
            selectbackground="#155e75",
            selectforeground="white",
            bd=0,
            highlightthickness=1,
            highlightbackground="#334155"
        )

        self.lista_historial.pack(
            fill="x"
        )

    # ========================================================
    # TECLADO DE LA CALCULADORA
    # ========================================================

    def crear_teclado(self, padre):

        teclado = tk.Frame(
            padre,
            bg="#101827"
        )

        teclado.pack(
            fill="both",
            expand=True
        )

        botones = [
            ["AC", "(", ")", "÷"],
            ["7", "8", "9", "×"],
            ["4", "5", "6", "-"],
            ["1", "2", "3", "+"],
            ["0", ".", "=", ""],
        ]

        for fila in range(5):

            teclado.rowconfigure(
                fila,
                weight=1
            )

        for columna in range(4):

            teclado.columnconfigure(
                columna,
                weight=1
            )

        for fila, elementos in enumerate(botones):

            for columna, texto in enumerate(elementos):

                if texto == "":
                    continue

                color = self.color_boton(
                    texto
                )

                boton = tk.Button(
                    teclado,
                    text=texto,
                    font=("Segoe UI", 13, "bold"),
                    bg=color,
                    fg="white",
                    activebackground="#64748b",
                    activeforeground="white",
                    relief="flat",
                    bd=0,
                    cursor="hand2",
                    command=lambda valor=texto:
                    self.presionar(valor)
                )

                if texto == "=":

                    boton.grid(
                        row=fila,
                        column=columna,
                        columnspan=2,
                        sticky="nsew",
                        padx=3,
                        pady=3
                    )

                else:

                    boton.grid(
                        row=fila,
                        column=columna,
                        sticky="nsew",
                        padx=3,
                        pady=3
                    )

    # ========================================================
    # COLORES DE LOS BOTONES
    # ========================================================

    def color_boton(self, texto):

        if texto in ["+", "-", "×", "÷"]:
            return "#f97316"

        if texto == "=":
            return "#0891b2"

        if texto in ["AC", "(", ")"]:
            return "#db2777"

        return "#334155"

    # ========================================================
    # TECLADO FÍSICO
    # ========================================================

    def configurar_teclas(self):

        self.ventana.bind(
            "<Key>",
            self.tecla_fisica
        )

    def tecla_fisica(self, evento):

        if evento.keysym in [
            "Return",
            "KP_Enter"
        ]:

            self.presionar("=")
            return

        if evento.keysym == "Escape":

            self.presionar("AC")
            return

        if evento.keysym == "BackSpace":

            self.borrar_ultimo()
            return

        tecla = evento.char

        if tecla in "0123456789+-./*()":

            conversion = {
                "*": "×",
                "/": "÷"
            }

            tecla = conversion.get(
                tecla,
                tecla
            )

            self.presionar(tecla)

    # ========================================================
    # PROCESAR BOTÓN
    # ========================================================

    def presionar(self, valor):

        if valor == "AC":

            self.limpiar()
            return

        if valor == "=":

            self.calcular()
            return

        if (
            self.resultado_anterior
            and valor.isdigit()
        ):

            self.operacion_actual = ""

        self.resultado_anterior = False

        self.operacion_actual += valor

        self.pantalla.set(
            self.operacion_actual
        )

    # ========================================================
    # BORRAR ÚLTIMO
    # ========================================================

    def borrar_ultimo(self):

        if not self.operacion_actual:
            return

        self.operacion_actual = (
            self.operacion_actual[:-1]
        )

        if self.operacion_actual:

            self.pantalla.set(
                self.operacion_actual
            )

        else:

            self.pantalla.set(
                "0"
            )

    # ========================================================
    # LIMPIAR
    # ========================================================

    def limpiar(self):

        self.operacion_actual = ""
        self.resultado_anterior = False

        self.pantalla.set(
            "0"
        )

    # ========================================================
    # REALIZAR CÁLCULO
    # ========================================================

    def calcular(self):

        if not self.operacion_actual:
            return

        expresion = (
            self.operacion_actual
            .replace("÷", "/")
            .replace("×", "*")
        )

        try:

            resultado = OperadorMatematico.resolver(
                expresion
            )

            if (
                isinstance(resultado, float)
                and resultado.is_integer()
            ):

                resultado = int(
                    resultado
                )

            resultado = str(
                resultado
            )

            self.agregar_historial(
                self.operacion_actual,
                resultado
            )

            self.pantalla.set(
                resultado
            )

            self.operacion_actual = (
                resultado
            )

            self.resultado_anterior = True

        except ZeroDivisionError:

            messagebox.showerror(
                "Error matemático",
                "No puedes dividir un número entre cero."
            )

            self.limpiar()

        except Exception:

            messagebox.showwarning(
                "Operación inválida",
                "Revisa la expresión ingresada."
            )

            self.limpiar()

    # ========================================================
    # HISTORIAL
    # ========================================================

    def agregar_historial(
        self,
        expresion,
        resultado
    ):

        registro = (
            f"{expresion} = {resultado}"
        )

        self.lista_historial.insert(
            tk.END,
            registro
        )

        if (
            self.lista_historial.size()
            > self.LIMITE_HISTORIAL
        ):

            self.lista_historial.delete(
                0
            )

        self.lista_historial.see(
            tk.END
        )

    # ========================================================
    # VACIAR HISTORIAL
    # ========================================================

    def vaciar_historial(self):

        if self.lista_historial.size() == 0:
            return

        confirmar = messagebox.askyesno(
            "Limpiar historial",
            "¿Deseas borrar todas las operaciones?"
        )

        if confirmar:

            self.lista_historial.delete(
                0,
                tk.END
            )


# ============================================================
# INICIO DEL PROGRAMA
# ============================================================

if __name__ == "__main__":

    ventana = tk.Tk()

    app = CalculadoraDigital(
        ventana
    )

    ventana.mainloop()