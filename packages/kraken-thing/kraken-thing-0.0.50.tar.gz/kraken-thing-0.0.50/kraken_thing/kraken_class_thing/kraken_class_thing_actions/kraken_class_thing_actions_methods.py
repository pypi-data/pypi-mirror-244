import asyncio
import aiohttp
import json



    

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