import os
import ipaddress
import smtplib
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from pathlib import Path


# Configurações do e-mail
EMAIL_REMETENTE = 'seu-endereco@seu-provedor.com.'
SENHA = 'seu-password'
EMAIL_DESTINATARIO = 'email-destinario@provedor.com'
SMTP_SERVER = 'smtp-do-envio.com' # exemplo gmail: smtp.gmail.com
SMTP_PORT = 587

hour = datetime.now().time()
hour_adjust = hour.strftime('%H:%M:%S')

# Arquivo de saída
arquivo_ip_mail = 'ip_ativo.txt'
arquivo_status = 'status_rede.txt'
arquivo_powershell = 'ip_ps.txt'

current = Path(__file__).parent
os.chdir(current)


# Função para verificar se o host está ativo
def is_host_active(ip):
    response = os.system(f'ping -n 1 -w 1000 {ip} > nul')
    return response == 0

# Rede a ser verificada
rede = ipaddress.ip_network('192.168.5.0/24')

# Abrir os arquivos em modo de escrita
with open(arquivo_ip_mail, 'w') as f_ip, open(arquivo_status, 'w') as f_status, open(arquivo_powershell, 'w') as f_ps:
    active = 0
    deactive = 0
    for ip in rede:
        if is_host_active(ip):
            active += 1
            f_ip.write(f'{ip}\n')
            f_ps.write(f'{ip}\n')
        else:
            deactive += 1
        status = f'IP: {ip}'
        print(status)
        f_status.write(f'{status}\n')
    resumo_all = f'\nAll List IPs...\n\nActive ip: {active}\nDeactive ip: {deactive}\nTime: {hour_adjust}'
    resumo_ip_active = f'\nOnly Active IPs...\n\nActive ip: {active}\nDeactive ip: {deactive}\nTime: {hour_adjust}'
    print(resumo_all)
    f_ip.write(resumo_ip_active)

# Função para enviar e-mail
def enviar_email(assunto, mensagem, destinatario, anexo):
    remetente = EMAIL_REMETENTE
    senha = SENHA

    # Configuração do e-mail
    email = MIMEMultipart()
    email["From"] = remetente
    email["To"] = destinatario
    email["Subject"] = assunto
    email.attach(MIMEText(mensagem, "plain"))

    # Anexar arquivo
    with open(anexo, "rb") as attachment:
        part = MIMEBase("application", "octet-stream")
        part.set_payload(attachment.read())
        encoders.encode_base64(part)
        part.add_header("Content-Disposition", f"attachment; filename= {anexo}")
        email.attach(part)

    # Enviar o e-mail
    try:
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(remetente, senha)
        server.sendmail(remetente, destinatario, email.as_string())
        server.quit()
        print("E-mail enviado com sucesso!")
    except Exception as e:
        print(f"Erro ao enviar e-mail: {e}")

# Enviar o e-mail com o relatório
enviar_email(
    assunto="Relatório de Status da Rede",
    mensagem="O relatório de status da rede com os IPs ativos está em anexo.",
    destinatario=EMAIL_DESTINATARIO,
    anexo=arquivo_ip_mail
)
