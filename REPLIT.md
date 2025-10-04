# 🌐 Guia Rápido: Replit

## ✅ Como colocar o bot no ar em 5 minutos

### 1️⃣ Criar conta no Replit
- Acesse: https://replit.com
- Faça cadastro gratuito (pode usar conta do GitHub/Google)

### 2️⃣ Importar este projeto
**Opção A - Do GitHub:**
1. Clique em **"+ Create Repl"**
2. Selecione **"Import from GitHub"**
3. Cole a URL do repositório
4. Clique em **"Import from GitHub"**

**Opção B - Upload Manual:**
1. Clique em **"+ Create Repl"**
2. Selecione **"Python"**
3. Nomeie o projeto: `castigo-bot`
4. Faça upload de todos os arquivos

### 3️⃣ Configurar Token do Discord

#### Obter o Token:
1. Acesse: https://discord.com/developers/applications
2. Clique em **"New Application"**
3. Dê um nome ao bot
4. Vá para aba **"Bot"** no menu lateral
5. Clique em **"Reset Token"** ou **"View Token"**
6. **COPIE O TOKEN** (você só verá isso uma vez!)

#### Configurar no Replit:
1. No Replit, abra o painel lateral esquerdo
2. Clique no ícone **🔒 "Secrets"** (ou Tools > Secrets)
3. Clique em **"New Secret"**
4. Preencha:
   - **Key:** `DISCORD_TOKEN`
   - **Value:** Cole o token que você copiou
5. Clique em **"Add secret"**

⚠️ **NUNCA compartilhe seu token!** Ele dá acesso total ao seu bot.

### 4️⃣ Configurar Permissões do Bot

No Discord Developer Portal:
1. Vá para **OAuth2 > URL Generator**
2. Selecione:
   - ✅ `bot`
   - ✅ `applications.commands`
3. Em **Bot Permissions**, selecione:
   - ✅ Send Messages
   - ✅ Embed Links
   - ✅ Read Message History
   - ✅ Use Slash Commands
   - ✅ Manage Messages (para deletar mensagens)
   - ✅ Mention Everyone (opcional)
4. Copie a URL gerada no final da página
5. Cole no navegador e adicione o bot ao seu servidor

### 5️⃣ Habilitar Intents

No Discord Developer Portal:
1. Vá para aba **"Bot"**
2. Role até **"Privileged Gateway Intents"**
3. Habilite:
   - ✅ **MESSAGE CONTENT INTENT**
   - ✅ **SERVER MEMBERS INTENT**
4. Clique em **"Save Changes"**

### 6️⃣ Executar o Bot

1. No Replit, clique no botão verde **▶ Run**
2. Aguarde as dependências serem instaladas
3. Você deve ver no console:
   ```
   [OK] SeuBot esta online!
   [INFO] Conectado a 1 servidor(es)
   [OK] 5 comando(s) sincronizado(s)
   ```

🎉 **Pronto! Seu bot está online!**

### 7️⃣ Testar o Bot no Discord

1. Vá para o seu servidor Discord
2. Digite `/castigo` em qualquer canal
3. Se aparecer o comando, está funcionando! ✅

---

## 🔄 Manter o Bot Online 24/7

O bot tem um servidor web integrado, mas o Replit pode desligar após inatividade.

### Solução: UptimeRobot (Gratuito)

1. Acesse: https://uptimerobot.com
2. Crie uma conta gratuita
3. Clique em **"+ Add New Monitor"**
4. Configure:
   - **Monitor Type:** HTTP(s)
   - **Friendly Name:** Castigo Bot
   - **URL:** URL do seu Repl (copie da aba do navegador quando o bot estiver rodando)
   - **Monitoring Interval:** 5 minutes
5. Clique em **"Create Monitor"**

Pronto! O UptimeRobot vai fazer "ping" no seu bot a cada 5 minutos, mantendo-o ativo.

---

## 📊 Comandos do Bot

| Comando | Descrição |
|---------|-----------|
| `/castigo` | Mostra info completa e botão para abrir castigo |
| `/abrir_castigo` | Inicia criação de castigo diretamente |
| `/cancelar_castigo` | Cancela a criação em andamento |
| `/castigo_configurar` | [ADMIN] Configura canais |
| `/castigo_ajuda` | Mostra lista de comandos |

---

## ❓ Problemas Comuns

### ❌ Bot não aparece online
- Verifique se o token está correto em Secrets
- Verifique se as Intents estão habilitadas no Discord Developer Portal
- Veja o console do Replit para erros

### ❌ Comandos não aparecem
- Aguarde 1-2 minutos após iniciar o bot
- Execute `/castigo` para forçar sincronização
- Verifique permissões do bot no servidor

### ❌ Bot não responde a menções
- Verifique se **MESSAGE CONTENT INTENT** está habilitado
- O bot precisa dessa permissão para ler mensagens

### ❌ "Token nao encontrado"
- Verifique se criou o Secret com o nome exato: `DISCORD_TOKEN`
- Nomes são case-sensitive (maiúsculas/minúsculas importam)

### ❌ Bot desliga sozinho
- Configure o UptimeRobot (veja seção acima)
- O Replit gratuito desliga após inatividade

---

## 🔧 Editar o Bot

Para modificar o código:
1. Edite os arquivos direto no Replit
2. Clique em **Run** novamente
3. O bot reinicia automaticamente com as mudanças

**Arquivos principais:**
- `bot.py` - Código principal do bot
- `requirements.txt` - Dependências Python
- `.replit` - Configuração do Replit
- `replit.nix` - Pacotes do sistema

---

## 📚 Recursos Úteis

- [Discord.py Docs](https://discordpy.readthedocs.io/)
- [Discord Developer Portal](https://discord.com/developers/applications)
- [Replit Docs](https://docs.replit.com/)
- [UptimeRobot](https://uptimerobot.com/)

---

## 🆘 Suporte

Se tiver problemas:
1. Leia os erros no console do Replit
2. Verifique se todas as etapas foram seguidas
3. Veja a seção "Problemas Comuns" acima
4. Abra uma issue no GitHub do projeto

---

**Boa sorte! 🚀**
