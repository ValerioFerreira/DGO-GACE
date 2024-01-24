# Projeto de Transcrição do Banco de Dados para o Google Sheets

Este projeto tem como objetivo realizar a transcrição das informações do banco de dados do sistema Mapa de Força para uma planilha do Google Sheets. 

## Ele consiste nos seguintes componentes:

### `postgresql_connector.py`

Este script em Python é responsável por estabelecer a conexão com o banco de dados do sistema Mapa de Força. Ele extrai as informações necessárias usando uma query específica incluída no código. O resultado dessa query é armazenado em uma variável para uso posterior.

### `sheets_connector.py`

Este script em Python realiza a conexão com a planilha do Google Sheets e escreve os dados obtidos pelo script `postgresql_connector.py` nela.

### `credentials.json`

Este arquivo JSON contém as credenciais necessárias para acessar a planilha do Google Sheets.

### `token.json`

Este arquivo JSON contém as credenciais de acesso ao projeto do Google Projects. 
