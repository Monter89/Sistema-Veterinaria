import tkinter as tk
import os  # <--- NUEVO: Importante para las rutas
from PIL import Image, ImageTk
from tkinter import Toplevel, ttk, messagebox
from FuncionesVet import Mascota, Duenio, Veterinaria

# Colores y estilos 
COLOR_PRIMARY = "#4CAF50" 
COLOR_ACCENT = "#388E3C"  
COLOR_DARK = "#263238"    
COLOR_BG_LIGHT = "#E0F7FA" 
COLOR_BG_CARD = "#FFFFFF" 
COLOR_CANVAS = "#E8F5E9" 

# --------------------- Instancia Veterinaria ---------------------
vet = Veterinaria("Clínica Animal Feliz")

#  Función: Botón
def crear_boton_moderno(parent, texto, comando):
    """Crea un botón con estilos modernos y efecto hover."""
    frame_btn = tk.Frame(parent, bg=COLOR_DARK)
    frame_btn.pack(pady=2, ipadx=2, ipady=2, fill="x")
    
    boton = tk.Button(frame_btn, text=texto, font=("Segoe UI", 14, "bold"),
                      bg=COLOR_PRIMARY, fg="white", bd=0, relief="flat",
                      activebackground=COLOR_ACCENT, activeforeground="white",
                      command=comando)
    boton.pack(ipadx=10, ipady=8, fill="x")
    
    def on_enter(e):
        boton.config(bg=COLOR_ACCENT, relief="raised")
    def on_leave(e):
        boton.config(bg=COLOR_PRIMARY, relief="flat")
    boton.bind("<Enter>", on_enter)
    boton.bind("<Leave>", on_leave)
    
    return frame_btn

# Función: Treeview 
def mostrar_tabla_moderna(title, columnas, datos):
    """Muestra una nueva ventana con una tabla de datos (Treeview) y un campo de búsqueda."""
    ventana = Toplevel(root)
    ventana.title(title)
    ventana.geometry("800x600")
    ventana.grab_set()
    ventana.focus_set()
    ventana.configure(bg=COLOR_BG_LIGHT)

    frame_tabla = tk.Frame(ventana, bg=COLOR_BG_LIGHT, padx=10, pady=10)
    frame_tabla.pack(fill="both", expand=True)

    # Campo de búsqueda
    busqueda_var = tk.StringVar()
    tk.Label(frame_tabla, text="Buscar:", bg=COLOR_BG_LIGHT, fg=COLOR_DARK, font=("Segoe UI", 12)).pack(anchor="nw")
    tk.Entry(frame_tabla, textvariable=busqueda_var, font=("Segoe UI", 12)).pack(anchor="nw", fill="x", pady=(0, 10))

    # Estilo del Treeview
    style = ttk.Style()
    style.theme_use("clam")
    style.configure("Treeview", background="#F9F9F9", foreground="black",
                    rowheight=28, fieldbackground="#F9F9F9", font=("Segoe UI", 11))
    style.map("Treeview", background=[("selected", COLOR_PRIMARY)], foreground=[("selected", "white")])
    
    tree = ttk.Treeview(frame_tabla, columns=columnas, show="headings")
    
    # Scrollbars
    scrollbar_y = ttk.Scrollbar(frame_tabla, orient="vertical", command=tree.yview)
    scrollbar_x = ttk.Scrollbar(frame_tabla, orient="horizontal", command=tree.xview)
    tree.configure(yscrollcommand=scrollbar_y.set, xscrollcommand=scrollbar_x.set)
    scrollbar_y.pack(side="right", fill="y")
    scrollbar_x.pack(side="bottom", fill="x")
    tree.pack(fill="both", expand=True)

    # Configuración de columnas
    for col in columnas:
        tree.heading(col, text=col)
        tree.column(col, width=150, anchor="center", stretch=True)

    # Función de filtrado dinámico
    def filtrar(*args):
        query = busqueda_var.get().lower()
        tree.delete(*tree.get_children())
        for fila in datos:
            if any(query in str(valor).lower() for valor in fila):
                tree.insert("", "end", values=fila)

    busqueda_var.trace_add("write", filtrar)
    filtrar()

