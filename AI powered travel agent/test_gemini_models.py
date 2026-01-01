from utils import search_places, get_image_url, get_weather

print("🔍 Testing Serper API:")
places = search_places("Best places to visit in Paris")
print(places)

print("\n🌤 Testing Weather API:")
weather = get_weather("Paris")
print(weather)

print("\n🖼 Testing Unsplash API:")
image_url = get_image_url("Paris")
print(image_url)
