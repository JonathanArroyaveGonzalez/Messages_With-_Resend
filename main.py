import resend
from dotenv import load_dotenv
import os
from pathlib import Path
from jinja2 import Environment, FileSystemLoader

load_dotenv()
resend.api_key = os.getenv("API_KEY_RESEND")

# Configurar Jinja2 para los templates
templates_dir = Path(__file__).parent / 'templates'
env = Environment(loader=FileSystemLoader(templates_dir))

def send_welcome_email(to_email, user_name):
    # Obtener el template
    template = env.get_template('welcome.html')
    
    # Renderizar el template con datos dinámicos
    html_content = template.render(
        user_name=user_name,
        year=2024,
        company_name="Universidad de caldas",
        to_email=to_email,
        token="Hkxvsadewad",
    )
    
    # Enviar el email
    try:
        result = resend.Emails.send({
            "from": "onboarding@resend.dev",
            "to": to_email,
            "subject": "¡Bienvenido!",
            "html": html_content
        })
        print(f"Email enviado exitosamente: {result}")
        return result
    except Exception as e:
        print(f"Error al enviar el email: {e}")
        return None

# Uso
if __name__ == "__main__":
    send_welcome_email("arroyave3000g@gmail.com", "Juan")
