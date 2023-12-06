import requests
from utils import __append_parameter__, __parse_parameter__

class Creator():
    def __init__(self, jsondata) -> None:
        self.data = jsondata
        
    @property
    def username(self):
        return self.data["username"]
    
    @property
    def modelCount(self):
        return self.data["modelCount"]
    
    @property
    def link(self):
        return self.data["link"]
    
    @property
    def image(self):
        return self.data["image"]

class CreatorResponse():
    def __init__(self, response) -> None:
        self.data = response
        self.items = [Creator(i) for i in response["items"]]
    
    @property
    def totalItems(self):
        return self.data["metadata"]["totalItems"]
    
    @property
    def currentPage(self):
        return self.data["metadata"]["currentPage"]
    
    @property
    def pageSize(self):
        return self.data["metadata"]["pageSize"]
    
    @property
    def totalPages(self):
        return self.data["metadata"]["totalPages"]
    
    @property
    def nextPage(self):
        return self.data["metadata"]["nextPage"]
    
    
def get(CIVITAI_BASE_URL:str, limit:int=None, page:int=None, query:str=None):
    set_limit = __parse_parameter__(limit=limit)
    set_page  = __parse_parameter__(page=page)
    set_query = __parse_parameter__(query=query)
    url = f'{CIVITAI_BASE_URL}/creators{__append_parameter__([set_limit, set_page, set_query])}'
    x = requests.get(url)
    return CreatorResponse(x.json())