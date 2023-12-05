from .Config import Config;
import pandas as pd;


class Union:
    def __init__(self,yxdb_tool=None,execute=True,**kwargs):
        # LOAD DEFAULTS
        INPUT_CONSTRAINTS = [
            {
                "name":"mode",
                "required":False,
                "type":str,
                "multi_choice":["position","name","manual"]
            },
            {
                "name":"subset",
                "required":False,
                "type":bool,
                "default":True
            },
            {
                "name":"manual",
                "required":False,
                "type":list,
                "sub_type":list,
                "default":[]
            },
            {
                "name":"order",
                "required":False,
                "type":list,
                "default":[]
            },
        ]
        self.config = Config(INPUT_CONSTRAINTS);
        if yxdb_tool:
            self.load_yxdb_tool(yxdb_tool,execute=execute)
        else:
            self.config.load(kwargs)

    def get_yxdb_mapping(self):
        return {
            "Input":"__named_inputs__",
            "Output":"Output"
        }

    def load_yxdb_tool(self,tool,execute=True):
        xml = tool.xml;
        kwargs = {};

        mode_names = {"ByName":"name","ByPos":"position","Manual":"manual","ManualDelayed":"manual"}
        kwargs['mode'] = mode_names[xml.find(".//Configuration//Mode").text]
        kwargs['subset'] = xml.find(".//Configuration//ByName_OutputMode").text=="Subset"

        order_changed = xml.find(".//Configuration//SetOutputOrder").get("value")=="True"

        if order_changed:
            kwargs['order'] = [con.text for con in xml.find(".//Configuration//OutputOrder")]

        if kwargs['mode'] == "manual":
            kwargs['manual'] = []
            for meta_info in xml.find(".//Configuration//MultiMetaInfo"):
                kwargs['manual'].append([f.get("name") for f in meta_info.find("RecordInfo")])
        self.config.load(kwargs)
        print("HERE")
        print(self.config)
        if execute:
            dfs = tool.get_named_inputs("Input")
            ##TODO: rework the logic of how inputs are passed to exec. don't use dict, use list.
            next_df = self.execute(dfs)
            tool.data["Output"] = next_df


    def union_by_manual(self,dfs):
        c = self.config;

        renamed_dfs = []
        for i,df in enumerate(dfs):
            if i==0:
                renamed_dfs.append(df[c.manual[0]])
            else:
                new_df = df[c.manual[i]]
                renames = {}
                for j,old_name in enumerate(new_df.columns.tolist()):
                    renames[old_name] = c.manual[0][j]
                new_df.rename(columns=renames,inplace=True);
                renamed_dfs.append(new_df)
        merged = pd.concat(renamed_dfs,axis=0)
        return merged

    def union_by_pos(self,dfs):
        c = self.config;

        names = dfs[0].columns.tolist()
        for df in dfs[1:]:
            renames = {}
            for i,col in enumerate(df.columns):
                if i<len(names):
                    renames[col] = names[i]
                else:
                    names.append(df.columns[i])
            df.rename(columns=renames,inplace=True)

        merged = pd.concat(dfs,axis=0)
        if c.subset:
            length = min([len(df.columns) for df in dfs])
            merged = merged.iloc[:, :length]
        return merged

    def union_by_name(self,dfs):
        c = self.config;

        matched_names = [];
        unmatched_names = [];

        if c.subset:
            matched_names = []
            for name in dfs[0].columns:
                matched = True
                for df in dfs[1:]:
                    matched = matched and (name in df.columns)
                if matched:
                    matched_names.append(name)

            dfs = [df[matched_names] for df in dfs]

            merged = pd.concat(dfs,axis=0)
            return merged
        else:
            matched_names = dfs[0].columns.tolist()
            for df in dfs[1:]:
                for col in df.columns:
                    if col not in matched_names:
                        matched_names.append(col)
            new_dfs = []
            for df in dfs:
                for name in matched_names:
                    if name not in df.columns:
                        df[name] = pd.NA
                new_dfs.append(df[matched_names])

            merged = pd.concat(new_dfs,axis=0)
            return merged


    def execute(self,input_datasources):
        c = self.config;

        dfs = None;
        if isinstance(input_datasources[0],dict):
            dfs = {df["name"]:df["data"].copy() for df in input_datasources}
            if len(c.order)>0:
                dfs = [dfs[n] for n in c.order]
            else:
                dfs = list(dfs.values())
        else:
            dfs = [df.copy() for df in input_datasources]

        print(c.order)

        if c.mode == "name":
            new_df = self.union_by_name(dfs)
        elif c.mode == "position":
            new_df = self.union_by_pos(dfs)
        elif c.mode == "manual":
            new_df = self.union_by_manual(dfs)
        else:
            raise Exception("Invalid mode. Valid modes are: 'name','position' or 'manual'")


        for i,dtype in enumerate(new_df.dtypes):
            if dtype=="object":
                new_df[new_df.columns[i]] = new_df[new_df.columns[i]].astype(pd.StringDtype())

        return new_df.reset_index(drop=True)

    class Config:
        def __init__(
            self
        ):
            self.mode = "position"#|name|manual
            self.subset = True;
            self.manual = [];
            self.order = [];

        def __str__(self):
            attributes = vars(self)
            out=""
            max_spacing = max([len(attr) for attr,_ in attributes.items()])

            for attribute, value in attributes.items():
                space = " "*(max_spacing - len(attribute))
                newline = '\n' if len(out) else ''
                out +=(f"{newline}{attribute}: {space}{{{value}}}")
            return out
