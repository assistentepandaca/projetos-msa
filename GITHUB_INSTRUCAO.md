# INSTRUÇÃO — Criar Repositório GitHub

O token PAT não tem permissão para criar repositórios (falta escopo 'repo' ou 'public_repo').

## O que você precisa fazer:

1. Acesse: https://github.com/new
2. Preencha:
   - **Repository name:** `projetos-msa`
   - **Description:** Projetos MSA - Carla Felicio
   - **Public** ✅ (marcar)
   - **Add a README file:** ❌ (deixar desmarcado — já temos)
3. Clique em **Create repository**

## Depois de criar, me avise que eu executo:

```bash
cd /root/.openclaw/workspace/projetos-msa
git remote add origin https://github.com/assistentepandaca/projetos-msa.git
git push -u origin main
```

E pronto — projeto no ar! 🚀
