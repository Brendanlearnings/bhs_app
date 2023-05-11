#################### IMPORTS ####################
import streamlit as st
import streamlit.components.v1 as components
from datetime import date
import snowflake.connector
#################################################

def init_connection():
    return snowflake.connector.connect(
        **st.secrets["snowflake"], client_session_keep_alive=True
    )

def details():
    st.title('Class of 2013 Reunion')
    st.write()
    st.write("""Calling all Matrix Class of 2013 graduates from Paarl Boys High! 
    Get ready to embark on a thrilling journey down memory lane as we celebrate our monumental 10 year reunion. The anticipation is building, and the excitement is contagious! On the 5th of August 2023, our beloved school rugby field will transform into a pulsating hub of nostalgia and camaraderie. 
    Picture yourself surrounded by familiar faces, reliving those glorious moments that shaped our youth. The air will be filled with thunderous cheers, the echoes of our triumphs, and the unbreakable bonds of friendship. This is your chance to reconnect with old teammates, share stories of triumphs and challenges, and reignite the spirit that once burned so bright within us. Let's come together and create an unforgettable experience, where the spirit of the Matrix Class of 2013 shines once again. 
    Dust off your rugby jerseys, gather your memories, and prepare to be swept away by the electrifying energy that only a reunion of this magnitude can bring. The countdown has begun, and the stage is set. Brace yourselves for an extraordinary celebration, where we honor our legacy, relish our accomplishments, and create new memories that will last a lifetime. The Matrix Class of 2013 reunion is our moment to shine – let's make it legendary!""")
    components.html('''<iframe width="1128" height="635" src="https://www.youtube.com/embed/1oeaRq9-yBc" title="Paarl Boys High School" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen></iframe>''', height=650)

def merch():
    st.title('Merchandise')
    st.write('Would you like to purchase some merchandise for the up and coming event?')
# Set up the directory for pages in app
pages = {
    "Infromation": details,
    "Merchandise": merch
    
}

# Create a menu with the page names
selection = st.sidebar.radio("Navigate to:", list(pages.keys()))

# Display the selected page with its corresponding function
pages[selection]()