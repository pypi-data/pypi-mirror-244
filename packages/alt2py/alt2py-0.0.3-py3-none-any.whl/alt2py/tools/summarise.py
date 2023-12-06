from .Config import Config;
import pandas as pd
import re
from functools import reduce,partial;
from collections import OrderedDict;
from .._utils import Aggregators


class Summarise:
    def __init__(self,yxdb_tool=None,execute=True,**kwargs):
        # LOAD DEFAULTS
        INPUT_CONSTRAINTS = [
            {
                "name":"fields",
                "required":True,
                "type":list,
                "sub_type":dict
            },
            {
                "name":"fields.field",
                "required":True,
                "type":str,
                "field":True
            },
            {
                "name":"fields.action",
                "required":True,
                "type":str,
                "multi_choice":Aggregators.get_names() + ["GroupBy"]
            },
            {
                "name":"fields.name",
                "required":True,
                "type":str,
            },
            {
                "name":"fields.props",
                "required":False,
                "type":dict,
                "default":{}
            },
        ]
        self.config = Config(INPUT_CONSTRAINTS);

        self.aggregators = OrderedDict();
        self.group_names = [];
        self.group_renames = [];
        self.agg_renames = []; #agg_names
        self.order = []

        if yxdb_tool:
            self.load_yxdb_tool(yxdb_tool, execute=execute)
        else:
            self.config.load(kwargs)
            self.generate_properties()

    def add_aggregator(self,field,rename,aggregator,**kwargs):
        if field in self.aggregators:
            self.aggregators[field].append(partial(aggregator,**kwargs))
        else:
            self.aggregators[field] = [partial(aggregator,**kwargs)]
        self.agg_renames.append(rename)
        self.order.append(rename)

    def add_grouping(self,field,rename):
        self.group_names.append(field)
        self.group_renames.append(rename)
        self.order.append(rename)

    def map_props(self,props):
        arg_map = {
            "Concat_Start":"start",
            "Separator":"sep",
            "Concat_End":"end"
        }

        args = {}
        for p in props:
            args[arg_map[p]] = props[p]
        return args

    def generate_properties(self):
        c = self.config
        for field in c.fields:
            if field['action']=="GroupBy":
                self.add_grouping(field['field'],field['name'])
            else:
                other_args = self.map_props(field['props'])
                self.add_aggregator(field['field'],field['name'],Aggregators.get_by_name(field['action']),**other_args)


    def load_yxdb_tool(self,tool, execute=True):
        kwargs= {"fields":[]}
        xml = tool.xml
        summary_fields = xml.find("Properties/Configuration/SummarizeFields");
        for field in summary_fields:
            to_add = {}
            to_add['field'] = field.get('field')
            to_add['action'] = field.get('action')
            to_add['name'] = field.get('rename')
            to_add['props'] = {f.tag: f.text for f in field}
            kwargs["fields"].append(to_add)
        self.config.load(kwargs)
        self.generate_properties()

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
        print("Executing Summarise:")
        df = input_datasource.copy()
        if len(self.group_names)>0:
            grouped = df.groupby(self.group_names)
            if len(self.aggregators)==0:
                result_df = pd.DataFrame(list(grouped.groups.keys()))
            else:
                result_df = grouped.agg(self.aggregators).reset_index()
        else:
            if len(self.aggregators)==0:
                result_df = df
            else:
                result_df = df.agg(self.aggregators).reset_index(drop=True).T.stack().to_frame().T

        result_df.columns = self.group_renames + self.agg_renames
        result_df.reset_index(drop=True,inplace=True)

        result_df = result_df.loc[:,self.order]



        return result_df

    class Config:
        def __init__(
            self
        ):
            self.aggregators = OrderedDict();
            self.group_names = [];
            self.group_renames = [];
            self.agg_renames = []; #agg_names
            self.order = []

        def __str__(self):
            attributes = vars(self)
            out=""
            max_spacing = max([len(attr) for attr,_ in attributes.items()])

            for attribute, value in attributes.items():
                space = " "*(max_spacing - len(attribute))
                newline = '\n' if len(out) else ''
                out +=(f"{newline}{attribute}: {space}{{{value}}}")
            return out