# Funciones GUI de Operaciones 

# Registrar Dueño
def registrar_duenio_gui():
    ventana = Toplevel(root)
    ventana.title("Registrar Dueño")
    ventana.geometry("400x250")
    ventana.grab_set()
    ventana.focus_set()
    ventana.configure(bg=COLOR_BG_LIGHT)

    tk.Label(ventana, text="Nombre del dueño:", bg=COLOR_BG_LIGHT, fg=COLOR_DARK, font=("Segoe UI", 12)).pack(anchor="nw", padx=20, pady=(20,5))
    nombre_var = tk.StringVar()
    tk.Entry(ventana, textvariable=nombre_var, font=("Segoe UI", 12)).pack(anchor="nw", padx=20, fill="x")

    tk.Label(ventana, text="Teléfono:", bg=COLOR_BG_LIGHT, fg=COLOR_DARK, font=("Segoe UI", 12)).pack(anchor="nw", padx=20, pady=(15,5))
    telefono_var = tk.StringVar()
    tk.Entry(ventana, textvariable=telefono_var, font=("Segoe UI", 12)).pack(anchor="nw", padx=20, fill="x")

    def guardar():
        nombre = nombre_var.get().strip()
        telefono = telefono_var.get().strip()

        if not telefono.isdigit():
            messagebox.showerror("Error", "El teléfono debe contener solo números (sin guiones ni espacios).")
            return 

        if nombre and telefono:
            d = Duenio(nombre, telefono)
            
            exito = vet.registrar_duenio(d)
            if exito:
                messagebox.showinfo("Éxito", f"Dueño {nombre} registrado correctamente")
                ventana.destroy()
            else:
                messagebox.showerror("Error", "No se pudo registrar el dueño")
        else:
            messagebox.showerror("Error", "Completar ambos campos")

    crear_boton_moderno(ventana, "Registrar", guardar)

# Ver Dueños
def ver_duenios_gui():
    datos = [(d.nombre, d.telefono) for d in vet.clientes]
    mostrar_tabla_moderna("Dueños Registrados", ["Nombre", "Teléfono"], datos)

