use test_database;

db.createCollection("orders")
db.createCollection("products")
db.createCollection("cards")
db.createCollection("deleted_cards")

 db.products.insertMany([
     {
         "_id" : ObjectId("63ef4839a6a36ecd62717f00"),
         'name': "milk",
         "price": 2
     },
     {
         "_id" : ObjectId("63ef4839a6a36ecd62717f01"),
         'name': "bread",
         "price": 2,
     },
     {
         "_id" : ObjectId("63ef4839a6a36ecd62717f02"),
         'name': "butter",
         "price": 5
     },
     {
         "_id" : ObjectId("63ef4839a6a36ecd62717f03"),
         'name': "gum",
         "price": 1
     },
     {
         "_id" : ObjectId("63ef4839a6a36ecd62717f04"),
         'name': "pizza",
         "price": 10
     },
 ])

 db.orders.insertMany([
     {
         "_id" : ObjectId("63f2173fcb5528905e90e5ef"),
         "card_number": "1-0000",
         'date': new ISODate('2023-02-15T10:00:00Z'),
         'price': 10,
         'discount': 3.5,
         'total': 9.65,
         'products': [
             {
                 "id": ObjectId('63ef4839a6a36ecd62717f00'),
                 'amount': 2
             },
             {
                 "id": ObjectId('63ef4839a6a36ecd62717f02'),
                 'amount': 1
             },
             {
                 "id": ObjectId('63ef4839a6a36ecd62717f03'),
                 'amount': 1
             },
         ]
     },
     {
         "_id" : ObjectId("63f2173fcb5528905e90e5f0"),
         "card_number": "1-0001",
        'date': new ISODate('2023-02-06T10:00:00Z'),
        'price': 20,
        'discount': 5,
        'total': 19.0,
         'products': [
             {
                 "id": ObjectId('63ef4839a6a36ecd62717f04'),
                 'amount': 2
             }
         ]
     },
     {
         "_id" : ObjectId("63f2173fcb5528905e90e5f1"),
         "card_number": "1-0001",
         'date': new ISODate('2023-02-07T10:00:00Z'),
         'price': 4,
         'discount': 5,
         'total': 3.8,
         'products': [
             {
                 "id": ObjectId('63ef4839a6a36ecd62717f00'),
                 'amount': 1
             },
             {
                 "id": ObjectId('63ef4839a6a36ecd62717f01'),
                 'amount': 1
             }
         ]
     },
     {
         "_id" : ObjectId("63f2173fcb5528905e90e5f2"),
         "card_number": "1-0001",
         'date': new ISODate('2023-02-08T10:00:00Z'),
         'price': 1,
         'discount': 5,
         'total': 0.95,
         'products': [
             {
                 "id": ObjectId('63ef4839a6a36ecd62717f03'),
                 'amount': 1
             }
         ]
     },
 ])



db.cards.insertMany([
   {
       'series':'1',
       'number':'1-0000',
       'create_date':new ISODate('2023-02-14T10:00:00Z'),
       'start_date':new ISODate('2023-02-14T10:00:00Z'),
       'end_date':new ISODate('2023-03-14T10:00:00Z'),
       'recent_buy_date':new ISODate('2023-02-15T10:00:00Z'),
       'buy_counter':1,
       'card_state':"Activated",
       'discount': 3.5,
       'orders': [ObjectId('63f2173fcb5528905e90e5ef')]
   },
   {
       'series':'1',
       'number':'1-0001',
       'create_date':new ISODate('2023-01-09T10:00:00Z'),
       'start_date':new ISODate('2023-01-09T10:00:00Z'),
       'end_date':new ISODate('2023-02-09T10:00:00Z'),
       'recent_buy_date':new ISODate('2023-02-08T10:00:00Z'),
       'buy_counter':3,
       'card_state':"Expired",
       'discount': 5,
       'orders': [
           ObjectId('63f2173fcb5528905e90e5f0'),
           ObjectId('63f2173fcb5528905e90e5f1'),
           ObjectId('63f2173fcb5528905e90e5f2')
       ]
   },
   {
       'series':'2',
       'number':'2-0000',
       'create_date':new ISODate('2023-02-12T10:00:00Z'),
       'start_date': '',
       'end_date': '',
       'recent_buy_date':'',
       'buy_counter':0,
       'card_state':"Not activated",
       'discount': 1,
       'orders': []
   },
    {
        'series':'2',
        'number':'2-0001',
        'create_date':new ISODate('2023-02-12T10:00:00Z'),
        'start_date': '',
        'end_date': '',
        'recent_buy_date':'',
        'buy_counter':0,
        'card_state':"Not activated",
        'discount': 1,
        'orders': []
    }
])

db.cards.find({})

db.orders.find({})

db.products.find({})

db.deleted_cards.find({})



db.cards.insertOne({
        'series':'2',
        'number':'2-0001',
        'create_date':new ISODate('2023-02-19T18:27:00Z'),
        'start_date': '',
        'end_date': new ISODate('2023-02-19T15:37:00Z'),
        'recent_buy_date':'',
        'buy_counter':0,
        'card_state':"Activated",
        'discount': 1,
        'orders': []
    }
)



db.cards.aggregate([
{
        $match: {"_id": ObjectId('63f226f1cb5528905e90e5fc')}
    },
{
    $lookup: {
        from: "orders",
        localField: "orders",
        foreignField: "_id",
        as: "fromorders"
    }},
   { $project: { "_id": 0, "fromorders": 1 } }
]);



