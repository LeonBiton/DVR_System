from flask_restful import reqparse


class ParsePut:
    mission_put_args = reqparse.RequestParser()

    def __init__(self):
        self.mission_put_args.add_argument("mission_name", type=str, help="mission_name", required=True)
        self.mission_put_args.add_argument("ip", type=str, help="IP", required=True)
        self.mission_put_args.add_argument("port", type=int, help="Port", required=True)
        self.mission_put_args.add_argument("type", type=str, help="Type", required=True)
        self.mission_put_args.add_argument("duration", type=int, help="Duration", required=True)


class ParseUpdate:
    mission_update_args = reqparse.RequestParser()

    def __init__(self):
        self.mission_update_args.add_argument("mission_name", type=str, help="Mission_name")
        self.mission_update_args.add_argument("ip", type=str, help="IP")
        self.mission_update_args.add_argument("port", type=int, help="Port")
        self.mission_update_args.add_argument("type", type=str, help="Type")
        self.mission_update_args.add_argument("duration", type=int, help="Duration")

