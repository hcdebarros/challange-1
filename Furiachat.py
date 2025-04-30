from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

JOGOS = ["CS2", "LOL", "Rocket League", "Rainbow Six", "Valorant"]

# /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    teclado = [
        [InlineKeyboardButton("📰 Notícias", callback_data="menu_noticias")],
        [InlineKeyboardButton("🚨 Alertas", callback_data="menu_alertas")],
        [InlineKeyboardButton("❓ Quiz", callback_data="menu_quiz")],
        [InlineKeyboardButton("🌐 Redes", callback_data="menu_redes")],
    ]
    await update.message.reply_text(
        "🎮 Bem vindo à selva, escolha uma das opções abaixo para continuar:",
        reply_markup=InlineKeyboardMarkup(teclado)
    )

# Gera menu com botões a partir da lista de jogos
def gerar_menu_jogos(prefixo_callback):
    teclado = [[InlineKeyboardButton(jogo, callback_data=f"{prefixo_callback}_{jogo}")] for jogo in JOGOS]
    return InlineKeyboardMarkup(teclado)

# Generalizada: envia texto com botões, tanto pra comandos quanto pra callback
async def responder(update, text, reply_markup=None):
    if update.message:
        await update.message.reply_text(text, reply_markup=reply_markup)
    elif update.callback_query:
        await update.callback_query.message.edit_text(text, reply_markup=reply_markup)

# /noticias
async def noticias(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await responder(update, "📰 Escolha o jogo para ver notícias:", gerar_menu_jogos("noticias"))

# /alertas
async def alertas(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await responder(update, "🚨 Escolha o jogo para configurar alertas:", gerar_menu_jogos("alertas"))

# /quiz
async def quiz(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await responder(update, "❓ Escolha o jogo para jogar o quiz:", gerar_menu_jogos("quiz"))

# /redes
async def redes(update: Update, context: ContextTypes.DEFAULT_TYPE):
    redes = """
🌐 Siga a FURIA nas redes sociais:

- [Instagram](https://instagram.com/furiagg)
- [Twitter](https://twitter.com/FURIA)
- [YouTube](https://www.youtube.com/channel/UCE4elIT7DqDv545IA71feHg)
- [TikTok](https://tiktok.com/@furiagg)
- [Twitch](https://twitch.tv/team/furia)
"""
    if update.message:
        await update.message.reply_text(redes, parse_mode="Markdown", disable_web_page_preview=True)
    elif update.callback_query:
        await update.callback_query.message.edit_text(redes, parse_mode="Markdown", disable_web_page_preview=True)

# Callback geral para todos os botões
async def handle_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "menu_noticias":
        await noticias(update, context)
        return
    elif query.data == "menu_alertas":
        await alertas(update, context)
        return
    elif query.data == "menu_quiz":
        await quiz(update, context)
        return
    elif query.data == "menu_redes":
        await redes(update, context)
        return

    tipo, jogo = query.data.split("_", 1)

    if tipo == "noticias":
        await query.edit_message_text(f"📰 Aqui estão as últimas notícias sobre {jogo}. (a implementar)")
    elif tipo == "alertas":
        await query.edit_message_text(f"🚨 Alertas de {jogo}: escolha o tipo de alerta. (a implementar)")
    elif tipo == "quiz":
        await query.edit_message_text(f"❓ Quiz de {jogo}: escolha uma categoria. (a implementar)")

# Main
def main():
    app = ApplicationBuilder().token("7753296815:AAEniJ4_oYuXSKWcKujODqfP6J4nmrdwCUI").build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("noticias", noticias))
    app.add_handler(CommandHandler("alertas", alertas))
    app.add_handler(CommandHandler("quiz", quiz))
    app.add_handler(CommandHandler("redes", redes))
    app.add_handler(CallbackQueryHandler(handle_callback))

    print("Bot rodando...")
    app.run_polling()

if __name__ == "__main__":
    main()
