from xlsxwriter.workbook import Workbook
from xlsxwriter.format import Format

FORMATS = {
    "header": {
        "bold": True,
        "bg_color": "#D9E1F2",
        "border": 1,
        "align": "center",
        "valign": "vcenter"
    },
    
    "money": {
        "num_format": 'R$ #,##0.00'
    },

    "percent": {
        "num_format": '0.00%'
    },

    "integer": {
        "num_format": '0'
    },
    
    "decimal": {
        "num_format": '0.00'
    },
    
    "date": {
        "num_format": 'dd/mm/yyyy'
    },
    
    "text": {
        "num_format": '@'
    }
}

def build_formats(workbook: Workbook, formats_definitions: dict = {}) -> dict[str, Format]:
    formats = FORMATS | formats_definitions
    return {

        name: workbook.add_format(props)
        
        for name, props 
        in formats.items()
    }