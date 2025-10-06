# 🚂 Guia Completo: Railway

## ✅ Como hospedar seu bot GRÁTIS no Railway

O Railway é uma plataforma de deploy moderna e super simples. **Melhor que Replit!**

### 🎁 Plano Gratuito

- ✅ **$5 de crédito grátis por mês** (mais do que suficiente para um bot Discord)
- ✅ **Sempre online 24/7** (não precisa de UptimeRobot)
- ✅ **Deploy automático** do GitHub
- ✅ **Logs em tempo real**
- ✅ **Reinício automático** em caso de erro

---

## 📋 Passo a Passo Completo

### 1️⃣ Criar conta no Railway

1. Acesse: **https://railway.app**
2. Clique em **"Login"** ou **"Start a New Project"**
3. Faça login com sua conta do **GitHub** (recomendado)
4. Confirme seu email

💡 **Dica:** Use sua conta do GitHub para deploy automático!

---

### 2️⃣ Preparar o Repositório GitHub

#### Se ainda não tem um repositório:

1. Crie um novo repositório no GitHub
2. Faça commit de todos os arquivos do projeto:
   ```bash
   git init
   git add .
   git commit -m "Initial commit - Bot de Castigos"
   git branch -M main
   git remote add origin https://github.com/SEU_USUARIO/SEU_REPOSITORIO.git
   git push -u origin main
   ```

#### Se já tem o repositório:

1. Certifique-se de que todos os arquivos estão commitados:
   ```bash
   git add .
   git commit -m "Adiciona suporte para Railway"
   git push
   ```

---

### 3️⃣ Obter Token do Discord

1. Acesse: **https://discord.com/developers/applications**
2. Clique em **"New Application"**
3. Dê um nome ao bot (ex: "Castigo Bot")
4. Vá para a aba **"Bot"** no menu lateral
5. Clique em **"Reset Token"** (ou **"View Token"** se for a primeira vez)
6. **COPIE O TOKEN** e guarde em algum lugar seguro!

⚠️ **IMPORTANTE:** Você só verá o token UMA VEZ. Se perder, terá que resetar.

---

### 4️⃣ Configurar Intents do Bot

Ainda no Discord Developer Portal:

1. Na aba **"Bot"**, role até **"Privileged Gateway Intents"**
2. **Habilite:**
   - ✅ **PRESENCE INTENT** (opcional)
   - ✅ **SERVER MEMBERS INTENT** ⚠️ **OBRIGATÓRIO**
   - ✅ **MESSAGE CONTENT INTENT** ⚠️ **OBRIGATÓRIO**
3. Clique em **"Save Changes"**

---

### 5️⃣ Criar Invite Link (Adicionar bot ao servidor)

1. Vá para **OAuth2 > URL Generator**
2. Selecione os **Scopes:**
   - ✅ `bot`
   - ✅ `applications.commands`
3. Selecione as **Permissões:**
   - ✅ Send Messages
   - ✅ Send Messages in Threads
   - ✅ Embed Links
   - ✅ Attach Files
   - ✅ Read Message History
   - ✅ Mention Everyone
   - ✅ Use Slash Commands
   - ✅ Manage Messages (para deletar mensagens)
   - ✅ Manage Roles (para adicionar cargo @castigo)
4. Copie a **URL gerada** no final da página
5. Cole no navegador e **adicione o bot ao seu servidor**

---

### 6️⃣ Criar Cargo @castigo no Discord

Para que o bot possa adicionar o cargo quando alguém for castigado:

1. No seu servidor Discord, vá em **Configurações do Servidor**
2. Clique em **Cargos (Roles)**
3. Clique em **Criar Cargo**
4. Nome: **castigo** (exatamente assim, tudo minúsculo)
5. Escolha uma cor (ex: vermelho)
6. Salve o cargo
7. **IMPORTANTE:** Arraste o cargo do bot para **ACIMA** do cargo @castigo

💡 A hierarquia deve ser:

```
Bot's Role
  └─ castigo
      └─ @everyone
```

---

### 7️⃣ Deploy no Railway

#### Criar Projeto:

1. No Railway, clique em **"New Project"**
2. Selecione **"Deploy from GitHub repo"**
3. Se for a primeira vez:
   - Clique em **"Configure GitHub App"**
   - Autorize o Railway a acessar seus repositórios
4. Selecione o repositório do seu bot
5. Clique no repositório para confirmar

#### Configurar Variáveis de Ambiente:

1. O deploy vai começar, mas vai falhar (normal, falta o token!)
2. Clique no projeto que acabou de criar
3. Vá na aba **"Variables"** (ícone de engrenagem)
4. Clique em **"New Variable"**
5. Adicione:
   - **Variable:** `DISCORD_TOKEN`
   - **Value:** Cole o token que você copiou antes
6. Clique em **"Add"**

#### Fazer Redeploy:

1. Vá na aba **"Deployments"**
2. Clique nos três pontinhos (...) no último deploy
3. Clique em **"Redeploy"**
4. Aguarde o deploy completar

---

### 8️⃣ Verificar se está Funcionando

#### Ver Logs:

1. Na aba **"Deployments"**, clique no deploy mais recente
2. Você verá os logs em tempo real
3. Procure por:
   ```
   [OK] SeuBot esta online!
   [INFO] Conectado a 1 servidor(es)
   [OK] 5 comando(s) sincronizado(s)
   [OK] Views persistentes registradas
   ```

✅ Se aparecer isso, está tudo certo!

#### Testar no Discord:

1. Vá para seu servidor Discord
2. Digite `/castigo`
3. Se o comando aparecer, **SUCESSO!** 🎉

---

## 🔄 Deploy Automático

O Railway tem **deploy automático** do GitHub:

1. Sempre que você fizer `git push`, o Railway detecta
2. Faz o build e deploy automaticamente
3. Seu bot reinicia com as novas mudanças

Para desabilitar (se quiser):

1. Vá em **Settings > Service**
2. Desmarque **"Automatically deploy"**

---

## 💰 Monitorar Custos

O plano gratuito dá **$5/mês de crédito**:

1. No dashboard, veja o uso no canto superior direito
2. Um bot Discord geralmente usa **$0.20 - $1.00 por mês**
3. Você pode ver detalhes em **Usage**

💡 **Dica:** Se gastar tudo, pode adicionar cartão para créditos ilimitados ou esperar o próximo mês.

---

## ⚙️ Configurações Úteis

### Variáveis de Ambiente Adicionais

Além do `DISCORD_TOKEN`, você pode adicionar outras variáveis no futuro.

### Reiniciar o Bot

1. Vá em **Deployments**
2. Clique em **"Restart"** (ícone de reload)

### Ver Logs Antigos

1. Vá em **Deployments**
2. Clique em qualquer deploy anterior
3. Veja os logs daquela versão

### Configurar Domínio Customizado (Opcional)

Se quiser acessar logs do bot via web:

1. Vá em **Settings**
2. Em **Networking**, clique em **"Generate Domain"**
3. Você terá uma URL pública (mas o bot não precisa disso)

---

## 🐛 Solução de Problemas

### ❌ Bot não fica online

**Possíveis causas:**

- Token incorreto → Verifique a variável `DISCORD_TOKEN`
- Intents desabilitadas → Habilite no Discord Developer Portal
- Deploy falhou → Veja os logs no Railway

**Como resolver:**

1. Vá em **Deployments** e veja os logs
2. Procure por `[ERRO]` nos logs
3. Se o token estiver errado, atualize em **Variables**
4. Faça **Redeploy**

---

### ❌ Comandos Slash não aparecem

**Possíveis causas:**

- Bot não tem permissão `applications.commands`
- Discord está com cache

**Como resolver:**

1. Expulse o bot do servidor
2. Use o link de convite novamente (com `applications.commands`)
3. Aguarde 1-2 minutos
4. Tente `/castigo` novamente

---

### ❌ Bot não adiciona cargo @castigo

**Possíveis causas:**

- Cargo não existe ou nome está errado
- Bot não tem permissão "Manage Roles"
- Cargo do bot está abaixo do cargo @castigo

**Como resolver:**

1. Crie o cargo exatamente como: **castigo** (minúsculo)
2. Arraste o cargo do bot para **acima** do cargo @castigo
3. Verifique se o bot tem permissão "Manage Roles"

