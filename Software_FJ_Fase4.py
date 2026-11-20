# ==========================================================
# UNIVERSIDAD NACIONAL ABIERTA Y A DISTANCIA - UNAD
# Programa: Ingeniería de Sistemas
# Curso: Programación - 213023
# Fase 4: Componente práctico - Prácticas simuladas
# Proyecto: Sistema Integral de Gestión de Clientes,
# Servicios y Reservas - Software FJ
# Modalidad: Entrega individual
# ==========================================================


# ==========================================================
# 1. IMPORTACIÓN DE LIBRERÍAS
# ==========================================================

from abc import ABC, abstractmethod
from pathlib import Path
import re
import logging


# ==========================================================
# 2. CONFIGURACIÓN DEL ARCHIVO DE REGISTROS
# ==========================================================

RUTA_LOG = Path(__file__).resolve().parent / "logs.txt"

logging.basicConfig(
    filename=str(RUTA_LOG),
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%d/%m/%Y %H:%M:%S",
    encoding="utf-8",
    force=True
)

logger = logging.getLogger("SoftwareFJ")


def registrar_evento(mensaje):
    """Guarda un evento normal del sistema."""
    logger.info(mensaje)


def registrar_error(mensaje):
    """Guarda un error que ha sido controlado."""
    logger.error(mensaje)


def registrar_excepcion(mensaje):
    """Guarda el detalle de una excepción activa."""
    logger.exception(mensaje)


# ==========================================================
# 3. EXCEPCIONES PERSONALIZADAS
# ==========================================================

class ErrorSistema(Exception):
    """Clase base para los errores propios del sistema."""
    pass


class DatosInvalidosError(ErrorSistema):
    """Se presenta cuando un dato no cumple las condiciones."""
    pass


class ClienteNoEncontradoError(ErrorSistema):
    """Se presenta cuando el cliente no está registrado."""
    pass


class ServicioNoDisponibleError(ErrorSistema):
    """Se presenta cuando no hay disponibilidad del servicio."""
    pass


class ReservaInvalidaError(ErrorSistema):
    """Se presenta cuando una reserva no puede realizarse."""
    pass


class OperacionNoPermitidaError(ErrorSistema):
    """Se presenta cuando una operación no está permitida."""
    pass


# ==========================================================
# 4. ENTIDAD GENERAL DEL SISTEMA
# ==========================================================

class EntidadSistema(ABC):
    """
    Clase abstracta que reúne información común
    de las entidades utilizadas en Software FJ.
    """

    def __init__(self, identificacion):
        if not isinstance(identificacion, (str, int)):
            raise DatosInvalidosError(
                "La identificación debe ser texto o número."
            )

        identificacion = str(identificacion).strip()

        if not identificacion or not identificacion.isalnum():
            raise DatosInvalidosError(
                "La identificación está vacía o contiene caracteres no válidos."
            )

        self._identificacion = identificacion

    @property
    def identificacion(self):
        """Permite consultar la identificación."""
        return self._identificacion

    @abstractmethod
    def mostrar_informacion(self):
        """Cada clase derivada debe definir este método."""
        pass


# ==========================================================
# 5. CLASE CLIENTE
# ==========================================================

class Cliente(EntidadSistema):
    """
    Representa a una persona que utiliza los servicios
    ofrecidos por la empresa Software FJ.
    """

    def __init__(self, identificacion, nombre, correo, telefono):
        super().__init__(identificacion)

        self.__nombre = self._validar_nombre(nombre)
        self.__correo = self._validar_correo(correo)
        self.__telefono = self._validar_telefono(telefono)

    def _validar_nombre(self, nombre):
        if not isinstance(nombre, str) or not nombre.strip():
            raise DatosInvalidosError(
                "El nombre del cliente es obligatorio."
            )

        nombre = nombre.strip()

        if not all(
            caracter.isalpha() or caracter.isspace()
            for caracter in nombre
        ):
            raise DatosInvalidosError(
                "El nombre solo debe contener letras y espacios."
            )

        return nombre

    def _validar_correo(self, correo):
        if not isinstance(correo, str):
            raise DatosInvalidosError(
                "El correo debe ser un texto."
            )

        correo = correo.strip()
        patron = r"^[\w.+-]+@[\w.-]+\.[A-Za-z]{2,}$"

        if not re.fullmatch(patron, correo):
            raise DatosInvalidosError(
                "El formato del correo electrónico no es válido."
            )

        return correo.lower()

    def _validar_telefono(self, telefono):
        if not isinstance(telefono, (str, int)):
            raise DatosInvalidosError(
                "El teléfono debe contener números."
            )

        telefono = str(telefono).strip()

        if not telefono.isdigit() or not 7 <= len(telefono) <= 15:
            raise DatosInvalidosError(
                "El teléfono debe tener entre 7 y 15 dígitos."
            )

        return telefono

    @property
    def nombre(self):
        return self.__nombre

    @property
    def correo(self):
        return self.__correo

    @property
    def telefono(self):
        return self.__telefono

    def mostrar_informacion(self):
        return (
            f"Identificación: {self.identificacion}\n"
            f"Nombre: {self.nombre}\n"
            f"Correo: {self.correo}\n"
            f"Teléfono: {self.telefono}"
        )


