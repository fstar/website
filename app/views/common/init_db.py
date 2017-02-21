from app.models import db, UN_Country
from app.config import UN_user
import requests



def create_UN_Country():
    UN_Country_query = UN_Country.query.count()
    if UN_Country_query == 0:
        url = "http://api.geonames.org/countryInfoJSON?lang=zh&username={UN_user}".format(UN_user=UN_user)
        req = requests.get(url)
        data = req.json()
        for i in data["geonames"]:
            one = UN_Country(i)
            db.session.add(one)
        db.session.commit()
    print("UN_Country db done")
