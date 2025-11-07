# Paso 1: Importar módulos necesarios
import tkinter as tk
from tkinter import ttk, messagebox

# Paso 2: Definir la función de conversión
def convertir():
    try:
        valor = float(entry_valor.get())
    except ValueError:
        messagebox.showerror("Error", "Ingrese un valor numérico válido.")
        return

    origen = unidad_origen.get()
    destino = unidad_destino.get()

    if origen == destino:
        resultado.set(f"{valor:.2f}° {origen} = {valor:.2f}° {destino}")
    elif origen == "Celsius" and destino == "Fahrenheit":
        convertido = (valor * 9/5) + 32
        resultado.set(f"{valor:.2f}° C = {convertido:.2f}° F")
    elif origen == "Fahrenheit" and destino == "Celsius":
        convertido = (valor - 32) * 5/9
        resultado.set(f"{valor:.2f}° F = {convertido:.2f}° C")
    else:
        resultado.set("Conversión no soportada.")

# Paso 3: Crear la ventana principal
ventana = tk.Tk()
ventana.title("Conversor de Temperatura")
ventana.geometry("400x300")

# Paso 4: Agregar título visual
tk.Label(ventana, text="Conversor de Temperatura", font=("Arial", 16, "bold")).pack(pady=10)

# Paso 5: Crear campo de entrada
tk.Label(ventana, text="Valor a convertir:").pack()
entry_valor = tk.Entry(ventana, width=10)
entry_valor.pack(pady=5)

# Paso 6: Definir unidades disponibles
unidades = ["Celsius", "Fahrenheit"]

# Paso 7: Crear menú desplegable de unidad origen
tk.Label(ventana, text="Unidad de origen:").pack()
unidad_origen = tk.StringVar(value="Celsius")
menu_origen = ttk.OptionMenu(ventana, unidad_origen, unidades[0], *unidades)
menu_origen.pack(pady=5)

# Paso 8: Crear menú desplegable de unidad destino
tk.Label(ventana, text="Unidad de destino:").pack()
unidad_destino = tk.StringVar(value="Fahrenheit")
menu_destino = ttk.OptionMenu(ventana, unidad_destino, unidades[1], *unidades)
menu_destino.pack(pady=5)

# Paso 9: Crear botón de conversión
tk.Button(ventana, text="Convertir", command=convertir).pack(pady=10)

# Paso 10: Mostrar resultado
resultado = tk.StringVar()
tk.Label(ventana, textvariable=resultado, font=("Arial", 12), fg="blue").pack(pady=5)

# Paso 11: Crear botón de salida
tk.Button(ventana, text="Salir", command=ventana.destroy, bg="gray", fg="white").pack(pady=10)

# Paso 12: Ejecutar el bucle principal
ventana.mainloop()