from django.core.mail import send_mail

def send_reset_email(data):
    subject = data.get('subject')
    body = data.get('body')
    to_email = data.get('to_email')

    send_mail(
        subject,
        body,
        'mubeenjutt9757@gmail.com',  # Replace with your actual sender email
        [to_email],
        fail_silently=False,
    )