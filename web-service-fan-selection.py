import json, requests

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

# Get SessionID
session_dict = {
	'cmd': 'create_session',
	'username': user_ws,
	'password': pass_ws
}

session_id = get_response(session_dict)['SESSIONID']
print('Session ID:', session_id)

# Fan parameters to test
article_no = '115683/A01'
qv, psf= 28218, 752
voltage, nominal_frequency = 230, 60

# article_no = '115510/A01'
# qv, psf= 2500, 200
# voltage, nominal_frequency = 400, 50

height, width = 1614, 2784

# Fan request
fan_dict = {
	'language': 'EN',
	'unit_system': 'm',
	'username': user_ws,
	'password': pass_ws,
	'cmd': 'select',
	'cmd_param': '0',
	'zawall_mode': 'ZAWALL_PLUS',
	'zawall_size': '4',
	'qv': qv,
	'psf': psf,
	'spec_products': 'PF_00',
	'article_no': article_no,
	'current_phase': '3',
	'voltage': voltage,
	'nominal_frequency': nominal_frequency,
	'installation_height_mm': height,
	'installation_width_mm': width,
	'installation_length_mm': '2000',
	'installation_mode': 'RLT_2017',
	'sessionid': session_id
}

try:
	zawall_size = get_response(fan_dict)['ZAWALL_SIZE']
	power_input = get_response(fan_dict)['ZA_PSYS']

	print('Number of fans:', zawall_size)
	print('Power input W:', power_input)
	
except:
	print('No fan was found this time.')