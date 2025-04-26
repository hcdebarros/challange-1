import requests
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder, CommandHandler, ContextTypes,
    ConversationHandler, MessageHandler, CallbackQueryHandler, filters
)
from bs4 import BeautifulSoup

# Token do Bot
TOKEN = '7753296815:AAEniJ4_oYuXSKWcKujODqfP6J4nmrdwCUI'  # Troca isso pelo token real

# Estados da conversa
WAITING_FOR_GAME_SELECTION = 1
WAITING_FOR_ALERT = 2
MELHOR_JOGADOR = 3

# /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    welcome_message = """
    Bem-vindo à Selva! Escolha uma das opções abaixo:
    
    /noticias - Veja as últimas notícias de e-sports
    /alertas - Receba alertas sobre os rounds
    /quiz - Participe da votação para o melhor jogador
    /redes - Acesse as redes sociais da FURIA
    """
    await update.message.reply_text(welcome_message)

# ======== SCRAPING DE NOTÍCIAS ========
def obter_noticias_lol():
    url = "https://lol.fandom.com/wiki/League_of_Legends_Esports_Wiki"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    noticias = [item.get_text(strip=True) for item in soup.find_all('h3', {'class': 'pi-item'})]
    return "\n".join(noticias)

def obter_noticias_gosugamers():
    url = "https://www.gosugamers.net/lol"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    noticias = [item.get_text(strip=True) for item in soup.find_all('h3', {'class': 'article-title'})]
    return "\n".join(noticias)

def obter_noticias_dust2():
    url = "https://www.dust2.com.br"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    noticias = [item.get_text(strip=True) for item in soup.find_all('h2', {'class': 'entry-title'})]
    return "\n".join(noticias)

def obter_noticias_draft5():
    url = "https://draft5.gg"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    noticias = [item.get_text(strip=True) for item in soup.find_all('h2', {'class': 'entry-title'})]
    return "\n".join(noticias)

def obter_noticias_hltv():
    url = "https://www.hltv.org"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    noticias = [item.get_text(strip=True) for item in soup.find_all('a', {'class': 'newsitem'})]
    return "\n".join(noticias)

# /noticias
async def noticias(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[
        InlineKeyboardButton("LOL", callback_data="lol"),
        InlineKeyboardButton("CS2", callback_data="cs2")
    ]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("📰 Escolha o jogo para receber as últimas notícias:", reply_markup=reply_markup)
    return WAITING_FOR_GAME_SELECTION

async def exibir_noticias(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    game_choice = query.data

    if game_choice == "lol":
        msg = "Últimas notícias de **League of Legends**:\n"
        msg += f"\n**LOL Fandom**:\n{obter_noticias_lol()}"
        msg += f"\n**LOL GosuGamers**:\n{obter_noticias_gosugamers()}"
    elif game_choice == "cs2":
        msg = "Últimas notícias de **CS2**:\n"
        msg += f"\n**Dust2**:\n{obter_noticias_dust2()}"
        msg += f"\n**Draft5**:\n{obter_noticias_draft5()}"
        msg += f"\n**HLTV**:\n{obter_noticias_hltv()}"

    await query.edit_message_text(msg)
    return ConversationHandler.END

# /quiz

async def exibir_noticias(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    game_choice = query.data  # "lol" ou "cs2"

    if game_choice == "lol":
        msg = "📰 *Últimas notícias de League of Legends:*\n"
        msg += f"\n📌 *LOL Fandom:*\n{obter_noticias_lol()}"
        msg += f"\n📌 *LOL GosuGamers:*\n{obter_noticias_gosugamers()}"
        await query.edit_message_text(msg, parse_mode="Markdown")

    elif game_choice == "cs2":
        msg = "📰 *Últimas notícias de CS2:*\n"
        msg += f"\n📌 *Dust2:*\n{obter_noticias_dust2()}"
        msg += f"\n📌 *Draft5:*\n{obter_noticias_draft5()}"
        msg += f"\n📌 *HLTV:*\n{obter_noticias_hltv()}"
        await query.edit_message_text(msg, parse_mode="Markdown")

    else:
        await query.edit_message_text("❌ Escolha inválida. Tente novamente.")

    return ConversationHandler.END

# Estado do ConversationHandler
MELHOR_JOGADOR = 3

# Lista dos jogadores (você pode trocar pelos da FURIA mesmo)
JOGADORES = ["KSCERATO", "yuurih", "YEKINDAR", "molodoy", "Fallen"]

# Função inicial do quiz
async def quiz(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if "votos" not in context.bot_data:
        context.bot_data["votos"] = {jogador: 0 for jogador in JOGADORES}

    keyboard = [
        [InlineKeyboardButton(jogador, callback_data=jogador)] for jogador in JOGADORES
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        "🏆 Quem foi o melhor jogador do último jogo?",
        reply_markup=reply_markup
    )
    return MELHOR_JOGADOR

# Função de votação
async def votacao(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    voto = query.data

    if voto in context.bot_data["votos"]:
        context.bot_data["votos"][voto] += 1

    votos = context.bot_data["votos"]
    resultado = "📊 *Parcial da votação:*\n\n"
    for jogador, qtd in votos.items():
        resultado += f"• {jogador}: {qtd} voto(s)\n"

    await query.edit_message_text(resultado, parse_mode="Markdown")
    return ConversationHandler.END

# /alertas
async def alertas(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[
        InlineKeyboardButton("League of Legends", callback_data="alerta_lol"),
        InlineKeyboardButton("CS2", callback_data="alerta_cs2")
    ]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("🔔 Escolha o jogo para perguntar algo sobre o round:", reply_markup=reply_markup)
    return WAITING_FOR_GAME_SELECTION

async def jogo_escolhido_para_alerta(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    jogo = query.data.replace("alerta_", "")
    context.user_data["jogo_alerta"] = jogo
    await query.edit_message_text(f"🎮 Jogo escolhido: {jogo.upper()}. Agora me diga o que você quer saber:")
    return WAITING_FOR_ALERT

async def round_alert(update: Update, context: ContextTypes.DEFAULT_TYPE):
    pergunta = update.message.text.lower()
    jogo = context.user_data.get("jogo_alerta", "cs2")

    if "quando" in pergunta or "data" in pergunta:
        resposta = f"O próximo jogo de {jogo.upper()} é amanhã às 18h (simulado)"
    elif "mapa" in pergunta:
        resposta = f"O mapa mais jogado recentemente pela FURIA no {jogo.upper()} foi Mirage."
    elif "lineup" in pergunta or "jogadores" in pergunta:
        resposta = f"O lineup atual da FURIA no {jogo.upper()} é: KSCERATO, yuurih, arT, chelo e fallen."
    else:
        resposta = f"🤖 Não entendi bem... Pergunta tipo: 'Quando é o próximo jogo?', 'Qual o mapa?', 'Quem joga?'"

    await update.message.reply_text(resposta)
    return ConversationHandler.END

# /redes (exemplo simples)
async def redes_sociais(update: Update, context: ContextTypes.DEFAULT_TYPE):
    redes = """
    Siga a FURIA nas redes sociais:
    - Instagram: [@FURIA](https://instagram.com/furiagg)
    - Twitter: [@FURIA](https://twitter.com/FURIA)
    - YouTube: [@FURIA](https://www.youtube.com/channel/UCE4elIT7DqDv545IA71feHg)
    - TikTok Esports: [@FURIA](https://tiktok.com/@furiagg)
    - Twitch: [@FURIA](https://twitch.tv/team/furia)
    """
    # Escape para o MarkdownV2
    redes = redes.replace("-", "\-")  # Escapa o hífen
    await update.message.reply_text(redes, parse_mode="MarkdownV2")

# ========================
# MONTA O APP E OS HANDLERS
# ========================
app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("redes", redes_sociais))

# Noticias
app.add_handler(ConversationHandler(
    entry_points=[CommandHandler("noticias", noticias)],
    states={WAITING_FOR_GAME_SELECTION: [CallbackQueryHandler(exibir_noticias)]},
    fallbacks=[]
))

# Alertas
app.add_handler(ConversationHandler(
    entry_points=[CommandHandler("alertas", alertas)],
    states={
        WAITING_FOR_GAME_SELECTION: [CallbackQueryHandler(jogo_escolhido_para_alerta)],
        WAITING_FOR_ALERT: [MessageHandler(filters.TEXT & ~filters.COMMAND, round_alert)]
    },
    fallbacks=[]
))

# Quiz
app.add_handler(ConversationHandler(
    entry_points=[CommandHandler("quiz", quiz)],
    states={MELHOR_JOGADOR: [CallbackQueryHandler(votacao)]},
    fallbacks=[]
))

print("Bot rodando... Ctrl+C pra parar")
app.run_polling()
