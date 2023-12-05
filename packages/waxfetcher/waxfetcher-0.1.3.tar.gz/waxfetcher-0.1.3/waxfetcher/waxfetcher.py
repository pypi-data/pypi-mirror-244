import time
import json
import requests

print('init fetcher')
ENTRYPOINT_TRANSFERS = f"http://wax.blacklusion.io/atomicassets/v1/transfers"
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'}



# Set the number of rows displayed
#pd.options.display.max_rows = 1000



def fetch_container(
	address = '',
	schema = '',
	template = '',
	coll_name = 'pixeltycoons'
	):
    
    max_tries = 3
    limit = 1000
    resultcount = limit
    data = []
    page = 1
    urls = ["http://wax.eosusa.io/atomicassets/v1/assets", "https://api.wax-aa.bountyblok.io/atomicassets/v1/assets", "http://wax.blokcrafters.io/atomicassets/v1/assets", "http://wax.blacklusion.io/atomicassets/v1/assets"]
    n = 1
    while resultcount == limit:
        print(n)
        n+=1
        url = urls[0]#[random.randint(0,3)]
        params = {#"collection_name": coll_name, 
        "limit": limit, "order": "asc", "page": page, "burned": "false"}
        if address:
        	params['owner'] = address
        if schema:
        	params['schema_name'] = schema
        if template:
        	params['template_id'] = template
        if coll_name:
        	params["collection_name"] = coll_name
        results = requests.get(url, params, headers=headers)
        tries = 0
        sleep_sec = 3
        #print(results.status_code)
        while (results.status_code != 200) and (tries < max_tries):
            #print(results.status_code)
            tries += 1
            time.sleep(sleep_sec)
            url = urls[0]
            results = requests.get(url, params, headers=headers)
        
        assets = json.loads(results.content)
        data += assets["data"]
        resultcount = len(assets['data'])
        page += 1
    
    return data

def save_and_supply(data, address=""):
	print('saving data')
	if not address:
		address = "global"
	with open(f"{address}.json", "w") as f:
		f.write(json.dumps(data, indent=4))
		print("Job's done")
			
	with open(f"{address}.json", "r") as f:
		data = json.load(f)
		dict = {}
		for asset in data:
			name = asset["data"]["name"]
			schema = asset["schema"]["schema_name"]
			template_id = asset["template"]["template_id"]
			if name not in dict.keys():
				dict[name] = {"template": template_id, "schema": schema, "count": 1}
			else:
				dict[name]["count"] += 1
		with open(f"{address}_supply.json", "w") as f:
			f.write(json.dumps(dict, indent=4))

def read_blockchain_and_save(
	address = '',
	schema = '',
	template = ''
	):
	
	data = fetch_container(address, schema, template)
	save_and_supply(data, address)
	print(f'{address} fetched and saved')
	


def get_transfers_deposit(sender, recipient, limit, memo='', txn=''):
    payload = {
    	"sender": sender,
        "recipient": recipient,
        "limit": limit,
    }
    if memo:
    	payload['memo'] = memo
    if txn:
        payload['txid'] = txn
        
    response = requests.get(ENTRYPOINT_TRANSFERS, params=payload, headers=headers)
    print(response.headers["x-ratelimit-remaining"])
    return response.json()

# address, schema, template
#read_blockchain_and_save()


def parse_collections(data):
	dict = {}
	for asset in data:
		#name = asset["data"]["name"]
		#schema = asset["schema"]["schema_name"]
		#template_id = asset["template"]["template_id"]
		collection = asset["collection"]["collection_name"]
		if collection not in dict.keys():
			dict[collection] = 1
		else:
			dict[collection] += 1
	return dict


collections = 'pixeltycoons,funmangalaxy,smellykoalas,aquascapeart, waxitalianft,pixtalgiawax,nethrimdsign'

'''
collections = [
	'pixeltycoons',
	'funmangalaxy',
	'smellykoalas',
	'aquascapeart', 
	'waxitalianft',
	'pixtalgiawax'
]
'''

def get_template_name_and_count(data):
	output = {}
	for i in data:
		if i["name"] not in output.keys():
			output[i["name"]] = 1
		else:
			output[i["name"]] = 1
			
	return output
		
#data = fetch_container(address='pixeltycoons', coll_name='pixeltycoons')
#print(data)
#print(get_template_name_and_count(data))
