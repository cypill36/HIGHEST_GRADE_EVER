from csi3335sp2023 import mysql
from app import db, create_app, models

if __name__ == "__main__":
    app = create_app(mysql)

    with app.app_context():
        db.create_all()

    app.run(debug=True)
