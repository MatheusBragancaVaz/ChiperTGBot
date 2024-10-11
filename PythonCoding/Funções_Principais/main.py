from typing import Final
from telegram.ext import Application, CommandHandler
from database import init_db
from commands import add_expense, view_report

TOKEN: Final = '6060743931:AAEgce0Ok7Fjwjwnf_r2PJ83wJyjhij_V-g'
BOT_USERNAME: Final = '@Cipher'

def main() -> None:
    init_db()  # Aqui ele Inicializa o banco de dados
    app = Application.builder().token(TOKEN).build()

    # Aq adiciona os handlers para os comandos
    app.add_handler(CommandHandler("add_expense", add_expense))
    app.add_handler(CommandHandler("view_report", view_report))

    # Aq inicia o bot
    app.run_polling(poll_interval=3)

if __name__ == '__main__':
    main()