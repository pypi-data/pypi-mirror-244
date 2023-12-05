from .Config import Config;
import pandas as pd;
import numpy as np;
from .._utils import dtype_map;

class Select:
    def __init__(self,yxdb_tool=None,xml=None,execute=True,**kwargs):
        # LOAD DEFAULTS
        INPUT_CONSTRAINTS = [
            {
                "name":"selected",
                "required":True,
                "type":list,
                "sub_type":str,
                "field":True
            },
            {
                "name":"deselected",
                "required":False,
                "type":list,
                "sub_type":str,
                "default":[]
            },
            {
                "name":"keep_unknown",
                "required":False,
                "type":bool,
                "default":False
            },
            {
                "name":"reorder",
                "required":False,
                "type":bool,
                "default":True
            },
            {
                "name":"change_types",
                "required":False,
                "type":dict,
                "default":{},
                "validation":[{
                    "validator": lambda kwargs:
                                    all(i==True for i in [j in change_types for j in kwargs["selected"]]), ##MAKE SURE THAT ALL VALUES TO CHANGE TYPES OF ARE SELECTED
                    "error_msg": "A value in change_types is not selected"
                    },{
                    "validator": lambda kwargs:
                                    all(i==True for i in [j in dtype_map.keys() for j in kwargs["change_types"].values()]), ##MAKE SURE THAT ALL VALUES ARE A VAILD DTYPE
                    "error_msg":"Invalid dtype in change_types"
                }]
            },
            {
                "name":"renames",
                "required":False,
                "type":dict,
                "default":{},
                "validation":[{
                    "validator": lambda kwargs:
                                    all(i==True for i in [j in change_types for j in kwargs["selected"]]), ##MAKE SURE THAT ALL VALUES TO CHANGE TYPES OF ARE SELECTED
                    "error_msg": "A value in renames is not selected"
                }]
            }
        ]
        self.config = Config(INPUT_CONSTRAINTS);

        if yxdb_tool:
            self.load_yxdb_tool(yxdb_tool, execute=execute)
        elif xml:
            self.load_yxdb_tool(xml=xml)
        else:
            self.config.load(kwargs)


    def load_yxdb_tool(self,tool=None,xml = None,execute=True):
        kwargs = {}
        if xml is None:
            xml = tool.xml
        else:
            execute=False
        kwargs['reorder'] = xml.find(".//Configuration/OrderChanged").get("value")=="True"
        kwargs['keep_unknown'] = xml.find(".//SelectField[@field='*Unknown']").get("selected")=="True"
        kwargs['selected'] = []
        kwargs['deselected'] = []
        kwargs['change_types'] = {}
        kwargs['renames'] = {}

        for field in xml.findall(".//SelectField"):
            if field.get('field') == "*Unknown":
                continue;

            current_field = field.get('field')
            selected = field.get('selected')=='True'

            if selected:
                kwargs['selected'].append(current_field)
                if 'rename' in field.attrib:
                    kwargs['renames'][current_field] = field.get('rename')
                if 'type' in field.attrib:
                    kwargs['change_types'][current_field] = field.get('type')
            else:
                kwargs['deselected'].append(current_field)

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
        print("Executing Select:")
        c = self.config
        df = input_datasource.copy();
        fields = [];
        if c.keep_unknown:
            fields = [] if not c.reorder else c.selected
            for f in df.columns:
                if f not in c.deselected and (f not in c.selected or not c.reorder):
                    fields.append(f)
        else:
            fields = c.selected

        for fld in c.change_types:
            if c.change_types[fld] =="SpatialObj":
                continue
            df[fld] = df[fld].astype(dtype_map[c.change_types[fld]])

        df = df.loc[:, fields]
        df.rename(columns=c.renames,inplace=True)
        return df
