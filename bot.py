import discord
from discord import app_commands
from discord.ext import commands
from discord.ui import Button, View
import re
import os
import asyncio
from dotenv import load_dotenv
from threading import Thread
from flask import Flask

# Carrega variáveis de ambiente (.env para local, Secrets para Replit)
load_dotenv()

# ==================== SERVIDOR WEB PARA REPLIT ====================
# Mantém o bot online no Replit
app = Flask('')

@app.route('/')
def home():
    return "Bot está online! 🤖"

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix='!', intents=intents)
tree = bot.tree

active_castigos = {}
active_creations = {}

REQUIRED_VOTERS = 4
ALLOWED_CHANNEL_ID = None
RESULTADO_CHANNEL_ID = None  # Canal onde os resultados serão enviados

# ==================== CLASSES ====================

class Castigo:
    def __init__(self, creator, trollador, participantes, motivo, url, channel, message):
        self.creator = creator
        self.trollador = trollador
        self.participantes = participantes
        self.motivo = motivo
        self.url = url
        self.channel = channel
        self.message = message
        self.votes_sim = []
        self.votes_nao = []
        self.finished = False
    
    def get_total_votes(self):
        return len(self.votes_sim) + len(self.votes_nao)
    
    def is_complete(self):
        return self.get_total_votes() >= REQUIRED_VOTERS
    
    def get_result(self):
        sim = len(self.votes_sim)
        nao = len(self.votes_nao)
        # Precisa de 3 votos "Sim" para aprovar
        if sim >= 3:
            return "APROVADO"
        else:
            return "REJEITADO"

class CastigoCreation:
    def __init__(self, creator, channel, guild):
        self.creator = creator
        self.channel = channel
        self.guild = guild
        self.step = 0
        self.trollador = None
        self.participantes = []
        self.link = None
        self.motivo = None
        self.last_confirmation_msg = None

# ==================== VIEW COM BOTÃO PARA ABRIR CASTIGO ====================

class AbrirCastigoView(View):
    def __init__(self):
        super().__init__(timeout=None)
    
    @discord.ui.button(label="📝 Abrir Castigo", style=discord.ButtonStyle.primary, custom_id="abrir_castigo_btn")
    async def abrir_castigo_button(self, interaction: discord.Interaction, button: Button):
        if ALLOWED_CHANNEL_ID and interaction.channel_id != ALLOWED_CHANNEL_ID:
            await interaction.response.send_message("❌ Este comando só pode ser usado no canal configurado!", ephemeral=True)
            return
        
        if interaction.user.id in active_creations:
            await interaction.response.send_message("❌ Você já está criando um castigo!", ephemeral=True)
            return
        
        creation = CastigoCreation(interaction.user, interaction.channel, interaction.guild)
        active_creations[interaction.user.id] = creation
        
        await interaction.response.send_message(
            "✅ **Criação de castigo iniciada!**\n\n"
            "📝 **Passo 1 de 4**: Digite no chat uma **menção** do usuário trollador\n"
            "💡 Use @ para mencionar (ex: @NomeDoUsuario)\n"
            "⚠️ Clique no nome para ele ficar azul/mencionável\n\n"
            "🗑️ Suas mensagens serão **auto-deletadas**\n"
            "⏱️ Confirmações somem quando você envia a **próxima mensagem**",
            ephemeral=True
        )
    
    @discord.ui.button(label="❌ Cancelar Castigo", style=discord.ButtonStyle.danger, custom_id="cancelar_castigo_btn")
    async def cancelar_castigo_button(self, interaction: discord.Interaction, button: Button):
        if interaction.user.id not in active_creations:
            await interaction.response.send_message("❌ Você não está criando nenhum castigo!", ephemeral=True)
            return
        
        del active_creations[interaction.user.id]
        await interaction.response.send_message("✅ Criação de castigo cancelada!", ephemeral=True)

# ==================== VIEW COM BOTÕES DE VOTAÇÃO ====================

