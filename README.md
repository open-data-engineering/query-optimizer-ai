# 🚀 Query Optimizer AI

[![Deploy - Cloud Run](https://img.shields.io/badge/Cloud%20Run-Deployed-brightgreen?logo=googlecloud&style=flat-square)](https://query-optimizer-ai-517665453940.us-central1.run.app/)
![Docker Build Status](https://img.shields.io/badge/Docker-Build-blue)

**Query Optimizer AI** é uma plataforma interativa que utiliza modelos de linguagem (LLMs) como OpenAI GPT-4 e Gemini para analisar, sugerir melhorias e estimar o custo de queries SQL — com suporte completo ao Google BigQuery.

## 🔗 Acesse a aplicação:
👉 [query-optimizer-ai](https://query-optimizer-ai-517665453940.us-central1.run.app)


## 🎯 Funcionalidades

- ✅ Análise manual de queries SQL com IA (OpenAI ou Gemini)
- 📊 Análise histórica de queries executadas no BigQuery
- 🔍 Detecção de queries pesadas com alto custo e processamento
- 💡 Geração de sugestões de otimização com estimativas de economia
- ⚡ Execução simulada (dry run) das sugestões, com preview de resultados
- 📄 Exibição automática dos esquemas das tabelas envolvidas
- 📦 Estimativa precisa de bytes processados e custo estimado por consulta

## 🖥️ Interface

A interface é feita com [Streamlit](https://streamlit.io/), com navegação lateral:

- **Análise Manual**: cole sua query SQL e receba sugestões.
- **Análise Histórica**: conecte-se ao histórico de jobs do BigQuery e analise queries automaticamente.

## 🧠 Modelos de IA Suportados

- **GPT-4 (OpenAI)**
- **Gemini (Google)**

Você pode alternar entre os modelos facilmente pelo seletor no app.

## 🔧 Pré-requisitos

- Python 3.10+
- Conta no Google Cloud com acesso ao BigQuery
- Chaves de API:
  - OpenAI: `OPENAI_API_KEY`
  - Gemini: `GOOGLE_API_KEY`

## 📦 Instalação

```bash
git clone https://github.com/seu-usuario/query-optimizer-ai.git
cd query-optimizer-ai
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

Crie um .env na raiz do projeto:

OPENAI_API_KEY=sk-...
GOOGLE_API_KEY=AIza...
```

## ▶️ Como Rodar

```python
streamlit run app/main.py
```

## 🧱 Estrutura do Projeto

```bash
app/
│
├── ui/                  # Interfaces de navegação (manual, histórico, login)
├── core/                # Utilitários e integração com BigQuery
├── suggestor/           # Motores de sugestão (openai, gemini)
├── collectors/          # Coleta de jobs do BigQuery
├── parser/              # Analisador de performance
```

## 📈 Exemplo de Uso

Query de entrada:

```sql
SELECT * FROM `project.dataset.sales`
WHERE EXTRACT(YEAR FROM date) = 2023
```

Sugestão gerada:
```bash
“Evite funções no filtro WHERE. Use BETWEEN '2023-01-01' AND '2023-12-31' para melhorar o uso do particionamento.”
```


## 🧪 Testes

Em breve!


## ✨ Contribuições

Sinta-se à vontade para abrir issues e pull requests. Feedbacks são muito bem-vindos!

## ⚡ Configuração do pre-commit

Para garantir que todo código segue os padrões definidos antes de ser commitado, este projeto utiliza pre-commit hooks.

## 📥 Instalação do pre-commit
###	1.	Instale o pre-commit globalmente (caso ainda não tenha):
```bash
pip install pre-commit
```

###	2.	Instale os hooks do pre-commit no repositório:
```bash
pre-commit install
```

Agora, toda vez que você fizer um commit (git commit -m "mensagem"), o pre-commit verificará automaticamente o código.

## 🔍 Testando o pre-commit

Caso queira rodar manualmente todas as verificações, execute:
```bash
pre-commit run --all-files
```

## 🛠 Hooks configurados

Os hooks de pré-commit configurados incluem:
	•	black: Formatação automática do código Python
	•	isort: Organização dos imports
	•	flake8: Análise estática do código
	•	mypy: Verificação de tipagem

Se precisar adicionar ou remover hooks, edite o arquivo .pre-commit-config.yaml.

## 📝 Licença

[MIT](./LICENSE)


## 👨‍💻 Autor

Desenvolvido por Tiago Navarro

[LinkedIn](https://www.linkedin.com/in/tiagornavarro/) | [GitHub](https://github.com/tiagornandrade)
