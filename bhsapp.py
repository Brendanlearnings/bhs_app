#################### IMPORTS ####################
import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
from datetime import date
import snowflake.connector
import random
from datetime import datetime
import base64
#################################################

def init_connection():
    return snowflake.connector.connect(
        **st.secrets["snowflake"], client_session_keep_alive=True
    )

# def display_pdf(file):
#     with open(file,'rb') as file:
#         pdf = base64.b64encode(file.read()).decode('utf-8')
#     return pdf


def run_query(query,expectResult=1):
    conn = init_connection()
    with conn.cursor() as cur:
        cur.execute(query)
        
        if expectResult == 2:
            # Get the column headers
            headers = [desc[0] for desc in cur.description]
            results = cur.fetchall()
            df = pd.DataFrame(results, columns=headers)
            return df
        
        if expectResult != 0:
            return cur.fetchall()
        cur.close()

def random_id_gen():
    digits = [str(random.randint(0, 9)) for _ in range(8)]
    random.shuffle(digits)
    return int(''.join(digits))

if 'user' not in st.session_state:
    st.session_state.user = random_id_gen()
    now = datetime.now()
    st.session_state.timestamp = now.strftime('%Y-%m-%d %H:%M:%S.%f %z')


def ref_num_gen():
    digits = [str(random.randint(0, 9)) for _ in range(5)]
    random.shuffle(digits)
    return int(''.join(digits))

def details():
    st.title('Class of 2013 Reunion')
    st.write()
    st.write('Dear Paarl Boys’ High Class of 2013,')
    st.write("It's hard to believe that 10 years have passed since we walked the halls of Paarl Boys’ High, but here we are! It's time to gather together and celebrate a decade of memories, accomplishments, and friendships at our long-awaited 10-year reunion.")
    st.write("We have planned various activities  to make this reunion truly special. Whether you were a sports star, a member of the debate team, a talented musician, or simply a student who enjoyed the camaraderie of our incredible class, there will be something for everyone.")
    st.write("We are eagerly looking forward to seeing you and reconnecting with our class. Let's gather once again to celebrate the friendships and experiences that shaped our lives at Paarl Boys’ High. Together, let's make this reunion one to remember.")
    # with open('HJS 10 Jaar Reunie Final.pdf','rb') as file:
    #     pdf = base64.b64encode(file.read()).decode('utf-8')
    # display_pdf = f'<iframe src="https://github.com/Brendanlearnings/bhs_app/blob/main/HJS_10_Jaar_Reunie_Final.pdf" width="700" height="1000" type="application/pdf"></iframe>'
    # st.markdown(display_pdf,unsafe_allow_html=True)
    # components.html('''<iframe width="650" height="650" src="https://www.youtube.com/embd/1oeaRq9-yBc" title="Paarl Boys High School" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen></iframe>''', height=650, width=650)


def contact_deets():
    st.title('We require your information')
    st.write('Kindly provide us with the below information!')
    name = st.text_input('Name')
    surname = st.text_input('Surname')
    phone = st.text_input('Phone Number')
    address = st.text_input('Address')

    if st.button('Submit'):
        st.session_state.name, st.session_state.surname, st.session_state.phone, st.session_state.address = name, surname, phone, address
        run_query(f"INSERT INTO BHSAPP.APPDATA.USER_DETAILS (USER_ID,NAME,SURNAME,PHONE,ADDRESS,TMSTMP) VALUES ({st.session_state.user},'{st.session_state.name}','{st.session_state.surname}','{st.session_state.phone}','{st.session_state.address}','{datetime.now()}')")
        st.write('Successfully captured your data!')

    

def merch():
    st.title('Merchandise')
    st.write('Would you like to purchase some merchandise for the up and coming event?')
    st.write('Please choose None if you dont want the specific merchandise.')
    sizes = ['None','XS','S','M','L','XL','XXL','XXL','XXXL','XXXXL']
    size_select = st.selectbox('Old School Rugby Jersey',sizes)
    soft_shell = st.selectbox('Soft Shell',sizes)
    puffer_jack = st.selectbox('Puffer Jacket',sizes)
    if st.button('Submit'):
        st.session_state.size_select, st.session_state.soft_shell, st.session_state.puffer = size_select, soft_shell, puffer_jack
        run_query(f"INSERT INTO BHSAPP.APPDATA.MERCHANDISE (USER_ID, JERSEY,SHELL,PUFFER,TMSTMP) VALUES ({st.session_state.user},'{st.session_state.size_select}','{st.session_state.soft_shell}','{st.session_state.puffer}','{datetime.now()}')")
        st.write('Successfully captured your data!')


def events():
    st.title('Up and coming events')

    choices = ['No','Yes']
    inter_tickets = ['Walk-in','Stand']
    events = st.multiselect('What events would you like to attend?', ['Friday Big Brag (Stadsaal)','Interschools Rugby','10 Year Reunion Dinner'])
    
    if st.button('Submit'):
        # st.write(st.session_state.event)
        # st.write(type(st.session_state.event))
        # st.session_state.event = events
        if 'Friday Big Brag (Stadsaal)' in events:
            member = st.selectbox('Are you a paid up OBU Member?',choices)
            
        if 'Interschools Rugby' in events:
            ticket_type = st.selectbox('Interschools Rugby ticket type', inter_tickets)
            
        if '10 Year Reunion Dinner' in events:
            reunion = st.selectbox('Is your partner attending the reunion dinner?', choices)
            

        if st.button('Done'):
            if len(st.session_state.event) != 0:
                for eve in events:
                    if eve == 'Friday Big Brag (Stadsaal)':
                        run_query(f"INSERT INTO BHSAPP.APPDATA.EVENTS (USER_ID, EVENT, ADDITION, TMSTP) VALUES ({st.session_state.user},'Friday Big Brag (Stadsaal)','{member}','{datetime.now()}')")
                    if eve == 'Interschools Rugby':
                        run_query(f"INSERT INTO BHSAPP.APPDATA.EVENTS (USER_ID, EVENT, ADDITION), TMSTP VALUES ({st.session_state.user},'Interschools Rugby','{ticket_type}','{datetime.now()}')")
                    if eve == '10 Year Reunion Dinner':
                        run_query(f"INSERT INTO BHSAPP.APPDATA.EVENTS (USER_ID, EVENT, ADDITION), TMSTP VALUES ({st.session_state.user},'10 Year Reunion Dinner','{reunion}','{datetime.now()}')")
                st.write('Successfully captured your data!')



        
            

        
    

def checkout():
    st.session_state.ref_num = f'REF{ref_num_gen()}'
    st.title('Payment information')
    st.write('Please find the total for your selections below, along with the relevant payment information')
    st.write(st.session_state)
    

# Set up the directory for pages in app
pages = {
    "Infromation": details,
    "Contact details": contact_deets,
    "Merchandise": merch,
    "Events": events,
    "Checkout": checkout
}


# Create a menu with the page names
selection = st.sidebar.radio("Navigate to:", list(pages.keys()))

# Display the selected page with its corresponding function
pages[selection]()