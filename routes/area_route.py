from flask import Blueprint, request
from routes.region_route import Region, AreaTaxParam
from config import db


third_route = Blueprint('third_route', __name__)


@third_route.route('/v1/area/tax-param/add', methods=['POST'])
def add_new_tax_area():
    try:
        area_id = request.json['id']
        city_id = request.json['city_id']
        rate = request.json['rate']
        areas = list(map(lambda x: x.get_id(), AreaTaxParam.query.all()))
        if area_id in areas:
            error_body = {'reason': 'This tax already exist'}
            return error_body, 400
        else:
            new_data = AreaTaxParam(area_id, city_id, rate)
            db.session.add(new_data)
            db.session.commit()
            message = {'reason': 'OK'}
            return message, 200
    except Exception as e:
        print(e)
        error_body = {'reason': 'Unknown error'}
        return error_body, 400


@third_route.route('/v1/area/tax-param/update', methods=['POST'])
def update_tax_area():
    try:
        area_id = request.json['id']
        city_id = request.json['city_id']
        rate = request.json['rate']
        areas = list(map(lambda x: x.get_id(), AreaTaxParam.query.all()))
        if area_id in areas:
            AreaTaxParam.query.filter_by(id=area_id).update({'city_id': city_id, 'rate':rate})
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


@third_route.route('/v1/area/tax-param/delete', methods=['POST'])
def delete_tax_area():
    try:
        area_id = request.json['id']
        areas = list(map(lambda x: x.get_id(), AreaTaxParam.query.all()))
        if area_id in areas:
            AreaTaxParam.query.filter_by(id=area_id).delete()
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


@third_route.route('/v1/area/tax-param/get/<id>')
def fetch_tax_area(id):
    try:
        if id is None:
            error_body = {'reason': 'id is empty'}
            return error_body, 400
        if id == "all":
            area = list(map(lambda x: x.__repr__(), AreaTaxParam.query.all()))
            return area, 200
        else:
            areas = list(map(lambda x: x.get_id(), AreaTaxParam.query.all()))
            if int(id) in areas:
                area = list(map(lambda x: x.__repr__(), AreaTaxParam.query.filter_by(id=id).all()))
                return area, 200
            else:
                error_body = {'reason': 'This tax is not exist'}
                return error_body, 400
    except Exception as e:
        print(e)
        error_body = {'reason': 'Unknown error'}
        return error_body, 400


@third_route.route('/v1/area/tax/calc/<id>/<price>')
def tax_area_calc(id, price):
    try:
        if id is None or price is None:
            error_body = {'reason': 'Not enough data'}
            return error_body, 400
        rate = list(map(lambda x: x.get_data_for_rate(), AreaTaxParam.query.filter_by(city_id=id).all()))
        if rate is None:
            error_body = {'reason': 'There is no tax for this region'}
            return error_body, 400
        else:
            rate = int(rate[0])
            res = int(rate)*int(price)
            message = {'result': res}
            return message, 200
    except Exception as e:
        print(e)
        error_body = {'reason': 'Unknown error'}
        return error_body, 400