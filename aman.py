from flask import Flask
from flask_restful import Api, Resource, reqparse, abort

#Creates an app within Flask
app = Flask(__name__)
#Wraps our app in an api
api = Api(app)


#Creats a request pareser object which automatically parse throught he requests being sent
video_put_args = reqparse.RequestParser()
video_put_args.add_argument("name", type=str, help="Name of the video is required", required=True)
video_put_args.add_argument("views", type=int, help="Views of the video", required=True)
video_put_args.add_argument("likes", type=int, help="Likes on the video", required=True)
#Creating an object which will give specific info about the name
videos = {}


def abort_if_video_doesnot_exist(video_id):
    if video_id not in videos:
        abort(404, message="Video ID is not valid... ")

def abort_if_video_exists(video_id):
    if video_id in videos:
        abort(409, message="Video already exists with that ID...")

#Inherting from resource
class Video(Resource):
    #Method for sending GET Request
    def get(self, video_id):
        abort_if_video_doesnot_exist(video_id)
        return videos[video_id]
    
    #Method for CREATE Request
    def put(self, video_id):
        #Will take all the arguments
        abort_if_video_exists(video_id)
        args = video_put_args.parse_args()
        videos[video_id] = args
        return videos[video_id], 201
        
    def delete(self, video_id):
        abort_if_video_doesnot_exist(video_id)
        del videos[video_id]
        return '', 204



#Register this as a resource in an api
api.add_resource(Video, "/video/<int:video_id>") #Helps accesing specific names


#Starts our server and starts our flask application
if __name__ == "__aman__":
    app.run(debug=True)

