import tkinter
from tkinter import filedialog
import os
from Automation import create_product_from_csv


def select_csv() -> str:
	file_path = filedialog.askopenfilename(title="select directory")
	if file_path:
		file_name = os.path.basename(file_path)
		selected_file_label.config(text=f'Chosen file: {file_name}')
		selected_file_name.set(file_name)
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
	return selected_template.get()


def automation() -> None:
	# print(f'file name: {selected_file_name.get()}: {type(selected_file_name.get())}')
	# print(f'template name:{selected_template.get()}: {type(selected_template.get())}')
	# print(f'Publish?:{publish_bool.get()}: {type(publish_bool.get())}')
	create_product_from_csv(
		template=selected_template.get(),
		publish=publish_bool.get(),
		file_name=selected_file_name.get()
	)


# Main window logic
root: tkinter.Tk = tkinter.Tk()
root.geometry("1280x720")
# button to select files
select_directory_button: tkinter.Button = tkinter.Button(root, text='Select file', command=select_csv)
select_directory_button.pack()

# MyDesign export csv
selected_file_label: tkinter.Label = tkinter.Label(root, text='Chosen file: Null', bg='white', width=20)
selected_file_label.pack()
selected_file_name: tkinter.StringVar = tkinter.StringVar()

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
checkbox.pack()

# template drop down
templates: list[str] = ['test', 'test2', 'test3']  # change with modular templates
selected_template: tkinter.StringVar = tkinter.StringVar(root)
selected_template.set(templates[0])
# noinspection PyTypeChecker
dropdown = tkinter.OptionMenu(root, selected_template, *templates, command=template_select)
dropdown.pack()

# Publish feedback
publish_label: tkinter.Label = tkinter.Label(root, bg='white', width=20, text='Staying in Printify')
publish_label.pack()

# final call for automations
final_button: tkinter.Button = tkinter.Button(root, text='Start', command=automation)
final_button.pack()
root.mainloop()
