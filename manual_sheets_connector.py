import os
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from postgresql_connector import upload_data

SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]
SPREADSHEET_ID = "15-AVwbfVX_ZfCr8InZeCBGJEgypRuKtxrtwgKPcSGpU"
REDIRECT_URI = "http://localhost:55892/"

def main():
    credentials = None

    if os.path.exists("token.json"):
        credentials = Credentials.from_authorized_user_file("token.json", SCOPES)

    if not credentials or not credentials.valid:
        if credentials and credentials.expired and credentials.refresh_token:
            credentials.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES, redirect_uri=REDIRECT_URI)
            credentials = flow.run_local_server(port=0)
        with open("token.json", "w") as token:
            token.write(credentials.to_json())

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