class VotingView(View):
    def __init__(self, allowed_voters):
        super().__init__(timeout=None)
        self.allowed_voters = allowed_voters
        self.castigo = None
    
    @discord.ui.button(label="Sim", style=discord.ButtonStyle.success, emoji="✅")
    async def vote_sim(self, interaction: discord.Interaction, button: Button):
        await self.process_vote(interaction, True)
    
    @discord.ui.button(label="Não", style=discord.ButtonStyle.danger, emoji="❌")
    async def vote_nao(self, interaction: discord.Interaction, button: Button):
        await self.process_vote(interaction, False)
    
    async def process_vote(self, interaction: discord.Interaction, vote_sim: bool):
        if not self.castigo:
            await interaction.response.send_message("❌ Erro ao carregar castigo!", ephemeral=True)
            return
        
        if self.castigo.finished:
            await interaction.response.send_message("❌ Esta votação já foi encerrada!", ephemeral=True)
            return
        
        if interaction.user.id not in self.allowed_voters:
            await interaction.response.send_message("❌ Apenas os participantes da partida podem votar!", ephemeral=True)
            return
        
        if interaction.user.id in self.castigo.votes_sim or interaction.user.id in self.castigo.votes_nao:
            await interaction.response.send_message("❌ Você já votou!", ephemeral=True)
            return
        
        if vote_sim:
            self.castigo.votes_sim.append(interaction.user.id)
            await interaction.response.send_message("✅ Seu voto 'Sim' foi registrado!", ephemeral=True)
        else:
            self.castigo.votes_nao.append(interaction.user.id)
            await interaction.response.send_message("❌ Seu voto 'Não' foi registrado!", ephemeral=True)
        
        await self.update_castigo_embed()
        
        if self.castigo.is_complete():
            await self.finalize_voting()
    
    async def update_castigo_embed(self):
        if not self.castigo or not self.castigo.message:
            return
        
        try:
            embed = self.castigo.message.embeds[0]
            sim_count = len(self.castigo.votes_sim)
            nao_count = len(self.castigo.votes_nao)
            total = self.castigo.get_total_votes()
            
            voting_text = f"✅ Sim: {sim_count}\n❌ Não: {nao_count}\n\n"
            voting_text += "✅ Votação completa!" if self.castigo.is_complete() else f"⏳ Votos: {total}/{REQUIRED_VOTERS}"
            
            for i, field in enumerate(embed.fields):
                if field.name == "📊 Votação":
                    embed.set_field_at(i, name="📊 Votação", value=voting_text, inline=False)
                    break
            
            await self.castigo.message.edit(embed=embed, view=self)
        except Exception as e:
            print(f"Erro ao atualizar embed: {e}")
    
    async def finalize_voting(self):
        if not self.castigo:
            return
        
        self.castigo.finished = True
        result = self.castigo.get_result()
        sim_count = len(self.castigo.votes_sim)
        nao_count = len(self.castigo.votes_nao)
        
        color = 0x00ff00 if result == "APROVADO" else 0xff0000
        emoji = "✅" if result == "APROVADO" else "❌"
        
        embed = discord.Embed(
            title=f"{emoji} Votação Finalizada - {result}",
            color=color,
            timestamp=discord.utils.utcnow()
        )
        embed.add_field(name="👤 Usuário Acusado", value=self.castigo.trollador.mention, inline=False)
        embed.add_field(name="📊 Resultado Final", value=f"✅ Sim: {sim_count}\n❌ Não: {nao_count}", inline=False)
        embed.add_field(name="📄 Motivo", value=self.castigo.motivo, inline=False)
        embed.add_field(name="🔗 URL da Partida", value=self.castigo.url, inline=False)
        embed.set_footer(text=f"Castigo aberto por {self.castigo.creator.display_name}")
        
        try:
            await self.castigo.message.edit(embed=embed, view=None)
        except:
            pass
        
        # Se aprovado, adiciona o cargo @castigo
        if result == "APROVADO":
            try:
                guild = self.castigo.trollador.guild
                cargo_castigo = discord.utils.get(guild.roles, name="castigo")
                
                if cargo_castigo:
                    await self.castigo.trollador.add_roles(cargo_castigo)
                    print(f"[OK] Cargo @castigo adicionado a {self.castigo.trollador.display_name}")
                else:
                    print("[AVISO] Cargo 'castigo' não encontrado no servidor")
            except Exception as e:
                print(f"[ERRO] Não foi possível adicionar o cargo: {e}")
        
        # Envia resultado APENAS no canal de resultados configurado (se houver)
        if RESULTADO_CHANNEL_ID:
            try:
                target_channel = bot.get_channel(RESULTADO_CHANNEL_ID)
                if target_channel:
                    # GIFs diferentes para aprovado/rejeitado
                    gif_url = "https://media1.tenor.com/m/F-CfTC0b1bwAAAAd/hammer.gif" if result == "APROVADO" else "https://media.tenor.com/gx3jCmdyMR0AAAAC/nope-no.gif"
                    
                    await target_channel.send(
                        f"## {emoji} Votação Encerrada!\n"
                        f"{self.castigo.trollador.mention}\n"
                        f"{gif_url}\n\n"
                        f"**Resultado:** {result}\n"
                        f"**Votos:** ✅ {sim_count} x ❌ {nao_count}"
                    )
                else:
                    print("[AVISO] Canal de resultados não encontrado")
            except Exception as e:
                print(f"[ERRO] Não foi possível enviar resultado: {e}")
        
        if self.castigo.message.id in active_castigos:
            del active_castigos[self.castigo.message.id]

