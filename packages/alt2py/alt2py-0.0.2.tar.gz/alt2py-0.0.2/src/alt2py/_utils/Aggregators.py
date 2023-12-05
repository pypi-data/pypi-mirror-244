import shapely
from shapely.ops import unary_union

# THIS FILE CONTAINS ALL OF THE ALTERYX AGGREGATION FUNCTIONS

class Aggregators:

    @staticmethod
    def get_by_name(name):
        names = {
            'Sum':Aggregators.sum,
            'Min':Aggregators.min,
            'Max':Aggregators.max,
            'Concat':Aggregators.concat,
            'Count':Aggregators.count,
            'First':Aggregators.first,
            'Last':Aggregators.last,
            'Longest':Aggregators.longest,
            'Shortest':Aggregators.shortest,
            'Average':Aggregators.avg,
            'Avg':Aggregators.avg,
            'Median':Aggregators.median,
            'Mode':Aggregators.mode,
            'StdDev':Aggregators.std_dev,
            'Variance':Aggregators.var,
            'SpatialObjCombine':Aggregators.spatial_combine,
            'SpatialObjConvexHull':Aggregators.convex_hull,
            'CountBlank':Aggregators.count_blanks,
            'CountNonBlank':Aggregators.count_non_blanks
        }
        if name not in names:
            return;
        return names[name]

    @staticmethod
    def get_names():
        names = {
            'Sum':Aggregators.sum,
            'Min':Aggregators.min,
            'Max':Aggregators.max,
            'Concat':Aggregators.concat,
            'Count':Aggregators.count,
            'First':Aggregators.first,
            'Last':Aggregators.last,
            'Longest':Aggregators.longest,
            'Shortest':Aggregators.shortest,
            'Average':Aggregators.avg,
            'Avg':Aggregators.avg,
            'Median':Aggregators.median,
            'Mode':Aggregators.mode,
            'StdDev':Aggregators.std_dev,
            'Variance':Aggregators.var,
            'SpatialObjCombine':Aggregators.spatial_combine,
            'SpatialObjConvexHull':Aggregators.convex_hull,
            'CountBlank':Aggregators.count_blanks,
            'CountNonBlank':Aggregators.count_non_blanks
        }
        return list(names.keys())
    @staticmethod
    def sum(x):
        return sum(x)

    @staticmethod
    def min(x):
        return x.min()

    @staticmethod
    def max(x):
        return x.max()

    @staticmethod
    def concat(x,**kwargs):
        start = kwargs["start"] if "start" in kwargs else "";
        sep = kwargs["sep"] if "sep" in kwargs else ",";
        end = kwargs["end"] if "end" in kwargs else "";
        return start + x.str.cat(sep=sep) + end

    @staticmethod
    def count(x):
        return len(x)

    @staticmethod
    def first(x):
        return x.iloc[0]

    @staticmethod
    def last(x):
        return x.iloc[-1]

    @staticmethod
    def longest(x):
        string_lengths = x.str.len()
        max_length = string_lengths.max()
        longest_strings = x[string_lengths == max_length]
        return longest_strings.iloc[0]

    @staticmethod
    def shortest(x):
        string_lengths = x.str.len()
        min_length = string_lengths.min()
        longest_strings = x[string_lengths == min_length]
        return longest_strings.iloc[0]

    @staticmethod
    def avg(x):
        return x.mean()

    @staticmethod
    def median(x):
        return x.median()

    @staticmethod
    def mode(x):
        return x.mode().iloc[0]

    @staticmethod
    def std_dev(x):
        return x.std()

    @staticmethod
    def var(x):
        return x.var()

    @staticmethod
    def spatial_combine(x):
        return unary_union(x)

    @staticmethod
    def convex_hull(x):
        return unary_union(x).convex_hull

    @staticmethod
    def count_blanks(x,xml=None):
        filtered_series = x.loc[lambda x: x.isna() | (x == '')]
        return len(filtered_series)

    @staticmethod
    def count_non_blanks(x,xml=None):
        filtered_series = x.dropna().loc[lambda a: a != '']
        return len(filtered_series)

    @staticmethod
    def count_non_null(x,xml=None):
        filtered_series = x.dropna()
        return len(filtered_series)
