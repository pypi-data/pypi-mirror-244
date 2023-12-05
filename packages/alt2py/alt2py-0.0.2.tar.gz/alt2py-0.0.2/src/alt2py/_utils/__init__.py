import pandas as pd
import numpy as np
from .Aggregators import Aggregators
from .Functions import Functions

dtype_map = {
    "Bool":pd.BooleanDtype(),
    "Byte":np.bytes_,
    "Int16":pd.Int64Dtype(),
    "Int32":pd.Int64Dtype(),
    "Int64":pd.Int64Dtype(),
    "Int":pd.Int64Dtype(),
    "FixedDecimal":pd.Float64Dtype(),
    "Double":pd.Float64Dtype(),
    "String":pd.StringDtype(),
    "WString":pd.StringDtype(),
    "V_String":pd.StringDtype(),
    "V_WString":pd.StringDtype(),
    "Date":'datetime64[ns]',
    "Time":'datetime64[ns]',
    "DateTime":'datetime64[ns]',
    "SpatialObj":'geometry'
}
