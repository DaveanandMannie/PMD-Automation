import csv
import tkinter
from tkinter import filedialog
import os
from Automation import create_product_from_csv, TEMPLATES_DICT
from EtsyTags import login_etsy, update_tags, close_driver

header_bools: list[bool] = []
header_names: list[str] = []
# TODO add check for header_bools before changing the automation button to green


def create_dropdowns() -> None:
	image_dropdown: tkinter.OptionMenu = tkinter.OptionMenu(
		root, selected_image_name, *header_names, command=image_name_select)

	url_dropdown: tkinter.OptionMenu = tkinter.OptionMenu(root, selected_url, *header_names, command=url_select)

	title_dropdown: tkinter.OptionMenu = tkinter.OptionMenu(
		root, selected_title, *header_names, command=title_select)

	description_dropdown: tkinter.OptionMenu = tkinter.OptionMenu(
		root, selected_description, *header_names, command=description_select)

	tags_dropdown: tkinter.OptionMenu = tkinter.OptionMenu(
		root, selected_tags, *header_names, command=tag_select)

	image_dropdown.grid(row=5, sticky='nsew')
	url_dropdown.grid(row=6, sticky='nsew')
	title_dropdown.grid(row=7, sticky='nsew')
	description_dropdown.grid(row=8, sticky='nsew')
	tags_dropdown.grid(row=9, sticky='nsew')

	image_label.grid(row=5, column=1, sticky='nsew')
	url_label.grid(row=6, column=1, sticky='nsew')
	title_label.grid(row=7, column=1, sticky='nsew')
	description_label.grid(row=8, column=1, sticky='nsew')
	tags_label.grid(row=9, column=1, sticky='nsew')
	return


def get_csv_headers(file_path: str) -> list:
	global header_names
	with open(file_path, 'r') as file:
		reader: csv.DictReader = csv.DictReader(file)
		# noinspection PyTypeChecker
		header_names = reader.fieldnames
		# noinspection PyTypeChecker
		return header_names


def select_csv() -> str:
	file_path = filedialog.askopenfilename(title="select directory")
	file_name = os.path.basename(file_path)
	selected_file_label.config(text=f'Chosen file: {file_name}')
	selected_file.set(file_path)
	get_csv_headers(file_path)
	create_dropdowns()
	if selected_file.get() and selected_template.get() != 'Click to select Template':
		final_automation_button.config(bg='#90EE90')
	return file_name


def checkbox_bool() -> bool:
	if publish_int.get() == 1:
		publish_label.config(text='Publishing to Etsy')
		publish_bool.set(True)
		return True
	else:
		publish_label.config(text='Staying in Printify')
		publish_bool.set(False)
		return False


def template_select(value: str) -> str:
	if value in templates:
		selected_template.set(value)
		dropdown_label.config(text=f'Template: {value}')
	if selected_file.get() and selected_template.get():
		final_automation_button.config(bg='#90EE90')
	return selected_template.get()


def image_name_select(value) -> None:
	if value:
		header_bools.append(True)
		image_label.config(text=f'Image column: {value}')
	return


def url_select(value) -> None:
	if value:
		header_bools.append(True)
		url_label.config(text=f'URL column: {value}')
	return


def title_select(value) -> None:
	if value:
		header_bools.append(True)
		title_label.config(text=f'Title column: {value}')
	return


def description_select(value) -> None:
	if value:
		header_bools.append(True)
		description_label.config(text=f'Description column: {value}')
	return


def tag_select(value) -> None:
	if value:
		header_bools.append(True)
		tags_label.config(text=f'Tags column: {value}')
	return


def printify_automation() -> None:
	create_product_from_csv(
		template=selected_template.get(),
		publish=publish_bool.get(),
		file_name=selected_file.get()
	)
	return


def etsy_tagging() -> None:
	csv_file = selected_file.get()
	driver = login_etsy()
	with open(csv_file, 'r') as file:
		reader: csv.DictReader = csv.DictReader(file)
		for row in reader:
			title: str = row['Listing.Title']
			tag_list: list[str] = [tag for tag in row['Tags.All Tags'].strip().split(',')]
			update_tags(driver=driver, title=title, tags=tag_list)
	close_driver(driver)
	return


