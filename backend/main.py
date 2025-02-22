import os
import sys

sys.path.insert(0, '/')
from app_instance import app
from app_configuration import configure_current_application


configure_current_application()


@app.route('/')
def hello():
    return '<h1>Hello World!</h1><br><i>Server is running</i>'


# Required for Vercel to detect the app
def handler(event, context):
    return app(event, context)


if __name__ == '__main__':
    app.run(debug=True)
