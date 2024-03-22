import requests
import os
import json
import csv

with open('Variables.txt') as f:
	for line in f:
		key, value = line.strip().split('=')
		os.environ[key] = value
# Global variables
API_KEY = os.environ.get('API_KEY')
ENDPOINT_URL = 'https://api.printify.com/v1/'
HEADERS = {
	'Authorization': f'Bearer {API_KEY}',
	'Content-Type': 'application/json;charset=utf-8'
}
PRINT_GEEK_ID = 27

# getting shop id
shop_id_response = requests.get(ENDPOINT_URL + 'shops.json', headers=HEADERS)
shop_id_response.raise_for_status()
shop_data = shop_id_response.json()
shop_id = shop_data[0]['id']

# getting product id
product_list_response = requests.get(ENDPOINT_URL + f'shops/{shop_id}/products.json', headers=HEADERS)
product_list_response.raise_for_status()
product_list_data = product_list_response.json()
product_id = product_list_data['data'][0]['id']

# first product  blueprint id
product_response = requests.get(ENDPOINT_URL + f'shops/{shop_id}/products/{product_id}.json', headers=HEADERS)
product_data = product_response.json()
print(product_data['blueprint_id'])


# uploading an image
image_data = {
	"file_name": "test_image.png",
	"url": "https://cdn.mydesigns.io/design/file/408dfbb6-77d1-42c6-9bdd-54d8a5a6e056.jpeg?Expires=1713647585&Signature=gD~vXx6MO2Awym90FKb1GwULKXWIJZcovS66WlyiCFlzJhnCAha74XhdjqMezQ27AHNcwAblRa2LhqRmh7n4kmx8dTwpAKZlMcCfe-IqNuEXAcUl5qWm~r4QJVQvxRhWStkO6Ato8mwNi7G6ShdwL-o-cIibTshXTWv7hvQgzVpbQNc4Dp56pfiO7j5t38RV4OoH~urW8m-uYZkDvH6E5EXJbxEWCZZRtVpWXv-h90FlshmSBHBo5xZM09oYaETv1VADYH8MA~Gx94aLX2VUBU2FtB1hUk92lcRqp5xgkcHEWK8--lxm1nI2qoXU7uBVwju~eiaID7d35WI~u-z4ew__&Key-Pair-Id=K3GS08609RBYMI"
}
image_post = requests.post(ENDPOINT_URL + 'uploads/images.json', headers=HEADERS, json=image_data)
response = image_post.json()
image_id = response["id"]
print(json.dumps(response, indent=4))

# Creating a product
product_data = {
	"title": "Product",
	"description": "Good Product",
	"blueprint_id": 6,
	"print_provider_id": PRINT_GEEK_ID,
	"variants": [
		{
			"id": 12053,
			"price": 4000,
			"is_enabled": True
		}
	],
	"print_areas": [
		{
			"variant_ids": [45740],
			"placeholders": [
				{
					"position": "front",
					"images": [
						{
							"id": image_id,
							"x": 0.5,
							"y": 0.5,
							"scale": 1,
							"angle": 0
						}
					]
				}
			]
		}
	]
}
create_product_test = requests.post(ENDPOINT_URL + f'shops/{shop_id}/products.json', headers=HEADERS, json=product_data)

response_json = create_product_test.json()
response_status = create_product_test.status_code


# one time function to create csv file of the blueprints
# api_response = requests.get(ENDPOINT_URL + f'catalog/print_providers/{PRINT_GEEK_ID}.json/', headers=HEADERS)
# data = api_response.json()
# blueprints_data = [(blueprint['id'], blueprint['title']) for blueprint in data['blueprints']]
# csv_file_path = 'Blueprints.csv'
# with open(csv_file_path, 'w', newline='') as csvfile:
# 	fieldnames = ['ID', 'Title']
# 	writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
# 	writer.writeheader()
# 	for blueprint_id, title in blueprints_data:
# 		writer.writerow({'ID': blueprint_id, 'Title': title})
# print('CSV file is finished ')