---

### ❌ Deploy falha

**Possíveis causas:**

- Erro no código
- Arquivo requirements.txt incorreto
- Falta Procfile

**Como resolver:**

1. Veja os logs do deploy
2. Procure por erros Python
3. Certifique-se que todos os arquivos foram commitados:
   - `bot.py`
   - `requirements.txt`
   - `Procfile`
   - `runtime.txt`
   - `railway.json`

---

### ❌ Bot desconecta sozinho

**Possíveis causas:**

- Erro não tratado no código
- Problema de conexão temporário

**Como resolver:**

1. Veja os logs antes da desconexão
2. O Railway reinicia automaticamente em caso de erro
3. Se persistir, abra uma issue no GitHub

---

### ❌ Créditos acabaram

**O que fazer:**

- Railway dá $5/mês de crédito gratuito
- Se acabar, o bot para até o próximo mês
- Você pode adicionar um cartão para crédito ilimitado (paga só o que usar)

---

## 📊 Estrutura de Arquivos

Certifique-se de ter todos esses arquivos no repositório:

```
projeto/
├── bot.py              # Código principal
├── requirements.txt    # Dependências Python
├── Procfile           # Comando de execução (Railway)
├── runtime.txt        # Versão do Python
├── railway.json       # Configuração Railway
├── .gitignore         # Arquivos ignorados
├── README.md          # Documentação principal
└── RAILWAY.md         # Este guia
```

---

## 📚 Comandos do Bot

| Comando               | Descrição                                       |
| --------------------- | ----------------------------------------------- |
| `/castigo`            | Mostra informações e botão para abrir castigo   |
| `/abrir_castigo`      | Inicia criação de castigo diretamente           |
| `/cancelar_castigo`   | Cancela criação em andamento                    |
| `/castigo_configurar` | [ADMIN] Configura canais de votação e resultado |
| `/castigo_ajuda`      | Mostra lista de comandos                        |

---

## 🎯 Recursos do Bot

### Funcionalidades Principais:

- ✅ Criação guiada de castigos (4 passos)
- ✅ Votação restrita aos 4 participantes
- ✅ Atualização em tempo real dos votos
- ✅ Aprovação com 3+ votos "Sim"
- ✅ Mensagens auto-deletadas para privacidade
- ✅ Adiciona cargo @castigo automaticamente
- ✅ Canal separado para resultados (configurável)
- ✅ Botões persistentes (funcionam após reiniciar)
- ✅ Validação de links (op.gg, u.gg, leagueofgraphs)

### Configurações Admin:

- `/castigo_configurar canal_votacao:#canal` - Define onde abrir votações
- `/castigo_configurar canal_resultado:#canal` - Define onde enviar resultados

---

## 🔗 Links Úteis

- **Railway:** https://railway.app
- **Dashboard:** https://railway.app/dashboard
- **Documentação:** https://docs.railway.app
- **Discord Developer Portal:** https://discord.com/developers/applications
- **Discord.py Docs:** https://discordpy.readthedocs.io/

---

## ✨ Vantagens do Railway vs Replit

| Característica     | Railway    | Replit                 |
| ------------------ | ---------- | ---------------------- |
| Sempre online      | ✅ Sim     | ⚠️ Precisa UptimeRobot |
| Deploy automático  | ✅ GitHub  | ❌ Manual              |
| Logs em tempo real | ✅ Sim     | ✅ Sim                 |
| Custo mensal       | $0.20-1.00 | Grátis\*               |
| Facilidade setup   | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐               |
| Performance        | ⭐⭐⭐⭐⭐ | ⭐⭐⭐                 |
| Confiabilidade     | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐               |

\*Replit gratuito desliga com inatividade

---

## 🎉 Conclusão

Parabéns! Seu bot está rodando 24/7 no Railway! 🚀

**Próximos passos:**

1. Teste todos os comandos no Discord
2. Configure os canais com `/castigo_configurar`
3. Crie o cargo @castigo no servidor
4. Monitore os logs no Railway
5. Customize o bot como quiser!

**Dúvidas?** Veja a seção de problemas comuns ou abra uma issue no GitHub.

---

**Feito com ❤️ para a comunidade Discord**
