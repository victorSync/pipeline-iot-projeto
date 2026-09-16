"""
Script de ingestao de dados IoT.

Le o arquivo CSV do dataset "Temperature Readings: IoT Devices" (Kaggle),
trata e padroniza os dados, e insere na tabela `temperature_readings`
de um banco PostgreSQL rodando em Docker.
"""

import os
import sys

import pandas as pd
from sqlalchemy import create_engine, text

# --- Configuracao da conexao (ajuste via variaveis de ambiente) ---
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD", "sua_senha")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "iot_db")

DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

CSV_PATH = os.getenv("CSV_PATH", "data/IOT-temp.csv")
TABLE_NAME = "temperature_readings"


def load_csv(path: str) -> pd.DataFrame:
    if not os.path.exists(path):
        print(f"Arquivo nao encontrado: {path}")
        print(
            "Baixe o dataset no Kaggle (Temperature Readings: IoT Devices) e "
            "salve em data/IOT-temp.csv, ou rode 'python src/generate_sample_data.py' "
            "para gerar uma amostra de teste."
        )
        sys.exit(1)

    return pd.read_csv(path)


def clean_transform(df: pd.DataFrame) -> pd.DataFrame:
    # O dataset original do Kaggle traz as colunas:
    # id, room_id/id, noted_date, temp, out/in
    rename_map = {
        "room_id/id": "device_id",
        "noted_date": "reading_time",
        "temp": "temperature",
        "out/in": "location",
    }
    df = df.rename(columns=rename_map)

    required_cols = {"id", "device_id", "reading_time", "temperature", "location"}
    missing = required_cols - set(df.columns)
    if missing:
        raise ValueError(f"Colunas esperadas ausentes no CSV: {missing}")

    df = df.dropna(subset=["device_id", "reading_time", "temperature"])

    # Formato original: dd-mm-yyyy HH:MM
    df["reading_time"] = pd.to_datetime(
        df["reading_time"], format="%d-%m-%Y %H:%M", errors="coerce"
    )
    df = df.dropna(subset=["reading_time"])

    df["temperature"] = pd.to_numeric(df["temperature"], errors="coerce")
    df = df.dropna(subset=["temperature"])

    df = df.drop_duplicates(subset=["id"])

    return df[["id", "device_id", "reading_time", "temperature", "location"]]


def insert_into_postgres(df: pd.DataFrame, engine) -> None:
    df.to_sql(TABLE_NAME, engine, if_exists="replace", index=False, chunksize=5000)

    with engine.connect() as conn:
        conn.execute(text(f"CREATE INDEX IF NOT EXISTS idx_device_id ON {TABLE_NAME} (device_id);"))
        conn.execute(text(f"CREATE INDEX IF NOT EXISTS idx_reading_time ON {TABLE_NAME} (reading_time);"))
        conn.commit()


def main() -> None:
    print("Lendo arquivo CSV...")
    df_raw = load_csv(CSV_PATH)
    print(f"{len(df_raw)} linhas lidas.")

    print("Processando e limpando os dados...")
    df_clean = clean_transform(df_raw)
    print(f"{len(df_clean)} linhas validas apos limpeza.")

    print("Conectando ao PostgreSQL...")
    engine = create_engine(DATABASE_URL)

    print(f"Inserindo dados na tabela '{TABLE_NAME}'...")
    insert_into_postgres(df_clean, engine)

    print("Pipeline concluido com sucesso!")
    print(f"Total de registros inseridos: {len(df_clean)}")


if __name__ == "__main__":
    main()
