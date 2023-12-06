from .Config import Config;
import pandas as pd;
import numpy as np;
from .._utils import Functions,dtype_map

class Formula:
    def __init__(self,yxdb_tool=None,execute=True,**kwargs):
        # LOAD DEFAULTS

        INPUT_CONSTRAINTS = [
            {
                "name":"formulae",
                "required":True,
                "type":list,
                "sub_type":dict
            },
            {
                "name":"formulae.field",
                "required":True,
                "type":str
            },
            {
                "name":"formulae.expression",
                "required":True,
                "type":str
            },
            {
                "name":"formulae.size",
                "required":False,
                "type":str
            },
            {
                "name":"formulae.type",
                "required":False,
                "type":str,
                "multi_choice":list(dtype_map.keys())
            },
        ]

        self.config = Config(INPUT_CONSTRAINTS);
        if yxdb_tool:
            self.load_yxdb_tool(yxdb_tool, execute=execute)
        else:
            self.config.load(kwargs)

    def load_yxdb_tool(self,tool,execute=True):
        xml = tool.xml
        kwargs = {"formulae":[]}
        formulaFields = xml.find("Properties/Configuration/FormulaFields")

        for f in formulaFields:
            subkwargs = {}
            subkwargs['field'] = f.get('field')
            subkwargs['type'] = f.get('type')
            subkwargs['size'] = f.get('size')
            subkwargs['expression'] = f.get('expression')
            kwargs["formulae"].append(subkwargs)

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

    def add_formula(self,**kwargs):
        c = self.config
        if not ('field' in kwargs and 'expression' in kwargs):
            raise Exception("A new formula must include 'field' and 'expression'")
        else:
            for k in kwargs.keys():
                if k not in ('field','expression','type','size'):
                    raise Exception("'"+k+"'" + " is not a formula argument")

            c.formulae.append(kwargs)

    def applier(self,series,**kwargs):

        field=kwargs.get("field",None)
        type=kwargs.get("type",None)
        size=kwargs.get("size",None)
        expression=kwargs.get("expression",None)


        if field not in series:
            series.at[field] = None

        series.at[field] = eval(expression)
        if type=='FixedDecimal' and size is not None:
            series.at[field] = round(series.at[field],int(size.split('.')[-1]))
        else:
            series.at[field] = series.at[field]

        return series

    def execute(self,input_datasource):
        print("Executing Formula:")
        next_df = input_datasource.copy()

        print(self.config.formulae)
        for exp in self.config.formulae:
            exp['expression'] = Functions.parse_formula(exp['expression'],column_names=next_df.columns,df_name='series')
            next_df = next_df.apply(self.applier,axis=1,**exp)
        #     next_df[exp["field"]] = next_df[exp["field"]].astype(dtype_map[exp["type"]])
        #
        # print(self.config.formulae)
        # next_df[input_datasource.columns] = next_df[input_datasource.columns].astype(input_datasource.dtypes)
        return next_df
