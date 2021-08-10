import requests 

BASE = "http://127.0.0.1:5000/"

data = [{"name": "aman", "views": 15000, "likes": 10},
        {"name": "garima", "views": 14000, "likes": 20},
        {"name": "rahul", "views": 16000, "likes": 5}]


for i in range(len(data)):
    response = requests.put(BASE + "video/" + str(i), data[i])
    print(response.json())

input()
response = requests.delete(BASE + "video/0") 
print(response) #Not printing any JSON Value

input()
response = requests.get(BASE + "video/0")
print(response.json())

input()
response = requests.patch(BASE + "video/0", {"views": 40000})
print(response.json())