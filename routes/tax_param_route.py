from flask import Blueprint, request, render_template
from routes.region_route import Region
from config import db

second_route = Blueprint('second_route', __name__)

class CarTaxParam(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    city_id = db.Column(db.Integer, nullable=False)
    from_hp_car = db.Column(db.Integer, nullable=False)
    to_hp_car = db.Column(db.Integer, nullable=False)
    from_production_year_car = db.Column(db.Integer, nullable=False)
    to_production_year_car = db.Column(db.Integer, nullable=False)
    rate = db.Column(db.Numeric, nullable=False)

    def __init__(self, id, city_id, from_hp_car, to_hp_car, from_production_year_car, to_production_year_car, rate):
        self.id = id
        self.city_id = city_id
        self.from_hp_car = from_hp_car
        self.to_hp_car = to_hp_car
        self.from_production_year_car = from_production_year_car
        self.to_production_year_car = to_production_year_car
        self.rate = rate

    def __repr__(self):
        return f'< Tax ID: {self.id}; City ID {self.city_id}; From HP car: {self.from_hp_car}; To HP car: {self.to_hp_car}; From production year car {self.from_production_year_car}; To production year car: {self.to_production_year_car}; Rate {self.rate}>'

    def get_data_for_rate(self):
        return self.id, self.city_id, self.from_hp_car, self.to_hp_car, self.from_production_year_car, self.to_production_year_car, self.rate

    def get_id(self):
        return self.id

    def get_region (self):
        return self.city_id

@second_route.route('/v1/tax-param/add', methods=['POST'])
def add_new_tax_auto():
    try:
        car_id = int(request.form['id'])
        city_id = int(request.form['city_id'])
        from_hp_car = int(request.form['from_hp_car'])
        to_hp_car = int(request.form['to_hp_car'])
        from_production_year_car = int(request.form['from_production_year_car'])
        to_production_year_car = int(request.form['to_production_year_car'])
        rate = int(request.form['rate'])
        tax = list(map(lambda x: x.get_id(), CarTaxParam.query.all()))
        regions = list(map(lambda x: x.get_id(), Region.query.all()))
        if city_id not in regions:
            error_body = {'reason': 'This region is not exist'}
            return render_template('tax_param_add.html', res=error_body)
        if car_id in tax :
            error_body = {'reason': 'This tax already exist'}
            return render_template('tax_param_add.html', res=error_body)
        else:
            new_tax = CarTaxParam(car_id, city_id, from_hp_car, to_hp_car, from_production_year_car, to_production_year_car, rate)
            db.session.add(new_tax)
            db.session.commit()
            message = {'reason': 'OK'}
            return render_template('tax_param_add.html', res=message)
    except Exception as e:
        print(e)
        error_body = {'reason': 'Unknown error'}
        return render_template('tax_param_add.html', res=error_body)


@second_route.route('/v1/tax-param/update', methods=['POST'])
def update_tax_auto():
    try:
        car_id = int(request.form['id'])
        city_id = int(request.form['city_id'])
        from_hp_car = int(request.form['from_hp_car'])
        to_hp_car = int(request.form['to_hp_car'])
        from_production_year_car = int(request.form['from_production_year_car'])
        to_production_year_car = int(request.form['to_production_year_car'])
        rate = int(request.form['rate'])
        regions = list(map(lambda x: x.get_id(), Region.query.all()))
        if city_id not in regions:
            error_body = {'reason': 'This region is not exist'}
            return render_template('tax_param_updatee.html', res=error_body)
        tax = list(map(lambda x: x.get_id(), CarTaxParam.query.all()))
        if car_id in tax:
            CarTaxParam.query.filter_by(id=car_id).update({'city_id': city_id, 'from_hp_car': from_hp_car, 'to_hp_car': to_hp_car, 'from_production_year_car': from_production_year_car, 'to_production_year_car': to_production_year_car, 'rate': rate})
            db.session.commit()
            message = {'reason': 'Taxes update'}
            return render_template('tax_param_update.html', res=message)
        else:
            error_body = {'reason': 'This tax is not exist'}
            return render_template('tax_param_update.html', res=error_body)
    except Exception as e:
        print(e)
        error_body = {'reason': 'Unknown error'}
        return render_template('tax_param_update.html', res=error_body)


@second_route.route('/v1/tax-param/delete', methods=['POST'])
def delete_tax_auto():
    try:
        car_id = int(request.form['id'])
        city= list(map(lambda x: x.get_region(), CarTaxParam.query.filter_by(id=car_id)))
        city_id = int(city[0])
        regions = list(map(lambda x: x.get_id(), Region.query.all()))
        if city_id not in regions:
            error_body = {'reason': 'This region is not exist'}
            return render_template('tax_param_delete.html', res=error_body)
        car = list(map(lambda x: x.get_id(), CarTaxParam.query.all()))
        if car_id in car:
            CarTaxParam.query.filter_by(id=car_id).delete()
            db.session.commit()
            message = {'reason': 'Tax removed'}
            return render_template('tax_param_delete.html', res=message)
        else:
            error_body = {'reason': 'This tax is not exist'}
            return render_template('tax_param_delete.html', res=error_body)
    except Exception as e:
        print(e)
        error_body = {'reason': 'Unknown error'}
        return render_template('tax_param_delete.html', res=error_body)


@second_route.route('/web/tax-param/add')
def first():
    return render_template('tax_param_add.html')


@second_route.route('/web/tax-param/update')
def second():
    return render_template('tax_param_update.html')


@second_route.route('/web/tax-param/delete')
def third():
    return render_template('tax_param_delete.html')


@second_route.route('/web/tax-param')
def forth():
    try:
        tax_auto = list(map(lambda x: x.__repr__(), CarTaxParam.query.all()))
        return render_template('tax_param_list.html', list=tax_auto)
    except Exception as e:
        print(e)
        error_body = {'reason': 'Unknown error'}
        return error_body, 400
