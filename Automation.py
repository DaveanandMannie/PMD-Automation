import os
import csv
import json
import requests
from typing import Union
import Templates

# TODO revoke and reinstate API key while utilizing windows environ
with open('Variables.txt') as f:
	for line in f:
		key, value = line.strip().split('=')
		os.environ[key] = value
# Global variables
PRINTIFY_API_KEY = os.environ.get('API_KEY')
PRINT_GEEK_ID = 27
ENDPOINT_URL = 'https://api.printify.com/v1/'
HEADERS = {
	'Authorization': f'Bearer {PRINTIFY_API_KEY}',
	'Content-Type': 'application/json;charset=utf-8'
}
ETSY_SHOP_ID = 15047741
TEMPLATES_DICT: dict[str, type:Templates.Template] = {
	'test': Templates.Test
}


def PrintGeek_blueprints_csv() -> None:
	""" Creates a csv of all blueprints provided by Print Geek in project directory """
	api_response = requests.get(ENDPOINT_URL + f'catalog/print_providers/{PRINT_GEEK_ID}.json/', headers=HEADERS)
	api_response.raise_for_status()
	data = api_response.json()
	blueprints_data = [(blueprint['id'], blueprint['title']) for blueprint in data['blueprints']]
	csv_file_path = 'Blueprints.csv'
	with open(csv_file_path, 'w', newline='') as csvfile:
		fieldnames = ['ID', 'Title']
		writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
		writer.writeheader()
		for blueprint_id, title in blueprints_data:
			writer.writerow({'ID': blueprint_id, 'Title': title})
	print('Blueprint CSV created in working directory')
	return


def get_all_shops() -> dict:
	""" Returns a dictionary of shops and their ids on Printify """
	shop_response = requests.get(ENDPOINT_URL + 'shops.json', headers=HEADERS)
	shop_response.raise_for_status()
	shop_response_data = shop_response.json()
	shops = {}
	for shop in shop_response_data:
		shop_name = shop['title']
		shop_id_number = shop['id']
		shops[shop_name] = shop_id_number
	return shops


def get_first_product_id(shop_id: int) -> int:
	""" Returns the first product id in the shop """
	product_list_response = requests.get(ENDPOINT_URL + f'shops/{shop_id}/products.json', headers=HEADERS)
	product_list_response.raise_for_status()
	product_list_data = product_list_response.json()
	product_id = product_list_data['data'][0]['id']
	return product_id


def get_product_variants(product_id: int, shop_id: int) -> list:
	""" Returns a list of all variants enabled on an existing product """
	product_response = requests.get(ENDPOINT_URL + f'shops/{shop_id}/products/{product_id}.json', headers=HEADERS)
	product_data = product_response.json()
	all_available_variants = product_data['variants']
	enabled_variants = [variant['id'] for variant in all_available_variants if variant.get('is_enabled')]
	return enabled_variants


def push_to_api(
		image_url: str,
		image_name: str,
		product_title: str,
		product_description: str,
		products_tags: list,
		product_variant_list: list,
		price: int,
		shop_id: int,
		blueprint_id: int) -> str:
	""" Takes all required Printify fields and sends a POST request through the API """
	# pushes the image to the api -> consider making a separate function
	image_data = {'file_name': image_name + '.png', 'url': image_url}
	image_post = requests.post(ENDPOINT_URL + 'uploads/images.json', headers=HEADERS, json=image_data)
	image_post.raise_for_status()
	image_response = image_post.json()
	image_id = image_response["id"]
	if image_post.status_code != 200:
		print(json.dumps(image_response, indent=4))
		return 'Image upload failure'

	product_variants = product_variant_list
	list_of_variants_dict = [
		{
			'id': variant_values,
			'price': price,
			'is_enabled': True
		} for variant_values in product_variants
	]
	# product properties
	product_data = {
		'title': product_title,
		'description': product_description,
		'blueprint_id': blueprint_id,
		'print_provider_id': PRINT_GEEK_ID,
		'variants': list_of_variants_dict,
		'tags': products_tags,
		'print_areas': [
			{
				'variant_ids': product_variants,
				'placeholders': [
					{
						'position': 'front',
						'images': [
							{
								'id': image_id,
								'x': 0.5,
								'y': 0.5,
								'scale': 1,
								'angle': 0
							}
						]
					}
				]
			}
		]
	}
	create_product = requests.post(
		ENDPOINT_URL + f'shops/{shop_id}/products.json',
		headers=HEADERS,
		json=product_data
	)
	create_product.raise_for_status()
	created_product_data = create_product.json()

	if create_product.status_code == 200:
		created_product_id = created_product_data['id']
		print('Product created!')
		return created_product_id


def publish_product(product_id: str, publish_json: dict[str: bool]) -> requests.Response:
	""" Publishes a product through the connected sales channel """
	publish_response = requests.post(
		ENDPOINT_URL + f'shops/{ETSY_SHOP_ID}/products/{product_id}/publish.json',
		json=publish_json,
		headers=HEADERS
	)
	return publish_response


def create_product_from_csv(template: str, publish: bool, file_name: str) -> None:
	""" Calls the production creation function with data from templates/profiles and MyDesign export """
	chosen_template: Union[Templates.Template, None] = None
	if template in TEMPLATES_DICT:
		chosen_template: Templates.Template = TEMPLATES_DICT[template]
	template_price: int = chosen_template.price
	template_variants: list[int] = chosen_template.variants
	template_blueprint: int = chosen_template.blueprint
	template_publish_data: dict[str: bool] = chosen_template.publish_data
	with open(file_name, 'r') as file:
		reader = csv.DictReader(file)
		for row in reader:
			# change based on the MyDesign template
			# noinspection PyTypeChecker
			image_name: str = row['Print File_slot_file_name']
			# noinspection PyTypeChecker
			image_url: str = row['Print File_slot_image_url']
			# noinspection PyTypeChecker
			title: str = row['Listing.Title']
			# noinspection PyTypeChecker
			description: str = row['Listing.Description']
			# noinspection PyTypeChecker
			tags: list[str] = [tag for tag in row['Tags.All Tags'].strip().split(',')]
			new_product_id = push_to_api(
				image_url=image_url,
				image_name=image_name,
				product_title=title,
				product_description=description,
				products_tags=tags,
				shop_id=ETSY_SHOP_ID,
				price=template_price,
				product_variant_list=template_variants,
				blueprint_id=template_blueprint
			)
			if publish:
				publish_product(product_id=new_product_id, publish_json=template_publish_data)
	print(f'Product creation complete.')
	return
