from .Config import Config;
import pandas as pd;
from functools import partial
from .._utils import Aggregators as agg;
from .sort import Sort;

class CrossTab:
    def __init__(self,yxdb_tool=None,execute=True,**kwargs):
        # LOAD DEFAULTS
        INPUT_CONSTRAINTS = [
            {
                "name":"groupings",
                "required":False,
                "type":list,
                "sub_type":str,
                "default":[],
                "field":True
            },{
                "name":"header",
                "required":True,
                "type":str,
                "field":True
            },{
                "name":"value_field",
                "required":True,
                "type":str,
                "field":True
            },{
                "name":"method",
                "required":True,
                "type":str,
                "multi_choice":["Sum","Average","Count","CountWithNulls","First","Last","Concat"]
            },{
                "name":"sep",
                "required":False,
                "type":str,
                "default":lambda kwargs: "," if kwargs["method"]=="Concat" else None
            }
        ]

        self.config = Config(INPUT_CONSTRAINTS);
        self.input_map = "Input"
        if yxdb_tool:
            self.load_yxdb_tool(yxdb_tool,execute=execute)
        else:
            self.config.load(kwargs)

    def load_yxdb_tool(self,tool,execute=True):
        xml = tool.xml;
        kwargs = {}
        sep = xml.find(".//Configuration//Methods//Separator")

        if sep is not None:
            sep = sep.text.replace("\s"," ")

        kwargs['groupings'] = [f.get("field") for f in xml.find(".//Configuration//GroupFields")]
        kwargs['header'] = xml.find(".//Configuration//HeaderField").get("field")
        kwargs['value_field'] = xml.find(".//Configuration//DataField").get("field")
        kwargs['method'] = xml.find(".//Configuration//Methods//Method").get("method")
        kwargs['sep'] = sep;

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
        # c.check_field_constraints(input_datasource)

        method_map = {
            "Sum":agg.sum,
            "Avg":agg.avg,
            "Count":agg.count_non_null,
            "CountWithNulls":agg.count,
            "First":agg.first,
            "Last":agg.last,
            "Concat":partial(agg.concat,sep=c.sep)
        }
        method = c.method
        if isinstance(method,str):
            method = method_map[method]


        new_df = input_datasource.copy()

        for header in c.header:
            new_df[c.header] = new_df[c.header].astype(pd.StringDtype())
            new_df[c.header] = new_df[c.header].str.replace(" ","_")
            new_df[c.header] = new_df[c.header].fillna('_Null_')

        indices = new_df[c.groupings]
        filled_indices = indices.astype("string").fillna("___NA___")

        # Create a crosstab
        crosstab_df = pd.crosstab(
            index=[filled_indices[col] for col in filled_indices.columns],
            columns=new_df[c.header],
            values=new_df[c.value_field],
            aggfunc=method
        )

        # Reset the index to get the columns 'presidentNumber', 'President', and 'Vice President'
        crosstab_df = crosstab_df.reset_index().rename_axis(None, axis=1)
        crosstab_df.columns = crosstab_df.columns.astype("object")

        crosstab_df[c.groupings] = crosstab_df[c.groupings].replace("___NA___",pd.NA).astype(indices.dtypes)

        crosstab_df = Sort(fields = c.groupings).execute(crosstab_df)
        return crosstab_df
