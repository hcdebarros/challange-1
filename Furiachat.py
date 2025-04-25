import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters
from telegram.ext import ConversationHandler

# Seu token do Bot
TOKEN = '7753296815:AAEniJ4_oYuXSKWcKujODqfP6J4nmrdwCUI'  # Coloque seu token aqui

# Função de boas-vindas quando o comando /start é chamado
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    welcome_message = """
    Bem-vindo à Selva! Escolha uma das opções abaixo:
    
    /noticias - Veja as últimas notícias de e-sports
    /alertas - Receba alertas sobre os rounds
    /quiz - Participe da votação para o melhor jogador
    /redes - Acesse as redes sociais da FURIA
    """
    await update.message.reply_text(welcome_message)

import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters
from telegram.ext import ConversationHandler
from bs4 import BeautifulSoup

# Seu token do Bot
TOKEN = '7753296815:AAEniJ4_oYuXSKWcKujODqfP6J4nmrdwCUI'

# Função de boas-vindas
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    welcome_message = """
    Bem-vindo à Selva! Escolha uma das opções abaixo:
    
    /noticias - Veja as últimas notícias de e-sports
    /alertas - Receba alertas sobre os rounds
    /quiz - Participe da votação para o melhor jogador
    /redes - Acesse as redes sociais da FURIA
    """
    await update.message.reply_text(welcome_message)

# Funções de Scraping para Notícias
def obter_noticias_lol():
    url = "https://lol.fandom.com/wiki/League_of_Legends_Esports_Wiki"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    noticias = []
    for item in soup.find_all('h3', {'class': 'pi-item'}):
        noticia = item.get_text(strip=True)
        noticias.append(noticia)
    return "\n".join(noticias)

def obter_noticias_gosugamers():
    url = "https://www.gosugamers.net/lol"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    noticias = []
    for item in soup.find_all('h3', {'class': 'article-title'}):
        noticia = item.get_text(strip=True)
        noticias.append(noticia)
    return "\n".join(noticias)

def obter_noticias_dust2():
    url = "https://www.dust2.com.br"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    noticias = []
    for item in soup.find_all('h2', {'class': 'entry-title'}):
        noticia = item.get_text(strip=True)
        noticias.append(noticia)
    return "\n".join(noticias)

def obter_noticias_draft5():
    url = "https://draft5.gg"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    noticias = []
    for item in soup.find_all('h2', {'class': 'entry-title'}):
        noticia = item.get_text(strip=True)
        noticias.append(noticia)
    return "\n".join(noticias)

def obter_noticias_hltv():
    url = "https://www.hltv.org"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    noticias = []
    for item in soup.find_all('a', {'class': 'newsitem'}):
        noticia = item.get_text(strip=True)
        noticias.append(noticia)
    return "\n".join(noticias)

# Função para pegar notícias de e-sports
async def noticias(update: Update, context: ContextTypes.DEFAULT_TYPE):
    esports = ["LOL", "CS2"]
    noticias_msg = "Últimas notícias e destaques de e-Sports:\n"
    
    noticias_msg += f"\n**LOL Fandom**:\n{obter_noticias_lol()}"
    noticias_msg += f"\n**LOL GosuGamers**:\n{obter_noticias_gosugamers()}"
    noticias_msg += f"\n**CS2 Dust2**:\n{obter_noticias_dust2()}"
    noticias_msg += f"\n**CS2 Draft5**:\n{obter_noticias_draft5()}"
    noticias_msg += f"\n**CS2 HLTV**:\n{obter_noticias_hltv()}"
    
    await update.message.reply_text(noticias_msg)




# Função para pegar alertas de início e término de round
async def alertas(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🔔 **Alerta de Round!**\n\nEscolha uma opção:\n1. Início do Round\n2. Término do Round")

async def inicio_round(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🚨 O round começou! Prepare-se!")

async def termino_round(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🛑 O round terminou! Hora de analisar o desempenho.")

# Função para o Quiz de Votação do Melhor Jogador
MELHOR_JOGADOR, VOTACAO = range(2)

async def quiz(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Quem foi o melhor jogador da FURIA na última partida?\n\nVote com o número correspondente:\n1. Jogador A\n2. Jogador B\n3. Jogador C")
    return MELHOR_JOGADOR

async def votacao(update: Update, context: ContextTypes.DEFAULT_TYPE):
    resposta = update.message.text
    if resposta == "1":
        await update.message.reply_text("Você votou no Jogador A!")
    elif resposta == "2":
        await update.message.reply_text("Você votou no Jogador B!")
    elif resposta == "3":
        await update.message.reply_text("Você votou no Jogador C!")
    else:
        await update.message.reply_text("Escolha inválida! Tente novamente.")
        return MELHOR_JOGADOR
    
    return ConversationHandler.END


# Função para exibir as redes sociais da FURIA

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


# Funções para completar o fluxo do Quiz
quiz_handler = ConversationHandler(
    entry_points=[CommandHandler("quiz", quiz)],
    states={MELHOR_JOGADOR: [MessageHandler(filters.TEXT & ~filters.Command(), votacao)]},
    fallbacks=[]
)

# Montar o bot
app = ApplicationBuilder().token(TOKEN).build()

# Adicionando o comando /start
app.add_handler(CommandHandler("start", start))

# Comandos principais
app.add_handler(CommandHandler("noticias", noticias))  # Notícias e destaques de e-sports
app.add_handler(CommandHandler("alertas", alertas))  # Alertas de round
app.add_handler(CommandHandler("redes", redes_sociais))  # Redes sociais da FURIA
app.add_handler(CommandHandler("noticias", noticias))
app.add_handler(quiz_handler)  # Quiz para votação de melhor jogador

# Comandos de round (pode ser em uma sequência ou botão)
app.add_handler(CommandHandler("inicio_round", inicio_round))
app.add_handler(CommandHandler("termino_round", termino_round))

# Rodando o bot
print("Bot rodando...")
app.run_polling()
