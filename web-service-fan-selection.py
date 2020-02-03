import json, requests, time
import pandas as pd
from pandas import ExcelWriter

url = "http://fanselect.net:8079/FSWebService"
user_ws, pass_ws = 'xxx', 'xxx'

# Get all the possible fans
all_results = True

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

print('List of fans:')
print(df.head())
print('\n')

# Open the quotation file
excel_file = 'DATA_INPUT.xlsx'
df_data = pd.read_excel(excel_file)

# AHU size for merge
excel_file = 'AHU_SIZE.xlsx'
df_size = pd.read_excel(excel_file)

# Merge operation
df_data = pd.merge(df_data, df_size, on='AHU')
cols = ['Height', 'Width', 'Airflow', 'Static Press.']

for col in cols:
	df_data[col] = df_data[col].astype(str)

print('Data input:')
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

	time.sleep(1)

	# Loop for fans on each number of line
	for i in range(len(df['Item'])):
		max_array = 4
		# Check several fan configuration
		for n in range(1, max_array):

			# Set values
			article_no = df['Item'].iloc[i]
			gross_price = df['Gross price'].iloc[i]
			print('Line:', line)

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
				#'current_phase': '3',
				#'voltage': '400',
				'nominal_frequency': '50',
				'installation_height_mm': height,
				'installation_width_mm': width,
				'installation_length_mm': '2000',
				'installation_mode': 'RLT_2017',
				'sessionid': session_id
			}

			print(fan_dict)
			print('\n')

			try:
				#no_fans = get_response(fan_dict)['ZAWALL_SIZE']
				power_input = get_response(fan_dict)['ZA_PSYS']
				zawall_arr = get_response(fan_dict)['ZAWALL_ARRANGEMENT']
				no_fans = 1 if zawall_arr == 0 else int(zawall_arr[:2])
				n_actual = get_response(fan_dict)['ERP_N_ACTUAL']
				n_stat = get_response(fan_dict)['ERP_N_STAT']
				n_target = get_response(fan_dict)['ERP_N_TRAGET']
				total_gross = no_fans*gross_price

				print('Number of line:', line)
				print('Fan found:', article_no)
				print('Power input W:', power_input)
				print('Eff. N_actual:', n_actual)
				print('Eff. N_stat:', n_stat)
				print('Eff. N_target:', n_target)
				print('Number of fans:', no_fans)
				print('Total gross:', total_gross)
				print('\n')

				inner_list.append([line, ahu, height, width, ref, qv, psf, power_input, n_stat, n_target, article_no, no_fans, total_gross])

				# Stop the loop
				print('Loop stopping!')
				print('\n')
				break
				
			except:
				pass

	print("--- %s seconds ---" % (time.time() - start_time))
	print('\n')
	print(sort_function(inner_list, len(inner_list[0])-1)) # So that gross price is always the last one

	# Once checked all the items and gathered the entire list, get the cheapest one only if all_results applies
	inner_len = len(inner_list)

	if all_results:
		for row in range(inner_len):
			outter_list.append(inner_list[row])
	else:
		outter_list.append(inner_list[0])

	inner_list = []

# Save all the results to a new dataframe
col = ['Line', 'AHU', 'Height', 'Width', 'Ref', 'Airflow', 'Static Press.', 'Consump. kW', 'N_stat', 'N_target', 'Article no', 'No fans', 'Total Gross']
result = pd.DataFrame(outter_list, columns = col)

# Export to Excel
name = 'Results.xlsx'
writer = pd.ExcelWriter(name)
result.to_excel(writer, index = False)
writer.save()