# ==================== FUNÇÕES AUXILIARES ====================

def extract_user_id(text, guild):
    match = re.search(r'<@!?(\d+)>', text)
    if match:
        user_id = int(match.group(1))
        member = guild.get_member(user_id)
        return member
    
    try:
        user_id = int(text.strip())
        member = guild.get_member(user_id)
        return member
    except:
        return None

def extract_multiple_users(text, guild):
    mentions = re.findall(r'<@!?(\d+)>', text)
    users = []
    
    for mention in mentions:
        user_id = int(mention)
        member = guild.get_member(user_id)
        if member and member not in users:
            users.append(member)
    
    return users

# ==================== EVENTOS ====================

@bot.event
async def on_ready():
    print(f'[OK] {bot.user} esta online!')
    print(f'[INFO] Conectado a {len(bot.guilds)} servidor(es)')
    
    # Registra Views persistentes para que funcionem após reiniciar o bot
    bot.add_view(AbrirCastigoView())
    print('[OK] Views persistentes registradas')
    
    try:
        print('[INFO] Sincronizando comandos slash...')
        synced = await tree.sync()
        print(f'[OK] {len(synced)} comando(s) sincronizado(s)')
    except Exception as e:
        print(f'[ERRO] Erro ao sincronizar: {e}')

@bot.event
async def on_message(message):
    if message.author.bot:
        return
    
    await bot.process_commands(message)
    
    user_id = message.author.id
    if user_id in active_creations:
        creation = active_creations[user_id]
        
        if message.channel.id != creation.channel.id:
            return
        
        # Deleta a mensagem de confirmação anterior
        if creation.last_confirmation_msg:
            try:
                await creation.last_confirmation_msg.delete()
                creation.last_confirmation_msg = None
            except:
                pass
        
        # Deleta a mensagem do usuário
        try:
            await message.delete()
        except:
            pass
        
        # Step 0: Trollador
        if creation.step == 0:
            trollador = extract_user_id(message.content, message.guild)
            
            if not trollador:
                creation.last_confirmation_msg = await message.channel.send(
                    f"{message.author.mention} ❌ Usuário não encontrado!\n"
                    f"💡 Use @ para mencionar o usuário"
                )
                return
            
            creation.trollador = trollador
            creation.step = 1
            
            creation.last_confirmation_msg = await message.channel.send(
                f"{message.author.mention} ✅ Trollador: {trollador.mention}\n"
                f"📝 **Passo 2 de 4**: Mencione os **4 participantes**"
            )
        
        # Step 1: Participantes
        elif creation.step == 1:
            participantes = extract_multiple_users(message.content, message.guild)
            
            if len(participantes) != REQUIRED_VOTERS:
                creation.last_confirmation_msg = await message.channel.send(
                    f"{message.author.mention} ❌ Mencione exatamente {REQUIRED_VOTERS} participantes!"
                )
                return
            
            if creation.trollador in participantes:
                creation.last_confirmation_msg = await message.channel.send(
                    f"{message.author.mention} ❌ O trollador não pode estar na lista!"
                )
                return
            
            creation.participantes = participantes
            creation.step = 2
            
            participantes_text = ", ".join([p.mention for p in participantes])
            creation.last_confirmation_msg = await message.channel.send(
                f"{message.author.mention} ✅ Participantes: {participantes_text}\n"
                f"📝 **Passo 3 de 4**: Envie o **link da partida**\n"
                f"Aceito: op.gg, u.gg ou leagueofgraphs.com"
            )
        
        # Step 2: Link
        elif creation.step == 2:
            url_pattern = r'https?://[^\s]+'
            urls = re.findall(url_pattern, message.content)
            
            if not urls:
                creation.last_confirmation_msg = await message.channel.send(
                    f"{message.author.mention} ❌ Link inválido! Envie uma URL válida."
                )
                return
            
            link = urls[0]
            
            # Valida se o link é de um dos sites permitidos
            allowed_domains = ['op.gg', 'u.gg', 'leagueofgraphs.com']
            is_valid = any(domain in link.lower() for domain in allowed_domains)
            
            if not is_valid:
                creation.last_confirmation_msg = await message.channel.send(
                    f"{message.author.mention} ❌ Link inválido!\n"
                    f"Use: **op.gg**, **u.gg** ou **leagueofgraphs.com**"
                )
                return
            
            creation.link = link
            creation.step = 3
            
            creation.last_confirmation_msg = await message.channel.send(
                f"{message.author.mention} ✅ Link validado!\n"
                f"📝 **Passo 4 de 4**: Escreva o **motivo**"
            )
        
        # Step 3: Motivo
        elif creation.step == 3:
            if len(message.content) < 10:
                creation.last_confirmation_msg = await message.channel.send(
                    f"{message.author.mention} ❌ Motivo muito curto! (mínimo 10 caracteres)"
                )
                return
            
            creation.motivo = message.content
            
            creation.last_confirmation_msg = await message.channel.send(
                f"{message.author.mention} ✅ Castigo criado! Publicando votação..."
            )
            
            # Deleta a mensagem de confirmação final após publicar
            await publish_castigo(creation)
            
            if creation.last_confirmation_msg:
                try:
                    await creation.last_confirmation_msg.delete()
                except:
                    pass
            
            del active_creations[user_id]

