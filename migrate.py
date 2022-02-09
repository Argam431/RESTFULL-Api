import sys

from app import create_app
from app.db import db
from app.countries.models import Country
from app.universities.models import University

from scrap import scrap


if __name__ == '__main__':
    appl = create_app()
    appl.app_context().push()
    db.create_all()

    if len(sys.argv) > 1 and sys.argv[1] == "data":
        universities = scrap()
        if universities is None:
            sys.exit(1)

        
        countries = {}
        for university in universities:

            name = university['country']

            if name not in countries:
                c = Country(name=name)
                db.session.add(c)
                countries[name] = None

            
                db.session.flush()
                db.session.refresh(c)
                countries[name] = c.id

       
        for university in universities:
            country = university['country']
            u = University(
                world_rank=university['world_rank'],
                name=university['name'],
                country_id=countries[country],
                score=university['score'],
            )
            db.session.add(u)

        db.session.commit()
