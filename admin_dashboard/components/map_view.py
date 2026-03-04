import streamlit as st
import folium
from streamlit_folium import st_folium
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from firebase_utils import get_geofences

def render_map():
    # Center map on New Delhi
    center_coords = [28.6139, 77.2090]
    
    # Create Folium Map with a dark tile theme
    m = folium.Map(location=center_coords, zoom_start=11, tiles="CartoDB dark_matter")
    
    geofences = get_geofences()
    
    # Add Geofences around project coordinates
    for gf in geofences:
        popup_html = f"""
        <div style="font-family: sans-serif; min-width: 250px;">
            <h4 style="margin-top: 0; color: #333;">{gf["title"]}</h4>
            <div style="
                display: inline-block; 
                padding: 3px 8px; 
                margin-bottom: 8px;
                border-radius: 4px; 
                background-color: {gf['color']}; 
                color: white; 
                font-weight: bold;
                font-size: 0.8em;">
                TYPE: {gf['type'].upper()}
            </div>
            <p style="margin: 5px 0; color: #555;"><strong>Radius:</strong> {gf["radius"]}m</p>
            <p style="margin: 5px 0; color: #333; font-style: italic;">"{gf["message"]}"</p>
        </div>
        """
        
        folium.Circle(
            location=gf["coords"],
            radius=gf["radius"],
            color=gf["color"],
            fill=True,
            fill_color=gf["color"],
            fill_opacity=0.4,
            popup=folium.Popup(popup_html, max_width=350),
            tooltip=f"{gf['title']} ({gf['type']})"
        ).add_to(m)

    st_data = st_folium(m, width=800, height=600, returned_objects=[])
