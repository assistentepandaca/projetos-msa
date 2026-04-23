# Cloudflare Pages — Configuração Manual

## Status
- ✅ Conta Cloudflare: assistente.pandaca@gmail.com
- ✅ Account ID: 397017ea644ac74593824a613fc81d51
- ✅ Repositório GitHub: assistentepandaca/projetos-msa
- ❌ Git integration: precisa autorizar via dashboard

---

## PASSO A PASSO (2 minutos)

### 1. Acesse o Dashboard
https://dash.cloudflare.com/

### 2. Vá em Pages
Menu lateral esquerdo → **Pages**

### 3. Connect to Git
Clique em **"Create a project"** ou **"Connect to Git"**

### 4. Autorize o GitHub
- Vai pedir para autorizar Cloudflare a acessar seus repos
- Aceite e autorize

### 5. Selecione o Repositório
- Escolha: **projetos-msa**
- Clique em **"Begin setup"**

### 6. Configure o Build
| Campo | Valor |
|-------|-------|
| Project name | `projetos-msa` |
| Production branch | `main` |
| Build command | *(deixar em branco)* |
| Build output directory | `landing-page` |

### 7. Deploy
Clique em **"Save and Deploy"**

---

## URL DO SITE

Depois de deployar, seu site vai estar em:
```
https://projetos-msa.pages.dev
```

---

## COMO FUNCIONA

- Cada vez que você fizer `git push` no repositório, o Cloudflare vai automaticamente atualizar o site
- Você pode editar os arquivos localmente, dar push, e o site atualiza sozinho
- Para adicionar seu domínio próprio: Pages → Custom domains