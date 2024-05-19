import tweepy 
from tweepy.errors import TweepyException
import requests
import matplotlib.pyplot as plt

api_key ="fGM8oicdXCoR9Ogwny4nV5Tp7"
api_secret="ohBcDkWSRMLrinKEXZEY0BMO8KhmsfMPSvTdK5V0tWpmQNounZ"
bearer_token=r"AAAAAAAAAAAAAAAAAAAAANV4twEAAAAAh%2FF5qFqKyD5wyq1gyPWHsV%2FSOZg%3DV5gz2P5lP2rcO1hgt2IpHemG3jmP6dcgoaIJde2E8oV5Bv4Aeu"
access_token="720636668122935296-T3e1GjSMFBUq1By4f0ixkKAKhFSwXhG"
access_secret="Y5J9r3YoL0sub3t7vL0V4OKBA7fslCW644sZDbcffVJbz"



# Function to authenticate with Twitter API
def authenticate_twitter():
  """
  Authenticates with Twitter API using OAuth 1.1
  """
  auth = tweepy.OAuthHandler(api_key, api_secret)
  auth.set_access_token(access_token, access_secret)
  api = tweepy.API(auth)
  return api

# Function to search tweets with basic error handling
def search_tweets(hashtag, api):
  """
  Searches for tweets containing a hashtag and performs basic error handling.

  Args:
      hashtag: The hashtag to search for (e.g., "#hackathon").
      api: The authenticated tweepy API object.

  Returns:
      A list of dictionaries containing cleaned tweet data with geolocation, 
      or None if an error occurs.
  """
  try:
    tweets = api.search_tweets(q=hashtag, count=100)

    cleaned_tweets = []
    for tweet in tweets:
      # Extract location text (consider user location or geotagged tweets)
      location_text = tweet.user.location

      # Clean location text (optional: standardize city names)
      # ... (implement logic for cleaning location text)

      # Process geolocation using Google Maps API
      geolocation = process_geolocation(location_text)

      if geolocation:
        # Add geolocation data and map URL (if generated) to tweet dictionary
        tweet_data = {
          "text": tweet.text,
          "location": location_text,  # Keep original location text
          "geolocation": geolocation
        }
        map_url = generate_static_map(geolocation)
        if map_url:
          tweet_data["map_url"] = map_url
        cleaned_tweets.append(tweet_data)
    return cleaned_tweets
  except TweepyException as e:
    print(f"Error searching tweets: {e}")
    return None

# Function to process geolocation using Google Maps API
def process_geolocation(location_text):
  """
  Processes a location string using Google Maps Geocoding API.

  Args:
      location_text: The location string obtained from tweets (e.g., city name).

  Returns:
      A dictionary containing latitude and longitude if successful, 
      or None if location processing fails.
  """
  base_url = "https://maps.googleapis.com/maps/api/geocode/json?"
  google_maps_api_key = "AIzaSyCz1eBLY1lws56Q6uPXKw-h0o16a-zcqUM"
  params = {
      "address": location_text,
      "key": google_maps_api_key 
  }

  response = requests.get(base_url, params=params)

  if response.status_code == 200:
    data = response.json()
    # Check for successful geocoding results
    if data["status"] == "OK":
      # Extract latitude and longitude from the first result
      location_data = data["results"][0]["geometry"]["location"]
      return location_data
    else:
      print(f"Geocoding failed for location: {location_text} - {data['status']}")
      return None
  else:
    print(f"Error making geocoding request: {response.status_code}")
    return None

# Function to generate static map URL using Google Maps Static API
def generate_static_map(location_data, zoom_level=10, size="400x400"):
  """
  Generates a static map image URL using Google Maps Static API.

  Args:
      location_data: A dictionary containing latitude and longitude for a location.
      zoom_level: The zoom level for the map (optional, default: 10).
      size: The size of the map image (optional, default: "400x400").

  Returns:
      A string containing the static map image URL if successful, None otherwise.
  """
  base_url = "https://maps.googleapis.com/maps/api/staticmap?"
  google_maps_api_key = "AIzaSyCz1eBLY1lws56Q6uPXKw-h0o16a-zcqUM"
  params = {
      "center": f"{location_data['lat']},{location_data['lng']}",
      "zoom": zoom_level,
      "size": size,
      "key": google_maps_api_key
        }

  response = requests.get(base_url, params=params)

  if response.status_code == 200:
    return response.url  # Return the static map image URL
  else:
    print(f"Error generating static map: {response.status_code}")
    return None

# Function to visualize tweet locations using Matplotlib (optional)
def visualize_locations(tweet_data):
  """
  Creates a scatter plot visualization of tweet locations.

  Args:
      tweet_data: A list of dictionaries containing tweet data with geolocation.
  """
  # Extract latitude and longitude data
  latitudes = [tweet["geolocation"]["lat"] for tweet in tweet_data if tweet["geolocation"]]
  longitudes = [tweet["geolocation"]["lng"] for tweet in tweet_data if tweet["geolocation"]]

  # Consider using a base map image (optional)
  # ... (implement logic for adding a base map image)

  # Basic scatter plot
  plt.scatter(longitudes, latitudes)
  plt.xlabel("Longitude")
  plt.ylabel("Latitude")
  plt.title("Tweet Locations by Geolocation")
  plt.show()

# Main program flow
if __name__ == "__main__":
  # Authenticate with Twitter API
  api = authenticate_twitter()

  # Define the hashtag to search for
  hashtag = "#hackathon2024"

  # Search for tweets and process geolocation
  cleaned_tweets = search_tweets(hashtag, api)

  if cleaned_tweets:
    # Optionally visualize tweet locations
    visualize_locations(cleaned_tweets)

    # Process or analyze the cleaned_tweets data further (e.g., sentiment analysis)
    # ... (implement your data analysis logic)
    print("Tweet data retrieved and processed successfully!")
  else:
    print("Error occurred while fetching tweets. Please check logs for details.")