# calculadora_btc/views.py
from django.shortcuts import render
import yfinance as yf

def calcular_accuracy(request):
    if request.method == 'POST':
        crypto = request.POST.get('crypto')
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')

        symbol = f'{crypto}-USD'

        try:
            # Descargar datos de Yahoo Finance
            data = yf.download(symbol, start=start_date, end=end_date)

            # Calcular el indicador RSI
            delta = data['Close'].diff()
            gain = delta.where(delta > 0, 0)
            loss = -delta.where(delta < 0, 0)
            avg_gain = gain.rolling(window=14, min_periods=1).mean()
            avg_loss = loss.rolling(window=14, min_periods=1).mean()
            rs = avg_gain / avg_loss
            rsi = 100 - (100 / (1 + rs))

            # Agregar columnas al DataFrame
            data['Gain'] = gain
            data['Loss'] = loss
            data['Avg Gain'] = avg_gain
            data['Avg Loss'] = avg_loss
            data['RS'] = rs
            data['RSI'] = rsi

            # Condiciones para compra y venta
            data['Compra'] = data['RSI'] <= 30
            data['Venta'] = data['RSI'] >= 70

            # Calcular operaciones acertadas
            compras_acertadas = data[data['Compra'] & (data['RSI'].shift(1) <= 30)].shape[0]
            ventas_acertadas = data[data['Venta'] & (data['RSI'].shift(1) >= 70)].shape[0]
            total_acertadas = compras_acertadas + ventas_acertadas
            total_operaciones = data['Compra'].sum() + data['Venta'].sum()

            # Calcular precisión (accuracy)
            accuracy = (total_acertadas / total_operaciones) * 100 if total_operaciones > 0 else None

            return render(request, 'calculadora_btc/resultado_accuracy.html', {'data': data, 'accuracy': accuracy})

        except Exception as e:
            # Manejar el error de manera adecuada, por ejemplo, mostrando un mensaje al usuario.
            return render(request, 'calculadora_btc/resultado_accuracy.html', {'error_message': str(e)})

    # Si no es una solicitud POST, renderizar el formulario para calcular el RSI
    return render(request, 'calculadora_btc/calcular_accuracy.html')


def resultado_accuracy(request):
    # Puedes manejar la lógica para obtener los datos necesarios (accuracy y data) aquí
    # ...
    accuracy = 90  # Reemplaza esto con tu lógica real
    data = {}      # Reemplaza esto con tus datos reales

    context = {'accuracy': accuracy, 'data': data}
    return render(request, 'calculadora_btc/resultado_accuracy.html', context)
