from flask import Flask
from flask_restful import Api, Resource, reqparse, abort

from pysolar.solar import *
import datetime
import time

app = Flask(__name__)
api = Api(app)

glare_post_args = reqparse.RequestParser()
glare_post_args.add_argument("lat", type=str, help="latitude of the location is required", required=True)
glare_post_args.add_argument("lon", type=str, help="longitude of the location is required", required=True)
glare_post_args.add_argument("epoch", type=str, help="Linux epoch in second is required", required=True)
glare_post_args.add_argument("orientation", type=str, help="orientation of car travel is required", required=True)


def abort_if_location_doesnt_exist(latitude, longitude):
	if latitude > 90 or latitude < -90 or longitude > 180 or longitude < -180:
		abort(404, message="the location doesn't exist...")

def abort_if_epoch_isnt_valid(epoch_time):
	if epoch_time < 0 or epoch_time > time.time() :
		abort(404, message="the epoch entered is not valid...")

def abort_if_orientation_isnt_valid(orientation_of_driving):
	if orientation_of_driving < -180 or orientation_of_driving > 180:
		abort(404, message="the orientation of driving is not valid...")

# define a function to determine two angle difference is less than 30 degrees
# in the angle coordinates 0~360 degrees
def angle_difference_is_less_than_30_degrees (x, y):
	"""Function that determine if the angle difference is less than 30 degrees
    Args:
        x: angle x in the coordinates 0~360 degrees
        y: angle y in the coordinates 0~360 degrees
    Returns:
        Return True if the angle difference is less than 30 degrees
        Return False if the angle difference is greater than 30 degrees
    """
	if x < 0 or x > 360 or y < 0 or y > 360:
		abort(404, message="the angles are not in 0~360 degrees...")
	if abs(x - y) < 30 or abs(x - y + 360) < 30 or abs(x - y - 360) < 30:
		return True
	return False

def glare_or_not (lat, lon, epoch, orientation):
	"""Function that determine if it is under the direct sun-glare conditions
    Args:
        lat: the latitude of the location where the image was taken
        lon: the longtitude of the location where the image was taken
        epoch: Linux epoch in second when the image was taken
        orientation: the direction of the car travel
    Returns:
        Return True if the angle difference is less than 30 degrees
        Return False if the angle difference is greater than 30 degrees
    """
	date = datetime.datetime.fromtimestamp(epoch, datetime.timezone.utc)
	altitude_deg = get_altitude(lat, lon, date)
	azimuth_deg = get_azimuth(lat, lon, date)

	# Convert orientation from the angle coordinates-180~180 degrees
	# to the angle coordinates 0~360 degrees
	if orientation < 0:
		orientation = 360 + orientation
		
	# Glare condition: altitude of the sun is 0~45 degrees
	if altitude_deg > 0 and altitude_deg < 50:
		# Glare condition: estimate of clear-sky radiation is greater than 500
		if radiation.get_radiation_direct(date, altitude_deg) > 500:
			# Glare condition: azimuthal difference between sun and
			# the direction of the car travel is 0~30 degrees
			if angle_difference_is_less_than_30_degrees (orientation,azimuth_deg):
				return {"glare": "true"}
		
	return {"glare": "false"}

class GetGlare(Resource):
	def post(self):
		# Parse the CLI arguments
		args = glare_post_args.parse_args()

		# Convert the input parameters from strings to floats
		lat = float(args.lat)
		lon = float(args.lon)
		epoch = float(args.epoch)
		orientation = float(args.orientation)

		# Validate if the input parameters are valid
		# abort and send error message if it is not valid
		abort_if_location_doesnt_exist (lat, lon)
		abort_if_epoch_isnt_valid (epoch)
		abort_if_orientation_isnt_valid (orientation)

		# Calculate glare or not and return the result
		return glare_or_not (lat, lon, epoch, orientation)


api.add_resource(GetGlare, "/detect_glare")

if __name__ == "__main__":
	app.run(debug=True)