frappe.ui.form.on('Item', {
    refresh(frm) {
        frm.remove_custom_button("Single Variant", 'Create');
        frm.add_custom_button(__("Custom Variant"), function () {
            // mapp function
            erpnext.item.show_single_variant_dialog(frm);
        }, __('Create'));

    },
    validate(frm) {
        // your code here
        var uom_table = cur_frm.doc.uoms
        uom_table.forEach((e) => {
            // console.log(e)
            if (e.uom == 'Kg' || e.uom == 'Cubic Meter') {

                try {
                    var a = eval(e.formula);
                    e.conversion_factor = a
                    // frappe.model.set_value(cdt,cdn,'conversion_factor',a);
                    frm.refresh_field('uoms');
                }
                catch (err) {
                    frappe.throw("Formula in UOM Conversion table is not defined properly")
                }
            }
        })
    }
})

frappe.provide("erpnext.item");

$.extend(erpnext.item, {

    show_single_variant_dialog: function (frm) {
        var fields = []

        for (var i = 0; i < frm.doc.attributes.length; i++) {
            var fieldtype = "Data";
            var row = frm.doc.attributes[i];
            var custom_value

            if (row.attribute == 'Height'){
                custom_value = frm.doc.height
            }
            else if(row.attribute == 'Yield'){
                custom_value = frm.doc.yield
            }
            else if(row.attribute == 'Width'){
                custom_value = frm.doc.width
            }

            fields = fields.concat({
                "label": row.attribute,
                "fieldname": row.attribute,
                "fieldtype": fieldtype,
                "default": custom_value,
                "reqd": 0,
                "read_only":1
            })
        }

        var d = new frappe.ui.Dialog({
            title: __('Create Variant'),
            fields: fields
        });

        d.set_primary_action(__('Create'), function () {
            var args = d.get_values();
            frappe.call({

                method: "practice.overrides.item_varient.create_variant",
                args: {
                    "item": frm.doc.name,
                    "args": d.get_values()
                },
                callback: function (r) {
                    var doclist = frappe.model.sync(r.message);
                    frappe.set_route("Form", doclist[0].doctype, doclist[0].name);
                }
            });
        });

        d.show();
    },


});