from flask import Blueprint, request, render_template
from config import db


first_route = Blueprint('first_route', __name__)



class Region(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)

    def get_id(self):
        return self.id

    def __repr__(self):
        return f'Region ID: {self.id}; Region name: {self.name}'

    def __init__(self, id, name):
        self.id = id
        self.name = name





class AreaTaxParam(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    city_id = db.Column(db.Integer, nullable=False)
    rate = db.Column(db.Numeric, nullable=False)

    def __repr__(self):
        return f'<Tax ID: {self.id}; Region ID: {self.city_id}; Rate: {self.rate}>'

    def __init__(self, id, city_id, rate):
        self.id = id
        self.city_id = city_id
        self.rate = rate

    def get_id(self):
        return self.id

    def get_data_for_rate(self):
        return self.rate




@first_route.route('/web/region')
def  print_region():
    try:
        query_all = Region.query.all()
        region = list(map(lambda x: x.__repr__(), query_all))
        return render_template('region_list.html', list=region)
    except Exception as e:
        print(e)
        error_body = {'reason': 'Unknown error'}
        return error_body, 400


@first_route.route('/v1/region/add', methods=['POST'])
def  add_region():
    try:
        region_id = request.form['id']
        region_name = request.form['name']
        region_id = int(region_id)
        regions = list(map(lambda x: x.get_id(), Region.query.all()))
        if region_id in regions:
            error_body = {'reason': 'This region already exist'}
            return render_template('region_add.html', res=error_body)
        else:
            new_region = Region(region_id, region_name)
            db.session.add(new_region)
            db.session.commit()
            message = {'reason': 'OK'}
            return render_template('region_add.html', res=message)
    except Exception as e:
        print(e)
        error_body = {'reason': 'Unknown error'}
        return render_template('region_add.html', res=error_body)


@first_route.route('/v1/region/update', methods=['POST'])
def update_region():
    try:
        region_id = request.form['id']
        region_name = request.form['name']
        region_id = int(region_id)
        regions = list(map(lambda x: x.get_id(), Region.query.all()))
        if region_id in regions:
            Region.query.filter_by(id=region_id).update({'name': region_name})
            db.session.commit()
            message = {'reason': 'OK'}
            return render_template('region_update.html', res=message)
        else:
            error_body = {'reason': 'This region is not exist'}
            return render_template('region_update.html', res=error_body)
    except Exception as e:
        print(e)
        error_body = {'reason': 'Unknown error'}
        return render_template('region_update.html', res=error_body)

@first_route.route('/v1/region/delete', methods=['POST'])
def delete_region():
    try:
        region_id = request.form['id']
        region_id = int(region_id)
        regions = list(map(lambda x: x.get_id(), Region.query.all()))
        if region_id in regions:
            AreaTaxParam.query.filter_by(city_id=region_id).delete()
            CarTaxParam.query.filter_by(city_id=region_id).delete()
            Region.query.filter_by(id=region_id).delete()
            db.session.commit()
            message = {'reason': 'Region removed'}
            return render_template('region_delete.html', res=message)
        else:
            error_body = {'reason': 'This region is not exist'}
            return render_template('region_delete.html', res=error_body)
    except Exception as e:
        print(e)
        error_body = {'reason': 'Unknown error'}
        return render_template('region_delete.html', res=error_body)


@first_route.route('/web/region/add')
def one():
    return render_template('region_add.html')


@first_route.route('/web/region/update')
def two():
    return render_template('region_update.html')


@first_route.route('/web/region/delete')
def three():
    return render_template('region_delete.html')

