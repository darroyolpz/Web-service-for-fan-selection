import json, requests

url = "http://fanselect.net:8079/FSWebService"
user_ws, pass_ws = 'XXX', 'XXX'

def fan_ws(request_string, url):	
	ws_output = requests.post(url=url, data=request_string)
	return ws_output

# Get SessionID
session_dict = {
	'cmd': 'create_session',
	'username': user_ws,
	'password': pass_ws
}

session_request = json.dumps(session_dict)
session_response = fan_ws(session_request, url)
session_id = json.loads(session_response.text)['SESSIONID']
print('Session ID:', session_id)

# Fan parameters to test
article_no = '115510/A01'
qv = 2500
psf = 200

# Fan request
fan_dict = {
	'username': user_ws,
	'password': pass_ws,
	'language': 'EN',
	'unit_system': 'm',
	'cmd': 'select',
	'article_no': article_no,
	'cmd_param': '0',
	'spec_products': 'PF_00',
	'product_range': 'BR_01',
	'qv': qv,
	'psf': psf,
	'current_phase': '3',
	'voltage': '400',
	'nominal_frequency': '50',
	'sessionid': session_id,
	'full_octave_band': 'true'
}

fan_request = json.dumps(fan_dict)
fan_response = fan_ws(fan_request, url)
value = json.loads(fan_response.text)['POWER_INPUT_KW']
print('Power input kW:', value)