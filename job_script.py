import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
import PyPDF2

# Встановіть дані для підключення до SMTP-сервера
smtp_server = 'smtp.gmail.com'
smtp_port = 587
smtp_username = 'your_smtp_username'
smtp_password = 'your_smtp_password'

# Шлях до резюме у форматі PDF
resume_path = 'B:\script smtp\CV Hordiienko Yelyzaveta.pdf'

# Шлях до текстового файлу змісту листа електронної пошти
email_content_path = 'B:\script smtp\letter.txt'

# Список компаній, куди потрібно відправити резюме
company_list = ['Company@gmail.com']

# Зчитуємо вміст резюме з PDF-файлу
with open(resume_path, 'rb') as resume_file:
    pdf_reader = PyPDF2.PdfReader(resume_file)
    resume_content = ''
    for page in range(len(pdf_reader.pages)):
        resume_content += pdf_reader.pages[page].extract_text()

# Зчитуємо вміст текстового файлу змісту листа електронної пошти
with open(email_content_path, 'r', encoding='utf-8') as email_content_file:
    email_content = email_content_file.read()

# Відправляємо лист до кожної компанії зі списку
for company_email in company_list:
    # Створюємо об'єкт листа
    message = MIMEMultipart()
    message['From'] = smtp_username
    message['To'] = company_email
    message['Subject'] = 'Job Application QA Engineer'

    # Додаємо текст листа
    message.attach(MIMEText(email_content, 'plain', 'utf-8'))

    # Додаємо резюме як вкладений файл
    resume_attachment = MIMEApplication(open(resume_path, 'rb').read())
    resume_attachment.add_header('Content-Disposition', 'attachment', filename='CV Hordiienko Yelyzaveta.pdf')
    message.attach(resume_attachment)

    # Встановлюємо з'єднання з SMTP-сервером
    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(smtp_username, smtp_password)
        
        # Відправляємо лист
        server.sendmail(smtp_username, company_email, message.as_string())

    print(f'Resume sent to {company_email}')

print('All resumes have been sent.')