from flask import Flask
from flask_restful import Api, Resource

#Creates an app within Flask
app = Flask(__name__)
#Wraps our app in an api
api = Api(app)

#Creating an object which will give specific info about the name
names = {"aman": {"age":23, "gender": "male"},
         "Garima": {"age":22, "gender": "female"}}

#Inherting from resource
class HelloWorld(Resource):
    #Creating a GET Method for sending get request
    def get(self, name):
        return names[name] #Dictionary - to get JSON Serializable Objects

#Register this as a resource in an api
api.add_resource(HelloWorld, "/helloworld/<string:name>") #Helps accesing specific names


#Starts our server and starts our flask application
if __name__ == "__code__":
    app.run(debug=True)

