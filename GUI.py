import csv
import tkinter
from tkinter import filedialog
import os
from Automation import create_product_from_csv, TEMPLATES_DICT
from EtsyTags import login_etsy, update_tags, close_driver


def select_csv() -> str:
	file_path = filedialog.askopenfilename(title="select directory")
	file_name = os.path.basename(file_path)
	selected_file_label.config(text=f'Chosen file: {file_name}')
	selected_file.set(file_path)
	if selected_file.get() and selected_template.get():
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
		dropdown_label.config(text=value)
	if selected_file.get() and selected_template.get():
		final_automation_button.config(bg='#90EE90')
	return selected_template.get()


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
		reader = csv.DictReader(file)
		for row in reader:
			# noinspection PyTypeChecker
			title: str = row['Listing.Title']
			# noinspection PyTypeChecker
			tag_list: list[str] = [tag for tag in row['Tags.All Tags'].strip().split(',')]
			update_tags(driver=driver, title=title, tags=tag_list)
	close_driver(driver)
	return


# Main window logic
root: tkinter.Tk = tkinter.Tk()
root.title('PMD Automation')
root.configure(padx=10, pady=10)
root.grid_rowconfigure(0, pad=10)
root.grid_rowconfigure(1, pad=10)
root.grid_rowconfigure(2, pad=10)
root.grid_rowconfigure(3, pad=10)
root.grid_rowconfigure(4, pad=10)
root.grid_rowconfigure(5, pad=10)
root.grid_rowconfigure(6, pad=10)
# button to select files
select_directory_button: tkinter.Button = tkinter.Button(root, text='Select file', command=select_csv)
select_directory_button.grid(row=0, column=0)

# MyDesign export csv
selected_file_label: tkinter.Label = tkinter.Label(root, text='Chosen file: Null', bg='white', width=20)
selected_file_label.grid(row=0, column=1)
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
checkbox.grid(row=1, column=0)

# template drop down
templates: list[str] = [key for key in TEMPLATES_DICT]
selected_template: tkinter.StringVar = tkinter.StringVar(root)
selected_template.set('Click to select Template')
# noinspection PyTypeChecker
dropdown = tkinter.OptionMenu(root, selected_template, *templates, command=template_select)
dropdown.grid(row=2, column=1)

dropdown_label: tkinter.Label = tkinter.Label(text='', width=20, bg='white')
dropdown_label.grid(row=2, column=0)

# Publish feedback
publish_label: tkinter.Label = tkinter.Label(root, bg='white', width=20, text='Staying in Printify')
publish_label.grid(row=1, column=1)

# final call for automations
final_automation_button: tkinter.Button = tkinter.Button(
	root,
	text='Start Automation',
	command=printify_automation,
	width=75,
	bg='red'
)
final_automation_button.grid(row=3, column=0, columnspan=2)

# Etsy tagger
tagger_label: tkinter.Label = tkinter.Label(
	text=(
		'* Please wait until all items are published on Printify before running the tagger\n'
		'* CSV file must be the same used for automation\n'
		"* Have Etsy's 2FA ready"
	),
	bg='white',
)
tagger_label.grid(row=4, column=0, columnspan=2)
etsy_tagger: tkinter.Button = tkinter.Button(
	root,
	text='Etsy Tagger',
	command=etsy_tagging,
	width=75,
	bg='pink'
)
etsy_tagger.grid(row=5, column=0, columnspan=2)

root.mainloop()
