import requests

BASE = "http://127.0.0.1:5000"

response = requests.post(BASE + "/detect_glare" , 
        {
            "lat":49.2699648,
            "lon":-123.1290368,
            "epoch":1588704959.321,
            "orientation":-10.2,
        })
            

print(response.json())