# Registrar Mascota
def registrar_mascota_gui():
    ventana = Toplevel(root)
    ventana.title("Registrar Mascota")
    ventana.geometry("400x480") # Tamaño ajustado
    ventana.grab_set()
    ventana.focus_set()
    ventana.configure(bg=COLOR_BG_LIGHT)

    tk.Label(ventana, text="Nombre del dueño:", bg=COLOR_BG_LIGHT, fg=COLOR_DARK, font=("Segoe UI", 12)).pack(anchor="nw", padx=20, pady=(20,5))
    duenio_var = tk.StringVar()
    tk.Entry(ventana, textvariable=duenio_var, font=("Segoe UI", 12)).pack(anchor="nw", padx=20, fill="x")

    tk.Label(ventana, text="Nombre mascota:", bg=COLOR_BG_LIGHT, fg=COLOR_DARK, font=("Segoe UI", 12)).pack(anchor="nw", padx=20, pady=(5,5))
    nombre_var = tk.StringVar()
    tk.Entry(ventana, textvariable=nombre_var, font=("Segoe UI", 12)).pack(anchor="nw", padx=20, fill="x")

    tk.Label(ventana, text="Edad (años):", bg=COLOR_BG_LIGHT, fg=COLOR_DARK, font=("Segoe UI", 12)).pack(anchor="nw", padx=20, pady=(5,5))
    edad_var = tk.StringVar()
    tk.Entry(ventana, textvariable=edad_var, font=("Segoe UI", 12)).pack(anchor="nw", padx=20, fill="x")

    tk.Label(ventana, text="Especie:", bg=COLOR_BG_LIGHT, fg=COLOR_DARK, font=("Segoe UI", 12)).pack(anchor="nw", padx=20, pady=(5,5))
    especie_var = tk.StringVar()
    tk.Entry(ventana, textvariable=especie_var, font=("Segoe UI", 12)).pack(anchor="nw", padx=20, fill="x")

    tk.Label(ventana, text="Peso (kg):", bg=COLOR_BG_LIGHT, fg=COLOR_DARK, font=("Segoe UI", 12)).pack(anchor="nw", padx=20, pady=(5,5))
    peso_var = tk.StringVar()
    tk.Entry(ventana, textvariable=peso_var, font=("Segoe UI", 12)).pack(anchor="nw", padx=20, fill="x")

    def guardar():
        nombre_duenio = duenio_var.get().strip()
        nombre = nombre_var.get().strip()
        edad = edad_var.get().strip()
        especie = especie_var.get().strip()
        peso = peso_var.get().strip()

        # --- VALIDACIONES NUEVAS ---
        if not edad.isdigit():
            messagebox.showerror("Error", "La edad debe ser un número entero (ej: 5).")
            return

        try:
            # Intentamos ver si el peso es un número válido (ej: 10.5)
            float(peso)
        except ValueError:
            messagebox.showerror("Error", "El peso debe ser un número válido (ej: 10.5). Use punto para decimales.")
            return
        

        duenio = vet.buscar_duenio(nombre_duenio)
        if not duenio:
            messagebox.showerror("Error", f"Dueño '{nombre_duenio}' no encontrado. Regístrelo primero.")
            return

        if nombre and edad and especie and peso:
            try:
                mascota = Mascota(nombre, edad, especie, peso) 
                
                if duenio.registrar_mascota(mascota):
                    messagebox.showinfo("Éxito", f"{nombre} registrada a nombre de {duenio.nombre}.")
                    ventana.destroy()
                else:
                    messagebox.showerror("Error", "No se pudo registrar la mascota")
            except Exception as e:
                messagebox.showerror("Error", f"Error inesperado: {e}")
        else:
            messagebox.showerror("Error", "Completar todos los campos")

    crear_boton_moderno(ventana, "Registrar Mascota", guardar)

# Ver Servicios
def ver_servicios_gui():
    datos = [(s, f"${p:.2f}") for s, p in vet.servicios.items()]
    mostrar_tabla_moderna("Servicios Registrados", ["Servicio", "Precio"], datos)

# Agregar Servicio
def agregar_servicio_gui():
    ventana = Toplevel(root)
    ventana.title("Agregar Servicio")
    ventana.geometry("400x250")
    ventana.grab_set()
    ventana.focus_set()
    ventana.configure(bg=COLOR_BG_LIGHT)

    tk.Label(ventana, text="Nombre del servicio:", bg=COLOR_BG_LIGHT, fg=COLOR_DARK, font=("Segoe UI", 12)).pack(anchor="nw", padx=20, pady=(20,5))
    servicio_var = tk.StringVar()
    tk.Entry(ventana, textvariable=servicio_var, font=("Segoe UI", 12)).pack(anchor="nw", padx=20, fill="x")

    tk.Label(ventana, text="Precio:", bg=COLOR_BG_LIGHT, fg=COLOR_DARK, font=("Segoe UI", 12)).pack(anchor="nw", padx=20, pady=(15,5))
    precio_var = tk.StringVar()
    tk.Entry(ventana, textvariable=precio_var, font=("Segoe UI", 12)).pack(anchor="nw", padx=20, fill="x")

    def guardar():
        nombre_servicio = servicio_var.get().strip()
        
        precio_str = precio_var.get().strip().replace(",", ".") 
        
        # --- VALIDACIÓN NUEVA ---
        try:
            float(precio_str) 
        except ValueError:
            messagebox.showerror("Error", "El precio debe ser un número (ej: 1500 o 1500.50).")
            return
        
        
        if nombre_servicio and precio_str:
            exito = vet.agregar_servicio(nombre_servicio, precio_str)
            
            if exito:
                messagebox.showinfo("Éxito", f"Servicio {nombre_servicio} agregado.")
                ventana.destroy()
            else:
                messagebox.showerror("Error", "No se pudo agregar el servicio.")
        else:
            messagebox.showerror("Error", "Completar todos los campos")

    crear_boton_moderno(ventana, "Agregar Servicio", guardar)

