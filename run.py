# from app import create_app
from api import create_app

app = create_app('config.DevelopmentConfig')

if __name__ == '__main__':
    app.run()