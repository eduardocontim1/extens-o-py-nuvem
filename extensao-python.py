import gspread
from oauth2client.service_account import ServiceAccountCredentials
import smtplib
from email.mime.text import MIMEText

# Configura a conexão com o Google Sheets
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name('credenciais.json', scope)
client = gspread.authorize(creds)

# Abre a planilha e seleciona a aba de imóveis
sheet = client.open("Gerenciamento_Imoveis").sheet1

# Função para enviar e-mail de notificação
def enviar_email(destinatario, assunto, mensagem):
    remetente = "seuemail@gmail.com"
    senha = "sua_senha"

    msg = MIMEText(mensagem)
    msg['Subject'] = assunto
    msg['From'] = remetente
    msg['To'] = destinatario

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(remetente, senha)
        smtp.send_message(msg)
    print(f"E-mail enviado para {destinatario}")

# Função para marcar um imóvel como vendido/alugado e notificar o cliente
def marcar_vendido(id_imovel, email_cliente):
    try:
        # Procura o imóvel pela ID
        cell = sheet.find(id_imovel)
        # Atualiza o status para "vendido/alugado"
        sheet.update_cell(cell.row, 3, 'Vendido/Alugado')  # Coluna de status

        # Envia e-mail de confirmação para o cliente
        mensagem = f"Prezado cliente, o imóvel com ID {id_imovel} foi vendido/alugado com sucesso!"
        enviar_email(email_cliente, "Confirmação de Venda/Aluguel", mensagem)

        print(f"Imóvel {id_imovel} marcado como vendido/alugado.")
    except gspread.exceptions.CellNotFound:
        print(f"Imóvel com ID {id_imovel} não encontrado.")

# Exemplo de uso fictício
marcar_vendido('123', 'cliente@exemplo.com')