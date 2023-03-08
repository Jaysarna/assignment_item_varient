# Copyright (c) 2023, jayakhilam and contributors
# For license information, please see license.txt

import json
import frappe
from frappe.model.document import Document
from frappe.utils import validate_json_string

class testAPI(Document):
	pass


@frappe.whitelist()
def make_sales_order():
	# order = "[{'text': \"\nOutput: command:create_sales_order,items = [{'item_name':'desktop','qty':2},{'item_name':'moues','qty':5}]\", 'index': 0, 'logprobs': None, 'finish_reason': 'stop'}]"
	# extract_create_sales_order(order)
	# import json
	# def extract_create_sales_order(input_str):
	# 	res = json.loads(input_str)
	# 	return res
	# 	# try:
	# 	# 	input_list = json.loads(input_str)
	# 	# 	text = input_list[0]['text']
	# 	# 	text = text.strip()
	# 	# 	command, items = text.split(',items =')
	# 	# 	command = command.split(':')[2].strip()
	# 	# 	items = eval(items)
	# 	# 	return (command, items)
	# 	# 	# if command == 'create_sales_order':
	# 	# 	# 	return (command, items)
	# 	# 	# else:
	# 	# 	# 	raise Exception("Not a valid create_sales_order command")
	# 	# except Exception as e:
	# 	# 	frappe.msgprint("Error occurred while parsing the input: {}".format(e))
	# 	# 	return (None, None)
	# input_str = "[{'text': \nOutput: command:create_sales_order,items = [{'item_name':'desktop','qty':2},{'item_name':'moues','qty':5}], 'index': 0, 'logprobs': None, 'finish_reason': 'stop'}]"
	# res = extract_create_sales_order(input_str)
	# frappe.msgprint(str(res))
	# if command:
	# 	frappe.msgprint("Command: {}".format(command))
	# 	frappe.msgprint("Items: {}".format(items))
	# else:
	# 	frappe.msgprint("Not a valid create_sales_order command")
	order = '[{"text": "\\nOutput: command:create_sales_order, items = [{\\"item_name\\":\\"desktop\\",\\"qty\\":2},{\\"item_name\\":\\"moues\\",\\"qty\\":5}]", "index": 0, "logprobs": None, "finish_reason": "stop"}]'
	try:
		validate_json_string(order)
		new_order= json.loads(order)
		doc = frappe.get_doc({
		'doctype': 'Sales Order',
		'customer': 'jay',
		'delivery_date':'2023-02-15',
		'items':[{'item_code':'desktop','description':'new','qty':2},{'item_code':'moues','description':'new','qty':5}]
					})
		doc.insert()

	except frappe.ValidationError:
		frappe.msgprint(str(frappe.ValidationError))
		frappe.msgprint('Not a valid JSON string')
	
	return 'working'

