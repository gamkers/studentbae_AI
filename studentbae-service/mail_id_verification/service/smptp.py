from service.hostinger import SMTPHostinger

def send_verification_email(email, token):
    verification_link = f'http://127.0.0.1:5001/verify_email/{token}'
    
    subject = 'Please Confirm Your Email Address'
    body = f'Click the following link to verify your email address: {verification_link}'
    
    
    try:
        smtp = SMTPHostinger()
        smtp.auth("support@studentbae.in", "Idm@Isac@1853@", "smtp.hostinger.com", 465, False)
        smtp.send(email, "support@studentbae.in", subject, body)
    except Exception as e:
        print(f"Failed to send email: {e}")
