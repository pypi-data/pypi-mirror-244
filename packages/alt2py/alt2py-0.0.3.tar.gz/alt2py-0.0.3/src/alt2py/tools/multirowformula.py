from . import Config;
import pandas as pd;
import numpy as np;
import re
from .._utils import Functions,dtype_map


class MultiRowFormula:
    def __init__(self,yxdb_tool=None,execute=True,**kwargs):
        # LOAD DEFAULTS
        INPUT_CONSTRAINTS = [
            {
                "name":"field",
                "required":True,
                "type":str
            },{
                "name":"groupings",
                "required":False,
                "type":list,
                "sub_type":str,
                "default":[],
                "field":True
            },{
                "name":"num_rows",
                "required":True,
                "type":int
            },{
                "name":"expression",
                "required":True,
                "type":str,
            },{
                "name":"type",
                "required":False,
                "type":str,
                "multi_choice":list(dtype_map.keys())
            },{
                "name":"size",
                "required":False,
                "type":str,
                "default":None
            },{
                "name":"unknown",
                "required":False,
                "type":(str,type(pd.NA)),
                "default":"null",
                "multi_choice":["null","nearest","empty"]
            }
        ]

        self.config = Config(INPUT_CONSTRAINTS);
        self.true = None;
        self.false = None;
        if yxdb_tool:
            self.load_yxdb_tool(yxdb_tool, execute=execute)
        else:
            self.config.load(kwargs)

    def load_yxdb_tool(self,tool,execute=True):
        xml = tool.xml;
        kwargs = {}

        kwargs["expression"] =  xml.find(".//Configuration/Expression").text
        kwargs["num_rows"] = int(xml.find(".//Configuration/NumRows").get("value"))
        kwargs["unknown"] = xml.find(".//Configuration/OtherRows").text.lower()

        if xml.find(".//Configuration/UpdateField").get("value")=="True":
            kwargs["field"] = xml.find(".//Configuration/UpdateField_Name").text
        else:
            kwargs["field"] = xml.find(".//Configuration/CreateField_Name").text
            kwargs["type"] = xml.find(".//Configuration/CreateField_Type").text
            kwargs["size"] = xml.find(".//Configuration/CreateField_Size").text

        kwargs["groupings"] = []
        for f in xml.find(".//Configuration/GroupByFields"):
            kwargs["groupings"].append(f.get('field'))

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

    def format_multirow_formula(self,index,column_names):
        pattern = re.compile(rf'series\[\'Row([\+\-]\d+):(.*?)\'\]', re.IGNORECASE)
        sub = rf"new_df['\2'].at[eval('{index}\1')]"
        text = Functions.parse_formula(self.config.expression,df_name="series",column_names=column_names)
        return re.sub(pattern,sub,text)

    def apply_formula(self,df):
        c = self.config;
        null_row = []
        null_row2 = []
        if c.unknown=="null":
            null_row=[pd.NA]*len(df.columns)
            null_row2 = null_row
        elif c.unknown=="empty":
            for col in df.columns:
                if pd.api.types.is_bool_dtype(df[col]):
                    null_row.append(pd.NA)
                elif pd.api.types.is_numeric_dtype(df[col]):
                    null_row.append(0)
                elif pd.api.types.is_string_dtype(df[col]):
                    null_row.append('')
                else:
                    null_row.append(pd.NA)
            null_row2 = null_row
        else:
            null_row = df.iloc[0].tolist()
            null_row2 = df.iloc[len(df)-1].tolist()


        null_df_start = pd.DataFrame([null_row]*c.num_rows,columns=df.columns,index=[-i for i in range(1,c.num_rows+1)])
        null_df_end = pd.DataFrame([null_row2]*c.num_rows,columns=df.columns,index=[i for i in range(len(df),c.num_rows+len(df))])
        new_df = pd.concat([null_df_start,df,null_df_end]).astype(df.dtypes)

        for i,series in new_df.loc[0:len(df)-1].iterrows():
            exp = self.format_multirow_formula(i,new_df.columns)
            new_element = eval(exp)
            if pd.api.types.is_bool_dtype(df[c.field]):
                new_df[c.field].at[i] = not not new_element
            else:
                new_df[c.field].at[i] = new_element
            # new_df["Year"] = eval(x)

        return new_df.loc[0:len(df)-1]

    def execute(self,input_datasource):
        c = self.config;
        new_df = input_datasource.copy()
        if c.field not in new_df:
            new_df[c.field] = pd.NA
            new_df[c.field] = new_df[c.field].astype(dtype_map[c.type])

        if len(c.groupings):
            dfs_to_concat = []
            for i,group in new_df.groupby(c.groupings):
                dfs_to_concat.append(self.apply_formula(group.reset_index(drop=True)))

            new_df = pd.concat(dfs_to_concat).reset_index(drop=True)
        else:
            new_df = self.apply_formula(new_df)

        if c.type:
            new_df[c.field] = new_df[c.field].astype(dtype_map[c.type])
            if c.size is not None and "." in c.size:
                new_df[c.field] = new_df[c.field].apply(lambda x: Functions.Round(x,10**(-int(c.size.split(".")[-1]))))
        return new_df;
