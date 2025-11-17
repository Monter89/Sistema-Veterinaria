# 🐾 Sistema de Gestión Veterinaria

Aplicación de escritorio desarrollada en **Python** para administrar la información de una clínica veterinaria ("Clínica Animal Feliz"). El sistema permite registrar clientes, pacientes, gestionar historias clínicas y generar facturas de forma sencilla.

## 📋 Funcionalidades

* **Registro de Dueños:** Alta de clientes con validación de datos (teléfonos numéricos).
* **Gestión de Mascotas:** Registro de pacientes validando edad (entero) y peso (decimal).
* **Historial Médico:** Visualización rápida de las consultas previas de cada animal.
* **Facturación:** Generación automática de costos basada en los servicios realizados.
* **Buscador:** Filtro en tiempo real para encontrar clientes o mascotas rápidamente.
* **Portable:** El sistema funciona en cualquier PC sin necesidad de configurar rutas de imágenes manualmente.

## 🛠️ Tecnologías

* **Lenguaje:** Python 3
* **Interfaz (GUI):** Tkinter (Diseño personalizado y moderno)
* **Imágenes:** Pillow (PIL)
* **Control de Versiones:** Git

## 🚀 Cómo ejecutar el proyecto

1.  **Clonar el repositorio:**
    ```bash
    git clone [https://github.com/Monter89/Sistema-Veterinaria.git](https://github.com/Monter89/Sistema-Veterinaria.git)
    ```

2.  **Entrar a la carpeta:**
    ```bash
    cd Sistema-Veterinaria
    ```

3.  **Instalar dependencias:**
    Solo necesitas instalar la librería de imágenes.
    ```bash
    pip install -r requirements.txt
    ```

4.  **Iniciar el programa:**
    ```bash
    python main.py
    ```

## 📂 Estructura de Archivos

* `main.py`: Archivo principal con la interfaz gráfica.
* `FuncionesVet.py`: Lógica del sistema (Clases: Mascota, Dueño, Veterinaria).
* `Fondo.png`: Imagen de portada.
* `requirements.txt`: Lista de librerías necesarias.

---
**Autor:** [Gaston Montero]
* [GitHub](https://github.com/Monter89)
* [LinkedIn](https://www.linkedin.com/in/gaston-montero)