# Registrar Consulta
def registrar_consulta_gui():
    ventana = Toplevel(root)
    ventana.title("Registrar Consulta")
    ventana.geometry("400x300")
    ventana.grab_set()
    ventana.focus_set()
    ventana.configure(bg=COLOR_BG_LIGHT)

    tk.Label(ventana, text="Nombre del dueño:", bg=COLOR_BG_LIGHT, fg=COLOR_DARK, font=("Segoe UI", 12)).pack(anchor="nw", padx=20, pady=(20,5))
    duenio_var = tk.StringVar()
    tk.Entry(ventana, textvariable=duenio_var, font=("Segoe UI", 12)).pack(anchor="nw", padx=20, fill="x")

    tk.Label(ventana, text="Nombre mascota:", bg=COLOR_BG_LIGHT, fg=COLOR_DARK, font=("Segoe UI", 12)).pack(anchor="nw", padx=20, pady=(15,5))
    mascota_var = tk.StringVar()
    tk.Entry(ventana, textvariable=mascota_var, font=("Segoe UI", 12)).pack(anchor="nw", padx=20, fill="x")

    tk.Label(ventana, text="Servicio:", bg=COLOR_BG_LIGHT, fg=COLOR_DARK, font=("Segoe UI", 12)).pack(anchor="nw", padx=20, pady=(15,5))
    servicio_var = tk.StringVar()
    tk.Entry(ventana, textvariable=servicio_var, font=("Segoe UI", 12)).pack(anchor="nw", padx=20, fill="x")

    def guardar():
        nombre_duenio = duenio_var.get().strip()
        nombre_mascota = mascota_var.get().strip()
        servicio = servicio_var.get().strip()

        if not (nombre_duenio and nombre_mascota and servicio):
            messagebox.showerror("Error", "Completar todos los campos")
            return

        exito = vet.registrar_consulta(nombre_duenio, nombre_mascota, servicio)
        
        if exito:
            messagebox.showinfo("Éxito", f"Consulta '{servicio}' registrada para {nombre_mascota}.")
            ventana.destroy()
        else:
            # El error puede ser por dueño, mascota o servicio no encontrado/válido
            error_msg = "Error al registrar: Verifique que el Dueño, Mascota y Servicio existan."
            messagebox.showerror("Error", error_msg)

    crear_boton_moderno(ventana, "Registrar Consulta", guardar)

# Historial de Mascota
def ver_historial_gui():
    ventana = Toplevel(root)
    ventana.title("Búsqueda de Historial")
    ventana.geometry("400x250")
    ventana.grab_set()
    ventana.focus_set()
    ventana.configure(bg=COLOR_BG_LIGHT)

    tk.Label(ventana, text="Nombre del dueño:", bg=COLOR_BG_LIGHT, fg=COLOR_DARK, font=("Segoe UI", 12)).pack(anchor="nw", padx=20, pady=(20,5))
    duenio_var = tk.StringVar()
    tk.Entry(ventana, textvariable=duenio_var, font=("Segoe UI", 12)).pack(anchor="nw", padx=20, fill="x")

    tk.Label(ventana, text="Nombre mascota:", bg=COLOR_BG_LIGHT, fg=COLOR_DARK, font=("Segoe UI", 12)).pack(anchor="nw", padx=20, pady=(15,5))
    mascota_var = tk.StringVar()
    tk.Entry(ventana, textvariable=mascota_var, font=("Segoe UI", 12)).pack(anchor="nw", padx=20, fill="x")

    def mostrar():
        nombre_duenio = duenio_var.get().strip()
        nombre_mascota = mascota_var.get().strip()
        
        duenio = vet.buscar_duenio(nombre_duenio)
        if not duenio:
            messagebox.showerror("Error", "Dueño no encontrado")
            return
        
        mascota = duenio.buscar_mascota(nombre_mascota)
        if not mascota:
            messagebox.showerror("Error", "Mascota no encontrada")
            return
        
        # Prepara los datos para la tabla
        datos = [(f"Especie: {mascota.especie}", "---")]
        datos.append((f"Edad Actual: {mascota.edad} años", f"Peso Actual: {mascota.peso} kg"))
        
        if mascota.historial_medico:
            # Las consultas se listan como [Detalle, Valor]
            datos.extend([(c, "---") for c in mascota.historial_medico])
        else:
            datos.append(("Sin registros de consultas.", "---"))
            
        mostrar_tabla_moderna(f"Historial de {mascota.nombre}", ["Detalle / Evento", "Valor"], datos)
        ventana.destroy()

    crear_boton_moderno(ventana, "Ver Historial", mostrar)

