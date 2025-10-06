# 🎯 Bot de Castigos - Discord

Um bot do Discord em Python para gerenciar votações de castigos com **sistema de botões interativos** e **validação automática**.

## 🚀 Quick Start

**Quer colocar o bot no ar AGORA?**

1. 📖 Leia o **[Guia do Railway](RAILWAY.md)** (5 minutos)
2. ✅ Faça deploy gratuito no [Railway](https://railway.app)
3. 🤖 Seu bot estará online 24/7!

💡 **Railway = Melhor opção!** Deploy automático do GitHub, sempre online, sem precisar de truques.

---

## ✨ Funcionalidades

- ✅ **Botão "📜 Abrir Castigo"** - Interface intuitiva
- ✅ **Modal interativo** - Formulário para coletar informações
- ✅ **Votação restrita** - Apenas os 4 participantes mencionados podem votar
- ✅ **Contagem em tempo real** - Votos atualizados automaticamente
- ✅ **Finalização automática** - Resultado mostrado quando todos votarem
- ✅ **Código limpo e organizado** - Fácil de customizar
- ✅ **Comandos Slash** - Interface moderna do Discord

## 📋 Fluxo Completo

### 1️⃣ Iniciar Castigo

```
/abrir_castigo
```

O bot envia uma mensagem com o botão **"📜 Abrir Castigo"**.

### 2️⃣ Preencher Formulário

Ao clicar no botão, abre um modal com:

- **Usuário Trollador**: @usuario ou ID
- **4 Usuários da Partida**: @user1, @user2, @user3, @user4 (separados por vírgula)
- **Motivo**: Descrição do que aconteceu
- **URL da Partida**: Link da partida

### 3️⃣ Publicação Automática

O bot publica automaticamente:

```
🎯 Castigo Aberto
👤 Usuário Acusado: @trollador
👥 Presentes na Partida: @user1, @user2, @user3, @user4
📄 Motivo: {motivo}
🔗 URL da Partida: {url}
📊 Votação:
✅ Sim: 0
❌ Não: 0
⏳ Votos: 0/4

[✅ Sim] [❌ Não]
```

### 4️⃣ Votação

- Apenas os **4 participantes mencionados** podem votar
- Cada pessoa vota apenas **uma vez**
- Votos são contabilizados em **tempo real**
- Outros usuários recebem mensagem de erro ao tentar votar

### 5️⃣ Resultado Automático

Quando todos os 4 votarem, o bot:

- **Encerra a votação** automaticamente
- **Mostra o resultado** (APROVADO/REJEITADO/EMPATE)
- **Remove os botões** de votação
- **Envia mensagem final** com o resultado

## 🚀 Instalação

### 🚂 Opção 1: Railway (Recomendado - Melhor plataforma!)

Hospedar no Railway é a **melhor opção**: deploy automático do GitHub, sempre online 24/7, sem gambiarras!

📖 **[Guia Completo do Railway](RAILWAY.md)** - Passo a passo detalhado em português

#### ✨ Por que Railway?

- ✅ **$5 de crédito grátis por mês** (suficiente para o bot)
- ✅ **Sempre online 24/7** (não precisa de UptimeRobot)
- ✅ **Deploy automático** - Push no GitHub = Deploy automático
- ✅ **Logs em tempo real**
- ✅ **Reinício automático** em caso de erro
- ✅ **Performance excelente**

#### Passo a Passo Rápido:

1. **Fazer commit do código no GitHub**

   ```bash
   git add .
   git commit -m "Bot de castigos"
   git push
   ```

2. **Criar conta no Railway**

   - Acesse [railway.app](https://railway.app)
   - Faça login com GitHub

3. **Criar projeto**

   - Clique em **"New Project"**
   - Selecione **"Deploy from GitHub repo"**
   - Escolha seu repositório

4. **Configurar variável de ambiente**

   - Vá em **Variables**
   - Adicione: `DISCORD_TOKEN` = seu_token_aqui

5. **Fazer Redeploy**
   - Vá em **Deployments**
   - Clique em **"Redeploy"**
   - Pronto! Bot online! 🎉

📖 **Detalhes completos:** Veja [RAILWAY.md](RAILWAY.md) para instruções detalhadas.

---

### 💻 Opção 2: Instalação Local

#### 1. Instalar Dependências

```bash
pip install -r requirements.txt
```

#### 2. Configurar Token

Crie um arquivo `.env` na raiz do projeto:

```
DISCORD_TOKEN=seu_token_aqui
```

#### 3. Executar Bot

```bash
python bot.py
```

---

### 4. Configurar no Discord

1. Acesse o [Discord Developer Portal](https://discord.com/developers/applications)
2. Crie uma nova aplicação
3. Vá para a aba "Bot" e crie um bot
4. Copie o token e adicione no arquivo `.env`
5. Em "OAuth2 > URL Generator":
   - Selecione: `bot` e `applications.commands`
   - Permissões: `Send Messages`, `Embed Links`, `Read Message History`, `Use Slash Commands`
6. Use a URL gerada para convidar o bot

## 📝 Comandos

| Comando           | Descrição                         | Permissão     |
| ----------------- | --------------------------------- | ------------- |
| `/abrir_castigo`  | 🎯 Abre o sistema de castigos     | Todos         |
| `/castigo_config` | ⚙️ Configura o canal dos castigos | Administrador |
| `/castigo_ajuda`  | ℹ️ Mostra informações sobre o bot | Todos         |

## ⚙️ Customização

### Restringir a um Canal Específico

**Opção 1: Comando (Recomendado)**

1. Vá para o canal desejado
2. Execute: `/castigo_config`
3. Pronto! O bot só funcionará nesse canal

**Opção 2: Configuração Manual**

No arquivo `bot.py`, linha 28:

```python
ALLOWED_CHANNEL_ID = 1234567890123456789  # Coloque o ID do canal
```

Para pegar o ID do canal:

- Ative o Modo Desenvolvedor no Discord (Configurações > Avançado)
- Clique com botão direito no canal > Copiar ID do canal

Para remover a restrição:

```python
ALLOWED_CHANNEL_ID = None  # Bot funciona em qualquer canal
```

### Alterar Quantidade de Votantes

No arquivo `bot.py`, linha 24:

```python
REQUIRED_VOTERS = 4  # Altere para a quantidade desejada
```

### Personalizar Cores

```python
# Castigo aberto (linha ~120)
color=0xff6b6b  # Vermelho

# Aprovado (linha ~290)
color=0x00ff00  # Verde

# Rejeitado (linha ~293)
color=0xff0000  # Vermelho escuro

# Empate (linha ~296)
color=0xffaa00  # Laranja
```

### Personalizar Textos

Todos os textos estão em strings facilmente identificáveis no código:

- Títulos dos embeds
- Mensagens de erro
- Labels dos botões
- Placeholders do formulário

## 📂 Estrutura do Código

```python
# ==================== CONFIGURAÇÕES ====================
REQUIRED_VOTERS = 4  # Quantidade de votantes

# ==================== CLASSES DE DADOS ====================
class Castigo:  # Armazena informações do castigo

# ==================== MODAL PARA CRIAR CASTIGO ====================
class CastigoModal:  # Formulário interativo
    def extract_user_id()  # Extrai ID de usuário
    def extract_multiple_user_ids()  # Extrai múltiplos IDs
    def publish_castigo()  # Publica o castigo

# ==================== VIEW COM BOTÕES DE VOTAÇÃO ====================
class VotingView:  # Botões Sim/Não
    def process_vote()  # Processa um voto
    def update_castigo_embed()  # Atualiza contagem
    def finalize_voting()  # Finaliza e mostra resultado

# ==================== VIEW COM BOTÃO INICIAL ====================
class OpenCastigoView:  # Botão "Abrir Castigo"

# ==================== COMANDOS SLASH ====================
/castigo  # Envia botão inicial
/ajuda    # Mostra ajuda
```

## 🎨 Preview

### Mensagem Inicial

```
📜 Sistema de Castigos
Clique no botão abaixo para abrir um novo castigo.

ℹ️ Como funciona
1. Clique em 📜 Abrir Castigo
2. Preencha o formulário
3. Aguarde os votos dos participantes
4. O resultado será mostrado automaticamente

[📜 Abrir Castigo]
```

### Formulário (Modal)

```
📜 Abrir Castigo

Usuário Trollador: @usuario ou ID do usuário
4 Usuários da Partida: @user1, @user2, @user3, @user4
Motivo: Descreva o motivo do castigo...
URL da Partida: https://...

[Enviar]
```

### Castigo Publicado

```
🎯 Castigo Aberto

👤 Usuário Acusado: @João
👥 Presentes na Partida: @Maria, @Pedro, @Ana, @Carlos
📄 Motivo: Trollou a partida inteira
🔗 URL da Partida: https://exemplo.com/partida
📊 Votação:
✅ Sim: 2
❌ Não: 1
⏳ Votos: 3/4

[✅ Sim] [❌ Não]
```

### Resultado Final

```
✅ Votação Finalizada - APROVADO

👤 Usuário Acusado: @João
📊 Resultado Final:
✅ Sim: 3
❌ Não: 1
📄 Motivo: Trollou a partida inteira
🔗 URL da Partida: https://exemplo.com/partida

---

## ✅ Votação Encerrada!
Resultado: APROVADO
Votos: ✅ 3 x ❌ 1
```

## 🔧 Requisitos

- Python 3.8+
- discord.py 2.3.2
- python-dotenv 1.0.0

## 📊 Funcionalidades Técnicas

- **Comandos Slash** - Interface moderna do Discord
- **Modais Interativos** - Formulários nativos do Discord
- **Views Persistentes** - Botões que funcionam mesmo após reiniciar o bot
- **Validação de Usuários** - Verifica IDs e mentions automaticamente
- **Extração Inteligente** - Aceita @mentions ou IDs diretos
- **Armazenamento em Memória** - Castigos ativos em dicionário
- **Atualização em Tempo Real** - Embeds atualizados automaticamente
- **Finalização Automática** - Detecta quando todos votaram
- **Prevenção de Votos Duplicados** - Cada usuário vota apenas uma vez
- **Restrição de Votantes** - Apenas participantes mencionados podem votar

## 🎯 Validações Implementadas

✅ Verifica se o usuário trollador existe  
✅ Verifica se exatamente 4 participantes foram mencionados  
✅ Verifica se o trollador não está na lista de participantes  
✅ Verifica se o votante está na lista de participantes  
✅ Verifica se o votante já votou  
✅ Verifica se a votação já foi encerrada

## 💡 Dicas de Uso

1. **Restringir Canal**: Use `/castigo_config` no canal desejado (apenas admin)
2. **Mencionar Usuários**: Você pode usar `@usuario` ou apenas o ID do usuário
3. **Separar Participantes**: Use vírgula para separar os 4 participantes
4. **Votos Privados**: As confirmações de voto aparecem apenas para quem votou
5. **Resultado Automático**: Não precisa fazer nada, o bot finaliza sozinho

## 🆘 Solução de Problemas

**Bot não responde aos comandos slash:**

- Execute `/castigo` novamente
- Verifique se o bot tem permissão de "Use Slash Commands"
- Aguarde alguns minutos após adicionar o bot (sincronização)

**Erro ao mencionar usuários:**

- Use o formato: `@usuario` ou apenas o ID
- Separe os 4 participantes por vírgula
- Certifique-se de que os usuários estão no servidor

**Botões não funcionam:**

- Verifique se o bot tem permissão de "Send Messages"
- Verifique se o bot está online

**Comando não funciona em um canal:**

- Verifique se o bot está restrito a um canal específico
- Use `/castigo_ajuda` para ver qual canal está configurado
- Administradores podem usar `/castigo_config` para mudar

## 📄 Licença

Este projeto é de código aberto e pode ser modificado livremente.
