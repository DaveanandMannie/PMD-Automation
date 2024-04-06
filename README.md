# PMD Automation
A quick project that takes Print on demand listing data from a CSV, creates and publishes it to your Printify store. 
It also has an Etsy tagger that adds tags to your listing based on the same CSV. 


The automation script simply uses Printify's public API and the etsy tagger uses selenium to enter listing data.

This project spawned as a proof of concept at my current place of employment. I wanted to create something that automates the tedium of scale.

## Requirements 
Aside from the Python packages in requirements.txt
* Printify API key with the following scopes;
  * shops.read
  * catalog.read
  * products.read
  * products.write
  * uploads.read
  * uploads.write
  * print_providers.read
* CSV containing;
  * all required list information
  * the image URL for each product
 ## Optional Requirements
* integrated sales channel via Printify
## Guide 
* If using the pre-release all that is need is the Etsy login and the Printify API key

Once the repository is cloned and the requirements are installed a few things need to be changed for the script to work.
* In ```secrets.txt``` add your Printify API key after the ```=``` with no spaces
* The ```get_all_shops()```  returns a dict of shop titles and their IDS. 
* Add shop ID in ```secrets.txt``` after the ```=``` with no spaces
  * eg: ```SHOP_ID=1234567```
* The ```get_all_print_providers()``` returns a dict with all print provider's id 
  * eg: ```{'PrintGeek' : 27}```
  * Add to ```secrets.txt``` after the ```=``` with no spaces 
* In your Printify shop you can create a shirt with your desired colours, print provider, and shirt make.
  * In ```Templates.py``` I have product data that is specific if the provider is PrintGeek it may not work with 
  provider
  * If your created template is your only product call ```get_product_info(productid=get_first_product_id(SHOP_ID), SHOP_ID)```
  * This returns a dictionary with the necessary data to create a template instance in ```Templates.py```
* Create a template object with your specified data 
* In ```Automation.py``` add a key value pair to ```TEMPLATES_DICT``` they key being your title and value being the import of your template
  * eg: ```{'Gildan 5000': Templates.Popular_Gildan_5000,}```
* Make sure that ```secrets.txt``` is in the same directory as the scripts
* In the working directory terminal call ```python GUI.py```
  * Select the CSV with your listing Data, select a template, assign relevant headers and start your automation 👍
## Optional
  * Add your Etsy details to ```secrets.txt```
  * Start the tagger via the UI assuming the CSV headers are assigned, wait for Etsy`s 2FA 
  * Enter the code and continue 
  * Watch the robots take over 🤖🤖🤖
## The future
This will probably not be an ongoing development unless my employers move forward👷‍♂️👷‍♀️

I may tinker around with pyinstaller and its associated spec file system for portability✈✈✈✈ 

Maybe a less early 2000's UI but I have plans for other languages in this field 🤷‍♀️