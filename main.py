import asyncio

from markets.binance import Binance


"""
 Binance: 
 Fiats - коды валют на рынки
 Assets - коды обменной криптовалюты
 МОЖНО ДОБАВЛЯТЬ ЛЮБОЕ КОЛИЧЕСТВО ПАР 
"""




binance_fiats = ['BYN', 'GEL', 'KZT', 'TRY', 'AMD', 'AZN']
binance_assets = ['USDT',]

async def binance_():
        for f in binance_fiats:
            for a in binance_assets:
                p2p = Binance(f, a, 'buy')
                buyParse = await p2p.parse()
                buy = await p2p.create_list(buyParse)
                # print('массив cобран') ! test
                await asyncio.sleep(5)
                p2p = Binance(f, a, 'sell')
                buySell = await p2p.parse()
                sell  = await p2p.create_list(buySell)
                print(f"Продажа — {buy}") 
                print(f"Покупка — {sell}") 
                await asyncio.sleep(10)




async def main():
    await asyncio.gather( binance_())




if __name__ == '__main__':
     asyncio.run(main())

