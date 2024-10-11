from telegram import Update
from telegram.ext import ContextTypes
from database import add_expense_to_db, get_expenses

async def add_expense(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    
    user_id = update.effective_user.id
    try:
        amount, category, *description_parts = context.args
        amount = float(amount)
        description = ' '.join(description_parts)

        add_expense_to_db(user_id, amount, category, description)

        await update.message.reply_text(f"Despesa registrada: R${amount:.2f} em {category} - {description}")
    except (ValueError, IndexError):
        await update.message.reply_text("Uso correto: /add_expense <valor> <categoria> <descrição>")

async def view_report(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.effective_user.id
    try:
        period = context.args[0].lower()
        if period not in ["diário", "semanal", "mensal"]:
            raise ValueError

        expenses = get_expenses(user_id, period)
        if expenses:
            report = f"Relatório de despesas {period}:\n\n"
            total = 0
            for category, amount in expenses:
                report += f"{category}: R${amount:.2f}\n"
                total += amount
            report += f"\nTotal: R${total:.2f}"
        else:
            report = f"Nenhuma despesa registrada no período {period}."

        await update.message.reply_text(report)
    except (IndexError, ValueError):
        await update.message.reply_text("Uso correto: /view_report <período> (diário, semanal ou mensal)")