from .Config import Config;
import pandas as pd;
import numpy as np;
from .._utils import Functions;
from .formula import Formula;

class MultiFieldFormula:
    def __init__(self,yxdb_tool=None,execute=True,**kwargs):
        # LOAD DEFAULTS
        INPUT_CONSTRAINTS = [
            {
                "name":"fields",
                "required":True,
                "type":list,
                "sub_type":str,
                "field":True
            },{
                "name":"expression",
                "required":True,
                "type":str
            },{
                "name":"type",
                "required":False,
                "type":str,
                "default":None
            },{
                "name":"size",
                "required":False,
                "type":str,
                "default":None
            },{
                "name":"prefix",
                "required":False,
                "type":str,
                "default":""
            },{
                "name":"suffix",
                "required":False,
                "type":str,
                "default":""
            }
        ]

        self.config = Config(INPUT_CONSTRAINTS);
        if yxdb_tool:
            self.load_yxdb_tool(yxdb_tool, execute=execute)
        else:
            self.config.load(kwargs)

    def load_yxdb_tool(self,tool,execute=True):
        kwargs = {}
        xml = tool.xml;

        kwargs['expression'] =  xml.find(".//Configuration/Expression").text

        fields =  xml.find(".//Configuration/Fields")

        kwargs['fields'] = []

        for f in fields:
            if not f.get("selected")=="False" and not f.get("name")=="*Unknown":
                kwargs['fields'].append(f.get("name"))

        change_type =  xml.find(".//Configuration/ChangeFieldType").get("value")=="True"

        if change_type:
            out = xml.find(".//Configuration/OutputFieldType")
            kwargs['type'] = out.get("type");
            if out.get("size"):
                kwargs['size'] = out.get("size");
                if out.get("scale"):
                    kwargs['size']+="."+out.get("scale")

        add_fields = xml.find(".//Configuration/CopyOutput").get("value")=="True"

        if add_fields:
            is_prefix =  xml.find(".//Configuration/NewFieldAddOnPos").text=="Prefix"
            if is_prefix:
                kwargs['prefix'] = xml.find(".//Configuration/NewFieldAddOn").text;
            else:
                kwargs['suffix'] = xml.find(".//Configuration/NewFieldAddOn").text;

        self.config.load(kwargs)
        if execute:
            df = tool.get_input("Input")
            next_df = self.execute(df)
            tool.data["Output"] = next_df

    def get_yxdb_mapping(self):
        return {
            "Input":"Input",
            "Output":"Output"
        }

    def execute(self,input_datasource):
        c = self.config
        df = input_datasource.copy();

        formulae = []

        for f in c.fields:
            formulae.append({
                "field":c.prefix +f+c.suffix,
                "expression":Functions.format_field_formula(c.expression,f),
                "type":c.type,
                "size":c.size
            })

        next_df = Formula(formulae=formulae).execute(df)

        return next_df
