# ============================================
# Paso 1. Instalar, importar y cargar paquetes
# ============================================
# - Instalar con: pip install mysql-connector-python
# - tkinter: interfaz gráfica
# - ttk: tabla tipo Treeview
# - messagebox: cuadros de diálogo
# - mysql.connector: conexión a MySQL
import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector

# ============================================
# Paso 2. Conexión a la base de datos
# ============================================
# Para qué sirve: centraliza los parámetros de conexión a MySQL
# Nota: asegúrate de haber creado la base 'tareas_db' y la tabla 'tareas'
def conectar():
    return mysql.connector.connect(
        host="localhost",
        user="root",       # cambia si tu usuario es distinto
        password="",       # pon tu contraseña si configuraste una
        database="tareas_db"
    )

# ============================================
# Paso 3. Clase auxiliar para Tooltips
# ============================================
# Para qué sirve: mostrar un mensaje flotante cuando el usuario pasa el mouse sobre un botón
class ToolTip:
    def __init__(self, widget, text):
        self.widget = widget
        self.text = text
        self.tip_window = None
        widget.bind("<Enter>", self.show_tip)
        widget.bind("<Leave>", self.hide_tip)

    def show_tip(self, event=None):
        if self.tip_window or not self.text:
            return
        x, y, _, _ = self.widget.bbox("insert")
        x += self.widget.winfo_rootx() + 25
        y += self.widget.winfo_rooty() + 25
        self.tip_window = tw = tk.Toplevel(self.widget)
        tw.wm_overrideredirect(True)  # ventana sin bordes
        tw.wm_geometry(f"+{x}+{y}")
        label = tk.Label(tw, text=self.text, background="yellow",
                         relief="solid", borderwidth=1,
                         font=("Arial", 9))
        label.pack(ipadx=4)

    def hide_tip(self, event=None):
        tw = self.tip_window
        self.tip_window = None
        if tw:
            tw.destroy()

# ============================================
# Paso 4. Funciones CRUD (Crear, Leer, Actualizar, Eliminar)
# ============================================

# 4.1 Mostrar todas las tareas
# Para qué sirve: refresca la tabla con todas las tareas, aplicando filtros
def actualizar_lista(filtro="todas"):
    for item in tree.get_children():
        tree.delete(item)

    con = conectar()
    cursor = con.cursor()
    cursor.execute("SELECT id, texto, completada FROM tareas ORDER BY texto ASC")
    for id, texto, completada in cursor.fetchall():
        if filtro == "pendientes" and completada:
            continue
        if filtro == "completadas" and not completada:
            continue
        estado = "Resuelta ✅" if completada else "Pendiente ⏳"
        tree.insert("", "end", iid=id, values=(estado, texto))
    con.close()

# 4.2 Agregar tarea
# Para qué sirve: inserta una nueva tarea en la base de datos
def agregar_tarea():
    texto = entry_tarea.get().strip()
    if texto:
        con = conectar()
        cursor = con.cursor()
        cursor.execute("INSERT INTO tareas (texto, completada) VALUES (%s, %s)", (texto, False))
        con.commit()
        con.close()
        entry_tarea.delete(0, tk.END)
        actualizar_lista()
    else:
        messagebox.showwarning("Atención", "Escribe una tarea antes de agregar.")

# 4.3 Marcar/Desmarcar tarea
# Para qué sirve: cambia el estado de una tarea (pendiente ↔ resuelta)
def completar_tarea():
    seleccion = tree.selection()
    if seleccion:
        id_tarea = int(seleccion[0])
        con = conectar()
        cursor = con.cursor()
        cursor.execute("SELECT completada FROM tareas WHERE id=%s", (id_tarea,))
        estado = cursor.fetchone()[0]
        nuevo_estado = not estado
        cursor.execute("UPDATE tareas SET completada=%s WHERE id=%s", (nuevo_estado, id_tarea))
        con.commit()
        con.close()
        actualizar_lista()
    else:
        messagebox.showwarning("Atención", "Selecciona una tarea para marcar.")

# 4.4 Eliminar tarea
# Para qué sirve: borra la tarea seleccionada de la base de datos
def eliminar_tarea():
    seleccion = tree.selection()
    if seleccion:
        id_tarea = int(seleccion[0])
        confirmar = messagebox.askyesno("Confirmar", "¿Seguro que deseas eliminar esta tarea?")
        if confirmar:
            con = conectar()
            cursor = con.cursor()
            cursor.execute("DELETE FROM tareas WHERE id=%s", (id_tarea,))
            con.commit()
            con.close()
            actualizar_lista()
    else:
        messagebox.showwarning("Atención", "Selecciona una tarea para eliminar.")

# ============================================
# Paso 5. Construir la interfaz gráfica
# ============================================
# Para qué sirve: organizar los widgets (entradas, botones, tabla, filtros)
ventana = tk.Tk()
ventana.title("Lista de Tareas con MySQL")
ventana.geometry("600x500")  # un poco más alta para que quepa todo

# Entrada de nueva tarea
frame_input = tk.Frame(ventana)
frame_input.pack(pady=10)

entry_tarea = tk.Entry(frame_input, width=40)
entry_tarea.pack(side=tk.LEFT, padx=5)

btn_agregar = tk.Button(frame_input, text="Agregar", command=agregar_tarea, bg="yellow")
btn_agregar.pack(side=tk.LEFT)

# Treeview para mostrar tareas
tree = ttk.Treeview(ventana, columns=("Estado", "Tarea"), show="headings", height=15)
tree.heading("Estado", text="Estado")
tree.heading("Tarea", text="Tarea")
tree.column("Estado", width=100, anchor="center")
tree.column("Tarea", width=400, anchor="w")
tree.pack(pady=10)

# Botones de acción
frame_botones = tk.Frame(ventana)
frame_botones.pack(pady=5)

btn_completar = tk.Button(frame_botones, text="Marcar/Desmarcar", command=completar_tarea, bg="lightgreen")
btn_completar.pack(side=tk.LEFT, padx=5)
ToolTip(btn_completar, "Marca las tareas o actividades que ya se han completado")

btn_eliminar = tk.Button(frame_botones, text="Eliminar", command=eliminar_tarea, bg="tomato")
btn_eliminar.pack(side=tk.LEFT, padx=5)

# Botones de filtro
frame_filtros = tk.Frame(ventana)
frame_filtros.pack(pady=10)

tk.Button(frame_filtros, text="Todas", command=lambda: actualizar_lista("todas")).pack(side=tk.LEFT, padx=5)
tk.Button(frame_filtros, text="Pendientes", command=lambda: actualizar_lista("pendientes")).pack(side=tk.LEFT, padx=5)
tk.Button(frame_filtros, text="Completadas", command=lambda: actualizar_lista("completadas")).pack(side=tk.LEFT, padx=5)

# Botón salir fijo abajo
btn_salir = tk.Button(
    ventana,
    text="Salir",
    command=ventana.destroy,
    bg="gray",
    fg="white",
    font=("Arial", 12, "bold")
)
btn_salir.pack(side="bottom", pady=15, fill="x")

# ============================================
# Paso 6. Inicializar la vista y ejecutar
# ============================================
# Para qué sirve: cargar las tareas al inicio y mantener la ventana abierta
actualizar_lista()
ventana.mainloop()