async def publish_castigo(creation):
    embed = discord.Embed(
        title="🎯 Castigo Aberto",
        color=0xff6b6b,
        timestamp=discord.utils.utcnow()
    )
    embed.add_field(name="👤 Usuário Acusado", value=creation.trollador.mention, inline=False)
    embed.add_field(name="👥 Presentes na Partida", value=", ".join([p.mention for p in creation.participantes]), inline=False)
    embed.add_field(name="📄 Motivo", value=creation.motivo, inline=False)
    embed.add_field(name="🔗 URL da Partida", value=creation.link, inline=False)
    embed.add_field(name="📊 Votação", value="✅ Sim: 0\n❌ Não: 0\n\n⏳ Aguardando votos...", inline=False)
    embed.set_footer(text=f"Aberto por {creation.creator.display_name}")
    
    participantes_ids = [p.id for p in creation.participantes]
    view = VotingView(participantes_ids)
    
    message = await creation.channel.send(embed=embed, view=view)
    
    castigo = Castigo(
        creation.creator,
        creation.trollador,
        creation.participantes,
        creation.motivo,
        creation.link,
        creation.channel,
        message
    )
    active_castigos[message.id] = castigo
    view.castigo = castigo

# ==================== COMANDOS ====================

@tree.command(name="castigo", description="Sistema de castigos - Informações e abertura")
async def castigo_info_command(interaction: discord.Interaction):
    embed = discord.Embed(
        title="⚖️ Sistema de Castigos",
        description="Sistema de votação para avaliar comportamento em partidas",
        color=0xff6b6b,
        timestamp=discord.utils.utcnow()
    )
    
    embed.add_field(
        name="📋 Como Funciona",
        value=(
            "1️⃣ Clique no botão **Abrir Castigo**\n"
            "2️⃣ Informe o **@usuário trollador**\n"
            "3️⃣ Mencione os **4 participantes** da partida\n"
            "4️⃣ Cole o **link da partida** (op.gg, u.gg ou leagueofgraphs.com)\n"
            "5️⃣ Descreva o **motivo** da acusação\n"
            "6️⃣ Votação aberta automaticamente"
        ),
        inline=False
    )
    
    embed.add_field(
        name="✅ Votação",
        value=(
            f"• Apenas os **{REQUIRED_VOTERS} participantes** podem votar\n"
            "• Cada pessoa vota **Sim** ou **Não**\n"
            "• **Aprovado:** 3 decidiram o castigo, vai pro cantinho\n"
            "• **Rejeitado:** Passou livre dessa vez..."
        ),
        inline=False
    )
    
    embed.add_field(
        name="🔒 Privacidade",
        value=(
            "• Suas mensagens são **auto-deletadas** instantaneamente\n"
            "• Confirmações somem quando você envia a **próxima mensagem**\n"
            "• Processo discreto até a votação final\n"
            "• Use o botão **Cancelar** para cancelar"
        ),
        inline=False
    )
    
    embed.set_footer(text="Clique no botão abaixo para começar")
    
    view = AbrirCastigoView()
    await interaction.response.send_message(embed=embed, view=view)

