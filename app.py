from flask import Flask, jsonify
from flask_restful import Api, Resource, reqparse
from flask_ngrok import run_with_ngrok
from flask import make_response


import random
app = Flask(__name__)
api = Api(app)

quotes = [
    {
        "id": 0,
        "author": "James Baldwin",
        "quote": "I cant believe what you say, because I see what you do.", 
        "source": "A Report from Occupied Territory"
    },
    {
        "id": 1,
        "author": "Annie Easley",
        "quote": "If I cant work with you, I will work around you",
        "source": "2001 NASA Interview"
    },
    {
        "id": 2,
        "author": "Bell Hooks",
        "quote": "It is in the act of having to do things that you don’t want to that you learn something about moving past the self. Past the ego.",
        "source": "Conversation with John Perry Barlow"
    },
    {
        "id": 3,
        "author": "Ehime Ora",
        "quote": "You worked so hard for this moment. Your new life is finally beginning and you are deserving of all of it.",
        "source": "https://twitter.com/ehimeora/status/1366168809074221056"
    }
]

class quote(Resource):
    def get(self, id=0):
        if not id:
            return random.choice(quotes), 200
        for quote in quotes:
            if(quote["id"] == id):
                return quote, 200
        return "Quote not found", 404
      
    def post(self):
      parser = reqparse.RequestParser()
      parser.add_argument("id",type=int,required=True)
      parser.add_argument("author",required=True)
      parser.add_argument("quote",required=True)
      parser.add_argument("source")
      params = parser.parse_args()
      id = params["id"]
      for quote in quotes:
          if(id == quote["id"]):
              return f"Quote with id {id} already exists add new id", 400
      quote = {
          "id": int(id),
          "author": params["author"],
          "quote": params["quote"],
          "source": params["source"]
      }
      quotes.append(quote)
      return quote, 201

    def delete(self, id='c'):
        if id is 'c':
          return make_response(jsonify({'error': 'ID is missing'}), 400)
        global quotes
        quotes = [quote for quote in quotes if quote["id"] != id]
        return f"Quote with id {id} is deleted.", 200

    def put(self):
      parser = reqparse.RequestParser()
      parser.add_argument("id",type=int,required=True)
      parser.add_argument("author",required=True)
      parser.add_argument("quote",required=True)
      parser.add_argument("source")      
      params = parser.parse_args()
      id = params["id"]
      for obj in quotes:
          if(id == obj["id"]):
              obj["author"] = params["author"]
              obj["quote"] = params["quote"]
              obj["source"] = params["source"]
              return obj, 204
      else:
            return make_response(jsonify({'error': 'ID is not present in database'}), 404)
    

class home(Resource):
  def get(self):
    return "Hey there! This is a simple quotes and affirmations API made by Mei Eyre <3 Based off of the Joke API by Ali Mustufa Shaikh;"

api.add_resource(quote, "/quote", "/quote/", "/quote/<int:id>")
api.add_resource(home,"/")

if __name__ == '__main__':
    app.run()