# ==========================================================
# 6. CLASE ABSTRACTA SERVICIO
# ==========================================================

class Servicio(ABC):
    """
    Clase base para los diferentes servicios de la empresa.
    Cada servicio define su costo, descripción y validación.
    """

    def __init__(self, codigo, nombre, tarifa, disponibles=1):
        if not isinstance(codigo, str) or not codigo.strip():
            raise DatosInvalidosError(
                "El código del servicio es obligatorio."
            )

        if not isinstance(nombre, str) or not nombre.strip():
            raise DatosInvalidosError(
                "El nombre del servicio es obligatorio."
            )

        if isinstance(tarifa, bool) or not isinstance(tarifa, (int, float)):
            raise DatosInvalidosError(
                "La tarifa debe ser numérica."
            )

        if tarifa <= 0:
            raise DatosInvalidosError(
                "La tarifa debe ser mayor que cero."
            )

        if isinstance(disponibles, bool) or not isinstance(disponibles, int):
            raise DatosInvalidosError(
                "La disponibilidad debe ser un número entero."
            )

        if disponibles < 0:
            raise DatosInvalidosError(
                "La disponibilidad no puede ser negativa."
            )

        self.codigo = codigo.strip()
        self.nombre = nombre.strip()
        self.tarifa = float(tarifa)
        self.disponibles = disponibles

    @abstractmethod
    def calcular_costo(self, duracion, impuesto=0, descuento=0):
        """Calcula el valor del servicio."""
        pass

    @abstractmethod
    def describir_servicio(self):
        """Devuelve una descripción del servicio."""
        pass

    @abstractmethod
    def validar_parametros(self, duracion):
        """Comprueba que los parámetros sean correctos."""
        pass


# ==========================================================
# 7. SERVICIO DE RESERVA DE SALAS
# ==========================================================

class ReservaSala(Servicio):

    def validar_parametros(self, duracion):
        if isinstance(duracion, bool) or not isinstance(duracion, (int, float)):
            raise DatosInvalidosError(
                "La duración de la sala debe ser numérica."
            )

        if duracion <= 0 or duracion > 12:
            raise DatosInvalidosError(
                "La reserva de sala debe ser mayor que cero y máximo 12 horas."
            )

    def calcular_costo(self, duracion, impuesto=0, descuento=0):
        self.validar_parametros(duracion)
        validar_condiciones_costo(impuesto, descuento)

        subtotal = self.tarifa * duracion
        return subtotal * (1 + impuesto / 100) * (1 - descuento / 100)

    def describir_servicio(self):
        return (
            f"Reserva de sala: {self.nombre}. "
            f"Tarifa por hora: ${self.tarifa:.2f}"
        )


# ==========================================================
# 8. SERVICIO DE ALQUILER DE EQUIPOS
# ==========================================================

