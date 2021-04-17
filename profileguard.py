import requests
import sys
import re
import json
import getpass
url = 'https://m.facebook.com/login.php'
urlgraph = 'https://www.facebook.com/api/graphql'
target = {}
data = {}
data['email'] = input("Username:")
data['pass'] = getpass.getpass("Password:")
target['url'] = input("Target URL:")
facebookurl = 'https://www.facebook.com/'+target['url']
graphql = {}
s = requests.Session()
r = s.post(url,data=data)
r.raise_for_status()
html = s.get(facebookurl).text
target['profile_guard'] = input("Enable/Disable:")
target['account_id'] = r'"ACCOUNT_ID":"([0-9]+)"'
target['token_id'] = r'"token":"([0-9A-Za-z:-_]+)"'
if re.findall(target['account_id'],html) is not None:
	target['account_id'] = (re.findall(target['account_id'],html))
	account_id = target['account_id'][0]
else:
	print("404")
if re.findall(target['token_id'],html) is not None:
	target['token_id'] = (re.findall(target['token_id'],html))
	token_id = target['token_id'][0]
else:
	print("404")
if token_id is not None:
	variables = {}
	variables["0"] = {}
	if target['profile_guard'] == "yes":
		variables["0"]["is_shielded"] = "1"
	elif target['profile_guard'] == "no":
		variables["0"]["is_shielded"] = "0"
	else:
		variables["0"]["is_shielded"] = "1"
	variables["0"]["session_id"] = "1"
	variables["0"]["actor_id"] = account_id
	variables["0"]["client_mutation_id"] = "1"
	graphql['fb_dtsg'] = token_id
	graphql['__user'] = account_id
	graphql['__a'] = '1'
	#graphql['variables'] = '{"0":{"is_shielded":true,"session_id":"1","actor_id":"100039975033023","client_mutation_id":"1"}}'
	graphql['variables'] = json.dumps(variables)
	graphql['doc_id'] = '1477043292367183'
	req = s.post(urlgraph,data=graphql)
	req = json.loads(req.text)
	if req['data']['is_shielded_set']['is_shielded'] == True:
		print("Profile Guard Activated!")
	else:
		print("Profile Guard Deactivated")
else:
	print("404")