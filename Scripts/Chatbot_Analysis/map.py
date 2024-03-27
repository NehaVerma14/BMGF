import folium
import pandas as pd

def main():
    # Create a Folium map centered around Nepal
    nepal_map = folium.Map(location=[28.3949, 84.1240], zoom_start=7)

    # Load the GeoJSON file outlining Nepal's borders
    nepal_geojson_url = "https://raw.githubusercontent.com/Acesmndr/nepal-geojson/master/generated-geojson/nepal-acesmndr.geojson"
    nepal_layer = folium.GeoJson(
        nepal_geojson_url,
        name='Nepal',
        style_function=lambda x: {
            'color': 'black',
            'weight': 2,
            'fillColor': 'transparent'  
        }
    )
    nepal_layer.add_to(nepal_map)

    # Load municipality coordinates data
    municipality_data = pd.read_csv("Data/municipality_coordinates.csv")

    # Plot municipality coordinates
    for index, row in municipality_data.iterrows():
        folium.Marker(location=[row['Latitude'], row['Longitude']], popup=row['Municipality']).add_to(nepal_map)

    # Display the map
    nepal_map.save("Results/Chatbot_Analysis/nepal_map.html")

if __name__ == "__main__":
    main()