# Main window logic
root: tkinter.Tk = tkinter.Tk()
root.title('PMD Automation')
root.minsize(555, 265)
root.configure(padx=10, pady=10)
# TODO: update for new widgets
for i in range(12):
	root.grid_rowconfigure(i, weight=1, pad=10)
for j in range(2):
	root.grid_columnconfigure(j, weight=1)

# button to select files
select_directory_button: tkinter.Button = tkinter.Button(root, text='Select file', command=select_csv)
select_directory_button.grid(row=0, column=0, sticky='nsew')

# MyDesign export csv
selected_file_label: tkinter.Label = tkinter.Label(root, text='Chosen file: Null', bg='white', width=20)
selected_file_label.grid(row=0, column=1, sticky='nsew')
selected_file: tkinter.StringVar = tkinter.StringVar()

# Etsy publish check box
publish_int: tkinter.IntVar = tkinter.IntVar()
publish_bool: tkinter.BooleanVar = tkinter.BooleanVar()
publish_bool.set(False)
checkbox: tkinter.Checkbutton = tkinter.Checkbutton(
	root,
	text='Publish to Etsy',
	variable=publish_int,
	onvalue=1,
	offvalue=0,
	width=20,
	command=checkbox_bool
)
checkbox.grid(row=1, column=0, sticky='nsew')

# template drop down
templates: list[str] = [key for key in TEMPLATES_DICT]
selected_template: tkinter.StringVar = tkinter.StringVar(root)
selected_template.set('Click to select Template')
# noinspection PyTypeChecker
dropdown: tkinter.OptionMenu = tkinter.OptionMenu(root, selected_template, *templates, command=template_select)
dropdown.grid(row=2, column=0, sticky='nsew')
# drop down label
dropdown_label: tkinter.Label = tkinter.Label(text='Template: Null', width=20, bg='white')
dropdown_label.grid(row=2, column=1, sticky='nsew')

# Publish feedback
publish_label: tkinter.Label = tkinter.Label(root, bg='white', width=20, text='Staying in Printify')
publish_label.grid(row=1, column=1, sticky='nsew')

# header routing vars and labels
selected_image_name: tkinter.StringVar = tkinter.StringVar(root)
selected_url: tkinter.StringVar = tkinter.StringVar(root)
selected_title: tkinter.StringVar = tkinter.StringVar(root)
selected_description: tkinter.StringVar = tkinter.StringVar(root)
selected_tags: tkinter.StringVar = tkinter.StringVar(root)

image_label: tkinter.Label = tkinter.Label(text='Select image column', width=20, bg='white')
url_label: tkinter.Label = tkinter.Label(text='Select URL column', width=20, bg='white')
title_label: tkinter.Label = tkinter.Label(text='Select title column', width=20, bg='white')
description_label: tkinter.Label = tkinter.Label(text='Select description column', width=20, bg='white')
tags_label: tkinter.Label = tkinter.Label(text='Select tags column', width=20, bg='white')

# final call for automations
final_automation_button: tkinter.Button = tkinter.Button(
	root,
	text='Start Automation',
	command=printify_automation,
	width=75,
	bg='red'
)
final_automation_button.grid(row=10, column=0, columnspan=2, sticky='nsew')

# Etsy tagger
tagger_label: tkinter.Label = tkinter.Label(
	text=(
		'* Please wait until all items are published on Etsy before running the tagger\n'
		'* CSV file must be the same used for automation\n'
		"* Have Etsy's 2FA ready"
	),
	bg='white',
)
tagger_label.grid(row=11, column=0, columnspan=2, sticky='nsew')

# Etsy tagger button
etsy_tagger: tkinter.Button = tkinter.Button(
	root,
	text='Etsy Tagger',
	command=etsy_tagging,
	width=75,
	bg='pink'
)
etsy_tagger.grid(row=12, column=0, columnspan=2, sticky='nsew')

root.mainloop()
