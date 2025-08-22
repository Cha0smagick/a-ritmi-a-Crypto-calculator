# Crypto Price Fetcher from Binance API

Script de Python que obtiene precios históricos de criptomonedas desde la API de Binance y completa un archivo Excel con los valores correspondientes.

## 📋 Descripción

Este script lee un archivo Excel (`data.xlsx`) que contiene transacciones de criptomonedas y utiliza la API de Binance para:
- Obtener el precio histórico de cada criptomoneda en la fecha especificada
- Calcular el valor en USDT de cada transacción
- Generar sumatorias de cantidades y valores
- Guardar los resultados en un nuevo archivo Excel

## 🚀 Características

- ✅ Consulta la API oficial de Binance
- ✅ Ajusta automáticamente a hora de California (PST/PDT)
- ✅ Manejo robusto de errores y excepciones
- ✅ Preserva el formato original del Excel
- ✅ Genera reporte con totales y resumen

## 📊 Estructura del Archivo Excel de Entrada

El archivo `data.xlsx` debe tener las siguientes columnas:
- `crypto`: Símbolo de la criptomoneda (ej: ETH, BTC, ADA)
- `Quantity`: Cantidad de la criptomoneda
- `Date`: Fecha de la transacción (formato YYYY-MM-DD HH:MM:SS)
- `Crypto Value (USDT)`: (Vacío - se completará automáticamente)
- `Quantity Value (USDT)`: (Vacío - se completará automáticamente)

## 📦 Instalación

1. Clona o descarga el repositorio
2. Instala las dependencias:

```bash
pip install -r requirements.txt
