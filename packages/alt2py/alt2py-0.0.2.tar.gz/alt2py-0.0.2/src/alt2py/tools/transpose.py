from .Config import Config;
import pandas as pd;

class Transpose:
    def __init__(self,yxdb_tool=None,execute=True,**kwargs):
        # LOAD DEFAULTS
        INPUT_CONSTRAINTS = [
            {
                "name":"key_fields",
                "required":True,
                "type":list,
                "sub_type":str,
                "field":True
            },
            {
                "name":"data_fields",
                "required":True,
                "type":list,
                "sub_type":str,
                "field":True
            },
            {
                "name":"keep_unknown",
                "required":False,
                "type":bool,
                "default":False
            },
            {
                "name":"var_name",
                "required":False,
                "type":str,
                "default":"Name"
            },
            {
                "name":"value_name",
                "required":False,
                "type":str,
                "default":"Value"
            },
            {
                "name":"sort",
                "required":False,
                "type":bool,
                "default":False
            }
        ]

        self.config = Config(INPUT_CONSTRAINTS);
        if yxdb_tool:
            self.load_yxdb_tool(yxdb_tool, execute=execute)
        else:
            self.config.load(kwargs)

    def load_yxdb_tool(self,tool,execute=True):
        xml = tool.xml;
        kwargs = {};

        kwargs['sort']=True;
        kwargs['key_fields'] = [f.get("field") for f in xml.find(".//Configuration//KeyFields")]
        kwargs['data_fields'] = []
        for f in xml.find(".//Configuration//DataFields"):
            if f.get("selected")=="True" and f.get("field")!="*Unknown":
                kwargs['data_fields'].append(f.get("field"))

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
        new_df = input_datasource.copy()

        if not c.keep_unknown:
            new_df = new_df[c.key_fields + c.data_fields]

        dtypes_of_values = set(new_df[c.data_fields].dtypes.tolist())

        new_df = pd.melt(new_df, id_vars=c.key_fields, var_name=c.var_name, value_name=c.value_name)

        field_order_mapping = {month: i+1 for i, month in enumerate(c.data_fields)}

        new_df = new_df.sort_values(by=c.var_name, key=lambda x: x.map(field_order_mapping)).reset_index(drop=True)
        new_df.index.name = "__INDEX__"
        new_df = new_df.sort_values(by=c.key_fields+["__INDEX__"]).reset_index(drop=True)
        new_df.index.name = None

        new_df[c.var_name] = new_df[c.var_name].astype(pd.StringDtype())
        if len(dtypes_of_values)>1:
            is_numeric_result = input_datasource[c.data_fields].applymap(pd.api.types.is_numeric_dtype).all().all()
            if is_numeric_result:
                new_df[c.value_name] = new_df[c.value_name].astype(pd.Float64Dtype())
            else:
                new_df[c.value_name] = new_df[c.value_name].astype(pd.StringDtype())
        # if len(dtypes_of_values)==1:
        #     new_df[c.value_name] = new_df[c.value_name].astype(dtypes_of_values[0])
        return new_df
