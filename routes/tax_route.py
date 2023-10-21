from flask import Blueprint, request, render_template
from routes.tax_param_route import CarTaxParam


third_route = Blueprint('third_route', __name__)


@third_route.route('/v1/car/tax/calc', methods=['POST'])
def auto_calc():
    try:
        city_id = int(request.form['city_id'])
        hp = int(request.form['hp'])
        year = int(request.form['year'])
        rate = list(map(lambda x: x.get_data_for_rate(), CarTaxParam.query.filter_by(city_id=city_id).all()))
        print(rate)
        print(rate[1])
        if len(rate)==0:
            error_body = {'reason': 'For this region taxes not exist'}
            return render_template('index.html', res=error_body)
        else:
            for i in rate:
                if int(i[2]) < int(hp) <= int(i[3]) and int(i[4]) < int(year) <= int(i[5]):
                    res = int(i[6]) * int(hp)
                    message = {'result': res}
                    return render_template('index.html', res=message)
        error_body = {'reason': 'There is no suitable tax'}
        return render_template('index.html', res=error_body)
    except Exception as e:
        print(e)
        error_body = {'reason': 'Unknown error'}
        return render_template('index.html', res=error_body)


@third_route.route('/')
def print_form():
    return render_template('index.html')