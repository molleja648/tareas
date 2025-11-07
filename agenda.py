# Paso 1: Cargar paquetes
import tkinter as tk
from tkinter import messagebox
import mysql.connector

# Paso 2: Conexión a la base de datos
def conectar():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="agenda"
    )

# Paso 3: Variables globales
contacto_actual_id = None

# Paso 4: Funciones CRUD
def agregar_contacto():
    global contacto_actual_id
    nombre = entry_nombre.get().strip()
    telefono = entry_telefono.get().strip()

    if not nombre or not telefono:
        messagebox.showerror("Error", "Debe ingresar nombre y teléfono.")
        return
    if not telefono.isdigit():
        messagebox.showerror("Error", "El teléfono debe contener solo números.")
        return

    con = conectar()
    cursor = con.cursor()
    cursor.execute("SELECT id FROM contactos WHERE nombre=%s OR telefono=%s", (nombre, telefono))
    if cursor.fetchone():
        messagebox.showerror("Error", "Ya existe un contacto con ese nombre o teléfono.")
        con.close()
        return

    cursor.execute("INSERT INTO contactos (nombre, telefono) VALUES (%s, %s)", (nombre, telefono))
    con.commit()
    con.close()

    messagebox.showinfo("Contacto agregado", f"{nombre} ha sido guardado.")
    entry_nombre.delete(0, tk.END)
    entry_telefono.delete(0, tk.END)
    mostrar_todos()

def buscar_contacto():
    global contacto_actual_id
    nombre = entry_buscar.get().strip()
    if not nombre:
        messagebox.showwarning("Atención", "Ingrese un nombre para buscar.")
        return

    con = conectar()
    cursor = con.cursor()
    cursor.execute("SELECT id, nombre, telefono FROM contactos WHERE nombre=%s", (nombre,))
    fila = cursor.fetchone()
    con.close()

    if fila:
        contacto_actual_id = fila[0]
        entry_nombre.delete(0, tk.END)
        entry_nombre.insert(0, fila[1])
        entry_telefono.delete(0, tk.END)
        entry_telefono.insert(0, fila[2])
        resultado.set(f"{fila[1]}: {fila[2]} (ID {fila[0]})")
        seleccionar_en_lista(contacto_actual_id)
    else:
        contacto_actual_id = None
        resultado.set("Contacto no encontrado.")

def mostrar_todos():
    lista.delete(0, tk.END)
    con = conectar()
    cursor = con.cursor()
    cursor.execute("SELECT id, nombre, telefono FROM contactos ORDER BY nombre ASC")
    for id, nombre, telefono in cursor.fetchall():
        lista.insert(tk.END, f"{id} - {nombre}: {telefono}")
    con.close()

def eliminar_contacto():
    global contacto_actual_id
    id_a_borrar = contacto_actual_id

    if id_a_borrar is None:
        seleccionado = lista.curselection()
        if not seleccionado:
            messagebox.showwarning("Atención", "Seleccione un contacto de la lista o búsquelo primero.")
            return
        item = lista.get(seleccionado[0])
        id_a_borrar = item.split(" - ")[0]

    confirmar = messagebox.askyesno("Confirmar eliminación", "¿Seguro que deseas eliminar este contacto?")
    if not confirmar:
        return

    con = conectar()
    cursor = con.cursor()
    cursor.execute("DELETE FROM contactos WHERE id=%s", (id_a_borrar,))
    con.commit()
    con.close()

    entry_nombre.delete(0, tk.END)
    entry_telefono.delete(0, tk.END)
    resultado.set("")
    contacto_actual_id = None

    messagebox.showinfo("Éxito", "Contacto eliminado 🗑️")
    mostrar_todos()

