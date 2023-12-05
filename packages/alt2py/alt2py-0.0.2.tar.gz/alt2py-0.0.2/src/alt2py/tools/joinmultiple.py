from .Config import Config;
import pandas as pd;
from .select import Select
import re


class JoinMultiple:
    def __init__(self,yxdb_tool=None,execute=True,**kwargs):
        # LOAD DEFAULTS
        INPUT_CONSTRAINTS = [
            {
                "name":"fields",
                "required":lambda kwargs: not kwargs["by_position"],
                "required_error_msg":"fields are required when by_position=False",
                "type":list,
                "sub_type":list,
                "required":"True"
            },{
                "name":"prefixes",
                "required":True,
                "type":list,
                "sub_type":str
            },{
                "name":"by_position",
                "required":False,
                "type":bool,
                "default":False
            },{
                "name":"inner",
                "required":False,
                "type":bool,
                "default":True
            }
        ]
        self.config = Config(INPUT_CONSTRAINTS);
        if yxdb_tool:
            self.xml = yxdb_tool.xml
            self.load_yxdb_tool(yxdb_tool,skip_preload=True)
        else:
            self.config.load(kwargs)

    def load_yxdb_tool(self,tool,execute=True, skip_preload = False, preload_data = None):
        if not skip_preload:
            kwargs = {}
            xml = self.xml;

            kwargs['prefixes'] = [df["name"] for df in preload_data]
            kwargs['by_position'] = xml.find(".//Properties//Configuration//JoinByRecPos").get("value")=="True"
            kwargs['inner'] = xml.find(".//Properties//Configuration//OutputJoinOnly").get("value")=="True"

            join_infos = xml.find(".//Configuration//JoinFields")
            kwargs['fields'] = []
            if not kwargs['by_position']:
                kwargs['prefixes'] = [j.get("connection") for j in join_infos]
                for join_info in join_infos:
                    prefix = ''
                    if re.match(rf'#\d$',join_info.get("connection")):
                        prefix = f'Input_{join_info.get("connection")}_'
                    else:
                        prefix = f'{join_info.get("connection")}_'
                    kwargs['fields'].append([f'{prefix}{f.get("field")}' for f in join_info])
            self.config.load(kwargs)
        if execute:
            self.xml = tool.xml;
            dfs = tool.get_named_inputs("Input")
            next_df = self.execute(dfs)
            tool.data["Output"] = next_df


    def join_by_pos(self,dfs):
        c = self.config;

        merged_dfs = pd.concat(dfs, axis=1)

        if c.inner:
            length = min([len(df) for df in dfs])
            merged_dfs = merged_dfs.head(length)

        return merged_dfs

    def join_by_key(self,dfs):
        c = self.config;
        with pd.option_context('display.max_rows', None, 'display.max_columns', None):  # more options can be specified also
            merged_dfs = dfs.pop(0);

            for i, next_df in enumerate(dfs):
                merged_dfs = pd.merge(
                    merged_dfs,
                    next_df,
                    left_on=c.fields[i],
                    right_on=c.fields[i+1],
                    how="inner" if c.inner else "outer",
                    sort=True
                )
        return merged_dfs

    def execute(self,input_datasources):
        c = self.config;
        dfs = None;

        if self.xml:
            self.load_yxdb_tool(self.xml,execute=False,preload_data=input_datasources)
            dfs = {df["name"]:df["data"].copy() for df in input_datasources}

            dfs = [dfs[n] for n in c.prefixes]
            #SELECT TOOL CONFIG IS PREFACED WITH NAME
            for i,df in enumerate(dfs):
                prefix = f'Input_{c.prefixes[i]}_' if re.match('^#\d$',c.prefixes[i]) else f'{c.prefixes[i]}_'
                df.columns = [f"{prefix}{col}" for col in df.columns]

        else:
            dfs = [df.copy() for df in input_datasources]

        new_df = None;
        if c.by_position:
            new_df = self.join_by_pos(dfs)
        else:
            new_df = self.join_by_key(dfs)

        if self.xml:
            new_df = Select(xml = self.xml.find(".//SelectConfiguration")).execute(new_df)

            rename_back = {} # IF THE COLUMN WASN't RENAMED AND DOESN'T NEED TO BE CHANGE IT BACK

            actual_renames = []

            for f in self.xml.find(".//SelectConfiguration//Configuration//SelectFields"):
                if f.get("rename") is not None:
                    actual_renames.append(f.get("rename"))

            for col in new_df.columns:
                if col in actual_renames:
                    continue
                else:
                    prefixes = [f'Input_{n}_' if re.match('^#\d$',n) else f'{n}_' for n in c.prefixes]
                    prefixes_or = '|'.join(prefixes)
                    pattern = f'({prefixes_or})(.*)'
                    match = re.match(pattern,col)
                    if match:
                        if match.group(2) not in rename_back.values():
                            rename_back[col] = match.group(2)
            new_df = new_df.rename(columns = rename_back)
        return new_df