# Cumplir Años
def cumplir_anios_gui():
    ventana = Toplevel(root)
    ventana.title("Cumplir Años")
    ventana.geometry("400x250")
    ventana.grab_set()
    ventana.focus_set()
    ventana.configure(bg=COLOR_BG_LIGHT)

    tk.Label(ventana, text="Nombre del dueño:", bg=COLOR_BG_LIGHT, fg=COLOR_DARK, font=("Segoe UI", 12)).pack(anchor="nw", padx=20, pady=(20,5))
    duenio_var = tk.StringVar()
    tk.Entry(ventana, textvariable=duenio_var, font=("Segoe UI", 12)).pack(anchor="nw", padx=20, fill="x")

    tk.Label(ventana, text="Nombre mascota:", bg=COLOR_BG_LIGHT, fg=COLOR_DARK, font=("Segoe UI", 12)).pack(anchor="nw", padx=20, pady=(15,5))
    mascota_var = tk.StringVar()
    tk.Entry(ventana, textvariable=mascota_var, font=("Segoe UI", 12)).pack(anchor="nw", padx=20, fill="x")

    def aplicar():
        nombre_duenio = duenio_var.get().strip()
        nombre_mascota = mascota_var.get().strip()
        
        duenio = vet.buscar_duenio(nombre_duenio)
        if not duenio:
            messagebox.showerror("Error", "Dueño no encontrado")
            return
        
        mascota = duenio.buscar_mascota(nombre_mascota)
        if not mascota:
            messagebox.showerror("Error", "Mascota no encontrada")
            return
            
        # Pide confirmación al usuario antes de modificar
        if messagebox.askyesno("Confirmar", f"Confirmar que {mascota.nombre} cumplirá {mascota.edad + 1} años?"):
            mascota.cumplir_anios()
            messagebox.showinfo("¡Felicidades!", f"{mascota.nombre} ahora tiene {mascota.edad} años.")
            ventana.destroy()
        else:
            messagebox.showinfo("Cancelado", "Operación cancelada.")

    crear_boton_moderno(ventana, "Aplicar Cumpleaños", aplicar)

