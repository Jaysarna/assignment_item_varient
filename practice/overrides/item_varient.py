import copy
import json

import frappe
from frappe import _
from frappe.utils import cstr, flt

@frappe.whitelist()
def create_variant(item, args):
	if isinstance(args, str):
		args = json.loads(args)

	template = frappe.get_doc("Item", item)
	variant = frappe.new_doc("Item")
	variant.variant_based_on = "Item Attribute"
	variant_attributes = []

	for d in template.attributes:
		variant_attributes.append({"attribute": d.attribute, "attribute_value": args.get(d.attribute)})

	variant.set("attributes", variant_attributes)
	copy_attributes_to_variant(template, variant)
	# make_variant_item_code(template.item_code, template.item_name, variant)

	return variant
def copy_attributes_to_variant(item, variant):
	# copy non no-copy fields

	exclude_fields = [
		"naming_series",
		"item_code",
		"item_name",
		"published_in_website",
		"opening_stock",
		"variant_of",
		"valuation_rate",
	]

	if item.variant_based_on == "Manufacturer":
		# don't copy manufacturer values if based on part no
		exclude_fields += ["manufacturer", "manufacturer_part_no"]

	allow_fields = [d.field_name for d in frappe.get_all("Variant Field", fields=["field_name"])]

	custom_fields = ['height','width','yield']

	allow_fields.extend(custom_fields)

	# frappe.msgprint(str(allow_fields))
	if "variant_based_on" not in allow_fields:
		allow_fields.append("variant_based_on")
	for field in item.meta.fields:
		# "Table" is part of `no_value_field` but we shouldn't ignore tables
		if (field.reqd or field.fieldname in allow_fields) and field.fieldname not in exclude_fields:
			if variant.get(field.fieldname) != item.get(field.fieldname):
				if field.fieldtype == "Table":
					variant.set(field.fieldname, [])
					for d in item.get(field.fieldname):
						row = copy.deepcopy(d)
						if row.get("name"):
							row.name = None
						variant.append(field.fieldname, row)
				else:
					variant.set(field.fieldname, item.get(field.fieldname))

	variant.variant_of = item.name

