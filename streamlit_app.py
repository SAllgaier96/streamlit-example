"""
# Player Analysis Dashboard
This is a test to see if streamlit can link with google sheets data
"""

import streamlit as st
from google.oauth2 import service_account
from gsheetsdb import connect

# Create a connection object.
credentials = service_account.Credentials.from_service_account_info(
    st.secrets["gcp_service_account"],
    scopes=[
        "https://www.googleapis.com/auth/spreadsheets",
    ],
)
conn = connect(credentials=credentials)

# Perform SQL query on the Google Sheet.
# Uses st.cache to only rerun when the query changes or after 10 min.
@st.cache(ttle=600)
def run_query(query)
    rows = conn.execute(query, headers=1)
    rows = rows.fetchall()
    return rows

sheet_url = st.secrets["PlayerOllie_gsheets_url"]
rows = run_query(f'SELECT * FROM "{sheet_url}"')

# Print results.
st.write(f'PlayerOllie tab successfully loaded, contains {sum(rows.GameID)} rows')
st.write(f'URL: {st.secrets["private_gsheets_url"]}')

# for row in rows:
#     st.write(f"{row.name} has a :{row.pet}:")
    
############################## BELOW IS ANOTHER QUERY FROM BEFORE THAT HASN'T BEEN TESTED YET #######################################
# try
#     st.write(f'Starting Data Pull...')
#     WORKSHEET_ID = '1-kUlYLeDEQyzw2PYnLn6quq7kFYJbduI_Zrk_bQ7_9A'
#     scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
#     path = 'assets/creds.json'
#     google_key_file = path
#     credentials = ServiceAccountCredentials.from_json_keyfile_name(google_key_file, scope)
#     gc = gspread.authorize(credentials)
    
#     # Opening the workbook
#     workbook = gc.open_by_key(WORKSHEET_ID)

#     # Opening separate worksheets
#     PullingData = workbook.worksheet('PullingData')
#     PlayerOllie = workbook.worksheet('PlayerOllie')
#     TeamOllie = workbook.worksheet('TeamOllie')
#     RosterOverview = workbook.worksheet('RosterOverview')
    
#     print('Data Pull SUCCESS')
# except Exception as e:
#     print('Data Pull FAILED')
    
########################### BELOW IS STREAMLIT SAMPLE OUTPUT NOT CONNECTING TO ANYTHING #############################################

# with st.echo(code_location='below'):
#     total_points = st.slider("Number of points in spiral", 1, 5000, 2000)
#     num_turns = st.slider("Number of turns in spiral", 1, 100, 9)

#     Point = namedtuple('Point', 'x y')
#     data = []

#     points_per_turn = total_points / num_turns

#     for curr_point_num in range(total_points):
#         curr_turn, i = divmod(curr_point_num, points_per_turn)
#         angle = (curr_turn + 1) * 2 * math.pi * i / points_per_turn
#         radius = curr_point_num / total_points
#         x = radius * math.cos(angle)
#         y = radius * math.sin(angle)
#         data.append(Point(x, y))

#     st.altair_chart(alt.Chart(pd.DataFrame(data), height=500, width=500)
#         .mark_circle(color='#0068c9', opacity=0.5)
#         .encode(x='x:Q', y='y:Q'))
