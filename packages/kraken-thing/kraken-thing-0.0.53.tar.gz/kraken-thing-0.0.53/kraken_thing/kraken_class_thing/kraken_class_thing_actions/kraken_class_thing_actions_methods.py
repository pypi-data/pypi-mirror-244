import asyncio
import aiohttp
import json
import requests

from kraken_thing import kraken_thing_methods as kr


def run_api(action, record):
    """
    """

    object = action.get('object', None)

    instrument = action.get('instrument', {})
    url = instrument.get('url', None)

    if not object or not instrument or not url:
        print('Missing')
        return False


    headers = {'content-type': "application/json", "Authorization": "bob"}
    data = json.dumps(object, default=str)
    print(data)
    try:
        r = requests.post(url, headers=headers, data=data)

        content = r.text
        records = kr.json.loads(content)
        
    except Exception as e:
        print(e)
        return False

    print('task finished')

    return records

async def run_api_async(action, record):
    """
    """
    
    object = action.get('object', None)

    instrument = action.get('instrument', {})
    url = instrument.get('url', None)
    
    if not object or not instrument or not url:
        print('Missing')
        return False
    

    headers = {'content-type': "application/json", "Authorization": "bob"}
    data = json.dumps(object, default=str)
    print(data)
    try:
        async with aiohttp.ClientSession(headers=headers) as session:
            async with session.post(url, data=data) as response:
                html = await response.text()
                print(html)
                result = await response.json()
                status =  response.status
    
    except Exception as e:
        print(e)
    
    print('task finished')

    return result