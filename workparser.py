from fake_useragent import UserAgent
import requests
import json
import asyncio

ua = UserAgent()
print(ua.random)

res = []



async def collect_data(type, user_id, procent, money_from, money_to):

    offset = 0
    batch_size = 60
    result = []
    count = 0
    for i in range(9999):
        await asyncio.sleep(1)
        for item in range(offset, offset + batch_size, 60):
            try:      
                url = f'https://inventories.cs.money/5.0/load_bots_inventory/730?buyBonus=40&hasTradeLock=false&hasTradeLock=true&isStore=true&limit=60&maxPrice={money_to}&minPrice={money_from}&offset={item}&tradeLockDays=1&tradeLockDays=2&tradeLockDays=3&tradeLockDays=4&tradeLockDays=5&tradeLockDays=6&tradeLockDays=7&tradeLockDays=0&type={type}&withStack=true'
                response = requests.get(
                    url=url,
                    headers={'user-agent': f'{ua.random}'}
                )
                
                offset += batch_size
                
                data = response.json()
                
                if data.get('error') == 2:
                    return 'Data were collected'
                
                items = data.get('items')
                
                for i in items:
                    if i.get('overprice') is not None and i.get('overprice') < -int(procent):
                        item_full_name = i.get('fullName')
                        item_3d = i.get('3d')
                        item_price = i.get('price')
                        item_over_price = i.get('overprice')
                        
                        result.append(
                            {
                                'full_name': item_full_name,
                                '3d': item_3d,
                                'overprice': item_over_price,
                                'item_price': item_price
                            }
                        )
            except:
                break
                    
        count += 1
        print(f'Page #{count}')
        print(url)
    
        with open(f'{user_id}.json', 'w', encoding='utf-8') as file:
            json.dump(result, file, indent=4, ensure_ascii=False)
            
        print(len(result))
    
    
def main():
    print(collect_data())
    
    
if __name__ == '__main__':
    main()