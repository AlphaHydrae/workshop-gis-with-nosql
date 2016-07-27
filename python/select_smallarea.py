import json
import pymongo

conn = pymongo.MongoClient()
db = conn.pubs

allpubs_near = db.allpubs.find({
    'geometry': {
        '$near': {
            '$geometry': {
                'type': "Point" ,
                'coordinates': [ 24.9495854, 60.1694509 ]
            },
            '$maxDistance': 500
        }
    }
})

for pub in allpubs_near:
    db.smallarea.insert(pub)

db.smallarea.ensure_index([("geometry", pymongo.GEOSPHERE)])

conn.close()