def actualizar_contacto():
    global contacto_actual_id
    if contacto_actual_id is None:
        seleccionado = lista.curselection()
        if not seleccionado:
            messagebox.showwarning("Atención", "Busque o seleccione un contacto para actualizar.")
            return
        item = lista.get(seleccionado[0])
        contacto_actual_id = item.split(" - ")[0]

    nuevo_nombre = entry_nombre.get().strip()
    nuevo_telefono = entry_telefono.get().strip()

    if not nuevo_nombre or not nuevo_telefono:
        messagebox.showwarning("Atención", "Ingrese nombre y teléfono para actualizar.")
        return
    if not nuevo_telefono.isdigit():
        messagebox.showerror("Error", "El teléfono debe contener solo números.")
        return

    con = conectar()
    cursor = con.cursor()
    cursor.execute(
        "SELECT id FROM contactos WHERE (nombre=%s OR telefono=%s) AND id<>%s",
        (nuevo_nombre, nuevo_telefono, contacto_actual_id)
    )
    if cursor.fetchone():
        messagebox.showerror("Error", "Ya existe otro contacto con ese nombre o teléfono.")
        con.close()
        return

    cursor.execute(
        "UPDATE contactos SET nombre=%s, telefono=%s WHERE id=%s",
        (nuevo_nombre, nuevo_telefono, contacto_actual_id)
    )
    con.commit()
    con.close()

    messagebox.showinfo("Éxito", "Contacto actualizado ✨")
    mostrar_todos()
    resultado.set(f"{nuevo_nombre}: {nuevo_telefono} (ID {contacto_actual_id})")
    seleccionar_en_lista(contacto_actual_id)

def seleccionar_en_lista(id_objetivo):
    for i in range(lista.size()):
        item = lista.get(i)
        id_item = item.split(" - ")[0]
        if str(id_objetivo) == str(id_item):
            lista.selection_clear(0, tk.END)
            lista.selection_set(i)
            lista.see(i)
            break

def confirmar_salida():
    if messagebox.askyesno("Confirmar salida", "¿Seguro que deseas salir de la agenda?"):
        ventana.destroy()

# Paso 5: Interfaz gráfica
ventana = tk.Tk()
ventana.title("Programa: Agenda de Contactos")
ventana.geometry("540x750")

titulo = tk.Label(ventana, text="Agenda de Contactos", font=("Arial", 18, "bold"))
titulo.pack(pady=10)

frame_agregar = tk.LabelFrame(ventana, text="Agregar / Actualizar contacto", font=("Arial", 12, "bold"))
frame_agregar.pack(pady=10, fill="x", padx=10)

tk.Label(frame_agregar, text="Nombre:").pack()
entry_nombre = tk.Entry(frame_agregar)
entry_nombre.pack()

tk.Label(frame_agregar, text="Teléfono:").pack()
entry_telefono = tk.Entry(frame_agregar)
entry_telefono.pack()

tk.Button(frame_agregar, text="Agregar", command=agregar_contacto,
          bg="yellow", fg="black", font=("Arial", 11, "bold")).pack(pady=5, fill="x")

tk.Button(frame_agregar, text="Actualizar", command=actualizar_contacto,
          bg="blue", fg="white", font=("Arial", 11, "bold")).pack(pady=5, fill="x")

frame_buscar = tk.LabelFrame(ventana, text="Buscar contacto", font=("Arial", 12, "bold"))
frame_buscar.pack(pady=10, fill="x", padx=10)

tk.Label(frame_buscar, text="Nombre:").pack()
entry_buscar = tk.Entry(frame_buscar)
entry_buscar.pack()

resultado = tk.StringVar()
tk.Label(frame_buscar, textvariable=resultado, fg="blue").pack(pady=5)

tk.Button(frame_buscar, text="Buscar libremente", command=buscar_contacto,
          bg="yellow", fg="black", font=("Arial", 11, "bold")).pack(pady=5, fill="x")

frame_lista = tk.LabelFrame(ventana, text="Todos los contactos", font=("Arial", 12, "bold"))
frame_lista.pack(pady=10, fill="both", expand=True, padx=10)

scrollbar = tk.Scrollbar(frame_lista)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

lista = tk.Listbox(frame_lista, yscrollcommand=scrollbar.set, font=("Consolas", 11))
lista.pack(side=tk.LEFT, fill="both", expand=True)

scrollbar.config(command=lista.yview)

# ✅ Botón Salir en lugar de "Mostrar todos"
tk.Button(
    ventana,
    text="Salir",
    command=confirmar_salida,
    bg="yellow", fg="black", font=("Arial", 12, "bold")
).pack(pady=15, fill="x")

tk.Button(ventana, text="Eliminar seleccionado / encontrado", command=eliminar_contacto,
          bg="red", fg="white", font=("Arial", 11, "bold")).pack(pady=5, fill="x")

# Paso 6: Ejecutar aplicación
mostrar_todos()
ventana.mainloop()