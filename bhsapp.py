#################### IMPORTS ####################
import streamlit as st
from streamlit_extras.switch_page_button import switch_page
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
    sizes = ['None','XS','S','M','L','XL','XXL','XXL','XXXL','XXXXL']
    size_select = st.selectbox('Old School Rugby Jersey',sizes)
    soft_shell = st.selectbox('Soft Shell',sizes)
    puffer_jack = st.selectbox('Puffer Jacket',sizes)
    if st.button('Submit'):
        st.session_state.size_select, st.session_state.soft_shell, st.session_state.puffer = size_select, soft_shell, puffer_jack
        run_query(f"INSERT INTO BHSAPP.APPDATA.MERCHANDISE (USER_ID, JERSEY,SHELL,PUFFER,TMSTMP) VALUES ({st.session_state.user},'{st.session_state.size_select}','{st.session_state.soft_shell}','{st.session_state.puffer}','{datetime.now()}')")
        st.write('Successfully captured your data!')

def choices():
    st.title('Additional Requirements')
    st.write('Please provide us with the following choices')
    choices = ['No','Yes']
    inter_tickets = ['Walk-in','Old Boys Stand']
    obj = {
        'member': None,
        'ticket': None,
        'amount': None,
        'reunion': None
    }
    tick_amount = [1,2,3,4,5,6,7,8,9]
    if 'event' not in st.session_state:
        st.write('No need for any additional questions, thank you!')
    else:
        for i in st.session_state.event:
            if 'Friday Big Brag (Stadsaal)' in i:
                member = st.selectbox('Are you a paid up OBU Member?',choices)
                obj['member'] = member
            if 'Interschools Rugby' in i:
                ticket_type = st.selectbox('Interschools Rugby ticket type', inter_tickets)
                ticket_amount = st.selectbox('How many tickets do you require?',tick_amount)
                obj['ticket'] = ticket_type
                obj['amount'] = ticket_amount
            if '10 Year Reunion Dinner' in i:
                reunion = st.selectbox('Is your partner attending the reunion dinner?', choices)
                obj['reunion'] = reunion
        

    if st.button('Submit'):
        if obj['member'] is not None:
            st.session_state.member = member
            run_query(f"INSERT INTO BHSAPP.APPDATA.EVENTS_INFO (USER_ID,EVENT, DESC, TMSTP, TICKET_AMOUNT) VALUES ({st.session_state.user},'Friday Big Brag (Stadsaal)','{st.session_state.member}','{datetime.now()}', NULL)")
        if obj['ticket'] is not None:
            st.session_state.ticket_type = ticket_type
            st.session_state.ticket_amount = ticket_amount
            run_query(f"INSERT INTO BHSAPP.APPDATA.EVENTS_INFO (USER_ID,EVENT, DESC, TMSTP, TICKET_AMOUNT) VALUES ({st.session_state.user},'Interschools Rugby','{st.session_state.ticket_type}','{datetime.now()}', {st.session_state.ticket_amount})")
        if obj['reunion'] is not None:
            st.session_state.reunion = reunion
            run_query(f"INSERT INTO BHSAPP.APPDATA.EVENTS_INFO (USER_ID,EVENT, DESC, TMSTP, TICKET_AMOUNT) VALUES ({st.session_state.user},'10 Year Reunion Dinner','{st.session_state.reunion}','{datetime.now()}',NULL)")
        st.write('Successfully captured your data!')
        
        # run_query(f"INSERT INTO BHSAPP.APPDATA.EVENTS (USER_ID, EVENT_, ADDITION, TMSTP) VALUES ({st.session_state.user},'Friday Big Brag (Stadsaal)','{member}','{datetime.now()}')")


def events():
    st.title('Up and coming events')
    events = st.multiselect('What events would you like to attend?', ['Friday Big Brag (Stadsaal)','Interschools Rugby','10 Year Reunion Dinner'])
    if st.button('Submit'):
        st.session_state.event = events
        for event in st.session_state.event:
            run_query(f"INSERT INTO BHSAPP.APPDATA.EVENTS (USER_ID, EVENT, TMSTP) VALUES ({st.session_state.user},'{event}','{datetime.now()}')")

        st.write('Successfully captured your data!')

def checkout():
    st.title('Payment information')
    check_user = run_query(f'SELECT USER_ID FROM BHSAPP.APPDATA.USER_DETAILS WHERE USER_ID = {st.session_state.user}')
    if check_user[0][0] == None or check_user[0][0] == 'NULL' or check_user[0][0] == 'null':
        st.write('Woops something went wrong - please refresh the page and try again!')
    else:
        st.write('Please find the summary for your selections below:')
        order = run_query(f"SELECT ITEM, PRICE FROM BHSAPP.APPDATA.TOTAL WHERE USER_ID = '{st.session_state.user}'",2)
        st.dataframe(order)
        total = run_query(f"SELECT SUM(PRICE) FROM BHSAPP.APPDATA.TOTAL WHERE USER_ID = '{st.session_state.user}'")
        st.subheader(f"Your total is: R{total[0][0]}")
    
        st.write('Please see the below account details for payment, NB - use your name as the reference for the payment to help Warne out!')
        st.write('Account Name: HJS OUDSTUDENTE UNIE')
        st.write('Bank: ABSA, PAARL')
        st.write('Account Number: 9350129123')
        st.write('Ref: (Name and Surname)')

    

# Set up the directory for pages in app
pages = {
    "Information": details,
    "Contact details": contact_deets,
    "Merchandise": merch,
    "Events": events,
    "Additional": choices,
    "Checkout": checkout
}


# Create a menu with the page names
selection = st.sidebar.radio("Navigate to:", list(pages.keys()))

# Display the selected page with its corresponding function
pages[selection]()