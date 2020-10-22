from flask_restful import Resource, reqparse
from db import db
from models.book import BookModel


class BookList(Resource):

    def get(self):
        return {'Books': [i.json()['book'] for i in db.session.query(BookModel).all()]}, 200


class Book(Resource):

    def get(self, id):
        book = BookModel.find_by_id(id)
        if book:
            return {'Book': book.json()}, 200
        return {'message': "Book with ['ISBN': {}] not found".format(id)}, 404

    def post(self):
        data = self.__parse_request__()
        exists = BookModel.find_by_name(data.get('name'))
        if exists:
            return {'message': "A book with ['name': {}] already exists".format(exists.name)}, 409
        new_book = BookModel(data.get('id'), data.get('name'), data.get('author'), data.get('genre'),
                             data.get('year'), data.get('editorial'), data.get('language'), data.get('price'),
                             data.get('synopsis'), data.get('num_sales'))
        new_book.save_to_db()
        return new_book.json(), 200

    def delete(self, id):
        book = BookModel.find_by_id(id)
        if not book:
            return {'message': "There is no book with ['ISBN': {}], therefore it cannot be deleted".format(id)}, 404
        book.delete_from_db()
        return {'message': "Book with ['ISBN': {}, 'name': {}] has successfully been"
                           " deleted".format(id, book.name)}, 200

    def put(self, id):
        data = self.__parse_request__()
        exists = BookModel.find_by_id(id)
        if not exists:
            return {'message': "A book with ['ISBN': {}] not found".format(id)}, 404
        exists.delete_from_db()
        new_book = BookModel(data.get('id'), data.get('name'), data.get('author'), data.get('genre'),
                             data.get('year'), data.get('editorial'), data.get('language'), data.get('price'),
                             data.get('synopsis'), data.get('num_sales'))
        new_book.save_to_db()
        return new_book.json(), 200

    def __parse_request__(self):
        parser = reqparse.RequestParser()
        parser.add_argument('id', type=str, required=True, help="Operation not valid: 'ISBN' not provided")
        parser.add_argument('name', type=str, required=True, help="Operation not valid: 'name' not provided")
        parser.add_argument('author', type=str, required=True, help="Operation not valid: 'author' not provided")
        parser.add_argument('genre', type=str, required=True, help="Operation not valid: 'genre' not provided")
        parser.add_argument('year', type=str, required=True, help="Operation not valid: 'year' not provided")
        parser.add_argument('editorial', type=str, required=True, help="Operation not valid: 'editorial' not provided")
        parser.add_argument('language', type=str, required=True, help="Operation not valid: 'language' not provided")
        parser.add_argument('price', type=str, required=True, help="Operation not valid: 'price' not provided")
        parser.add_argument('synopsis', type=str, required=True, help="Operation not valid: 'synopsis' not provided")
        parser.add_argument('num_sales', type=str, required=True, help="Operation not valid: 'num_sales' not provided")
        return parser.parse_args()