class AlquilerEquipo(Servicio):

    def validar_parametros(self, duracion):
        if isinstance(duracion, bool) or not isinstance(duracion, int):
            raise DatosInvalidosError(
                "La duración del alquiler debe expresarse en días enteros."
            )

        if duracion <= 0 or duracion > 30:
            raise DatosInvalidosError(
                "El alquiler debe ser de 1 a 30 días."
            )

    def calcular_costo(self, duracion, impuesto=0, descuento=0):
        self.validar_parametros(duracion)
        validar_condiciones_costo(impuesto, descuento)

        subtotal = self.tarifa * duracion
        return subtotal * (1 + impuesto / 100) * (1 - descuento / 100)

    def describir_servicio(self):
        return (
            f"Alquiler de equipo: {self.nombre}. "
            f"Tarifa por día: ${self.tarifa:.2f}"
        )


# ==========================================================
# 9. SERVICIO DE ASESORÍAS ESPECIALIZADAS
# ==========================================================

class AsesoriaEspecializada(Servicio):

    def validar_parametros(self, duracion):
        if isinstance(duracion, bool) or not isinstance(duracion, int):
            raise DatosInvalidosError(
                "La duración de la asesoría debe expresarse en horas enteras."
            )

        if duracion <= 0 or duracion > 8:
            raise DatosInvalidosError(
                "La asesoría debe durar entre 1 y 8 horas."
            )

    def calcular_costo(self, duracion, impuesto=0, descuento=0):
        self.validar_parametros(duracion)
        validar_condiciones_costo(impuesto, descuento)

        subtotal = self.tarifa * duracion
        return subtotal * (1 + impuesto / 100) * (1 - descuento / 100)

    def describir_servicio(self):
        return (
            f"Asesoría especializada: {self.nombre}. "
            f"Tarifa por hora: ${self.tarifa:.2f}"
        )


# ==========================================================
# 10. VALIDACIÓN DE IMPUESTOS Y DESCUENTOS
# ==========================================================

def validar_condiciones_costo(impuesto, descuento):
    """
    Verifica que los porcentajes utilizados en los cálculos
    se encuentren dentro de un rango permitido.
    """

    for nombre, valor in (
        ("impuesto", impuesto),
        ("descuento", descuento)
    ):
        if isinstance(valor, bool) or not isinstance(valor, (int, float)):
            raise DatosInvalidosError(
                f"El {nombre} debe ser un valor numérico."
            )

        if not 0 <= valor <= 100:
            raise DatosInvalidosError(
                f"El {nombre} debe estar entre 0 y 100."
            )


# ==========================================================
# 11. CLASE RESERVA
# ==========================================================

class Reserva(EntidadSistema):
    """
    Relaciona un cliente con un servicio y controla
    el proceso de confirmación y cancelación.
    """

    def __init__(self, codigo, cliente, servicio, duracion):
        super().__init__(codigo)

        if not isinstance(cliente, Cliente):
            raise ClienteNoEncontradoError(
                "La reserva necesita un cliente válido."
            )

        if not isinstance(servicio, Servicio):
            raise ReservaInvalidaError(
                "La reserva necesita un servicio válido."
            )

        servicio.validar_parametros(duracion)

        self.cliente = cliente
        self.servicio = servicio
        self.duracion = duracion
        self.estado = "Pendiente"
        self.valor_total = 0

    def confirmar(self, impuesto=0, descuento=0):
        if self.estado != "Pendiente":
            raise OperacionNoPermitidaError(
                "Solo se pueden confirmar reservas pendientes."
            )

        if self.servicio.disponibles <= 0:
            raise ServicioNoDisponibleError(
                "No hay disponibilidad para el servicio solicitado."
            )

        self.valor_total = self.servicio.calcular_costo(
            self.duracion,
            impuesto,
            descuento
        )

        self.servicio.disponibles -= 1
        self.estado = "Confirmada"

        registrar_evento(
            f"Reserva {self.identificacion} confirmada."
        )

        return self.valor_total

    def cancelar(self):
        if self.estado != "Confirmada":
            raise OperacionNoPermitidaError(
                "Solo se pueden cancelar reservas confirmadas."
            )

        self.servicio.disponibles += 1
        self.estado = "Cancelada"

        registrar_evento(
            f"Reserva {self.identificacion} cancelada."
        )

    def procesar(self):
        if self.estado == "Pendiente":
            return self.confirmar()

        if self.estado == "Confirmada":
            return self.valor_total

        raise OperacionNoPermitidaError(
            "No se puede procesar una reserva cancelada."
        )

    def mostrar_informacion(self):
        return (
            f"Reserva: {self.identificacion}\n"
            f"Cliente: {self.cliente.nombre}\n"
            f"Servicio: {self.servicio.nombre}\n"
            f"Duración: {self.duracion}\n"
            f"Estado: {self.estado}\n"
            f"Valor: ${self.valor_total:.2f}"
        )


