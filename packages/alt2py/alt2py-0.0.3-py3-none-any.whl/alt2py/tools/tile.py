from .Config import Config;
import pandas as pd;
import numpy as np
import math;
from .sort import Sort
from .recordid import RecordID
import re

class Tile:
    def __init__(self,yxdb_tool=None,execute=True,**kwargs):
        # LOAD DEFAULTS
        INPUT_CONSTRAINTS = [
            {
                "name":"mode",
                "required":True,
                "type":str,
                "multi_choice":["records","sum","smart","manual","unique"]

            },
            {
                "name":"field",
                "required":lambda kwargs:kwargs["mode"]!="records",
                "type":(str,list),
                "field":True
            },
            {
                "name":"num_tiles",
                "required":lambda kwargs:kwargs["mode"] in["records","sum"],
                "type":int
            },
            {
                "name":"no_split",
                "required":False,
                "type":str
            },
            {
                "name":"manual",
                "required":False,
                "type":list,
                "sub_type":int
            },
            {
                "name":"tile_name",
                "required":False,
                "type":str,
                "default":"Tile_Num"
            },
            {
                "name":"seq_name",
                "required":False,
                "type":str,
                "default":"Tile_SequenceNum"
            },
            {
                "name":"smart_name",
                "required":False,
                "type":str,
                "default":"SmartTile_Name"
            },
        ]
        self.config = Config(INPUT_CONSTRAINTS);
        if yxdb_tool:
            self.load_yxdb_tool(yxdb_tool, execute=execute)
        else:
            self.config.load(kwargs)

    def load_yxdb_tool(self,tool,execute=True):
        kwargs = {}
        xml = tool.xml;

        mode = xml.find(".//Configuration//Method").text

        if mode=="EqualRecords":
            kwargs['mode']="records"
            kwargs['num_tiles'] = int(xml.find(".//Configuration//EqualRecords//NumTiles").get("value"))
            no_split = xml.find(".//Configuration//EqualRecords//EqualRecordsGroupField")
            kwargs['no_split'] = no_split.text if no_split is not None else None;

        elif mode=="EqualSum":
            kwargs['mode']="sum"
            kwargs['num_tiles'] = int(xml.find(".//Configuration//EqualSum//NumTiles").get("value"))
            kwargs['field'] = xml.find(".//Configuration//EqualSum//SumField").text

        elif mode=="SmartTile":
            kwargs['mode']="smart"
            kwargs['field'] = xml.find(".//Configuration//SmartTile//Field").text

        elif mode=="Manual":
            kwargs['mode']="manual"
            kwargs['field'] = xml.find(".//Configuration//Manual//Field").text
            kwargs['manual'] = [float(n) if "." in n else int(n) for n in re.split(r'\n',xml.find(".//Configuration//Manual//Cutoffs").text)]

        elif mode=="UniqueValue":
            kwargs['mode']="unique"
            kwargs['field'] = [f.get("field") for f in xml.find(".//Configuration//UniqueValue//UniqueFields")]
        print(kwargs)
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
    def equal_records(self,df):
        c = self.config;

        if c.no_split is None:
            remaining = len(df)
            tile_size = len(df)/c.num_tiles

            tiles = []
            tile_seq = []
            tile_num = 0;

            while remaining>0:
                if tile_size%1>0:
                    new_value = math.ceil(tile_size)
                else:
                    new_value = int(tile_size)

                tile_num += 1;
                remaining -= new_value

                if remaining>0:
                    tile_size = remaining/(c.num_tiles-tile_num)

                tiles += [tile_num]*new_value;
                tile_seq += list(range(1,new_value+1))

            df[c.tile_name] = tiles
            df[c.seq_name] = tile_seq
            return df
        else:
            tiles = []
            tile_seq = []
            tile_num = 1;
            splittable = (df[c.no_split] == df[c.no_split].shift().reset_index(drop=True))
            splittable = splittable[~splittable.isna() & ~splittable].reset_index().drop([c.no_split],axis=1)
            diff_splittable = splittable.diff()
            diff_splittable.iloc[0] = splittable.iloc[0]
            diff_splittable.loc[str(len(diff_splittable))] = len(df) - splittable.iloc[-1]


            x = self.equal_sum(None,series=diff_splittable)

            df = pd.concat([df, x], axis=1)
            return df

    def equal_sum(self,df,series=None):
        c = self.config;

        if series is not None:
            df = series
            cumsum = series["index"].cumsum()
        else:
            cumsum = df[c.field].cumsum()

        tiles = []
        tile_seq = []
        tile_num = 1;

        bins = pd.qcut(cumsum, q=5)

        while tile_num<c.num_tiles:
            total = cumsum.iloc[-1]
            avg_sum = total/(c.num_tiles-tile_num+1)

            split_index = (cumsum > avg_sum).idxmax()

            dif1 = avg_sum - cumsum.iloc[split_index-1]
            dif2 = cumsum.iloc[split_index] - avg_sum
            split_index = split_index if dif1 > dif2 else split_index-1
            split_value = int(cumsum.iloc[split_index])

            #prep next loop
            cumsum = cumsum - split_value
            cumsum = cumsum.iloc[split_index+1:].reset_index(drop=True)

            if series is None:
                tiles += [tile_num]*(split_index+1);
                tile_seq += list(range(1,split_index+2))
            else:
                tiles += [tile_num]*split_value
                tile_seq += list(range(1,split_value+1))

            tile_num+=1

        if series is None:
            tiles += [tile_num]*len(cumsum);
            tile_seq += list(range(1,len(cumsum)+1))
        else:
            v = int(cumsum.iloc[-1])
            tiles += [tile_num]*v;
            tile_seq += list(range(1,v+1))

        if series is None:
            df[c.tile_name] = tiles
            df[c.seq_name] = tile_seq
        else:
            df = pd.DataFrame({
                c.tile_name:tiles,
                c.seq_name:tile_seq
            })

        return df

    def smart_tile(self,df):
        c = self.config;
        tile_names = {
            3:"Extremely High",
            2:"High",
            1:"Above Average",
            0:"Average",
            -1:"Below Average",
            -2:"Low",
            -3:"Extremely Low"
        }

        df = Sort(
            fields = [c.field],
            orders = [False],
            na_position="last",
            maintain_order=True
        ).execute(df)

        series = df[c.field]
        series = series[~series.isna()]
        min = series.min();

        if min >= 0:
            min = series[series>0].min()
            #ASSUMES NORMAL LOG DIST

            log_series = np.log(series.replace({0:round(series[series>0].mean())}))
            std = log_series.std()
            mean = log_series.mean()

            series = series.replace({0:min})
            series = np.log(series)
        else:
            #ASSUMES NORMAL DIST
            std = series.std()
            mean = series.mean()

        # Create tile ranges based on mean and standard deviation
        tile_ranges = {
            3: (mean + (3 - 0.5) * std, float('inf')),
            2: (mean + (2 - 0.5) * std, mean + (3 - 0.5) * std),
            1: (mean + (1 - 0.5) * std, mean + (2 - 0.5) * std),
            0: (mean - 0.5 * std, mean + 0.5 * std),
            -1: (mean - (1 + 0.5) * std, mean - (0 + 0.5) * std),
            -2: (mean - (2 + 0.5) * std, mean - (1 + 0.5) * std),
            -3: (-float('inf'), mean - (2 + 0.5) * std)
        }

        # Function to map values to tile names
        def map_to_tile_name(value):
            for i, tile_range in tile_ranges.items():
                if tile_range[0] <= value < tile_range[1]:
                    return tile_names[i]
            return None


        # Apply the mapping function to the Series
        # Create tile_key using numpy digitize
        bins = [r[0] for r in tile_ranges.values()]
        tiles = (np.digitize(series, bins=bins[::-1])-4).tolist()

        tile_seq = []

        c_digit = None;
        for digit in tiles:
            if digit==c_digit:
                i+=1
            else:
                c_digit = digit
                i=1
            tile_seq.append(i)

        # Map tile_key to tile_name using a dictionary
        tile_names = [tile_names.get(key, 'Unknown') for key in tiles]

        df[c.tile_name] = tiles +[pd.NA]*(len(df)-len(tiles)) if len(tiles)< len(df) else tiles
        df[c.seq_name] = tile_seq +[pd.NA]*(len(df)-len(tiles)) if len(tiles)< len(df) else tile_seq
        df[c.smart_name] = tile_names +[pd.NA]*(len(df)-len(tiles)) if len(tiles)< len(df) else tile_names
        return df

    def manual_tile(self,df):
        c = self.config
        # Create a new column with the bin indices
        df[c.tile_name] = (pd.cut(df[c.field], bins=[-np.inf]+c.manual+[np.inf], labels=False) + 1).astype(pd.Int64Dtype())

        # Add a running count of each bin
        df[c.seq_name] = (df.groupby(c.tile_name).cumcount() + 1).astype(pd.Int64Dtype())
        return df

    def unique_tile(self,df):
        c = self.config;
        df = Sort(
            fields = c.field,
            orders = [True]*len(c.field),
            na_position="last",
            maintain_order=True
        ).execute(df)

        # Get unique combinations of values and assign bin indices
        unique_combinations = df[c.field].drop_duplicates().reset_index(drop=True)

        combination_to_bin_mapping = {tuple(combination): idx+1 for idx, combination in enumerate(unique_combinations.values)}

        # Map combinations to their corresponding bin indices
        df[c.tile_name] = df.apply(lambda row: combination_to_bin_mapping[tuple(row[c.field])], axis=1)
        # Add a running count of each bin
        df[c.seq_name] = df.groupby(c.tile_name).cumcount() + 1

        return df

    def execute(self,input_datasource):
        c = self.config;

        new_df = input_datasource.copy();

        if c.mode == "records":
            new_df = self.equal_records(new_df)
        elif c.mode == "sum":
            new_df = self.equal_sum(new_df)
        elif c.mode == "smart":
            new_df = self.smart_tile(new_df)
        elif c.mode == "manual":
            new_df = self.manual_tile(new_df)
        elif c.mode == "unique":
            new_df = self.unique_tile(new_df)
        return new_df
