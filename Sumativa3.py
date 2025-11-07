import tkinter as tk
import subprocess
import os

# ============================================
# Ruta base: carpeta donde está este archivo
# ============================================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# ============================================
# Funciones para abrir cada ejercicio
# ============================================
def abrir_calendario():
    subprocess.run(["python", os.path.join(BASE_DIR, "calendario.py")])

def abrir_qr():
    subprocess.run(["python", os.path.join(BASE_DIR, "generadorQR.py")])

def abrir_agenda():
    subprocess.run(["python", os.path.join(BASE_DIR, "agenda.py")])

def abrir_conversor():
    subprocess.run(["python", os.path.join(BASE_DIR, "conversion.py")])

def abrir_rueda():
    subprocess.run(["python", os.path.join(BASE_DIR, "adivinanza.py")])

def abrir_tareas():
    subprocess.run(["python", os.path.join(BASE_DIR, "tareas.py")])

# ============================================
# Ventana principal del menú
# ============================================
ventana = tk.Tk()
ventana.title("ACTIVIDAD SUMATIVA 3. Unidad IV: Introducción a Python")
ventana.geometry("500x600")

# Título arriba
tk.Label(
    ventana,
    text="ACTIVIDAD SUMATIVA 3\nUnidad IV: Introducción a Python",
    font=("Arial", 16, "bold"),
    fg="blue"
).pack(pady=20)

# Botones del menú
tk.Button(ventana, text="Ejercicio 01: Calendario", width=40, command=abrir_calendario).pack(pady=5)
tk.Button(ventana, text="Ejercicio 02: Generador de Códigos QR", width=40, command=abrir_qr).pack(pady=5)
tk.Button(ventana, text="Ejercicio 03: Agenda de Contactos", width=40, command=abrir_agenda).pack(pady=5)
tk.Button(ventana, text="Ejercicio 04: Conversor de Temperatura", width=40, command=abrir_conversor).pack(pady=5)
tk.Button(ventana, text="Ejercicio 05: Adivinanza (Rueda de la Fortuna)", width=40, command=abrir_rueda).pack(pady=5)
tk.Button(ventana, text="Ejercicio 06: Lista de Tareas", width=40, command=abrir_tareas).pack(pady=5)

# Autor al final
tk.Label(
    ventana,
    text="Autor: Jose Gregorio Molleja",
    font=("Arial", 12, "italic"),
    fg="gray"
).pack(side="bottom", pady=20)

ventana.mainloop()