# Detect Glare
The goal of this repository is to detect direct sun-glare conditions from the images. The images were taken from a driving car and it is facing forward. The repository is built in REST API using Flask library. At the API endpoint, users can send requests with the following four paremeters to the server and get the response whether the image is glare or not.

# Paremeters:
lat: the latitude of the location where the image was taken
lon: the longtitude of the location where the image was taken
epoch: Linux epoch in second when the image was taken
orientation: the direction of the car travel when the image was taken

# Requirements
This was tested on Python 3.6. To install the required packages, use the provided requirements.txt file like so:
```
pip install -r requirements.txt
```

# Running the server
Simply excuting the following command at the server end
```
python main.py
```

# Test
To test, simply input the four paremeters in test.py and send the request to the server by excuting the following command at the API endpoint
```
python test.py
```
It will send the result to the API endpoint. If it is glare, the result is "True". If not, the result is "False"


# Limitation
 - The algorithm to detecing glare doesn't consider if there is any obstacle blocking the direct sun, such as buildings, trucks, mountains, etc. In this case, the result is "True", but it might be "False" actually
 
 - The algorithm doesn't consider the location is on land or in the sea. The images were taken when a car was driving on road. If the lat/lon indicates the location is in the sea, it should be an invalid request.