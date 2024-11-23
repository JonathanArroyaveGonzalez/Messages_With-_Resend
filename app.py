from flask import Flask, render_template, request, redirect, url_for
import paho.mqtt.client as mqtt
import os
import threading
from dotenv import load_dotenv
from jinja2 import Environment, FileSystemLoader
import resend
from pathlib import Path

app = Flask(__name__)

# Load environment variables
load_dotenv()
resend.api_key = os.getenv("API_KEY_RESEND")

# MQTT setup
mqtt_broker = 'broker.hivemq.com'  # Use a free MQTT broker
mqtt_port = 1883
mqtt_topic = 'user/registration'

client = mqtt.Client()

# Configure Jinja2 for templates
templates_dir = Path(__file__).parent / 'templates'
env = Environment(loader=FileSystemLoader(templates_dir))

def send_welcome_email(to_email, user_name):
    # Get the template
    template = env.get_template('welcome.html')
    
    # Render the template with dynamic data
    html_content = template.render(
        user_name=user_name,
        year=2024,
        company_name="Universidad de Caldas",
        to_email=to_email,
        token="Hkxvsadewad",
    )
    
    # Send the email
    try:
        result = resend.Emails.send({
            "from": "onboarding@resend.dev",
            #"from": "arroyave3000g@gmail.com",
            "to": to_email,
            "subject": "¡Bienvenido!",
            "html": html_content
        })
        print(f"Email sent successfully: {result}")
        return result
    except Exception as e:
        print(f"Error sending email: {e}")
        return None

@app.route('/')
def index():
    return render_template('register.html')

@app.route('/register', methods=['POST'])
def register():
    username = request.form['username']
    email = request.form['email']

    # Publish to MQTT
    client.publish(mqtt_topic, f'{username},{email}')

    # Send email
    send_welcome_email(email, username)

    return redirect(url_for('index'))

# MQTT worker to handle user registration messages
def registration_worker():
    def on_message(client, userdata, message):
        # Process the registration message
        payload = message.payload.decode('utf-8')
        username, email = payload.split(',')
        print(f"Received registration for {username} with email {email}")
        # Here you can add additional processing if needed

    client.message_callback_add(mqtt_topic, on_message)
    client.subscribe(mqtt_topic)

# Connect and keep MQTT active in a separate thread
def start_mqtt():
    client.connect(mqtt_broker, mqtt_port, 60)
    client.loop_forever()

# Start the registration worker in a separate thread to listen for MQTT messages
threading.Thread(target=registration_worker, daemon=True).start()
threading.Thread(target=start_mqtt, daemon=True).start()

if __name__ == '__main__':
    app.run(debug=True)