# Generar Factura
def generar_factura_gui():
    ventana = Toplevel(root)
    ventana.title("Generar Factura")
    ventana.geometry("400x300")
    ventana.grab_set()
    ventana.focus_set()
    ventana.configure(bg=COLOR_BG_LIGHT)

    tk.Label(ventana, text="Nombre del dueño:", bg=COLOR_BG_LIGHT, fg=COLOR_DARK, font=("Segoe UI", 12)).pack(anchor="nw", padx=20, pady=(20,5))
    duenio_var = tk.StringVar()
    tk.Entry(ventana, textvariable=duenio_var, font=("Segoe UI", 12)).pack(anchor="nw", padx=20, fill="x")

    tk.Label(ventana, text="Nombre mascota:", bg=COLOR_BG_LIGHT, fg=COLOR_DARK, font=("Segoe UI", 12)).pack(anchor="nw", padx=20, pady=(15,5))
    mascota_var = tk.StringVar()
    tk.Entry(ventana, textvariable=mascota_var, font=("Segoe UI", 12)).pack(anchor="nw", padx=20, fill="x")

    tk.Label(ventana, text="Servicio:", bg=COLOR_BG_LIGHT, fg=COLOR_DARK, font=("Segoe UI", 12)).pack(anchor="nw", padx=20, pady=(15,5))
    servicio_var = tk.StringVar()
    tk.Entry(ventana, textvariable=servicio_var, font=("Segoe UI", 12)).pack(anchor="nw", padx=20, fill="x")

    def generar():
        nombre_duenio = duenio_var.get().strip()
        nombre_mascota = mascota_var.get().strip()
        servicio = servicio_var.get().strip()

        # Llamada a la lógica del negocio
        factura_data = vet.generar_factura(nombre_duenio, nombre_mascota, servicio)
        
        if factura_data:
            # Factura devuelta: [Vet, Dueño, Mascota, Servicio, Precio(float)]
            columnas = ["Veterinaria", "Dueño", "Mascota", "Servicio", "Precio"]
            precio_float_val = factura_data[4] 
            # Formatea el precio a string con el signo $
            datos = [factura_data[:4] + [f"${precio_float_val:.2f}"]]

            
            mostrar_tabla_moderna("Factura Generada", columnas, datos)
            ventana.destroy()
        else:
            messagebox.showerror("Error", "Error generando factura. Verifique Dueño, Mascota y Servicio.")

    crear_boton_moderno(ventana, "Generar Factura", generar)


# Ventana Principal 
root = tk.Tk()
root.title("Clínica Animal Feliz 🐾")
root.geometry("1000x750") 
root.resizable(False, False)
root.configure(bg=COLOR_BG_LIGHT)

# Marco contenedor para centrar el contenido horizontalmente
container_frame = tk.Frame(root, bg=COLOR_BG_LIGHT)
container_frame.place(relx=0.5, rely=0.5, anchor="center")

# 1. Marco Izquierdo: Imagen y Título

frame_image_side = tk.Frame(container_frame, bg=COLOR_BG_CARD, padx=20, pady=20, bd=5, relief="raised", width=400)
frame_image_side.pack(side=tk.LEFT, fill="y", padx=10, pady=10, expand=False)
frame_image_side.pack_propagate(False) # Evita que el frame se encoja por el contenido

tk.Label(frame_image_side, text=f"{vet.nombre} 🐾", font=("Segoe UI", 24, "bold"),
          fg=COLOR_DARK, bg=COLOR_BG_CARD).pack(pady=(10, 5))
tk.Label(frame_image_side, text="Bienvenido al Sistema de Gestión", font=("Segoe UI", 14),
          fg=COLOR_ACCENT, bg=COLOR_BG_CARD).pack(pady=(0, 20))

# Área de la Imagen
canvas_width = 360
canvas_height = 400
canvas_img = tk.Canvas(frame_image_side, width=canvas_width, height=canvas_height,
                        bg=COLOR_CANVAS, highlightthickness=0)
canvas_img.pack(pady=20)

# ----------------------- CAMBIO AQUÍ -----------------------
# Esta lógica hace que funcione en cualquier PC

# 1. Obtiene la carpeta donde está ESTE archivo .py
carpeta_base = os.path.dirname(os.path.abspath(__file__))

# 2. Busca la imagen "Fondo.png" en esa misma carpeta
image_path = os.path.join(carpeta_base, "Fondo.png")
# -----------------------------------------------------------

