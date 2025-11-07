# 1. IMPORTAMOS LAS BIBLIOTECAS
import tkinter as tk
from tkinter import ttk, messagebox
import calendar
from datetime import datetime

# 2. DECLARAMOS LISTAS Y CLASES
meses_nombres = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio",
                 "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"]

class Tooltip:
    def __init__(self, widget, text):
        self.widget = widget
        self.text = text
        self.tooltip = None
        widget.bind("<Enter>", self.mostrar)
        widget.bind("<Leave>", self.ocultar)

    def mostrar(self, event=None):
        x = self.widget.winfo_rootx() + 20
        y = self.widget.winfo_rooty() + 20
        self.tooltip = tk.Toplevel(self.widget)
        self.tooltip.wm_overrideredirect(True)
        self.tooltip.wm_geometry(f"+{x}+{y}")
        label = tk.Label(self.tooltip, text=self.text, background="lightyellow",
                         relief="solid", borderwidth=1, font=("Arial", 9))
        label.pack()

    def ocultar(self, event=None):
        if self.tooltip:
            self.tooltip.destroy()
            self.tooltip = None

# 3. FUNCIONES PRINCIPALES
def mostrar_calendario():
    for widget in marco_resultado.winfo_children():
        widget.destroy()

    opcion = seleccion.get()

    if opcion == "Mes":
        mes_nombre = combo_mes.get()
        if mes_nombre not in meses_nombres:
            messagebox.showerror("Error", "Selecciona un mes válido.")
            return
        mes = meses_nombres.index(mes_nombre) + 1
        año_actual = datetime.now().year

        marco_mes = tk.Frame(marco_resultado)
        marco_mes.pack(pady=10)

        titulo_mes = tk.Label(marco_mes, text=f"{mes_nombre} {año_actual}", font=("Arial", 14, "bold"))
        titulo_mes.grid(row=0, column=0, columnspan=7, pady=5)

        dias = ["Lun", "Mar", "Mié", "Jue", "Vie", "Sáb", "Dom"]
        for i, dia in enumerate(dias):
            color = "red" if dia == "Dom" else "black"
            tk.Label(marco_mes, text=dia, font=("Arial", 10, "bold"), width=6,
                     borderwidth=1, relief="solid", fg=color).grid(row=1, column=i)

        semanas = calendar.monthcalendar(año_actual, mes)
        for r, semana in enumerate(semanas):
            for c, dia in enumerate(semana):
                texto = str(dia) if dia != 0 else ""
                color = "red" if c == 6 else "black"
                tk.Label(marco_mes, text=texto, font=("Arial", 10), width=6, height=2,
                         borderwidth=1, relief="ridge", fg=color).grid(row=r+2, column=c)

    else:
        try:
            año = int(entry_año.get())
            if año < 1:
                messagebox.showerror("Error", "Solo se permiten años positivos. Usa valores después de Cristo.")
                return
        except ValueError:
            messagebox.showerror("Error", "Año inválido. Ingresa un número positivo.")
            return

        for mes in range(1, 13):
            marco_mes = tk.Frame(marco_resultado)
            marco_mes.pack(pady=10)

            titulo_mes = tk.Label(marco_mes, text=f"{calendar.month_name[mes]} {año}", font=("Arial", 12, "bold"))
            titulo_mes.grid(row=0, column=0, columnspan=7, pady=5)

            dias = ["Lun", "Mar", "Mié", "Jue", "Vie", "Sáb", "Dom"]
            for i, dia in enumerate(dias):
                color = "red" if dia == "Dom" else "black"
                tk.Label(marco_mes, text=dia, font=("Arial", 10, "bold"), width=6,
                         borderwidth=1, relief="solid", fg=color).grid(row=1, column=i)

            semanas = calendar.monthcalendar(año, mes)
            for r, semana in enumerate(semanas):
                for c, dia in enumerate(semana):
                    texto = str(dia) if dia != 0 else ""
                    color = "red" if c == 6 else "black"
                    tk.Label(marco_mes, text=texto, font=("Arial", 10), width=6, height=2,
                             borderwidth=1, relief="ridge", fg=color).grid(row=r+2, column=c)

