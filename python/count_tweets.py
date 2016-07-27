import json
import pymongo

conn = pymongo.MongoClient()
db = conn.pubs

pubs = db.smallarea.find({ 'properties.user': { '$exists': False } })

for pub in pubs:

    tweetcount = db.smallarea.count({
        '$and': [
            {
                'properties.user': {
                    '$exists': True
                }
            },
            {
                'geometry': {
                    '$near': {
                        '$geometry': {
                            'type': 'Point',
                            'coordinates': [ pub['geometry']['coordinates'][0] , pub['geometry']['coordinates'][1] ]
                        },
                        '$maxDistance': 50,
                        '$minDistance': 0
                    }
                }
            }
        ]
    })

    db.smallarea.update({ '_id' : pub['_id'] }, { '$set': { 'properties.tweet_count': tweetcount } }, upsert=False)

conn.close()
