exports = function() {

  const cards = context.services.get("Cluster0").db("test_database").collection("cards");
  return cards.updateMany({"card_state": "Activated", "end_date": {$lt: new Date(3*3600*1000)}},{$set: {"card_state": "Expired"}});
};