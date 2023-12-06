from .Config import Config;
import pandas as pd
from sklearn.model_selection import train_test_split


class Sample:
    def __init__(self,yxdb_tool=None,execute=True,**kwargs):
        # LOAD DEFAULTS
        INPUT_CONSTRAINTS = [
            {
                "name":"train",
                "required":False,
                "type":(int,float),
                "default":0.75
            },
            {
                "name":"validate",
                "required":False,
                "type":(int,float),
                "default":0.25
            },
            {
                "name":"seed",
                "required":False,
                "type":int,
                "default":None
            },
            {
                "name":"shuffle",
                "required":False,
                "type":bool,
                "default":True
            }
        ]
        self.config = Config(INPUT_CONSTRAINTS);
        self.train = None;
        self.validate = None;
        self.hold = None;
        self.yxdb_map = None

        if yxdb_tool:
            self.load_yxdb_tool(yxdb_tool,execute=execute)
        else:
            self.config.load(kwargs)

    def load_yxdb_tool(self,tool,execute=True):
        if tool.name[-1]=="RandomSample":
            self.yxdb_map = {
                "Input":"Input",
                "Output":"Output"
            }
            self.load_yxdb_tool_random(tool,execute=execute)
        else:
            self.yxdb_map = {
                "Input":"Input",
                "Output":{
                    "Estimation":"train",
                    "Validation":"validate",
                    "Holdout":"hold",
                }
            }
            self.load_yxdb_tool_sample(tool,execute=execute)

    def load_yxdb_tool_random(self,tool,execute=True):
        values = {v.get("name"):v.text for v in tool.xml.find(".//Configuration")}
        asNumber = values["Number"]=="True";
        asPercent = values["Percent"]=="True"
        seed = int(values["Seed"]) if values["Deterministic"]=="True" else None;
        train = int(values["NNumber"]) if asNumber else int(values["NPercent"])/100 if asPercent else None;

        if train is None:
            raise Exception("No train value")

        actual_tool = Sample(train=train,seed=seed)

        if execute:
            df = tool.get_input("Input")
            self.train = actual_tool.execute(df).train
            tool.data["Output"] = self.train

    def load_yxdb_tool_sample(self,tool,execute=True):
        xml = tool.xml

        kwargs = {}

        values = {v.get("name"):int(v.text) for v in xml.find(".//Configuration")}

        kwargs['train'] = values["estimation pct"]/100
        kwargs['validate'] = values["validation pct"]/100 #(100 - values["estimation pct"])
        kwargs['seed'] = values["rand seed"]
        kwargs['shuffle'] = False;

        self.config.load(kwargs)

        if execute:
            df = tool.get_input("Input")
            out = self.execute(df)

            tool.data["Estimation"] = out.train
            tool.data["Validation"] = out.validate
            tool.data["Holdout"] = out.hold

    def get_yxdb_mapping(self):
        return self.yxdb_map

    def execute(self,input_datasource):
        c = self.config;
        print(c)

        new_df = input_datasource.copy();
        print(len(new_df))
        if c.train <= 1:
            c.train = round(c.train*len(new_df))
            c.validate = round(c.validate*len(new_df))
        if c.validate == 0:
            c.validate = len(new_df) - c.train

        print(c)
        temp, train = train_test_split(new_df, test_size=c.train, random_state=c.seed,shuffle=c.shuffle)
        if len(temp)==c.validate:
            validate=temp
            hold = new_df.head(0);
        else:
            hold, validate = train_test_split(temp, test_size=c.validate, random_state=c.seed,shuffle=c.shuffle)

        self.train = train.reset_index(drop=True)
        self.validate = validate.reset_index(drop=True)
        self.hold = hold.reset_index(drop=True);

        return self
