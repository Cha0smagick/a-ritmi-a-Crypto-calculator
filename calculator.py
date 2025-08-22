import pandas as pd
import requests
from datetime import datetime, timedelta
import pytz
import openpyxl
import os

# Configuración de la API
BINANCE_API_URL = "https://api.binance.com/api/v3"

def get_crypto_price(symbol, date):
    """
    Obtiene el precio de una criptomoneda en una fecha específica
    """
    try:
        # Convertir la fecha a timestamp de Binance (en miliseegundos)
        target_date = datetime.strptime(str(date).split()[0], "%Y-%m-%d")
        target_date = target_date.replace(hour=12, minute=0, second=0, microsecond=0)
        
        # Ajustar a hora de California (UTC-7 o UTC-8 dependiendo del DST)
        # Para simplificar, usaremos UTC-8 (PST) como hora estándar de California
        california_tz = pytz.timezone('America/Los_Angeles')
        target_date_ca = california_tz.localize(target_date)
        target_date_utc = target_date_ca.astimezone(pytz.utc)
        
        start_time = int(target_date_utc.timestamp() * 1000)
        end_time = start_time + 3600000  # 1 hora después para asegurar datos
        
        # Construir el símbolo para Binance (ej: ETHUSDT)
        binance_symbol = f"{symbol}USDT"
        
        # Hacer la solicitud a la API de Binance
        params = {
            'symbol': binance_symbol,
            'interval': '1h',
            'startTime': start_time,
            'endTime': end_time,
            'limit': 1
        }
        
        response = requests.get(f"{BINANCE_API_URL}/klines", params=params)
        response.raise_for_status()
        
        data = response.json()
        
        if data:
            # El precio de cierre está en la posición 4 del array
            close_price = float(data[0][4])
            return close_price
        else:
            print(f"No se encontraron datos para {symbol} en {date}")
            return None
            
    except requests.exceptions.RequestException as e:
        print(f"Error en la solicitud para {symbol}: {e}")
        return None
    except Exception as e:
        print(f"Error procesando {symbol} en {date}: {e}")
        return None

def process_excel_file():
    """
    Procesa el archivo Excel y completa los valores faltantes
    """
    try:
        # Leer el archivo Excel
        file_path = "data.xlsx"
        df = pd.read_excel(file_path, sheet_name='Hoja1')
        
        print("Procesando datos...")
        
        # Iterar sobre cada fila y completar los valores
        for index, row in df.iterrows():
            crypto = row['crypto']
            quantity = row['Quantity']
            date = row['Date']
            
            # Si ya tiene valor, saltar
            if pd.notna(row['Crypto Value (USDT)']):
                continue
                
            print(f"Obteniendo precio para {crypto} en {date}...")
            
            # Obtener el precio de la criptomoneda
            crypto_price = get_crypto_price(crypto, date)
            
            if crypto_price is not None:
                # Actualizar los valores en el DataFrame
                df.at[index, 'Crypto Value (USDT)'] = crypto_price
                df.at[index, 'Quantity Value (USDT)'] = quantity * crypto_price
                
                print(f"  Precio encontrado: {crypto_price} USDT")
                print(f"  Valor de {quantity} {crypto}: {quantity * crypto_price} USDT")
            else:
                print(f"  No se pudo obtener el precio para {crypto}")
        
        # Calcular sumatorias
        total_quantity = df['Quantity'].sum()
        total_crypto_value = df['Crypto Value (USDT)'].sum()
        total_quantity_value = df['Quantity Value (USDT)'].sum()
        
        # Crear fila de totales
        totals_row = pd.DataFrame({
            'crypto': ['TOTAL'],
            'Quantity': [total_quantity],
            'Date': [None],
            'Crypto Value (USDT)': [total_crypto_value],
            'Quantity Value (USDT)': [total_quantity_value]
        })
        
        # Concatenar con el DataFrame original
        df_with_totals = pd.concat([df, totals_row], ignore_index=True)
        
        # Guardar el archivo con los resultados
        output_filename = "data_with_prices.xlsx"
        df_with_totals.to_excel(output_filename, index=False, sheet_name='Hoja1')
        
        print(f"\nProceso completado!")
        print(f"Archivo guardado como: {output_filename}")
        print(f"\nResumen de totales:")
        print(f"Total Quantity: {total_quantity}")
        print(f"Total Crypto Value: {total_crypto_value:.2f} USDT")
        print(f"Total Quantity Value: {total_quantity_value:.2f} USDT")
        
        return True
        
    except Exception as e:
        print(f"Error procesando el archivo: {e}")
        return False

if __name__ == "__main__":
    # Verificar que el archivo existe
    if not os.path.exists("data.xlsx"):
        print("Error: No se encuentra el archivo 'data.xlsx' en la carpeta actual")
    else:
        process_excel_file()
