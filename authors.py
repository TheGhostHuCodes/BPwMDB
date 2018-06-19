# This flask application expects a local mongodb database named 'test' with a
# collection named 'packt_authors'. The route /author/<name> can then be used
# to find a document with the parameterized name
from bson.json_util import dumps
from flask import Flask
from flask import request, Response
from flask_pymongo import PyMongo

app = Flask(__name__)
mongo = PyMongo()


def main():
    app.config['MONGO_URI'] = 'mongodb://localhost:27017/test'
    mongo.init_app(app)
    app.run(debug=True)


@app.route('/author/<name>')
def get_author_by_name(name):
    curs = mongo.db.packt_authors.find({'name': name})
    total = curs.count()
    skip = int(request.args.get('skip', 0))
    limit = int(request.args.get('limit', 50))
    curs = curs.skip(skip)
    curs = curs.limit(limit)
    response = dict(skip=skip, limit=limit, total=total, items=list(curs))
    return Response(dumps(response, indent=True), mimetype='application/json')


if __name__ == '__main__':
    main()
