# Pipeline de Dados IoT — Temperatura com Docker, PostgreSQL e Streamlit

Pipeline completo de dados para leituras de temperatura de dispositivos IoT: ingestão de um CSV, armazenamento em PostgreSQL (via Docker), consultas analíticas em SQL e visualização interativa em um dashboard Streamlit.

## Descrição do projeto

O objetivo é demonstrar, de ponta a ponta, um fluxo de Big Data aplicado a IoT: coleta de leituras de sensores de temperatura, tratamento e padronização dos dados, persistência em um banco relacional containerizado e exposição de insights através de um dashboard interativo. O dataset utilizado é o **"Temperature Readings: IoT Devices"**, disponível no Kaggle.

## Tecnologias utilizadas

- **Python 3.10+** — processamento e ingestão dos dados
- **Docker / Docker Compose** — containerização do banco de dados
- **PostgreSQL 15** — armazenamento relacional
- **SQLAlchemy** — camada de conexão e ORM leve
- **Pandas** — limpeza e transformação dos dados
- **Streamlit** — dashboard web interativo
- **Plotly Express** — gráficos interativos

## Estrutura do repositório

```
.
├── data/                      # coloque aqui o IOT-temp.csv baixado do Kaggle
├── docs/
│   └── screenshots/           # capturas de tela do dashboard em execução
├── sql/
│   └── views.sql              # as 3 views SQL do projeto
├── src/
│   ├── ingest.py              # script de ingestão CSV -> PostgreSQL
│   ├── dashboard.py           # dashboard Streamlit
│   └── generate_sample_data.py# gera dados sintéticos de teste (opcional)
├── docker-compose.yml
├── requirements.txt
├── .gitignore
└── README.md
```

## Pré-requisitos

- Git instalado
- Python 3.10 ou superior
- Docker e Docker Compose instalados
- Conta no Kaggle (para baixar o dataset)

## Como executar

### 1. Clonar o repositório

```bash
git clone <URL_DO_SEU_REPOSITORIO>
cd <nome-do-repositorio>
```

### 2. Criar o ambiente virtual

```bash
python -m venv venv
source venv/bin/activate      # Linux/Mac
venv\Scripts\activate         # Windows
```

### 3. Instalar as dependências

```bash
pip install -r requirements.txt
```

### 4. Subir o banco PostgreSQL com Docker

```bash
docker compose up -d
```

Isso cria o contêiner `postgres-iot`, expõe a porta `5432` e cria automaticamente o banco `iot_db`.

Alternativa sem `docker-compose` (comando único, conforme enunciado):

```bash
docker run --name postgres-iot -e POSTGRES_PASSWORD=sua_senha -e POSTGRES_DB=iot_db -p 5432:5432 -d postgres
```

### 5. Obter os dados

1. Acesse o dataset no Kaggle: `Temperature Readings: IoT Devices` (atulanandjha/temperature-readings-iot-devices)
2. Baixe o arquivo `IOT-temp.csv`
3. Salve-o em `data/IOT-temp.csv`

Para apenas testar o pipeline sem o dataset completo, é possível gerar uma amostra sintética com a mesma estrutura de colunas:

```bash
python src/generate_sample_data.py
```

### 6. Executar a ingestão dos dados

```bash
python src/ingest.py
```

O script lê o CSV, padroniza os nomes de colunas, converte datas, remove nulos/duplicados e insere os registros na tabela `temperature_readings` do PostgreSQL.

### 7. Criar as views SQL

```bash
docker exec -i postgres-iot psql -U postgres -d iot_db < sql/views.sql
```

### 8. Executar o dashboard

```bash
streamlit run src/dashboard.py
```

Acesse `http://localhost:8501` no navegador.

## Views SQL criadas

### `avg_temp_por_dispositivo`

Calcula a temperatura média e o total de leituras registradas por cada dispositivo (`device_id`). Permite identificar quais ambientes monitorados operam com temperaturas mais altas ou mais baixas em média — útil para detectar sensores fora do padrão esperado.

### `leituras_por_hora`

Conta a quantidade de leituras recebidas em cada hora do dia (0–23). Evidencia os horários de maior atividade dos sensores e ajuda a identificar padrões de uso ou eventuais falhas de transmissão em horários específicos.

### `temp_max_min_por_dia`

Agrega a temperatura máxima, mínima e média registrada em cada dia. Permite observar a amplitude térmica diária e identificar picos de calor ou frio ao longo do período monitorado.

## Capturas de tela

> Adicione aqui as capturas de tela do dashboard em execução (salve os arquivos em `docs/screenshots/` e referencie-os abaixo).

## Insights obtidos

- Ambientes classificados como "Out" (externos) tendem a apresentar temperatura média mais alta e maior variação que os ambientes "In" (internos).
- A distribuição de leituras por hora revela se a coleta dos sensores é constante ao longo do dia ou concentrada em determinados períodos, o que pode indicar configuração de amostragem ou problemas de conectividade.
- A amplitude térmica diária (diferença entre máxima e mínima) é um indicador direto de estabilidade ambiental — dias com alta amplitude podem sinalizar necessidade de climatização ou manutenção do sensor.
- Em um cenário real, esses indicadores poderiam alimentar alertas automáticos (ex.: temperatura fora da faixa esperada) e otimizar o uso de sistemas de climatização com base nos horários de pico.

## Comandos Git utilizados

```bash
git init
git add .
git commit -m "Projeto inicial: Pipeline de Dados IoT"
git remote add origin URL_DO_SEU_REPOSITORIO
git push -u origin main
```

## Fonte dos dados

Dataset "Temperature Readings: IoT Devices" — Kaggle:
https://www.kaggle.com/datasets/atulanandjha/temperature-readings-iot-devices

## Disciplina

Disruptive Architectures: IoT, Big Data e IA
