import json, requests, time
import pandas as pd
from pandas import ExcelWriter

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

# Open the quotation file
excel_file = 'DATA_INPUT.xlsx'
df_data = pd.read_excel(excel_file, dtype={'Line':int, 'AHU':object, 'Height':object, 'Width':object, 'Ref':object,
	'Voltage':object, 'Airflow':object, 'Static Press.':object})

print(df_data.head())
print('\n')

inner_list, outter_list = [], []

# Check execution time
start_time = time.time()

for j in range(len(df_data['Line'])):
	line = df_data['Line'].iloc[j]
	ahu = df_data['AHU'].iloc[j]
	ref = df_data['Ref'].iloc[j]
	height = df_data['Height'].iloc[j]
	width = df_data['Width'].iloc[j]
	qv = df_data['Airflow'].iloc[j]
	psf = df_data['Static Press.'].iloc[j]

	time.sleep(2)

	# Loop for fans on each number of line
	for i in range(len(df['Item'])):
		# Check several fan configuration
		for n in range(1, 10):

			# Set values
			article_no = df['Item'].iloc[i]
			gross_price = df['Gross price'].iloc[i]
			print(line)

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

			print(fan_dict)
			print('\n')

			try:
				no_fans = get_response(fan_dict)['ZAWALL_SIZE']

				print('Number of line:', line)
				print('Fan found:', article_no)
				print('Number of fans:', no_fans)
				print('\n')

				total_gross = no_fans*gross_price

				inner_list.append([line, ahu, ref, qv, psf, article_no, no_fans, total_gross])

				# Stop the loop
				print('Loop stopping!')
				break

				#power_input = get_response(fan_dict)['ZA_PSYS']
				#print('Power input W:', power_input)
				
			except:
				pass

	print("--- %s seconds ---" % (time.time() - start_time))
	print('\n')
	print(sort_function(inner_list, 7))

	# Once checked all the items and gathered the entire list, get the cheapest one
	outter_list.append(inner_list[0])
	inner_list = []

# Save all the results to a new dataframe
col = ['Line', 'AHU', 'Ref', 'Airflow', 'Static Press.', 'article_no', 'no_fans', 'total_gross']
result = pd.DataFrame(outter_list, columns = col)

# Export to Excel
name = 'Results.xlsx'
writer = pd.ExcelWriter(name)
result.to_excel(writer, index = False)
writer.save()