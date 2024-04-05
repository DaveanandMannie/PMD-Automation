import csv
import tkinter
from tkinter import filedialog
import os
from Automation import create_product_from_csv, TEMPLATES_DICT
from EtsyTags import login_etsy, update_tags, close_driver

header_bools: list[bool] = []
header_names: list[str] = []


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


def get_csv_headers(file_path: str) -> list[str]:
	global header_names
	with open(file_path, 'r') as file:
		reader: csv.DictReader = csv.DictReader(file)
		header_names = reader.fieldnames or []
		return header_names


def automations_check() -> None:
	if False in header_bools:
		final_automation_button.config(bg='red')
	elif selected_template.get() == 'Click to select Template':
		final_automation_button.config(bg='red')
	elif header_bools.count(True) == 5:
		final_automation_button.config(bg='#90EE90')


def select_csv() -> str:
	file_path = filedialog.askopenfilename(title="select directory")
	file_name = os.path.basename(file_path)
	selected_file_label.config(text=f'Chosen file: {file_name}', bg='#90EE90')
	selected_file.set(file_path)
	get_csv_headers(file_path)
	create_dropdowns()
	automations_check()
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
		dropdown_label.config(text=f'Template: {value}', bg='#90EE90')
	automations_check()
	return selected_template.get()


def image_name_select(value) -> None:
	if value:
		header_bools.append(True)
		image_label.config(text=f'Image column: {value}', bg='#90EE90')
	automations_check()
	return


def url_select(value) -> None:
	if value:
		header_bools.append(True)
		url_label.config(text=f'URL column: {value}', bg='#90EE90')
	automations_check()
	return


def title_select(value) -> None:
	if value:
		header_bools.append(True)
		title_label.config(text=f'Title column: {value}', bg='#90EE90')
	automations_check()
	return


def description_select(value) -> None:
	if value:
		header_bools.append(True)
		description_label.config(text=f'Description column: {value}', bg='#90EE90')
	automations_check()
	return


def tag_select(value) -> None:
	if value:
		header_bools.append(True)
		tags_label.config(text=f'Tags column: {value}', bg='#90EE90')
	automations_check()
	return


def task_in_progress() -> None:
	task_label.config(text='Task in progress', bg='yellow')
	root.update()
	return None


def printify_automation() -> None:
	task_in_progress()
	create_product_from_csv(
		template=selected_template.get(),
		publish=publish_bool.get(),
		file_name=selected_file.get(),
		image_name_header=selected_image_name.get(),
		image_url_header=selected_url.get(),
		title_header=selected_title.get(),
		description_header=selected_description.get(),
		tags_header=selected_tags.get()
	)
	task_label.config(text='Task finished', bg='#90EE90')
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
for i in range(14):
	root.grid_rowconfigure(i, weight=1, pad=15)
for j in range(2):
	root.grid_columnconfigure(j, weight=1, pad=15)

# button to select files
select_directory_button: tkinter.Button = tkinter.Button(root, text='Select file', command=select_csv)
select_directory_button.grid(row=1, column=0, sticky='nsew')

# MyDesign export csv
selected_file_label: tkinter.Label = tkinter.Label(root, text='Chosen file: Null', bg='white',)
selected_file_label.grid(row=1, column=1, sticky='nsew')
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
	command=checkbox_bool
)
checkbox.grid(row=10, column=0, sticky='nsew')

# template drop down
templates: list[str] = [key for key in TEMPLATES_DICT]
selected_template: tkinter.StringVar = tkinter.StringVar(root)
selected_template.set('Click to select Template')
# noinspection PyTypeChecker
dropdown: tkinter.OptionMenu = tkinter.OptionMenu(root, selected_template, *templates, command=template_select)
dropdown.grid(row=3, column=0, sticky='nsew')
# drop down label
dropdown_label: tkinter.Label = tkinter.Label(text='Template: Null', bg='white')
dropdown_label.grid(row=3, column=1, sticky='nsew')

# Publish feedback
publish_label: tkinter.Label = tkinter.Label(root, bg='white', text='Staying in Printify')
publish_label.grid(row=10, column=1, sticky='nsew')

# header routing vars and labels
selected_image_name: tkinter.StringVar = tkinter.StringVar(root)
selected_image_name.set('Click to select image name')

selected_url: tkinter.StringVar = tkinter.StringVar(root)
selected_url.set('Click to select URL')

selected_title: tkinter.StringVar = tkinter.StringVar(root)
selected_title.set('Click to select title')

selected_description: tkinter.StringVar = tkinter.StringVar(root)
selected_description.set('Click to select Description')

selected_tags: tkinter.StringVar = tkinter.StringVar(root)
selected_tags.set('Click to select tags')

image_label: tkinter.Label = tkinter.Label(text='Image column: Null', bg='white')
url_label: tkinter.Label = tkinter.Label(text='URL column: Null', bg='white')
title_label: tkinter.Label = tkinter.Label(text='Title column: Null', bg='white')
description_label: tkinter.Label = tkinter.Label(text='Description column: Null', bg='white')
tags_label: tkinter.Label = tkinter.Label(text='Tags column: Null', bg='white')

# final call for automations
final_automation_button: tkinter.Button = tkinter.Button(
	root,
	text='Start Automation',
	command=printify_automation,
	width=75,
	bg='red'
)
final_automation_button.grid(row=11, column=0, columnspan=2, sticky='nsew')

# Task feed back
task_label: tkinter.Label = tkinter.Label(text='No task started', bg='white')
task_label.grid(row=0, columnspan=2, sticky='nsew')

# Etsy tagger
tagger_label: tkinter.Label = tkinter.Label(
	text=(
		'* Please wait until all items are published on Etsy before running the tagger\n'
		'* CSV file must be the same used for automation\n'
		"* Have Etsy's 2FA ready"
	),
	bg='white',
)
tagger_label.grid(row=13, column=0, columnspan=2, sticky='nsew')

# Etsy tagger button
etsy_tagger: tkinter.Button = tkinter.Button(
	root,
	text='Etsy Tagger',
	command=etsy_tagging,
	width=75,
	bg='pink'
)
etsy_tagger.grid(row=14, column=0, columnspan=2, sticky='nsew')

root.mainloop()
