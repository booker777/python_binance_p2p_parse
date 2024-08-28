import re

import requests

from service.cookies import cks_binance
from service.headers import hd_binance
from service.service import Service

session = requests.Session()

"""BINANCE



"""
class Binance(Service):

        name = 'binance'
        url = 'https://p2p.binance.com/ru'
        # buy = 'buy'
        # sell = 'sell'

        def __init__(self, fiat, asset, side):
            self.fiat = fiat
            self.asset = asset
            self.side = side

        async def __create_json_data(self, tradeSide):
                json_data = { 'fiat': self.fiat, 'page': 1,
                    'rows': 10, 'tradeType': tradeSide,
                    'asset': self.asset, 'countries': [],
                    'proMerchantAds': False, 'publisherType': None,
                    'payTypes': [],
                }
                return json_data

        async def parse(self):
                """ПАРСИМ БИРЖУ"""
                json_ =  await self.__create_json_data(self.side)
                try:
                    data = session.post('https://p2p.binance.com/bapi/c2c/v2/friendly/c2c/adv/search',
                                        cookies=cks_binance, headers=hd_binance, json=json_ ).json()
                    return data
                except Exception as e:
                    with open(f'binance_parse_err.txt', 'w', encoding='utf-8') as txt:
                        txt.write(e)


        async def create_list(self, data):
            time_created = await self.create_moscow_time()
            if data:
                list_ = [
                    {"name": i["advertiser"]["nickName"],
                     "price": i["adv"]["price"],
                     "remark": None,
                     "minLimit": i["adv"]["minSingleTransAmount"],
                     "maxLimit": i["adv"]["dynamicMaxSingleTransAmount"],
                     "total": i['adv']['maxSingleTransQuantity'],
                     "rateCount": re.sub(r'\.[0-9]+', '', str(float((i["advertiser"]["monthFinishRate"] * 100)))),
                     "ordersCount": i["advertiser"]["monthOrderCount"],
                     "payMethods":  await self.__create_paymethods(i["adv"]["tradeMethods"]),
                     'market': self.name,
                     'time_created': time_created,
                     'marketLink': await self.__set_url()

                     }
                     for i in data["data"]
                ]
                return  list_


        async def __create_paymethods(self, paymethods):
            payMethods = [i["tradeMethodShortName"] for i in paymethods]
            return payMethods

        async def __set_url(self):
            """Cоздание ссылки на рынок"""
            url = f'https://p2p.binance.com/ru/trade/{self.side}/{self.asset}?fiat={self.fiat}&payment=all-payments'
            return url


