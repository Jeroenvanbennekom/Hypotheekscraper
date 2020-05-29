import os
import smtplib
from email.message import EmailMessage

#Credentials go here
mail_user = os.environ.get('EMAIL_USER')
mail_password = os.environ.get('EMAIL_PASS')

#Mail input goes here
recipients = mail_user
attachments = ['testplaatje.gif', 'testmail.pdf', 'test.csv']

subject = 'Testmail'
sender = mail_user
content = 'Hallo, hierbij de begeleidende tekst van de mail.'
html_content = r"""<!DOCTYPE html>
<html >
<head>
  <meta charset="UTF-8">
  <title>Een mooie mail van Jeroen</title>
</head>

<body>
  <!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">
Hallo, hier heb je een mooie mail.   
  </body>

</html>"""

#Attachment helper info goes here
image_filetypes = ['.jpg', '.jpeg', '.png', '.gif', '.tiff']
doc_filetypes = ['.docx', '.doc', '.xlsx', '.xlsm', '.xls', '.pdf', '.csv']

def create_email():
	msg = EmailMessage()
	msg['Subject'] = subject
	msg['From'] = mail_user
	msg['To'] = {", ".join(recipients)}
	msg.set_type('text/html')
	msg.set_content(content)
	msg.add_alternative(html_content, subtype="html")

	for attachment in attachments:
		filename, file_extension = os.path.splitext(attachment)
		if file_extension in image_filetypes:
			maintype = 'image'
			subtype = 'gif'
		elif file_extension in doc_filetypes:
			maintype = 'application'
			subtype = 'octet-stream'
		else:
			print('something is wrong. File_extension could not be identified.')
		with open(attachment, 'rb') as f:
			file_data = f.read()
		msg.add_attachment(file_data, maintype = maintype, subtype = subtype, filename = filename+file_extension)
	return msg

def send_mail():
	try:
		with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
			smtp.login(mail_user, mail_password)
			smtp.send_message(create_email())
			smtp.close()
	except: 
		print('Something went wrong with sending an e-mail')
