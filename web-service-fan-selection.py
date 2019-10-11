import json, requests

url = "http://fanselect.net:8079/FSWebService"
user_ws, pass_ws = 'XXX', 'XXX'

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
article_no = '115510/A01'
qv, psf= 2500, 200

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

value = get_response(fan_dict)['POWER_INPUT_KW']
print('Power input kW:', value)