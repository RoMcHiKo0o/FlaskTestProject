exports = function() {

  const cards = context.services.get("Cluster0").db("test_database").collection("cards");
  return cards.updateMany({"card_state": "Activated", "end_date": {$lt: new Date()}},{$set: {"card_state": "Expired"}});
};