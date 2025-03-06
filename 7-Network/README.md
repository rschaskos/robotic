<h1 align="center"> SCRIPT PARA MONITORAMENTO EM REDE </h1>

## Pré-requisitos

Antes de começar, você vai precisar ter instalado em sua máquina as seguintes bibliotecas, para isso digite os comandos abaixo no terminal:

```
pip install ipaddress
pip install smtplib (geralmente já instalada)
pip install email (geralmente já instalada)
pip install dotenv

```

## 1 - Defina o arranjo de IP que tem interesse em identificar e configure os valores de e-mail inicial. 

```
rede = ipaddress.ip_network('192.168.5.0/24') 
EMAIL_REMETENTE = 'seu-endereco@seu-provedor.com.'
SENHA = 'seu-password'
EMAIL_DESTINATARIO = 'email-destinario@provedor.com'
SMTP_SERVER = 'smtp-do-envio.com' # exemplo gmail: smtp.gmail.com
SMTP_PORT = 587
```

## Como executar

1. Clone o repositório ou faça uma cópia do arquivo "main.py" em sua IDE favorita e então basta dar um RUN.
2. Se preferir também pode abrir o terminal e navegar até o diretório onde o arquivo está localizado.
3. Execute o arquivo Python com o comando:
```
python main.py
```

O script irá fazer todo trabalho, basta aguardar

## Funcionalidades

Este código Python tem por objetivo indentificar quais computadores estão ativos numa rede e enviar o relatório dos IPs ativos por e-mail.

Trata-se de uma ferramenta para uso interno na organização, porém é possível usar com os conceitos empregados.