try:
    # Cargar la imagen usando PIL
    original_image = Image.open(image_path)
    
    # Redimensionar la imagen para que quepa en el canvas
    # Calcula la relación de aspecto para mantener las proporciones
    width_ratio = canvas_width / original_image.width
    height_ratio = canvas_height / original_image.height
    
    # Usa la relación más pequeña para asegurar que la imagen quepa completamente
    resize_ratio = min(width_ratio, height_ratio)
    
    new_width = int(original_image.width * resize_ratio)
    new_height = int(original_image.height * resize_ratio)
    
    resized_image = original_image.resize((new_width, new_height), Image.Resampling.LANCZOS)
    
    # Convertir a formato PhotoImage para Tkinter
    photo_image = ImageTk.PhotoImage(resized_image)
    
    # Guardar una referencia a la imagen para evitar que sea eliminada por el recolector de basura
    canvas_img.image = photo_image 
    
    # Dibujar la imagen en el centro del canvas
    # Calcula las coordenadas para centrar la imagen
    x_center = (canvas_width - new_width) / 2
    y_center = (canvas_height - new_height) / 2
    
    canvas_img.create_image(x_center, y_center, anchor=tk.NW, image=photo_image)
    
except FileNotFoundError:
    messagebox.showerror("Error de Imagen", f"No se encontró la imagen en:\n{image_path}\n\n"
                                             "Por favor, coloca 'Fondo.png' en la misma carpeta que este archivo.")
    # Si la imagen no se encuentra, puedes dejar un texto o el dibujo de la huella
    canvas_img.create_text(canvas_width/2, canvas_height/2, text="Imagen no encontrada", 
                            font=("Segoe UI", 16, "bold"), fill=COLOR_DARK)
    
except Exception as e:
    messagebox.showerror("Error de Imagen", f"No se pudo cargar la imagen: {e}")
    canvas_img.create_text(canvas_width/2, canvas_height/2, text="Error al cargar imagen", 
                            font=("Segoe UI", 16, "bold"), fill=COLOR_DARK)
    
    tk.Label(frame_image_side, text="¡El mejor cuidado para tus mascotas!", font=("Segoe UI", 12, "italic"),
          fg=COLOR_DARK, bg=COLOR_BG_CARD).pack(pady=(10, 0))


# 2. Marco Derecho: Botones de Funcionalidad

frame_button_side = tk.Frame(container_frame, bg=COLOR_BG_CARD, padx=20, pady=20, bd=5, relief="raised")
frame_button_side.pack(side=tk.RIGHT, fill="y", padx=10, pady=10, expand=True)

tk.Label(frame_button_side, text="Menú Principal de Gestión", font=("Segoe UI", 18, "bold"),
          fg=COLOR_ACCENT, bg=COLOR_BG_CARD).pack(pady=(10, 15))


# Bloque de Clientes y Mascotas
tk.Label(frame_button_side, text="— Clientes y Pacientes —", font=("Segoe UI", 14, "italic"),
          fg=COLOR_DARK, bg=COLOR_BG_CARD).pack(pady=(5, 5))

crear_boton_moderno(frame_button_side, "Registrar Dueño 👤", registrar_duenio_gui)
crear_boton_moderno(frame_button_side, "Ver Dueños 👨‍👩‍👧‍👦", ver_duenios_gui)
crear_boton_moderno(frame_button_side, "Registrar Mascota 🐾", registrar_mascota_gui)
crear_boton_moderno(frame_button_side, "Ver Historial 📜", ver_historial_gui)
crear_boton_moderno(frame_button_side, "Cumplir Años 🎂", cumplir_anios_gui)

# Bloque de Servicios y Consultas
tk.Label(frame_button_side, text="— Servicios y Consultas —", font=("Segoe UI", 14, "italic"),
          fg=COLOR_DARK, bg=COLOR_BG_CARD).pack(pady=(15, 5))

crear_boton_moderno(frame_button_side, "Ver Servicios y Precios 💊", ver_servicios_gui)
crear_boton_moderno(frame_button_side, "Agregar Nuevo Servicio ➕", agregar_servicio_gui)
crear_boton_moderno(frame_button_side, "Registrar Consulta 📝", registrar_consulta_gui)
crear_boton_moderno(frame_button_side, "Generar Factura 💰", generar_factura_gui)

root.mainloop()