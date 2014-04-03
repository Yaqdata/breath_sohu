from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client['sohu']
sohu_info_collection = db.sohu_info
sohu_useful_url_collection = db.sohu_useful_url
    
def insert_sohu(data):
    sohu_info_collection.save(data)

def update_useful_url(url):
    if sohu_useful_url_collection.find_one({'url': url}):
        print 'existed'
        return
    sohu_useful_url_collection.insert({'url': url})

def get_useful_url_count():
    return sohu_useful_url_collection.count()

def get_useful_urls(limit):
    return sohu_useful_url_collection.find().limit(limit)
