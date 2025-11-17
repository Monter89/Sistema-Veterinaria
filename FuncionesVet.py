# ------------------------- Clase Mascota ----------------------------------

class Mascota:
    
    def __init__(self, nombre, edad, especie, peso):
        self.nombre = nombre
        try:
            self.edad = int(edad)
            self.peso = float(peso)
        except (ValueError, TypeError):
            self.edad = 0
            self.peso = 0.0

        self.especie = especie
        self.historial_medico = []

    def __str__(self):
        return f"{self.nombre} ({self.especie}, {self.edad} años)"

    def agregar_consulta(self, descripcion):
        self.historial_medico.append(descripcion)
        return True

    def cumplir_anios(self):
        self.edad += 1
        return True

    def actualizar_peso(self, nuevo_peso):
        try:
            self.peso = float(nuevo_peso)
            self.agregar_consulta(f'Peso actualizado a {nuevo_peso} kg')
            return True
        except (ValueError, TypeError):
            return False


# ------------------------- Clase Dueño ----------------------------------

class Duenio:
    
    def __init__(self, nombre, telefono):
        self.nombre = nombre
        self.telefono = telefono
        self.mascotas = []

    def registrar_mascota(self, mascota):
        self.mascotas.append(mascota)
        return True 

    def buscar_mascota(self, nombre):
        for m in self.mascotas:
            if m.nombre.lower() == nombre.lower():
                return m
        return None


# ------------------------- Clase Veterinaria ----------------------------------

class Veterinaria:
    
    def __init__(self, nombre):
        self.nombre = nombre
        self.clientes = []
        self.servicios = {
            "Consulta General": 25000,
            "Vacuna Triple": 40000,
            "Desparasitación": 15000,
            "Corte": 10000
        } 

    def registrar_duenio(self, duenio):
        self.clientes.append(duenio)
        return True

    def buscar_duenio(self, nombre):
        for d in self.clientes:
            if d.nombre.lower() == nombre.lower():
                return d
        return None

    def agregar_servicio(self, nombre_servicio, precio):
        try:
            precio_float = float(precio)
            self.servicios[nombre_servicio] = precio_float
            return True
        except (ValueError, TypeError):
            return False 

    def registrar_consulta(self, nombre_duenio, nombre_mascota, servicio):
        duenio = self.buscar_duenio(nombre_duenio)
        if duenio:
            mascota = duenio.buscar_mascota(nombre_mascota)
            if mascota and servicio in self.servicios:
                precio = self.servicios[servicio]
                descripcion = f'Consulta: {servicio} (${precio:.2f})'
                mascota.agregar_consulta(descripcion)
                return True
        return False

    def generar_factura(self, nombre_duenio, nombre_mascota, servicio):
        duenio = self.buscar_duenio(nombre_duenio)
        if duenio:
            mascota = duenio.buscar_mascota(nombre_mascota)
            if mascota and servicio in self.servicios:
                precio = self.servicios[servicio]
                return [self.nombre, duenio.nombre, f"{mascota.nombre} ({mascota.especie})", servicio, precio]
        return [] 