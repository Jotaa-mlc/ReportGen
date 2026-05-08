def build_formats(workbook):
    return {
        "header": workbook.add_format({
            "bold": True,
            "bg_color": "#D9E1F2",
            "border": 1,
            "align": "center",
            "valign": "vcenter"
        }),
        
        "money": workbook.add_format({
            "num_format": 'R$ #,##0.00'
        }),

        "percent": workbook.add_format({
            "num_format": '0.00%'
        }),

        "integer": workbook.add_format({
            "num_format": '0'
        }),
        
        "decimal": workbook.add_format({
            "num_format": '0.00'
        }),

        "zero": workbook.add_format({
            "bg_color": "#D9D9D9",
            "font_color": "#808080"
        })
    }