def actualizar_visibilidad():
    for widget in campo_dinamico.winfo_children():
        widget.pack_forget()

    if seleccion.get() == "Mes":
        label_mes.pack(side="left", padx=5)
        combo_mes.pack(side="left", padx=5)
    else:
        label_año.pack(side="left", padx=5)
        entry_año.pack(side="left", padx=5)

def ajustar_scroll(event):
    canvas.configure(scrollregion=canvas.bbox("all"))

# 4. INTERFAZ GRÁFICA
ventana = tk.Tk()
ventana.title("Calendario Interactivo")
ventana.geometry("560x800")

# Saludo con hora
hora_actual = datetime.now()
hora_str = hora_actual.strftime("%H:%M")
saludo = "Buenos días" if hora_actual.hour < 12 else "Buenas tardes" if hora_actual.hour < 18 else "Buenas noches"
etiqueta_saludo = tk.Label(ventana, text=f"{saludo}, son las {hora_str}.", font=("Arial", 12), fg="blue")
etiqueta_saludo.pack(pady=5)

# Fila para selector y campo correspondiente
fila_seleccion = tk.Frame(ventana)
fila_seleccion.pack(pady=5)

# Selector principal
seleccion = tk.StringVar(value="Mes")
opciones = ttk.Combobox(fila_seleccion, textvariable=seleccion, values=["Mes", "Año completo"], state="readonly", width=15)
opciones.pack(side="left", padx=5)
opciones.bind("<<ComboboxSelected>>", lambda e: actualizar_visibilidad())

# Campo dinámico (mes o año)
campo_dinamico = tk.Frame(fila_seleccion)
campo_dinamico.pack(side="left")

# Campo de año
label_año = tk.Label(campo_dinamico, text="Año:")
entry_año = tk.Entry(campo_dinamico, width=10)
entry_año.insert(0, str(datetime.now().year))
Tooltip(entry_año, "Indique el año que desea consultar")

# Campo de mes
label_mes = tk.Label(campo_dinamico, text="Mes:")
combo_mes = ttk.Combobox(campo_dinamico, values=meses_nombres, state="readonly", width=12)
combo_mes.set(meses_nombres[datetime.now().month - 1])
Tooltip(combo_mes, "Seleccione el mes por nombre")

# Título
titulo = tk.Label(ventana, text="Calendario en Python", font=("Arial", 16, "bold"))
titulo.pack(pady=10)

# Botones Mostrar y Salir en la misma fila
fila_botones = tk.Frame(ventana)
fila_botones.pack(pady=10)

boton_mostrar = tk.Button(fila_botones, text="Mostrar", command=mostrar_calendario, width=10)
boton_mostrar.pack(side="left", padx=10)

boton_salir = tk.Button(fila_botones, text="Salir", command=ventana.destroy, bg="red", fg="white", width=10)
boton_salir.pack(side="left", padx=10)

# Área con scroll para mostrar los meses
contenedor_scroll = tk.Frame(ventana)
contenedor_scroll.pack(expand=True, fill="both", pady=10)

canvas = tk.Canvas(contenedor_scroll, height=500)
scrollbar = tk.Scrollbar(contenedor_scroll, orient="vertical", command=canvas.yview)
canvas.configure(yscrollcommand=scrollbar.set)

scrollbar.pack(side="right", fill="y")
canvas.pack(side="left", fill="both", expand=True)

marco_resultado = tk.Frame(canvas)
canvas.create_window((0, 0), window=marco_resultado, anchor="nw")
marco_resultado.bind("<Configure>", ajustar_scroll)

# Mostrar campos iniciales
actualizar_visibilidad()

ventana.mainloop()