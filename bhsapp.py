#################### IMPORTS ####################
import streamlit as st
import streamlit.components.v1 as components
# from streamlit.script_run_context import add_script_run_ctx
# from streamlit.report_thread import get_report_ctx
from datetime import date
import snowflake.connector
import random
#################################################

def init_connection():
    return snowflake.connector.connect(
        **st.secrets["snowflake"], client_session_keep_alive=True
    )

def random_id_gen():
    digits = [str(random.randint(0, 9)) for _ in range(8)]
    random.shuffle(digits)
    return int(''.join(digits))

if 'user' not in st.session_state:
    st.session_state.key = f'{user_id}'

def details():
    st.title('Class of 2013 Reunion')
    st.write()
    st.write(st.session_state)
    st.write('Calling all Matrix Class of 2013 graduates from Paarl Boys High!')
    st.write("Get ready to embark on a thrilling journey down memory lane as we celebrate our monumental 10 year reunion. The anticipation is building, and the excitement is contagious! On the 5th of August 2023, our beloved school rugby field will transform into a pulsating hub of nostalgia and camaraderie.")
    st.write("Picture yourself surrounded by familiar faces, reliving those glorious moments that shaped our youth. The air will be filled with thunderous cheers, the echoes of our triumphs, and the unbreakable bonds of friendship. This is your chance to reconnect with old teammates, share stories of triumphs and challenges, and reignite the spirit that once burned so bright within us. Let's come together and create an unforgettable experience, where the spirit of the Matrix Class of 2013 shines once again.")
    st.write("Dust off your rugby jerseys, gather your memories, and prepare to be swept away by the electrifying energy that only a reunion of this magnitude can bring. The countdown has begun, and the stage is set. Brace yourselves for an extraordinary celebration, where we honor our legacy, relish our accomplishments, and create new memories that will last a lifetime. The Matrix Class of 2013 reunion is our moment to shine – let's make it legendary!")
    components.html('''<iframe width="1128" height="635" src="https://www.youtube.com/embed/1oeaRq9-yBc" title="Paarl Boys High School" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen></iframe>''', height=650, width=700)


def contact_deets():
    st.title('We require your information')
    st.write('Kindly provide us with the below information!')
    name = st.text_input('Name')
    surname = st.text_input('Surname')
    phone = st.text_input('Phone Number')
    address = st.text_input('Address')
    st.write(st.session_state)


def merch():
    st.title('Merchandise')
    st.write('Would you like to purchase some merchandise for the up and coming event?')
    sizes = ['XS','S','M','L','XL','XXL','XXL']
    prices = {
        'XS':250,
        'S':266,
        'M':270,
        'L':300,
        'XL':330,
        'XXL':350,
        'XXL':400
    }
    st.selectbox('Size',sizes)
    st.write(st.session_state)

def events():
    st.title('Up and coming events')

    st.multiselect('Please select what events you would like to attend''Big Brag',
                ['Small Brag',
                'U18A Rugby',
                'Big Brag']
                )

# Set up the directory for pages in app
pages = {
    "Infromation": details,
    "Contact details": contact_deets,
    "Merchandise": merch,
    "Events": events
    
}


# Create a menu with the page names
selection = st.sidebar.radio("Navigate to:", list(pages.keys()))

# Display the selected page with its corresponding function
pages[selection]()