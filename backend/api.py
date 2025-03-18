from flask_restful import Api
from database.db import init_db, app
from resources.cardsResource import CardsResource

with app.app_context():
    init_db
    
api = Api(app)

api.add_resource(CardsResource, "/cards/cycle/")

if __name__ == "__main__":
    app.run(debug=True)

