use test_database;

//db.createCollection("orders")
//db.createCollection("products")
//db.createCollection("cards")



db.orders.insertMany([
    {
       'number': '6226',
       'date': new ISODate('2023-02-15T10:00:00Z'),
       'price': 10,
       'discount': 3.5,
       'total': 9.65    },
    {
       'number': '0000',
       'date': new ISODate('2023-02-06T10:00:00Z'),
       'price': 20,
       'discount': 5,
       'total': 19.0
    },
    {
       'number': '0001',
       'date': new ISODate('2023-02-07T10:00:00Z'),
       'price': 10,
       'discount': 5,
       'total': 9.5
    },
    {
       'number': '0083',
       'date': new ISODate('2023-02-08T10:00:00Z'),
       'price': 1,
       'discount': 5,
       'total': 4.75
    },
])

db.products.insertMany([
    {
        'name': "milk",
        "price": 2    },
    {
        'name': "bread",
        "price": 2,
    },
    {
        'name': "butter",
        "price": 5
    },
    {
        'name': "gum",
        "price": 1
    },
    {
        'name': "pizza",
        "price": 10
    },    
])


//db.cards.insertMany([
//    {
//        'series':'1',
//        'number':'9396',
//        'create_date':new ISODate('2023-02-14T10:00:00Z'),
//        'start_date':new ISODate('2023-02-14T10:00:00Z'),
//        'end_date':new ISODate('2023-03-14T10:00:00Z'),
//        'recent_buy_date':new ISODate('2023-02-15T10:00:00Z'),
//        'buy_counter':1,
//        'card_state':"Activated",
//        'discount': 3.5,
//        'orders': [ObjectId('63ed3a169a8f0b9eee7b42ce')]//    },
//    {
//        'series':'1',
//        'number':'9200',
//        'create_date':new ISODate('2023-01-09T10:00:00Z'),
//        'start_date':new ISODate('2023-01-09T10:00:00Z'),
//        'end_date':new ISODate('2023-02-09T10:00:00Z'),
//        'recent_buy_date':new ISODate('2023-02-08T10:00:00Z'),
//        'buy_counter':3,
//        'card_state':"Expired",
//        'discount': 5,
//        'orders': [
//            ObjectId('63ed3a169a8f0b9eee7b42cf'),
//            ObjectId('63ed3a169a8f0b9eee7b42d0'),
//            ObjectId('63ed3a169a8f0b9eee7b42d1')//        ]
//    },
//    {
//        'series':'2',
//        'number':'4299',
//        'create_date':new ISODate('2023-02-12T10:00:00Z'),
//        'start_date': null,
//        'end_date': null,
//        'recent_buy_date':null,
//        'buy_counter':0,
//        'card_state':"Not activated",
//        'discount': 1,
//        'orders': []
//    },//])


db.cards.insertOne({
        'series':'2',
        'number':'1111',
        'create_date':new ISODate('2023-02-12T10:00:00Z'),
        'start_date': null,
        'end_date': null,
        'recent_buy_date':null,
        'buy_counter':0,
        'card_state':"Not activated",
        'discount': 1,
        'orders': []
    })


db.createCollection("deleted_cards")

db.cards.find({})

db.orders.find({})

db.products.find({})

db.deleted_cards.find({})


db.cards.find({'number': '1111', discount})
