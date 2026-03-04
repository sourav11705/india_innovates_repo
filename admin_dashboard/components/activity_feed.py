import streamlit as st
import os
import sys

# Ensure parent directory is in path so we can import firebase_utils
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from firebase_utils import get_activities

def render_activity_feed():
    st.markdown("""
    <style>
    .activity-feed {
        max-height: 500px;
        overflow-y: auto;
        padding-right: 10px;
    }
    .feed-item {
        background-color: #262730;
        padding: 10px;
        margin-bottom: 10px;
        border-radius: 5px;
        border-left: 4px solid #00d2ff;
        font-size: 0.9em;
    }
    .time-stamp {
        color: #888;
        font-size: 0.8em;
        margin-bottom: 4px;
        display: block;
    }
    </style>
    """, unsafe_allow_html=True)

    # Use a container to inject custom HTML for the scrolling feed
    container = st.container()
    
    activities = get_activities()
    
    # Build HTML dynamically
    feed_html = '<div class="activity-feed">\n'
    for act in activities:
        # Default styling assuming act format
        time_ago = act.get('time_ago', 'JUST NOW')
        icon = act.get('icon', '📝')
        message = act.get('message', '')
        
        feed_html += f"""
        <div class="feed-item">
            <span class="time-stamp">{time_ago}</span>
            {icon} {message}
        </div>
        """
        
    feed_html += '</div>'
    
    container.markdown(feed_html, unsafe_allow_html=True)