# ==========================================================
# 12. LISTAS INTERNAS DEL SISTEMA
# ==========================================================

clientes_registrados = []
servicios_registrados = []
reservas_registradas = []


def registrar_cliente(cliente):
    if not isinstance(cliente, Cliente):
        raise TypeError("El objeto no corresponde a un cliente.")

    for registrado in clientes_registrados:
        if registrado.identificacion == cliente.identificacion:
            raise DatosInvalidosError(
                "Ya existe un cliente con esa identificación."
            )

    clientes_registrados.append(cliente)
    registrar_evento(f"Cliente {cliente.identificacion} registrado.")


def registrar_servicio(servicio):
    if not isinstance(servicio, Servicio):
        raise TypeError("El objeto no corresponde a un servicio.")

    for registrado in servicios_registrados:
        if registrado.codigo == servicio.codigo:
            raise DatosInvalidosError(
                "Ya existe un servicio con ese código."
            )

    servicios_registrados.append(servicio)
    registrar_evento(f"Servicio {servicio.codigo} registrado.")


def registrar_reserva(reserva):
    if not isinstance(reserva, Reserva):
        raise TypeError("El objeto no corresponde a una reserva.")

    for registrada in reservas_registradas:
        if registrada.identificacion == reserva.identificacion:
            raise ReservaInvalidaError(
                "Ya existe una reserva con ese código."
            )

    reservas_registradas.append(reserva)
    registrar_evento(f"Reserva {reserva.identificacion} creada.")


# ==========================================================
# 13. BÚSQUEDA DE CLIENTES Y SERVICIOS
# ==========================================================

def buscar_cliente(identificacion):
    for cliente in clientes_registrados:
        if cliente.identificacion == str(identificacion):
            return cliente

    raise ClienteNoEncontradoError(
        "No se encontró el cliente solicitado."
    )


def buscar_servicio(codigo):
    for servicio in servicios_registrados:
        if servicio.codigo == codigo:
            return servicio

    raise ServicioNoDisponibleError(
        "No se encontró el servicio solicitado."
    )


# ==========================================================
# 14. ENCADENAMIENTO DE EXCEPCIONES
# ==========================================================

def convertir_identificacion(valor):
    """
    Ejemplo de encadenamiento: si falla la conversión,
    se genera una excepción propia conservando el error original.
    """
    try:
        identificacion = int(valor)
    except ValueError as error:
        raise DatosInvalidosError(
            "No fue posible convertir la identificación a número."
        ) from error

    return identificacion


# ==========================================================
# 15. FUNCIÓN GENERAL PARA EJECUTAR SIMULACIONES
# ==========================================================

def ejecutar_prueba(numero, descripcion, operacion):
    print("\n" + "=" * 65)
    print(f"SIMULACIÓN {numero}: {descripcion}")

    try:
        operacion()

    except ErrorSistema as error:
        registrar_error(f"Simulación {numero}: {error}")
        print("Error controlado:", error)

    except (TypeError, ValueError) as error:
        registrar_excepcion(f"Simulación {numero}: error de datos.")
        print("Error de datos:", error)

    except Exception as error:
        registrar_excepcion(f"Simulación {numero}: error inesperado.")
        print("Error inesperado:", error)

    else:
        registrar_evento(f"Simulación {numero} terminada correctamente.")
        print("Resultado: operación realizada correctamente.")

    finally:
        registrar_evento(f"Finalización de simulación {numero}.")
        print("Finalizó la simulación.")


# ==========================================================
# 16. FUNCIONES PARA LAS DIEZ SIMULACIONES
# ==========================================================

def prueba_01_cliente_valido():
    cliente = Cliente("1001", "María López", "maria@gmail.com", "3001234567")
    registrar_cliente(cliente)
    print(cliente.mostrar_informacion())


def prueba_02_cliente_invalido():
    cliente = Cliente("", "Carlos Pérez", "carlos@gmail.com", "3001234567")
    registrar_cliente(cliente)


