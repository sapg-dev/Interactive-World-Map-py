import json
import folium
import branca
import requests

url = 'https://raw.githubusercontent.com/python-visualization/folium/master/examples/data/world-countries.json'
geo_json_data = json.loads(requests.get(url).text)


with open('country-by-population (1).json') as f:
    population_data = json.load(f)


country_population = {item['country']: item['population'] for item in population_data}


max_population = max(country_population.values())
colormap = branca.colormap.linear.YlOrRd_09.scale(0, max_population)
colormap = colormap.to_step(index=[0, 100000, 1000000, 10000000, 100000000, 500000000, max_population])
colormap.caption = 'Population of Countries'

# Function to return the color based on population
def style_function(feature):
    country_name = feature['properties']['name']
    population = country_population.get(country_name)  # Get population from the dictionary
    if population is None:
        return {
            'fillOpacity': 0,
            'weight': 0,
            'fillColor': '#black'
        }

    return {
        'fillOpacity': 0.5,
        'weight': 0,
        'fillColor': '#black' if population is None else colormap(population)
    }


m = folium.Map(location=[0, 0], zoom_start=2)


folium.GeoJson(
    geo_json_data,
    style_function=style_function,
    tooltip=folium.GeoJsonTooltip(
        fields=['name'],
        aliases=['Country'],
        labels=True,
        sticky=False
    )
).add_to(m)


colormap.add_to(m)

# Saving the map to an HTML file
m.save('interactive_world_map.html')
