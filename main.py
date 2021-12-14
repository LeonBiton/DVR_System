from flask_restful import Resource, abort, fields, marshal_with
from server import FlaskServer
from database import Database
from pareser import ParsePut, ParseUpdate

server = FlaskServer()
database = Database(server)


class DvrModel(database.table.Model):
    id = database.table.Column(database.table.Integer, primary_key=True)
    mission_name = database.table.Column(database.table.String(50), nullable=False)
    ip = database.table.Column(database.table.String(15), nullable=False)
    port = database.table.Column(database.table.Integer, nullable=False)
    type = database.table.Column(database.table.String(20), nullable=False)
    duration = database.table.Column(database.table.Integer, nullable=False)

    def __repr__(self):
        return f"MissionData('{self.mission_name}', '{self.ip}', '{self.port}', '{self.type}', '{self.duration}')"


database.table.create_all()

resource_field = {
    'id': fields.Integer,
    'mission_name': fields.String,
    'ip': fields.String,
    'port': fields.Integer,
    'type': fields.String,
    'duration': fields.Integer
}


class Mission(Resource):
    @marshal_with(resource_field)
    def get(self, mission_id):
        result = DvrModel.query.filter_by(id=mission_id).first()
        if not result:
            abort(404, message="Mission not found")
        return result

    @marshal_with(resource_field)
    def put(self, mission_id):
        args = ParsePut().mission_put_args.parse_args()
        result = DvrModel.query.filter_by(id=mission_id).first()
        if result:
            abort(409, message="Mission id taken")
        mission = DvrModel(id=mission_id, mission_name=args['mission_name'],
                           ip=args['ip'], port=args['port'],
                           type=args['type'], duration=args['duration'])
        database.add(mission)
        return mission

    @marshal_with(resource_field)
    def patch(self, mission_id):
        args = ParseUpdate().mission_update_args.parse_args()
        result = DvrModel.query.filter_by(id=mission_id).first()
        if not result:
            abort(404, message="Mission not found, cannot update")
        if args['mission_name']:
            result.mission_name = args['mission_name']
        if args['ip']:
            result.ip = args['ip']
        if args["port"]:
            result.port = args['port']
        if args["type"]:
            result.type = args['type']
        if args["duration"]:
            result.duration = args['duration']

        database.table.session.commit()
        return result

    @marshal_with(resource_field)
    def delete(self, mission_id):
        delete_this = DvrModel.query.filter_by(id=mission_id).first()
        if not delete_this:
            abort(404, message="Mission not found, cannot delete")
        DvrModel.query.filter_by(id=mission_id).delete()
        database.table.session.commit()
        return delete_this


class AllMissions(Resource):
    @marshal_with(resource_field)
    def get(self):
        result = []
        missions = DvrModel.query.all()
        for mission in missions:
            result.append(mission)
        return result


server.api.add_resource(Mission, "/mission/<int:mission_id>")
server.api.add_resource(AllMissions, "/mission")

if __name__ == "__main__":
    server.app.run(debug=True)
