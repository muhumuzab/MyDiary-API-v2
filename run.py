import os

from application import create_app

if __name__ == '__main__':
    app = create_app('development')
    port = int(os.environ.get("PORT", 5000))
    app.run(port=port)
