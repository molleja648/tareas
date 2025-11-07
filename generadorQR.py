# Paso previo: instalar la librería
# pip install qrcode[pil] pillow

import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import qrcode

# Función para generar el QR
def generar_qr():
    codigo = entry_codigo.get().strip()
    descripcion = entry_descripcion.get().strip()
    color = entry_color.get().strip()
    elaborado = entry_elaborado.get().strip()
    ubicacion = entry_ubicacion.get().strip()

    # Validaciones básicas
    if not codigo or not descripcion or not color or not elaborado or not ubicacion:
        messagebox.showerror("Error", "Debes llenar todos los campos.")
        return

    try:
        tamaño = int(entry_tamaño.get())
        if tamaño < 1 or tamaño > 20:
            raise ValueError
    except ValueError:
        messagebox.showerror("Error", "El tamaño debe ser un número entre 1 y 20.")
        return

    # Texto que irá dentro del QR
    texto_qr = (
        f"Código del Producto: {codigo}\n"
        f"Descripción: {descripcion}\n"
        f"Color: {color}\n"
        f"Elaborado por: {elaborado}\n"
        f"Ubicación: {ubicacion}"
    )

    # Generar QR como imagen PIL estándar
    qr = qrcode.QRCode(
        version=1,
        box_size=tamaño,
        border=4
    )
    qr.add_data(texto_qr)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white").convert("RGB")

    # Redimensionar para mostrar en la interfaz
    img = img.resize((250, 250), Image.Resampling.LANCZOS)
    img_tk = ImageTk.PhotoImage(img)

    # Mostrar en la etiqueta
    etiqueta_imagen.config(image=img_tk)
    etiqueta_imagen.image = img_tk

    messagebox.showinfo("Éxito", "QR generado y mostrado en pantalla")

# Ventana principal
ventana = tk.Tk()
ventana.title("Generador de QR de Producto")
ventana.geometry("420x650")

# Título
titulo = tk.Label(ventana, text="Generador de Código QR de Producto", font=("Arial", 14, "bold"))
titulo.pack(pady=10)

# Campos de entrada
tk.Label(ventana, text="Código del Producto:").pack()
entry_codigo = tk.Entry(ventana, width=40)
entry_codigo.pack(pady=5)

tk.Label(ventana, text="Descripción:").pack()
entry_descripcion = tk.Entry(ventana, width=40)
entry_descripcion.pack(pady=5)

tk.Label(ventana, text="Color:").pack()
entry_color = tk.Entry(ventana, width=40)
entry_color.pack(pady=5)

tk.Label(ventana, text="Elaborado por:").pack()
entry_elaborado = tk.Entry(ventana, width=40)
entry_elaborado.pack(pady=5)

tk.Label(ventana, text="Ubicación:").pack()
entry_ubicacion = tk.Entry(ventana, width=40)
entry_ubicacion.pack(pady=5)

# Campo de tamaño
tk.Label(ventana, text="Tamaño del QR (1 a 20):").pack()
entry_tamaño = tk.Entry(ventana, width=10)
entry_tamaño.insert(0, "10")
entry_tamaño.pack(pady=5)

# Botón para generar
boton_generar = tk.Button(ventana, text="Generar QR", command=generar_qr)
boton_generar.pack(pady=10)

# Área para mostrar el QR
etiqueta_imagen = tk.Label(ventana)
etiqueta_imagen.pack(pady=10)

# Botón para salir
boton_salir = tk.Button(ventana, text="Salir", command=ventana.destroy, bg="red", fg="white")
boton_salir.pack(pady=10)

ventana.mainloop()