@tree.command(name="abrir_castigo", description="Abre o sistema de castigos")
async def castigo_command(interaction: discord.Interaction):
    if ALLOWED_CHANNEL_ID and interaction.channel_id != ALLOWED_CHANNEL_ID:
        await interaction.response.send_message("❌ Este comando só pode ser usado no canal configurado!", ephemeral=True)
        return
    
    if interaction.user.id in active_creations:
        await interaction.response.send_message("❌ Você já está criando um castigo!", ephemeral=True)
        return
    
    creation = CastigoCreation(interaction.user, interaction.channel, interaction.guild)
    active_creations[interaction.user.id] = creation
    
    # Envia mensagem efêmera
    await interaction.response.send_message(
        "✅ **Criação de castigo iniciada!**\n\n"
        "📝 **Passo 1 de 4**: Digite no chat uma **menção** do usuário trollador\n"
        "💡 Use @ para mencionar (ex: @NomeDoUsuario)\n"
        "⚠️ Clique no nome para ele ficar azul/mencionável\n\n"
        "🗑️ Suas mensagens serão **auto-deletadas**\n"
        "⏱️ Confirmações somem quando você envia a **próxima mensagem**",
        ephemeral=True
    )

@tree.command(name="cancelar_castigo", description="Cancela a criação")
async def cancelar_command(interaction: discord.Interaction):
    if interaction.user.id not in active_creations:
        await interaction.response.send_message("❌ Você não está criando nenhum castigo!", ephemeral=True)
        return
    
    del active_creations[interaction.user.id]
    await interaction.response.send_message("❌ Criação cancelada!", ephemeral=True)

@tree.command(name="castigo_configurar", description="[ADMIN] Configura os canais do sistema")
@app_commands.describe(
    canal_votacao="Canal onde as votações serão abertas (deixe vazio para permitir qualquer canal)",
    canal_resultado="Canal onde os resultados serão enviados (deixe vazio para enviar no mesmo canal da votação)"
)
@app_commands.checks.has_permissions(administrator=True)
async def configurar_command(
    interaction: discord.Interaction,
    canal_votacao: discord.TextChannel = None,
    canal_resultado: discord.TextChannel = None
):
    # Defer the response immediately to prevent timeout
    await interaction.response.defer(ephemeral=True)
    
    global ALLOWED_CHANNEL_ID, RESULTADO_CHANNEL_ID
    
    response_parts = []
    
    if canal_votacao:
        ALLOWED_CHANNEL_ID = canal_votacao.id
        response_parts.append(f"✅ **Canal de votação:** {canal_votacao.mention}")
    else:
        ALLOWED_CHANNEL_ID = None
        response_parts.append("✅ **Canal de votação:** Qualquer canal permitido")
    
    if canal_resultado:
        RESULTADO_CHANNEL_ID = canal_resultado.id
        response_parts.append(f"✅ **Canal de resultados:** {canal_resultado.mention}")
    else:
        RESULTADO_CHANNEL_ID = None
        response_parts.append("✅ **Canal de resultados:** Mesmo canal da votação")
    
    response = "⚙️ **Configuração atualizada!**\n\n" + "\n".join(response_parts)
    await interaction.followup.send(response, ephemeral=True)

@tree.command(name="castigo_ajuda", description="Mostra ajuda")
async def help_command(interaction: discord.Interaction):
    embed = discord.Embed(
        title="🤖 Bot de Castigos",
        description="Sistema de votação com mensagens auto-destrutivas",
        color=0x7289da
    )
    embed.add_field(
        name="📝 Comandos Principais",
        value=(
            "`/castigo` - Informações completas do sistema\n"
            "`/abrir_castigo` - Inicia um novo castigo\n"
            "`/cancelar_castigo` - Cancela a criação"
        ),
        inline=False
    )
    embed.add_field(
        name="⚙️ Comandos de Admin",
        value=(
            "`/castigo_configurar` - Configura os canais\n"
            "• **canal_votacao:** Onde abrir votações\n"
            "• **canal_resultado:** Onde enviar resultados"
        ),
        inline=False
    )
    embed.add_field(
        name="🎯 Como usar",
        value=(
            "1. Use `/abrir_castigo`\n"
            "2. Responda as perguntas no chat\n"
            "3. Suas mensagens serão apagadas\n"
            "4. Castigo publicado para votação"
        ),
        inline=False
    )
    await interaction.response.send_message(embed=embed, ephemeral=True)

if __name__ == "__main__":
    # Inicia o servidor web para manter o bot online no Replit
    keep_alive()
    
    token = os.getenv('DISCORD_TOKEN')
    if not token:
        print("[ERRO] Token nao encontrado!")
        print("[INFO] Configure DISCORD_TOKEN nas variáveis de ambiente (Secrets no Replit)")
    else:
        try:
            print("[INFO] Iniciando bot...")
            bot.run(token)
        except Exception as e:
            print(f"[ERRO] Erro: {e}")