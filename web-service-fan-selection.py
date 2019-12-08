import json, requests
import pandas as pd

url = "http://fanselect.net:8079/FSWebService"
user_ws, pass_ws = 'xxx', 'xxx'

def fan_ws(request_string, url):	
	ws_output = requests.post(url=url, data=request_string)
	return ws_output

def get_response(dict_request):
	dict_json = json.dumps(dict_request)
	url_response = fan_ws(dict_json, url)
	url_result = json.loads(url_response.text)
	return url_result

def sort_function(lst, n):
	lst.sort(key = lambda x: x[n])
	return lst 

# Get SessionID
session_dict = {
	'cmd': 'create_session',
	'username': user_ws,
	'password': pass_ws
}

session_id = get_response(session_dict)['SESSIONID']
print('Session ID:', session_id)
print('\n')

# Pandas import
# Open the quotation file
excel_file = 'EC_FANS.xlsx'
df = pd.read_excel(excel_file, dtype={'Item': str, 'Gross price': float})

print(df.head())
print('\n')

inner_list, outter_list = [], []

# Fan parameters to test
qv, psf= 28218, 752
height, width = 1614, 2784
article_no = '115683/A01'

# Loop for the code
for i in range(len(df['Item'])):
	for n in range(1, 7):

		# Set values
		article_no = df['Item'].iloc[i]
		gross_price = df['Gross price'].iloc[i]

		# Fan request
		fan_dict = {
			'language': 'EN',
			'unit_system': 'm',
			'username': user_ws,
			'password': pass_ws,
			'cmd': 'select',
			'cmd_param': '0',
			'zawall_mode': 'ZAWALL_PLUS',
			'zawall_size': n,
			'qv': qv,
			'psf': psf,
			'spec_products': 'PF_00',
			'article_no': article_no,
			'current_phase': '3',
			'voltage': '230',
			'nominal_frequency': '60',
			'installation_height_mm': height,
			'installation_width_mm': width,
			'installation_length_mm': '2000',
			'installation_mode': 'RLT_2017',
			'sessionid': session_id
		}

		try:
			no_fans = get_response(fan_dict)['ZAWALL_SIZE']

			print('Fan found:', article_no)
			print('Number of fans:', no_fans)
			print('\n')

			total_gross = no_fans*gross_price

			inner_list.append([article_no, no_fans, total_gross])

			#power_input = get_response(fan_dict)['ZA_PSYS']
			#print('Power input W:', power_input)
			
		except:
			pass

print(sort_function(inner_list, 2))