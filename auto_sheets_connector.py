import os
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from postgresql_connector import upload_data

SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]
SPREADSHEET_ID = "15-AVwbfVX_ZfCr8InZeCBGJEgypRuKtxrtwgKPcSGpU"

SERVICE_ACCOUNT_FILE = "tabela-dgo-gace-c4e30c08bb0a.json"

def main():
    credentials = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)

    try:
        service = build("sheets", "v4", credentials=credentials)
        sheets = service.spreadsheets()

        results = upload_data()

        if len(results) > 1:
            values_to_insert = []
            for row in results:
                values_to_insert.append([str(value) for value in row])

            range_to_update = "Pag1!A1:I"
            sheets.values().update(spreadsheetId=SPREADSHEET_ID, range=range_to_update, body={"values": values_to_insert}, valueInputOption="RAW").execute()
            
            print("Dados inseridos na planilha com sucesso!")

    except HttpError as error:
        print("Erro ao acessar a API do Google Sheets:", error)

if __name__ == "__main__":
    main()