def prueba_03_cliente_duplicado():
    cliente = Cliente("1001", "María López", "maria@gmail.com", "3001234567")
    registrar_cliente(cliente)


def prueba_04_servicio_sala():
    sala = ReservaSala("S001", "Sala de reuniones", 50000, 2)
    registrar_servicio(sala)
    print(sala.describir_servicio())


def prueba_05_servicio_equipo():
    equipo = AlquilerEquipo("E001", "Computador portátil", 80000, 3)
    registrar_servicio(equipo)
    print(equipo.describir_servicio())


def prueba_06_servicio_asesoria():
    asesoria = AsesoriaEspecializada("A001", "Asesoría tecnológica", 100000, 2)
    registrar_servicio(asesoria)
    print(asesoria.describir_servicio())


def prueba_07_reserva_exitosa():
    cliente = buscar_cliente("1001")
    servicio = buscar_servicio("S001")
    reserva = Reserva("R001", cliente, servicio, 2)
    registrar_reserva(reserva)
    valor = reserva.confirmar(impuesto=19, descuento=10)
    print(reserva.mostrar_informacion())
    print(f"Total de la reserva: ${valor:.2f}")


def prueba_08_servicio_no_disponible():
    servicio = ReservaSala("S002", "Sala ocupada", 60000, 0)
    cliente = buscar_cliente("1001")
    reserva = Reserva("R002", cliente, servicio, 1)
    registrar_reserva(reserva)
    reserva.confirmar()


def prueba_09_reserva_duracion_invalida():
    cliente = buscar_cliente("1001")
    servicio = buscar_servicio("S001")
    reserva = Reserva("R003", cliente, servicio, -5)
    registrar_reserva(reserva)


def prueba_10_cancelar_reserva():
    reserva_confirmada = next(
        (r for r in reservas_registradas if r.estado == "Confirmada"),
        None
    )
    if reserva_confirmada is None:
        raise OperacionNoPermitidaError("No hay reservas confirmadas para cancelar.")

    reserva_confirmada.cancelar()
    print(reserva_confirmada.mostrar_informacion())


# ==========================================================
# 17. EJECUCIÓN PRINCIPAL DEL SISTEMA
# ==========================================================

def iniciar_sistema():
    print("=" * 65)
    print("SISTEMA INTEGRAL DE GESTIÓN - SOFTWARE FJ")
    print("=" * 65)

    registrar_evento("Inicio del sistema Software FJ.")

    pruebas = [
        (1, "Registro de cliente válido", prueba_01_cliente_valido),
        (2, "Registro con identificación vacía", prueba_02_cliente_invalido),
        (3, "Registro de cliente duplicado", prueba_03_cliente_duplicado),
        (4, "Creación de servicio de sala", prueba_04_servicio_sala),
        (5, "Creación de servicio de equipo", prueba_05_servicio_equipo),
        (6, "Creación de servicio de asesoría", prueba_06_servicio_asesoria),
        (7, "Creación y confirmación de reserva", prueba_07_reserva_exitosa),
        (8, "Intento de reservar un servicio no disponible", prueba_08_servicio_no_disponible),
        (9, "Creación de reserva con duración inválida", prueba_09_reserva_duracion_invalida),
        (10, "Cancelación de reserva confirmada", prueba_10_cancelar_reserva)
    ]

    for numero, descripcion, operacion in pruebas:
        ejecutar_prueba(numero, descripcion, operacion)

    print("\n" + "=" * 65)
    print("PRUEBA ADICIONAL: ENCADENAMIENTO DE EXCEPCIONES")

    try:
        convertir_identificacion("texto incorrecto")
    except DatosInvalidosError as error:
        registrar_error(
            f"Error de conversión de identificación: {error} | Causa original: {error.__cause__}"
        )
        print("Error controlado:", error)
        print("Causa original:", error.__cause__)

    registrar_evento("Finalización del sistema Software FJ.")

    print("\nSistema finalizado.")
    print(f"Los eventos y errores se encuentran en {RUTA_LOG}.")


# ==========================================================
# 18. PUNTO DE ENTRADA DEL PROGRAMA
# ==========================================================

if __name__ == "__main__":
    iniciar_sistema()