import os
import ipaddress
import smtplib
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from pathlib import Path
from dotenv import load_dotenv


# Configurações do e-mail
load_dotenv()

EMAIL_REMETENTE = os.getenv('EMAIL_REMETENTE', '')
SENHA = os.getenv('SENHA', '')
EMAIL_DESTINATARIO = os.getenv('EMAIL_DESTINATARIO', '')
SMTP_SERVER = os.getenv('SMTP_SERVER', '')
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
redes = [ipaddress.ip_network('192.168.4.0/24'), ipaddress.ip_network('192.168.5.0/24')]
# Rede a ser ignorada
ip_ignore = [ipaddress.ip_address(ip) for ip in [
    "192.168.4.1", "192.168.4.9", "192.168.4.13", "192.168.4.21", "192.168.4.22", "192.168.4.23", "192.168.4.25", "192.168.4.26",
    "192.168.4.27", "192.168.4.28", "192.168.4.29", "192.168.4.30", "192.168.4.32", "192.168.4.33", "192.168.4.34", "192.168.4.37", "192.168.4.38",
    "192.168.4.39", "192.168.4.42", "192.168.4.43", "192.168.4.44", "192.168.4.46", "192.168.4.47", "192.168.4.48", "192.168.4.50", "192.168.4.52",
    "192.168.4.55", "192.168.4.56", "192.168.4.61", "192.168.4.62", "192.168.4.63", "192.168.4.67", "192.168.4.69", "192.168.4.72", "192.168.4.75",
    "192.168.4.81", "192.168.4.91", "192.168.4.101", "192.168.4.123", "192.168.4.125", "192.168.4.140", "192.168.4.202", "192.168.4.203", "192.168.4.204",
    "192.168.4.208", "192.168.4.209", "192.168.4.213", "192.168.4.214", "192.168.4.215", "192.168.4.218", "192.168.4.221", "192.168.4.222", "192.168.4.224", 
    "192.168.4.226", "192.168.4.228", "192.168.4.231", "192.168.4.232","192.168.4.234", "192.168.4.235", "192.168.4.251", "192.168.4.254", "192.168.5.68", 
    "192.168.5.74", "192.168.5.131", "192.168.5.191", "192.168.5.208", "192.168.5.209", "192.168.5.212", "192.168.5.215", "192.168.5.250", "192.168.5.254"
]]

# Abrir os arquivos em modo de escrita
with open(arquivo_ip_mail, 'w') as f_ip, open(arquivo_status, 'w') as f_status, open(arquivo_powershell, 'w') as f_ps:
    for rede in redes:
        active = 0
        deactive = 0
        for ip in rede:
            if ip in ip_ignore:
                    continue
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
        resumo_ip_active = f'\nOnly Active IPs...\n\nActive ip: {active}\nDeactive ip: {deactive}\nTime: {hour_adjust}\n'
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
    assunto=f"Relatório de Status da Rede - {hour_adjust}",
    mensagem="O relatório de status da rede com os IPs ativos está em anexo.",
    destinatario=EMAIL_DESTINATARIO,
    anexo=arquivo_ip_mail
)
