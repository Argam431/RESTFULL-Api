from flask import Blueprint, jsonify, request

from flask.views import MethodView

from .models import Country

from app.db import db

bp = Blueprint('countries', __name__, url_prefix='/countries')



class CountryBaseView(MethodView):
    def is_column_unique(self, column, value): 
        return Country.query.filter_by(**{column: value}).first() is None

    def is_name_unique(self, name):
        return Country.query.filter_by(name=name).first() is None

    def get_country(self, country_id):
        return Country.query.filter_by(id=country_id).first()

    def validate_data(self, data):
        fields = {
            'name': str
        }

        errors = {}
        for field, _type in fields.items():
            try:
                data[field] = _type(data[field])
            except (KeyError, TypeError, ValueError):
                errors[field] = 'invalid'
        
        return data, errors



class CountryListCreateView(CountryBaseView):
    def get(self):
        limit = 20

        rows = Country.query.limit(limit)

        page = request.args.get('page', '1')
        if page and page.isnumeric():
            page = int(page)
            rows = rows.offset((page - 1) * limit)

        response = [{'id': row.id, 'name': row.name } for row in rows]

        return jsonify(response)

    def post(self):
        data = request.json

        data, errors = self.validate_data(request.json)

        if len(errors):
            return jsonify({'error': errors}), 400

        if not self.is_column_unique('name', data['name']):
            errors['name'] = 'unique'

        if len(errors):
            return jsonify({'error': errors}), 400


        c = Country(
            name=data['name'])

        db.session.add(c)
        db.session.commit()
        db.session.refresh(c)

        return jsonify({'id': c.id}), 201   



class CountryDetailUpdateDeleteView(CountryBaseView):
    def get_object_by_id(self, Country_id):
        return Country.query.filter_by(id=Country_id).first()

    def get(self, country_id):
        row = self.get_object_by_id(country_id)
        if row is None:
            return jsonify({'error': 'not_found'}), 404

        return jsonify({'id': row.id, 'name': row.name,})

    def put(self, country_id):
        country = self.get_object_by_id(country_id)
        if country is None:
            return jsonify({'error': 'not_found'}), 404
        
        data, errors = self.validate_data(request.json)
        
        if len(errors):
            return jsonify({'error': errors}), 400

        if Country.query.filter(Country.id != country_id).filter_by(name=data['name']).first():
            errors['name'] = 'unique'

        if len(errors):
            return jsonify({'error': errors}), 400

        country.name=data['name']
    
       
        db.session.commit()

        return jsonify({'id': country.id}), 200

    def delete(self, country_id):
        country = self.get_object_by_id(country_id)
        if country is None:
            return jsonify({'error': 'not_found'}), 404

        db.session.delete(country)
        db.session.commit()

        return jsonify({'deleted': 'ok'})





bp.add_url_rule('/', view_func=CountryListCreateView.as_view('countries'))
bp.add_url_rule('/<country_id>/', view_func= CountryDetailUpdateDeleteView.as_view('country'))
