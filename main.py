from flask import Flask
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy

#Creates an app within Flask
app = Flask(__name__)
#Wraps our app in an api
api = Api(app)

#Creating config to define the location of your database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
#Creates database
db = SQLAlchemy(app)

#To create database model
class VideoModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    views = db.Column(db.Integer, nullable=False)
    likes = db.Column(db.Integer, nullable=False)

    def __repr__(self): 
        return "fVideo(name = {name}, views = {views}, likes = {likes})"




#Creats a request pareser object which automatically parse throught he requests being sent
video_put_args = reqparse.RequestParser()
video_put_args.add_argument("name", type=str, help="Name of the video is required", required=True)
video_put_args.add_argument("views", type=int, help="Views of the video", required=True)
video_put_args.add_argument("likes", type=int, help="Likes on the video", required=True)

video_update_args = reqparse.RequestParser()
video_update_args.add_argument("name", type=str, help="Name of the video is required")
video_update_args.add_argument("views", type=int, help="Views of the video")
video_update_args.add_argument("likes", type=int, help="Likes on the video")



#A way to understand how objects can be serialized
resource_fields = {
       'id': fields.Integer,
       'name': fields.String,
       'views': fields.Integer,
       'likes': fields.Integer
}

#Inherting from resource
class Video(Resource):
    #Take the return values and serialize it according to that field
    @marshal_with(resource_fields)
    #Method for sending GET Request
    def get(self, video_id):
        result = VideoModel.query.filter_by(id=video_id).first() #Give instances of the VideoModel that matches with the video_id
        if not result:
            abort(404, message = "Could not find video with that ID") 
        return result
    
    @marshal_with(resource_fields)
    #Method for sending CREATE Request
    def put(self, video_id):
        #Will take all the arguments
        args = video_put_args.parse_args()
        result = VideoModel.query.filter_by(id=video_id).first()
        if result:
            abort(409, message = "Video_id Taken...")
        video = VideoModel(id = video_id, name = args['name'], views = args['views'], likes = args['likes'])
        #Temporarily adding data in database
        db.session.add(video)
        #Commit the changes made in the session in the database
        db.session.commit()
        return video, 201
    
    @marshal_with(resource_fields)
    #Method for sending UPDATE Request
    def patch(self, video_id):
        args = video_update_args.parse_args()
        result = VideoModel.query.filter_by(id=video_id).first()
        if not result:
            abort(404, message = "Could not find video with that ID.. Cannot Update")

        if args['name']:
            result.name = args['name']
        if args['views']:
            result.views = args['views']
        if args['likes']:
            result.likes = args['likes']

        db.session.commit()
        return result
        

    @marshal_with(resource_fields)
    #Method for sending DELETE Request    
    def delete(self, video_id):
        result = VideoModel.query.filter_by(id=video_id).first()
        if not result:
            abort(404, message = "Could not find video with that ID")
        db.session.delete(result)
        db.session.commit()
        return '', 204



#Register this as a resource in an api
api.add_resource(Video, "/video/<int:video_id>") #Helps accesing specific names


#Starts our server and starts our flask application
if __name__ == "__main__":
    app.run(debug=True)

