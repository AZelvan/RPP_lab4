from config import app

from routes.region_route import first_route
from routes.tax_param_route import second_route
from routes.area_route import third_route

app.register_blueprint(first_route)
app.register_blueprint(second_route)
app.register_blueprint(third_route)


if __name__ == '__main__':
    app.run(debug=True)