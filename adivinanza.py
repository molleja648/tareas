# Paso 1: Importar librerías necesarias
import tkinter as tk
from tkinter import messagebox
import random

# Paso 2: Definir lista de colores y equivalencias para Tkinter
colores = ["rojo", "verde", "azul", "amarillo", "naranja", "violeta", "rosado", "celeste", "gris", "negro"]

colores_tk = {
    "rojo": "red",
    "verde": "green",
    "azul": "blue",
    "amarillo": "yellow",
    "naranja": "orange",
    "violeta": "purple",
    "rosado": "pink",
    "celeste": "light sky blue",
    "gris": "gray",
    "negro": "black"
}

# Paso 3: Variables de estado global
girando = False
color_actual = None
color_final = None

# Paso 4: Función para iniciar el giro
def girar():
    global girando, color_actual, color_final
    if girando:
        return

    fuerza = escala_fuerza.get()
    if fuerza < 1:
        messagebox.showerror("Error", "Selecciona una fuerza mayor a 0.")
        return

    seleccion = color_seleccionado.get()
    if seleccion not in colores:
        messagebox.showerror("Error", "Selecciona un color válido.")
        return

    girando = True
    color_actual = None
    color_final = None

    ciclos = fuerza * 2
    tick_giro(ciclos, 30, seleccion)  # arranca rápido (30 ms)

# Paso 5: Función que simula el giro y freno
def tick_giro(ciclos_restantes, intervalo_ms, seleccion):
    global girando, color_actual, color_final

    if ciclos_restantes > 0:
        # Elegir y mostrar color
        color_actual = random.choice(colores)
        cuadro_color.config(bg=colores_tk[color_actual])
        etiqueta_color.set(f"Color actual: {color_actual.upper()}")

        # Aumentar intervalo en los últimos 20 ciclos para simular freno
        if ciclos_restantes < 20:
            intervalo_ms += 20

        ventana.after(intervalo_ms, lambda: tick_giro(ciclos_restantes - 1, intervalo_ms, seleccion))
    else:
        girando = False
        color_final = color_actual
        etiqueta_color.set(f"Color final: {color_final.upper()}")
        verificar_resultado(seleccion)

# Paso 6: Función para verificar si el usuario acertó
def verificar_resultado(seleccion):
    if color_final is None:
        resultado.set("No se obtuvo un color final. Intenta de nuevo.")
        return

    if seleccion == color_final:
        resultado.set("¡Éxito! Felicitaciones, acertaste el color.")
    else:
        resultado.set(f"😕 No coincidió. Cayó en {color_final.upper()}. Intenta otra vez.")

# Paso 7: Crear ventana principal
ventana = tk.Tk()
ventana.title("Rueda de la Fortuna")
ventana.geometry("460x480")

# Paso 8: Título y lista de colores
tk.Label(ventana, text="Rueda de la Fortuna", font=("Arial", 18, "bold")).pack(pady=8)
tk.Label(ventana, text="Colores disponibles: " + ", ".join(colores), wraplength=420).pack(pady=4)

# Paso 9: Menú desplegable para elegir color
tk.Label(ventana, text="Tu color elegido:").pack()
color_seleccionado = tk.StringVar(value=colores[0])
tk.OptionMenu(ventana, color_seleccionado, *colores).pack(pady=6)

# Paso 10: Slider para elegir fuerza
tk.Label(ventana, text="Fuerza (1 a 100):").pack()
escala_fuerza = tk.Scale(ventana, from_=1, to=100, orient="horizontal", length=300)
escala_fuerza.set(60)
escala_fuerza.pack(pady=6)

# Paso 11: Cuadro que muestra el color
cuadro_color = tk.Label(ventana, width=24, height=6, bg="white", relief="solid")
cuadro_color.pack(pady=14)

# Paso 12: Etiqueta para mostrar color actual
etiqueta_color = tk.StringVar(value="Color actual: —")
tk.Label(ventana, textvariable=etiqueta_color, font=("Arial", 12)).pack(pady=4)

# Paso 13: Botón para girar la rueda
tk.Button(ventana, text="Girar rueda", command=girar).pack(pady=10)

# Paso 14: Etiqueta para mostrar resultado
resultado = tk.StringVar(value="")
tk.Label(ventana, textvariable=resultado, font=("Arial", 12), fg="blue", wraplength=420).pack(pady=6)

# Paso 15: Botón para salir
tk.Button(ventana, text="Salir", command=ventana.destroy, bg="gray", fg="white").pack(pady=10)

# Paso 16: Ejecutar bucle principal
ventana.mainloop()