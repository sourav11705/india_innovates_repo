import streamlit as st
import base64
from components.map_view import render_map
from components.activity_feed import render_activity_feed
from firebase_utils import get_feedbacks

st.set_page_config(
    page_title="CivicSense Authority Portal",
    page_icon="🏛️",
    layout="wide",
    initial_sidebar_state="expanded"
)

def main():
    st.sidebar.title("🏛️ CivicSense Portal")
    st.sidebar.markdown("**Authority Command Center**")
    
    # Navigation
    st.sidebar.markdown("---")
    page = st.sidebar.radio("Command Navigation", ["Live Geofence Map", "Citizen Feedback Reports"])
    
    if page == "Live Geofence Map":
        st.title("📍 Civic Geofences Map")
        st.markdown("Real-time monitoring of Public Areas (Hospitals, Colleges, BRidges) ensuring civic sense push notifications.")
        
        col1, col2 = st.columns([3, 1])
        
        with col1:
            render_map()
            
        with col2:
            st.markdown("### 📡 Live Feed")
            render_activity_feed()

    elif page == "Citizen Feedback Reports":
        st.title("📥 Civic Rule Violations & Infrastructure Reports")
        st.markdown("Live complaints submitted by citizens actively situated inside designated Civic Zones.")

        if st.button("🔄 Refresh Reports"):
            st.cache_data.clear()

        feedbacks = get_feedbacks()
        
        if not feedbacks:
            st.info("No citizen reports have been filed yet.")
            return

        # Display forms creatively
        for report in feedbacks:
            with st.container():
                st.markdown(f"### Report from Region: `{report.get('zoneName', 'Unknown')}`")
                
                cols = st.columns([2, 1])
                with cols[0]:
                    st.markdown(f"**Description:**")
                    st.write(report.get('problemDescription', 'No description provided.'))
                    
                    st.markdown(f"**GPS Coordinates:** Lat {report.get('latitude', '--')}, Lng {report.get('longitude', '--')}")
                    st.markdown(f"**Date Filed:** {report.get('formatted_time', 'Recently')}")
                
                with cols[1]:
                    photo_data = report.get('photoBase64', '')
                    if photo_data and photo_data.startswith('data:image'):
                        try:
                            # Split header from base64 string "data:image/png;base64,iVBORw0K..."
                            header, base64_str = photo_data.split(',', 1)
                            img_bytes = base64.b64decode(base64_str)
                            st.image(img_bytes, caption="Attached Evidence", use_container_width=True)
                        except Exception as e:
                            st.warning(f"Could not load image data.")
                    else:
                        st.info("No accompanying photo evidence provided.")
                
                st.markdown("---")

if __name__ == "__main__":
    main()
