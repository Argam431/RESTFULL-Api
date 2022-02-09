from flask import Blueprint, jsonify, request
from flask.views import MethodView

from app.db import db

from app.countries.models import Country
from .models import University


bp = Blueprint('universities', __name__, url_prefix='/universities')


class UniversityBaseView(MethodView):
    def is_column_unique(self, column, value): 
        """
        Example:
        'world_rank', 98, 
        'name', 'Some university'
        """
        return University.query.filter_by(**{column: value}).first() is None

    def is_name_unique(self, name):
        return University.query.filter_by(name=name).first() is None

    def get_country(self, country_id):
        return Country.query.filter_by(id=country_id).first()

    def validate_data(self, data):
        fields = {
            'name': str,
            'world_rank': int,
            'score': float,
            'country_id': int,
        }

        errors = {}
        for field, _type in fields.items():
            try:
                data[field] = _type(data[field])
            except (KeyError, TypeError, ValueError):
                errors[field] = 'invalid'
        
        return data, errors


class UniversityListCreateView(UniversityBaseView):
    def get(self):
        limit = 20

        rows = University.query.limit(limit)

        page = request.args.get('page', '1')
        if page and page.isnumeric():
            page = int(page)
            rows = rows.offset((page - 1) * limit)

        response = [{'id': row.id, 'world_rank': row.world_rank, 'name': row.name, 'score': float(row.score), 'country_id': row.country_id} for row in rows]

        return jsonify(response)

    def post(self):
        data = request.json

        data, errors = self.validate_data(request.json)

        if len(errors):
            return jsonify({'error': errors}), 400

        if not self.is_column_unique('name', data['name']):
            errors['name'] = 'unique'
        
        if not self.is_column_unique('world_rank', data['world_rank']):
            errors['world_rank'] = 'unique'

        if not self.get_country(data['country_id']):
            errors['country_id'] = 'invalid'

        if len(errors):
            return jsonify({'error': errors}), 400

        u = University(
            name=data['name'], 
            world_rank=data['world_rank'], 
            score=data['score'],
            country_id=data['country_id'],
        )
        db.session.add(u)
        db.session.commit()
        db.session.refresh(u)

        return jsonify({'id': u.id}), 201 # created


class UniversityDetailUpdateDeleteView(UniversityBaseView):
    def get_object_by_id(self, university_id):
        return University.query.filter_by(id=university_id).first()

    def get(self, university_id):
        row = self.get_object_by_id(university_id)
        if row is None:
            return jsonify({'error': 'not_found'}), 404

        return jsonify({'id': row.id, 'world_rank': row.world_rank, 'name': row.name, 'score': float(row.score), 'country_id': row.country_id})

    def put(self, university_id):
        university = self.get_object_by_id(university_id)
        if university is None:
            return jsonify({'error': 'not_found'}), 404
        
        data, errors = self.validate_data(request.json)
        
        if len(errors):
            return jsonify({'error': errors}), 400

        if University.query.filter(University.id != university_id).filter_by(name=data['name']).first():
            errors['name'] = 'unique'

        if University.query.filter(University.id != university_id).filter_by(world_rank=data['world_rank']).first():
            errors['world_rank'] = 'unique'

        if not self.get_country(data['country_id']):
            errors['country_id'] = 'invalid'

        if len(errors):
            return jsonify({'error': errors}), 400

        university.name=data['name']
        university.world_rank=data['world_rank']
        university.score=data['score']
        university.country_id=data['country_id']
        
        db.session.commit()

        return jsonify({'id': university.id}), 200 # created

    def delete(self, university_id):
        university = self.get_object_by_id(university_id)
        if university is None:
            return jsonify({'error': 'not_found'}), 404

        db.session.delete(university)
        db.session.commit()

        return jsonify({'deleted': 'ok'})


bp.add_url_rule('/', view_func=UniversityListCreateView.as_view('universities'))
bp.add_url_rule('/<university_id>/', view_func=UniversityDetailUpdateDeleteView.as_view('university'))
