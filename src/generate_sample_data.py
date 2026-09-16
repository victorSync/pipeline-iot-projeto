"""
Gera um arquivo CSV de amostra com a MESMA estrutura do dataset
"Temperature Readings: IoT Devices" do Kaggle, para permitir testar
o pipeline localmente sem depender do download do arquivo completo.

Este script NAO substitui o dataset real: para a entrega final do
trabalho, utilize o arquivo oficial baixado do Kaggle em data/IOT-temp.csv.
"""

import random
from datetime import datetime, timedelta

import pandas as pd

random.seed(42)

DEVICES = ["Room Admin", "Room Cabin", "Room Garage", "Room Kitchen", "Room Lobby"]
LOCATIONS = ["In", "Out"]

N_ROWS = 5000
START = datetime(2018, 7, 1)


def generate() -> pd.DataFrame:
    rows = []
    current = START
    for i in range(N_ROWS):
        current += timedelta(minutes=random.randint(5, 45))
        device = random.choice(DEVICES)
        location = random.choice(LOCATIONS)
        base_temp = 24 if location == "In" else 30
        temp = round(base_temp + random.uniform(-6, 8), 1)
        rows.append(
            {
                "id": f"__export__.temp_log_{100000 + i}",
                "room_id/id": device,
                "noted_date": current.strftime("%d-%m-%Y %H:%M"),
                "temp": temp,
                "out/in": location,
            }
        )
    return pd.DataFrame(rows)


if __name__ == "__main__":
    df = generate()
    df.to_csv("data/IOT-temp.csv", index=False)
    print(f"Arquivo de amostra gerado: data/IOT-temp.csv ({len(df)} linhas)")
