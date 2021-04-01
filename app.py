from flask import Flask, request
from flask_marshmallow import Marshmallow
from flask_restful import Api, Resource
from flask_sqlalchemy import SQLAlchemy


DB_FILE = "/tmp/sku.db"
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///{}".format(DB_FILE)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
ma = Marshmallow(app)
api = Api(app)


class RefLocation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    location_name = db.Column(db.String, nullable=False)

    sku = db.relationship('Sku', backref='ref_location', uselist=False)


class RefDepartment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    department_name = db.Column(db.String, nullable=False)

    sku = db.relationship('Sku', backref='ref_department', uselist=False)


class RefCategory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    category_name = db.Column(db.String, nullable=False)

    sku = db.relationship('Sku', backref='ref_category', uselist=False)


class RefSubCategory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sub_category_name = db.Column(db.String, nullable=False)

    sku = db.relationship('Sku', backref='ref_sub_category', uselist=False)


class Sku(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sku_name = db.Column(db.String, nullable=False)

    location_id = db.Column(
        db.Integer, db.ForeignKey('ref_location.id'), nullable=False
    )
    department_id = db.Column(
        db.Integer, db.ForeignKey('ref_department.id'), nullable=False
    )
    category_id = db.Column(
        db.Integer, db.ForeignKey('ref_category.id'), nullable=False
    )
    sub_category_id = db.Column(
        db.Integer, db.ForeignKey('ref_sub_category.id'), nullable=False
    )


class SkuSchema(ma.Schema):
    class Meta:
        fields = (
            "id",
            "sku_name",
            "ref_location.location_name",
            "ref_department.department_name",
            "ref_category.category_name",
            "ref_sub_category.sub_category_name",
            "location_name",
            "department_name",
            "category_name",
            "sub_category_name"
        )


sku_schema = SkuSchema()
skus_schema = SkuSchema(many=True)


class LocationListResource(Resource):
    def get(self):
        loc = RefLocation.query.all()
        return skus_schema.dump(loc)

    def post(self):
        new_location = RefLocation(
            location_name=request.json['location_name'],
        )
        db.session.add(new_location)
        db.session.commit()
        return sku_schema.dump(new_location)


class DepartmentListResource(Resource):
    def get(self):
        dep = RefDepartment.query.all()
        return skus_schema.dump(dep)

    def post(self):
        new_department = RefDepartment(
            department_name=request.json['department_name'],
        )
        db.session.add(new_department)
        db.session.commit()
        return sku_schema.dump(new_department)


class CategoryListResource(Resource):
    def get(self):
        categorys = RefCategory.query.all()
        return skus_schema.dump(categorys)

    def post(self):
        new_category = RefCategory(
            category_name=request.json['category_name'],
        )
        db.session.add(new_category)
        db.session.commit()
        return sku_schema.dump(new_category)


class SubCategoryListResource(Resource):
    def get(self):
        sub_categorys = RefSubCategory.query.all()
        return skus_schema.dump(sub_categorys)

    def post(self):
        new_sub_category = RefSubCategory(
            sub_category_name=request.json['sub_category_name'],
        )
        db.session.add(new_sub_category)
        db.session.commit()
        return sku_schema.dump(new_sub_category)


class SkuListResource(Resource):
    def get(self):
        if request.args:
            sku = Sku.query.filter_by(**request.args).all()
        else:
            sku = Sku.query.all()

        return skus_schema.dump(sku)

    def post(self):
        new_sku = Sku(
            sku_name=request.json['sku_name'],
            location_id=request.json['location_id'],
            department_id=request.json['department_id'],
            category_id=request.json['category_id'],
            sub_category_id=request.json['sub_category_id']
        )
        db.session.add(new_sku)
        db.session.commit()
        return sku_schema.dump(new_sku)


api.add_resource(LocationListResource, '/api/v1/locations')
api.add_resource(DepartmentListResource, '/api/v1/departments')
api.add_resource(CategoryListResource, '/api/v1/categorys')
api.add_resource(SubCategoryListResource, '/api/v1/subcategorys')
api.add_resource(SkuListResource, '/api/v1/skus')


class SkuResource(Resource):
    def get(self, id):
        sku = Sku.query.get_or_404(id)
        return sku_schema.dump(sku)

    def patch(self, id):
        sku = Sku.query.get_or_404(id)

        if 'location_id' in request.json:
            sku.location_id = request.json['location_id']
        if 'department_id' in request.json:
            sku.department_id = request.json['department_id']
        if 'category_id' in request.json:
            sku.category_id = request.json['category_id']
        if 'sub_category_id' in request.json:
            sku.sub_category_id = request.json['sub_category_id']

        db.session.commit()
        return sku_schema.dump(sku)

    def delete(self, id):
        sku = Sku.query.get_or_404(id)
        db.session.delete(sku)
        db.session.commit()
        return '', 204


api.add_resource(SkuResource, '/api/v1/sku/<int:id>')


if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
