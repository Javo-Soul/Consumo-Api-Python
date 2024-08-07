import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

import os
from airflow.models import Variable, TaskInstance
from airflow.utils.email import send_email_smtp
from airflow.utils.log.logging_mixin import LoggingMixin

###########################################################################
def body_mail():
    resumen = ['resultado']
    texto   = ['Aca deberia decir si esta OK']

    texts = [
        f'Pais {resumen} ({texto})'
        for country, acronym in zip(resumen, texto)
    ]

    return '\n'.join(texts)

###########################################################################
def get_log_file_path(task_instance):
    """
    Get the log file path for a given task instance.
    
    Args:
    - task_instance (TaskInstance): The task instance for which to get the log file path.
    
    Returns:
    - str: The path of the log file.
    """
    log_base_dir = task_instance.log_url.replace('file://', '')

    if os.path.exists(log_base_dir):
        return log_base_dir
    return "No log file found."

###########################################################################
def send_email(**context):
    subject = context["var"]["value"].get("subject_mail")
    from_address = context["var"]["value"].get("email")
    password = context["var"]["value"].get("email_password")
    to_address = context["var"]["value"].get("to_address")

    # Create a MIMEText object
    msg = MIMEMultipart()
    msg['From'] = from_address
    msg['To'] = to_address
    msg['Subject'] = subject

    # Attach the body with the msg instance
    msg.attach(MIMEText(body_mail(), 'plain'))

    print(
    f"""
    subject:    {subject}
    from_address:   {from_address}
    password:   {password}
    to_address: {to_address}
    """
    )

    try:
        # Create an SMTP session
        server = smtplib.SMTP('smtp.gmail.com', 587)  # Use your SMTP server and port
        server.starttls()  # Enable security

        # Login to the server
        server.login(from_address, password)

        # Send the email
        text = msg.as_string()
        server.sendmail(from_address, to_address, text)
        server.quit()
        print("Email sent successfully")
    except Exception as e:
        print(f"Failed to send email: {str(e)}")

