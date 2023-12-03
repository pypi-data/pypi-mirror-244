import asyncio
import aiohttp
import json
from kraken_thing.kraken_class_thing.kraken_class_thing_actions import kraken_class_thing_actions_methods as m


class Thing_related_action:

    def __init__(self, thing):
        """
        """
        self._thing = thing

    
    def execute(self, action_name):
        """Dispatch for the actions
        """

        action = self.get(action_name)
        action['object'] = self._thing.dump()
        result = asyncio.run(m.run_api_async(action, self._thing.dump()))
        print(result)
        return result
    
    def get(self, action_name=None):
        """Retrieves available actions for record
        Retrieve specific action if specified
        """
        actions = [self.get_scrape()]

        # Return only specific action if specified
        if action_name:
            for i in actions:
                if i.get('@id', None) == action_name:
                    actions = i
                
        
        return actions
    
    
    
    def get_scrape(self):
        """
        """
        record = self._thing.dump()
        record_type = self._thing.type
        record_id = self._thing.id
        
        action = {
            "@type": "action", 
            "@id": "action_id_1", 
            "name": "scrape", 
            "target": f"/{record_type}/{record_id}/action/action_id_1",
            "instrument": {
                "@type": "WebApp",
                "@id": "webscraper",
                "name": "scraper",
                "url": "https://scraper.krknapi.com"
            }
        
        }
        return action