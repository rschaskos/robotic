<h1 align="center"> SCRIPT PARA CONSULTA AUTOMÁTICA DE CERTIDÃO DE ANTECEDENTES CRIMINAIS </h1>

## Pré-requisitos

Antes de começar, você vai precisar ter instalado em sua máquina as seguintes bibliotecas, para isso digite os comandos abaixo no terminal:

```
pip install selenium
pip install pyautogui
```


Além disso, você também precisa ter o Python e Google Chrome instalados em sua máquina.

## 1 - O arquivo TXT com a lista de pessoas precisa conter um separador. 

É muito comum que se utilizem os seguintes separadores: ( , ; | )
Para tanto basta ter a relação com os nomes que deseja buscar.
Esse código por padrão utiliza os seguintes dados separados por coluna com pipe "|" .

CPF|nome completo|data de nascimento|nome completo do pai|nome completo da mãe

## Como executar

1. Clone o repositório ou faça uma cópia do arquivo "main.py" em sua IDE favorita e então basta dar um RUN.
2. Se preferir também pode abrir o terminal e navegar até o diretório onde o arquivo está localizado.
3. Execute o arquivo Python com o comando:
```
python main.py
```

## Funcionalidades

Este código Python visa automatizar o processo de obtenção de certidões de antecedentes criminais. Ele interage com sites ou sistemas online, preenchendo formulários, clicando em botões e baixando os documentos necessários.
