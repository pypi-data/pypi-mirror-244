from .Config import Config;
import pandas as pd;

class TextInput:
    def __init__(self,yxdb_tool=None,execute=True,**kwargs):
        # LOAD DEFAULTS
        INPUT_CONSTRAINTS = []

        self.config = Config(INPUT_CONSTRAINTS);
        if yxdb_tool:
            self.load_yxdb_tool(yxdb_tool,execute=execute)
        else:
            self.config.load(kwargs)

    # def execute_TextInput(tool):
        # if tool.name[-1]=="TextInput":
        #     config = tool.xml.find("Properties").find("Configuration")
        #     fields = config.find("Fields")
        #     data = config.find("Data")
        #
        #     field_names = []
        #     column_arrays = {}
        #
        #     for field in fields:
        #         name = field.get("name");
        #         field_names.append(name);
        #         column_arrays[name] = []
        #
        #     # Populate the arrays with the data values
        #     for row in data:
        #         for i,col in enumerate(row):
        #             column_arrays[field_names[i]].append(col.text)
        #
        #     df = pd.DataFrame(column_arrays)
        #     df = handle_dtypes(df)
        #     tool.data["Output"] = df


    def load_yxdb_tool(self,tool,execute=True):
        xml = tool.xml;
        kwargs = {}


        config = tool.xml.find("Properties").find("Configuration")
        fields = config.find("Fields")
        data = config.find("Data")

        field_names = []
        column_arrays = {}

        for field in fields:
            name = field.get("name");
            field_names.append(name);
            column_arrays[name] = []

        # Populate the arrays with the data values
        for row in data:
            for i,col in enumerate(row):
                column_arrays[field_names[i]].append(col.text)

        kwargs["columns"] = column_arrays

        self.config.load(kwargs)
        tool.data["Output"] = True
        if execute:
            next_df = self.execute()
            tool.data["Output"] = next_df


    def get_yxdb_mapping(self):
        return {
            "Input":None,
            "Output":"Output"
        }

    def handle_dtypes(self,df,infer=True):
        for column in df.columns:
            is_bytes_df = df[column].apply(lambda x: isinstance(x, bytes))
            is_na = pd.isna(df[column])
            is_num_not_na = pd.to_numeric(df[column], errors='coerce').notna()
            is_numeric = (is_num_not_na | is_na).all() and (not is_na.all()) and (is_num_not_na.any())

            if is_numeric and infer:
                is_float = df[column].str.contains("\.",na=False).any()
                if not is_float:
                    df[column] = df[column].astype(pd.Int64Dtype())
                else:
                    df[column] = df[column].astype(pd.Float64Dtype())
                continue
            elif is_numeric:
                continue

            is_json = (df[column].str.startswith("{") & df[column].str.endswith("}")).all() and not is_na.all()

            if is_json:
                geometry = [shape(json.loads(x)) for x in df[column]]
                df[column] = geometry
                gdf = gpd.GeoDataFrame(df, geometry=column,crs='EPSG:4326')
                continue

            na_map = df[column].isna()
            date_map = df[column].str.match(r'\d{4}-\d{2}-\d{2}( \d{2}:\d{2}:\d{2})*')
            int_map = df[column].str.match(r'^\d+[\.]*\d+$')

            is_date = (not na_map.all()) and (na_map | date_map).all()
            is_int = (not na_map.all()) and (na_map | int_map).all()
            if is_date:
                # If all values have the 'yyyy-mm-dd' format, convert the column to datetime
                df[column] = pd.to_datetime(df[column])
                continue
            df[column] = df[column].astype(pd.StringDtype()).replace({"":pd.NA})

            # is_time = (is_na | df[column].str.match(r'\d{2}:\d{2}:\d{2}')).all() and (not is_na.all())
            # if is_time:
            #     df[column] = pd.to_datetime("1900-01-01 " +df[column])
            #     continue

        return df

    def execute(self):
        c = self.config
        print("Executing TextInput:")
        df = pd.DataFrame(c.columns)
        df = self.handle_dtypes(df)
        return df
