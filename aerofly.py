import streamlit as st
from datetime import datetime

# Clases
class Aerolinea:
    def __init__(self, nombre):
        self.nombre = nombre
        if "destinos" not in st.session_state:
            st.session_state.destinos = [
            "Albania", "Alemania", "Andorra", "Austria", "Bélgica", "Bielorrusia",
            "Bosnia y Herzegovina",  "Bulgaria",  "Chequia", "Chipre",  "Croacia",
            "Dinamarca",   "Eslovaquia",     "Eslovenia",   "España",   "Estonia",
            "Finlandia",   "Francia",    "Gran Bretaña",    "Grecia",   "Holanda",
            "Hungría",     "Italia",     "Irlanda",       "Islandia",   "Letonia",
            "Liechtenstein",   "Lituania",  "Luxemburgo", "Macedonia", "Moldavia",
            "Malta",   "Mónaco",   "Noruega",  "Polonia",   "Portugal", "Rumania",
            "Rusia",   "San Marino",  "Serbia y Montenegro",   "Suecia",  "Suiza",
            "Ucrania" ] # Destinos predefinidos
        if "vuelos" not in st.session_state:
            st.session_state.vuelos = []
        if "reservas" not in st.session_state:
            st.session_state.reservas = []
        self.horarios_salida = ["5:00 AM", "8:00 PM"]
        self.dias_salida = [0, 2, 4]  # Lunes=0, Miércoles=2, Viernes=4

    def agregar_destino(self, destino):
        if destino not in st.session_state.destinos:
            st.session_state.destinos.append(destino)
            st.success(f"Destino {destino} agregado correctamente.")
        else:
            st.warning(f"El destino {destino} ya existe.")

    def eliminar_destino(self, destino):
        if destino in st.session_state.destinos:
            st.session_state.destinos.remove(destino)
            st.success(f"Destino {destino} eliminado correctamente.")
        else:
            st.warning(f"El destino {destino} no existe.")

    def mostrar_destinos(self):
        return st.session_state.destinos

    def crear_vuelo(self, destino, fecha_salida, hora_salida, numero_vuelo, asientos_disponibles):
        if destino not in st.session_state.destinos:
            st.warning(f"El destino {destino} no está disponible.")
            return
        if hora_salida not in self.horarios_salida:
            st.warning(f"El horario {hora_salida} no es válido.")
            return
        dia_semana = fecha_salida.weekday()  # 0=Lunes, 1=Martes, ..., 6=Domingo
        if dia_semana not in self.dias_salida:
            st.warning(f"El día {fecha_salida.strftime('%A')} no es válido. Los vuelos solo salen los Lunes, Miércoles y Viernes.")
            return
        vuelo = Vuelo(destino, fecha_salida, hora_salida, numero_vuelo, asientos_disponibles)
        st.session_state.vuelos.append(vuelo)
        st.success(f"Vuelo {numero_vuelo} creado correctamente.")

    def buscar_vuelos(self, destino, fecha):
        vuelos_disponibles = []
        for vuelo in st.session_state.vuelos:
            if vuelo.destino == destino and vuelo.fecha_salida.date() == fecha.date():
                vuelos_disponibles.append(vuelo)
        return vuelos_disponibles

    def agregar_reserva(self, reserva):
        st.session_state.reservas.append(reserva)
        st.success(f"Reserva {reserva.codigo_reserva} creada correctamente.")

    def eliminar_reserva(self, codigo_reserva):
        for reserva in st.session_state.reservas:
            if reserva.codigo_reserva == codigo_reserva:
                # Liberar el asiento en el vuelo correspondiente
                reserva.vuelo.cancelar_reserva(reserva.pasajero)
                st.session_state.reservas.remove(reserva)
                st.success(f"Reserva {codigo_reserva} eliminada correctamente.")
                return
        st.warning(f"No se encontró una reserva con el código {codigo_reserva}.")

    def mostrar_reservas(self):
        return st.session_state.reservas

class Vuelo:
    def __init__(self, destino, fecha_salida, hora_salida, numero_vuelo, asientos_disponibles):
        self.destino = destino
        self.fecha_salida = fecha_salida
        self.hora_salida = hora_salida
        self.numero_vuelo = numero_vuelo
        self.asientos_disponibles = asientos_disponibles
        self.pasajeros = []

    def reservar_asiento(self, pasajero):
        if self.asientos_disponibles > 0:
            self.pasajeros.append(pasajero)
            self.asientos_disponibles -= 1
            return True
        else:
            return False

    def cancelar_reserva(self, pasajero):
        if pasajero in self.pasajeros:
            self.pasajeros.remove(pasajero)
            self.asientos_disponibles += 1
            return True
        else:
            return False

    def mostrar_info(self):
        return f"Vuelo {self.numero_vuelo} a {self.destino} el {self.fecha_salida.strftime('%Y-%m-%d')} a las {self.hora_salida}. Asientos disponibles: {self.asientos_disponibles}"

