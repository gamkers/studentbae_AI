
import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

class SMTPHostinger:
	"""
	SMTP module for Hostinger emails
	"""

	def auth(self, user: str, password: str, host: str, port: int, debug: bool = False):
		"""
		Authenticates a session

		Args:
			user (str): username
			password (str): password
			host (str): server hostname
			port (int): port number
			debug (bool): enables or disables logging

		Returns:
			bool: True if successful, False if otherwise

		Todo:
			Better exception handling
		"""

		self.user = user
		self.password = password
		self.host = host
		self.port = port

		context = ssl.create_default_context()

		self.conn = smtplib.SMTP_SSL(host, port, context=context)
		self.conn.set_debuglevel(debug)

		try:
			self.conn.login(user, password)
		except smtplib.SMTPAuthenticationError:
			return False
		except:
			return False

	def send(self, recipient: str, sender: str, subject: str, message: str):
		"""
		Sends an email to the specified recipient 

		Args:
			recipient (str): recipient of the email
			sender (str): sender of the email
			subject (str): subject of the email
			message (str): email body

		Returns:
			bool: True if successful, False otherwise

		Todo:
			Better exception handling
		"""

		raw = MIMEText(message)
		raw["Subject"] = subject
		raw["From"] = sender
		raw["To"] = recipient

		if self.conn:
			try:
				self.conn.sendmail(sender, recipient, raw.as_string())
			except:
				return False
			return True
		else:
			return False

smtp = SMTPHostinger()
smtp.auth("support@studentbae.in", "Idm@Isac@1853@", "smtp.hostinger.com", 465, False)
smtp.send("gamkersofficial@gmail.com", "support@studentbae.in", "This means that emails work", "Message body...")