#
#
# aggregator_fns = {}
#
# def summary_sum(x,xml=None):
#     return sum(x)
# aggregator_fns['Sum'] = summary_sum
#
# def summary_min(x,xml=None):
#     return x.min()
# aggregator_fns['Min'] = summary_min
#
# def summary_max(x,xml=None):
#     return x.max()
# aggregator_fns['Max'] = summary_max
#
# def summary_concat(x,xml=None):
#     start = xml.find('Concat_Start').text
#     sep = xml.find('Separator').text
#     end = xml.find('Concat_End').text
#     return start + x.str.cat(sep=sep) + end
# aggregator_fns['Concat'] = summary_concat
#
# def summary_count(x,xml=None):
#     return len(x)
# aggregator_fns['Count'] = summary_count
#
# def summary_first(x,xml=None):
#     print("FIRST----")
#     print(x)
#     return x.iloc[0]
# aggregator_fns['First'] = summary_first
#
# def summary_last(x,xml=None):
#     print("LAST----")
#     print(x)
#     return x.iloc[-1]
# aggregator_fns['Last'] = summary_last
#
# def summary_longest(x,xml=None):
#     print("LONGEST----")
#     string_lengths = x.str.len()
#     max_length = string_lengths.max()
#     longest_strings = x[string_lengths == max_length]
#     print(x.dtype)
#     return longest_strings.iloc[0]
# aggregator_fns['Longest'] = summary_longest
#
# def summary_shortest(x,xml=None):
#     print("SHORTEST----")
#     string_lengths = x.str.len()
#     min_length = string_lengths.min()
#     longest_strings = x[string_lengths == min_length]
#     return longest_strings.iloc[0]
# aggregator_fns['Shortest'] = summary_shortest
#
# def summary_avg(x,xml=None):
#     print('AVERAGE')
#     print(x.mean())
#     return x.mean()
# aggregator_fns['Avg'] = summary_avg
#
# def summary_median(x,xml=None):
#     print('MEDIAN')
#     print(x.median())
#     return x.median()
# aggregator_fns['Median'] = summary_median
#
# def summary_mode(x,xml=None):
#     print('MODE')
#     print(x.mode())
#     return x.mode().iloc[0]
# aggregator_fns['Mode'] = summary_mode
#
# def summary_std(x,xml=None):
#     print("STD")
#     print(x.std())
#     return x.std()
# aggregator_fns['StdDev'] = summary_std
#
# def summary_var(x,xml=None):
#     print("VAR")
#     print(x.var())
#     return x.var()
# aggregator_fns['Variance'] = summary_var
#
# def summary_spatialCombine(x,xml=None):
#     print("SpatialObjCombine")
#     return unary_union(x)
# aggregator_fns['SpatialObjCombine'] = summary_spatialCombine
#
# def summary_convexHull(x,xml=None):
#     print("SpatialObjConvexHull")
#     return unary_union(x).convex_hull
# aggregator_fns['SpatialObjConvexHull'] = summary_convexHull
#
# def summary_countBlanks(x,xml=None):
#     print("summary_countBlanks")
#     filtered_series = x.loc[lambda x: x.isna() | (x == '')]
#     print(len(filtered_series))
#     return len(filtered_series)
# aggregator_fns['CountBlank'] = summary_countBlanks
#
# def summary_countNonBlanks(x,xml=None):
#     print("CountNonBlank")
#     filtered_series = x.dropna().loc[lambda a: a != '']
#     print(len(filtered_series))
#     return len(filtered_series)
# aggregator_fns['CountNonBlank'] = summary_countNonBlanks
