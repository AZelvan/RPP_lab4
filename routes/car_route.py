from flask import Blueprint, request
from routes.region_route import Region, CarTaxParam
from config import db

second_route = Blueprint('second_route', __name__)


@second_route.route('/v1/car/tax-param/add', methods=['POST'])
def add_new_tax_auto():
    try:
        car_id = request.json['id']
        city_id = request.json['city_id']
        from_hp_car = request.json['from_hp_car']
        to_hp_car = request.json['to_hp_car']
        from_production_year_car = request.json['from_production_year_car']
        to_production_year_car = request.json['to_production_year_car']
        rate = request.json['rate']
        tax = list(map(lambda x: x.get_id(), CarTaxParam.query.all()))
        regions = list(map(lambda x: x.get_id(), Region.query.all()))
        if city_id not in regions:
            error_body = {'reason': 'This region is not exist'}
            return error_body, 400
        if car_id in tax :
            error_body = {'reason': 'This tax already exist'}
            return error_body, 400
        else:
            new_tax = CarTaxParam(car_id, city_id, from_hp_car, to_hp_car, from_production_year_car, to_production_year_car, rate)
            db.session.add(new_tax)
            db.session.commit()
            message = {'reason': 'OK'}
            return message, 200
    except Exception as e:
        print(e)
        error_body = {'reason': 'Unknown error'}
        return error_body, 400


@second_route.route('/v1/car/tax-param/update', methods=['POST'])
def update_tax_auto():
    try:
        car_id = request.json['id']
        city_id = request.json['city_id']
        from_hp_car = request.json['from_hp_car']
        to_hp_car = request.json['to_hp_car']
        from_production_year_car = request.json['from_production_year_car']
        to_production_year_car = request.json['to_production_year_car']
        rate = request.json['rate']
        regions = list(map(lambda x: x.get_id(), Region.query.all()))
        if city_id not in regions:
            error_body = {'reason': 'This region is not exist'}
            return error_body, 400
        tax = list(map(lambda x: x.get_id(), CarTaxParam.query.all()))
        if car_id in tax:
            CarTaxParam.query.filter_by(id=car_id).update({'city_id': city_id, 'from_hp_car': from_hp_car, 'to_hp_car': to_hp_car, 'from_production_year_car': from_production_year_car, 'to_production_year_car': to_production_year_car, 'rate': rate})
            db.session.commit()
            message = {'reason': 'Taxes update'}
            return message, 200
        else:
            error_body = {'reason': 'This tax is not exist'}
            return error_body, 400
    except Exception as e:
        print(e)
        error_body = {'reason': 'Unknown error'}
        return error_body, 400


@second_route.route('/v1/car/tax-param/delete', methods=['POST'])
def delete_tax_auto():
    try:
        car_id = request.json['id']
        # city_id = db.session.get(CarTaxParam, car_id)
        # print(city_id)
        city= list(map(lambda x: x.get_region(), CarTaxParam.query.filter_by(id=car_id)))
        print(city)
        city_id = int(city[0])
        regions = list(map(lambda x: x.get_id(), Region.query.all()))
        if city_id not in regions:
            error_body = {'reason': 'This region is not exist'}
            return error_body, 400
        car = list(map(lambda x: x.get_id(), CarTaxParam.query.all()))
        if car_id in car:
            CarTaxParam.query.filter_by(id=car_id).delete()
            db.session.commit()
            message = {'reason': 'Tax removed'}
            return message, 200
        else:
            error_body = {'reason': 'This tax is not exist'}
            return error_body, 400
    except Exception as e:
        print(e)
        error_body = {'reason': 'Unknown error'}
        return error_body, 400


@second_route.route('/v1/car/tax-param/get/<id>')
def fetch_tax_auto(id):
    try:
        if id is None:
            error_body = {'reason': 'id is empty'}
            return error_body, 400
        if id == "all":
            tax_auto = list(map(lambda x: x.__repr__(), CarTaxParam.query.all()))
            return tax_auto, 200
        else:
            id = int(id)
            car = list(map(lambda x: x.get_id(), CarTaxParam.query.all()))
            if id in car:
                tax_auto = list(map(lambda x: x.__repr__(), CarTaxParam.query.filter_by(id=id,).all()))
                return tax_auto, 200
            else:
                error_body = {'reason': 'This tax is not exist'}
                return error_body, 400
    except Exception as e:
        print(e)
        error_body = {'reason': 'Unknown error'}
        return error_body, 400


@second_route.route('/v1/car/tax/calc/<id>/<year>/<hp>')
def auto_calc(id, year, hp):
    try:
        rate = list(map(lambda x: x.get_data_for_rate(), CarTaxParam.query.filter_by(city_id=id).all()))
        print(rate)
        if len(rate)==0:
            error_body = {'reason': 'For this region taxes not exist'}
            return error_body, 400
        else:
            for i in rate:
                if int(i[2]) < int(hp) <= int(i[3]) and int(i[4]) < int(year) <= int(i[5]):
                    res = int(i[6]) * int(hp)
                    message = {'result': res}
                    return message, 200
                else:
                    error_body = {'reason': 'There is no suitable tax'}
                    return error_body, 400
    except Exception as e:
        print(e)
        error_body = {'reason': 'Unknown error'}
        return error_body, 400