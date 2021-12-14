from flask_sqlalchemy import SQLAlchemy


class Database:
    table = None

    def __init__(self, server):
        server.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///dvr_database.db'
        self.table = SQLAlchemy(server.app)

    def create_database(self):
        self.table.create_all()

    def add(self, data):
        self.table.session.add(data)
        self.table.session.commit()

    def delete(self, data):
        self.table.session.delete(data)