class Pasajero:
    def __init__(self, nombre, pasaporte, contacto):
        self.nombre = nombre
        self.pasaporte = pasaporte
        self.contacto = contacto

    def mostrar_info(self):
        return f"Pasajero: {self.nombre}, Pasaporte: {self.pasaporte}, Contacto: {self.contacto}"

class Reserva:
    def __init__(self, pasajero, vuelo, asientos_reservados, codigo_reserva):
        self.pasajero = pasajero
        self.vuelo = vuelo
        self.asientos_reservados = asientos_reservados
        self.codigo_reserva = codigo_reserva

    def mostrar_info(self):
        return f"Reserva {self.codigo_reserva}: {self.pasajero.nombre} en el vuelo {self.vuelo.numero_vuelo} con {self.asientos_reservados} asientos."

# Interfaz de Streamlit
def main():
    st.title("Sistema de Gestión de Reservas de AeroFly")

    if "aerolinea" not in st.session_state:
        st.session_state.aerolinea = Aerolinea("AeroFly")

    aerolinea = st.session_state.aerolinea

    menu = st.sidebar.selectbox("Menú", [ "Crear Vuelo", "Buscar Vuelos", "Reservar Vuelo", "Mostrar Reservas", "Eliminar Reserva"])

    if menu == "Crear Vuelo":
        destino = st.selectbox("Seleccione el destino:", aerolinea.mostrar_destinos())
        fecha_salida = st.date_input("Seleccione la fecha de salida:")
        hora_salida = st.selectbox("Seleccione la hora de salida:", aerolinea.horarios_salida)
        numero_vuelo = st.text_input("Ingrese el número de vuelo:")
        asientos_disponibles = st.number_input("Ingrese el número de asientos disponibles:", min_value=1)
        if st.button("Crear Vuelo"):
            aerolinea.crear_vuelo(destino, datetime.combine(fecha_salida, datetime.strptime(hora_salida, "%I:%M %p").time()), hora_salida, numero_vuelo, asientos_disponibles)

    elif menu == "Buscar Vuelos":
        destino = st.selectbox("Seleccione el destino:", aerolinea.mostrar_destinos())
        fecha = st.date_input("Seleccione la fecha:")
        if st.button("Buscar Vuelos"):
            vuelos_disponibles = aerolinea.buscar_vuelos(destino, datetime.combine(fecha, datetime.min.time()))
            if vuelos_disponibles:
                for vuelo in vuelos_disponibles:
                    st.write(vuelo.mostrar_info())
            else:
                st.warning("No hay vuelos disponibles para la fecha y destino seleccionados.")

    elif menu == "Reservar Vuelo":
        st.header("Reservar Vuelo")
        nombre = st.text_input("Nombre del pasajero:")
        pasaporte = st.text_input("Número de pasaporte:")
        contacto = st.text_input("Información de contacto:")
        destino = st.selectbox("Seleccione el destino:", aerolinea.mostrar_destinos())
        fecha = st.date_input("Seleccione la fecha:")
        if st.button("Buscar Vuelos para Reservar"):
            vuelos_disponibles = aerolinea.buscar_vuelos(destino, datetime.combine(fecha, datetime.min.time()))
            if vuelos_disponibles:
                st.session_state.vuelos_disponibles = vuelos_disponibles
            else:
                st.warning("No hay vuelos disponibles para la fecha y destino seleccionados.")

        if "vuelos_disponibles" in st.session_state:
            vuelo_seleccionado = st.selectbox("Seleccione el vuelo:", [vuelo.mostrar_info() for vuelo in st.session_state.vuelos_disponibles])
            if st.button("Reservar Vuelo"):
                pasajero = Pasajero(nombre, pasaporte, contacto)
                vuelo = st.session_state.vuelos_disponibles[[vuelo.mostrar_info() for vuelo in st.session_state.vuelos_disponibles].index(vuelo_seleccionado)]
                if vuelo.reservar_asiento(pasajero):
                    codigo_reserva = f"RES-{len(st.session_state.reservas) + 1}"
                    reserva = Reserva(pasajero, vuelo, 1, codigo_reserva)
                    aerolinea.agregar_reserva(reserva)
                else:
                    st.warning("No hay asientos disponibles en este vuelo.")

    elif menu == "Mostrar Reservas":
        st.header("Reservas Realizadas")
        reservas = aerolinea.mostrar_reservas()
        if reservas:
            for reserva in reservas:
                st.write(reserva.mostrar_info())
        else:
            st.warning("No hay reservas realizadas.")

    elif menu == "Eliminar Reserva":
        st.header("Eliminar Reserva")
        codigo_reserva = st.text_input("Ingrese el código de reserva:")
        if st.button("Eliminar Reserva"):
            aerolinea.eliminar_reserva(codigo_reserva)

if __name__ == "__main__":
    main()

!npm install localtunnel

!streamlit run /content/app.py &>/content/logs.txt &

!npx localtunnel --port 8501
