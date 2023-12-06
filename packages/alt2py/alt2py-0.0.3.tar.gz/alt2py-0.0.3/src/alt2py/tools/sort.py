from .Config import Config;
import pandas as pd;
import numpy as np;
from natsort import natsort_keygen;
from .recordid import RecordID


class Sort:
    def __init__(self,yxdb_tool=None,execute=True,**kwargs):
        INPUT_CONSTRAINTS = [
            {
                "name":"fields",
                "required":True,
                "type":list,
                "sub_type":str,
                "field":True
            },
            {
                "name":"orders",
                "required":False,
                "type":list,
                "sub_type":bool,##True = Ascending, False = Descending
                "default":[]
                #Defaults to all True
            },
            {
                "name":"handle_alpha_numeric",
                "required":False,
                "type":bool,
                "default":False
            },
            {
                "name":"na_position",
                "required":False,
                "type":str,
                "multi_choice":["last","first"],
                "default":"first" ##True = Top, False = Bottom
            },
            {
                "name":"maintain_order",
                "required":False,
                "type":bool,
                "default":False
            }
        ]
        # LOAD DEFAULTS
        self.config = Config(INPUT_CONSTRAINTS);
        if yxdb_tool:
            self.load_yxdb_tool(yxdb_tool, execute=execute)
        else:
            self.config.load(kwargs)

    def load_yxdb_tool(self,tool,execute=True):
        xml = tool.xml;
        kwargs = {};

        fields = xml.find(".//Configuration//SortInfo")
        kwargs['handle_alpha_numeric'] = fields.get("locale")!="0"

        kwargs['fields'] = []
        kwargs['orders'] = []
        for f in fields:
            kwargs['fields'].append(f.get("field"))
            kwargs['orders'].append(f.get("order")=="Ascending")

        kwargs['maintain_order'] = True;
        kwargs['na_position'] = "first";

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
        c = self.config;
        print("Executing Sort:")
        new_df = input_datasource.copy();
        while len(c.orders)<len(c.fields):
            c.orders += [True]

        if c.maintain_order:
            new_df = RecordID(field="___record_id___").execute(new_df)
            c.fields +=["___record_id___"]
            c.orders +=[True]

        if c.handle_alpha_numeric:
            new_df = new_df.sort_values(
                by=c.fields,
                ascending=c.orders,
                key=lambda x: natsort_keygen()(x.replace({pd.NA: None if c.na_position=="first" else "zzzzzzzzzzzzzzzzzzzzz"})),
            )
        else:
            new_df = new_df.sort_values(by=c.fields, ascending=c.orders, na_position=c.na_position)

        if c.maintain_order:
            new_df = new_df.drop("___record_id___", axis=1)
            c.fields.pop()
            c.orders.pop()

        return new_df.reset_index(drop=True)
