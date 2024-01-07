import requests
import PySimpleGUI as sg

def get_crypto_data():
    cryptos = ['bitcoin', 'ethereum', 'matic-network'] 
    api_url = 'https://api.coingecko.com/api/v3/coins/markets'
    params = {
        'vs_currency': 'brl',
        'ids': ','.join(cryptos),
        'order': 'market_cap_desc',
        'per_page': 100,
        'page': 1,
        'sparkline': False,
        'locale': 'en'
    }

    response = requests.get(api_url, params=params)

    if response.status_code == 200:
        data = response.json()
        return data
    else:
        return None

def get_crypto_history(coin_id, days):
    api_url = f'https://api.coingecko.com/api/v3/coins/%7Bcoin_id%7D/market_chart'
    params = {
        'vs_currency': 'brl',
        'days': days,
    }

    response = requests.get(api_url, params=params)

    if response.status_code == 200:
        data = response.json()
        prices = data['prices']
        price_changes = [prices[i][1] - prices[i-1][1] for i in range(1, len(prices))]
        return price_changes
    else:
        return []


def update_table(window, data, count):
    if data:
        table_data = []
        for crypto in data:
            name = crypto['name']
            price_brl = crypto['current_price']
            price_changes = get_crypto_history(crypto['id'], count)
            price_changes_str = '\n'.join([f"{change:+.2f}" for change in price_changes])
            table_data.append([name, f"R$ {price_brl:.2f}", price_changes_str])

        window['-TABLE-'].update(values=table_data)

sg.theme('Reddit')
layout = [
    [sg.Text('Preços das Criptomoedas em Tempo Real', font=('Helvetica', 18))],
    [sg.Table(values=[], headings=['Criptomoedas', 'Preços(BRL)'],
              display_row_numbers=False,
              auto_size_columns=True,
              num_rows=7,
              col_widths=[30, 15, 30],
              justification='left',
              key='-TABLE-')],
    [sg.Text('Você pode atualizar a cada 60 segundos.')],
    [sg.Button('Atualizar', key='-UPDATE-'), sg.Button('Sair', key='-EXIT-')]
]

window = sg.Window('Criptomoedas', layout, finalize=True)

count = 5

data = get_crypto_data()
update_table(window, data, count)

while True:
    event, values = window.read()
    if event in (sg.WIN_CLOSED, '-EXIT-'):
        break
    elif event == '-UPDATE-':
        data = get_crypto_data()
        update_table(window, data, count)

window.close()