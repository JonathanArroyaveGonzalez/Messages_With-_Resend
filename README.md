# **Sistema de Envío de Correos de Bienvenida**

Este proyecto es una aplicación de envío automatizado de correos electrónicos para dar la bienvenida a nuevos usuarios registrados. Utiliza **MQTT** como sistema de encolamiento de mensajes para gestionar registros y **Resend** como servicio de envío de correos electrónicos.

---

## **Características**
- **Registro de usuarios**: Los datos de los usuarios (nombre, correo, credenciales) se publican en un tema MQTT.
- **MQTT como encolador**: 
  - Un cliente suscrito al tema `user/registration` recibe los datos en tiempo real.
- **Correos de bienvenida automáticos**: 
  - Se envía un correo personalizado con las credenciales del usuario usando Jinja para gestionar los templates personalizados.
- **Plantilla de correo**: Incluye un saludo, credenciales de acceso, e instrucciones iniciales.

---

## **Tecnologías Utilizadas**
- **Python**: Lenguaje principal del proyecto.
- **MQTT (paho-mqtt)**: Para encolar los mensajes de registro.
- **Resend**: Servicio para enviar correos electrónicos.
- **JSON**: Para estructurar los datos de los mensajes.

---

## **Requisitos**
Antes de ejecutar el proyecto, asegúrate de tener:
1. **Python 3.8+** instalado.
2. Instalar las dependencias del proyecto:
   ```bash
   pip install -r requirements.txt
3. Una cuenta en [Resend](https://resend.com/onboarding) con una API Key válida.

---

## **Configuración**
1. Clonar el repositorio:
```bash
    git clone https://github.com/JonathanArroyaveGonzalez/Messages_With-_Resend.git
    cd MESSAGESMQTT
```


2. Configurar la API Key de Resend:
    - Reemplaza "your_resend_api_key" en el archivo principal con tu API Key de Resend.

3. Configurar el broker MQTT:

    - Si usas un broker distinto de broker.hivemq.com, actualiza la dirección y el puerto en la función mqtt_client.connect().

---

## **Ejecución**
1. Inicia la aplicación:

    ```bash
    python app.py

2. Publica un mensaje en el tema MQTT user/registration con los datos de un usuario. Ejemplo de payload:
    ```json
    {
        "name": "John Doe",
        "email": "johndoe@example.com",
        "username": "johndoe123",
        "password": "securepassword123"
    }
3. Verifica el correo del usuario para confirmar que recibió el mensaje de bienvenida.

## **Estructura del Proyecto**

    ```bash
    .
    ├── main.py               # Archivo principal del proyecto
    ├── requirements.txt      # Dependencias del proyecto
    ├── templates/            # Carpeta de plantillas HTML de jinja
    │   ├── welcome.html      # Plantilla del correo de bienvenida
    └── README.md             # Descripción del proyecto
