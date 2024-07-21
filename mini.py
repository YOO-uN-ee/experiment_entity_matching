# import polars as pl

# gbw = pl.read_csv('/home/yaoyi/pyo00005/Entity_Matching/data/GBW_MRDS.csv', ignore_errors=True).select(
#     pl.col(['OBJECTID', 'COMB_DEP_IDs']).cast(pl.Utf8)
# ).with_columns(
#     pl.col('COMB_DEP_IDs').str.split('|')
# ).explode(
#     'COMB_DEP_IDs'
# ).with_columns(
#     pl.col('COMB_DEP_IDs').str.strip_chars()
# ).rename(
#     {'COMB_DEP_IDs': 'dep_id',
#      'OBJECTID': 'grouping'}
# )

# idmt = pl.read_csv('/home/yaoyi/pyo00005/Entity_Matching/data/MineralSites.csv', ignore_errors=True).select(
#     pl.col(['OID_','source_ID']).cast(pl.Utf8)
# ).with_columns(
#     pl.col('source_ID').str.split(';')
# ).explode(
#     'source_ID'
# ).with_columns(
#     pl.col('source_ID').str.strip_chars()
# ).rename(
#     {'source_ID': 'dep_id'}
# ).with_columns(
#     grouping = pl.lit('A') + pl.col('OID_')
# ).filter(
#     pl.col('dep_id').str.contains(r'MRDS|USMIN')
# ).drop(
#     'OID_'
# )

# mrds_mapping = pl.read_csv('/home/yaoyi/pyo00005/Entity_Matching/data/MRDS(1).csv', ignore_errors=True).with_columns(pl.all().cast(pl.Utf8))
# dict_mrds = dict(zip(mrds_mapping['source_ID'], mrds_mapping['dep_id']))
# usmin_mapping = pl.read_csv('/home/yaoyi/pyo00005/Entity_Matching/data/USMIN(1).csv', ignore_errors=True).with_columns(pl.all().cast(pl.Utf8))
# dict_usmin = dict(zip(usmin_mapping['source_ID'], usmin_mapping['Site_ID']))
# dict_mrds.update(dict_usmin)

# idmt = idmt.with_columns(
#     pl.col('dep_id').replace(dict_mrds)
# )

# ground_truth_full = pl.concat(
#     [gbw, idmt],
#     how='diagonal_relaxed'
# )

# # print(ground_truth_full)

# mrds_data = pl.read_csv('/home/yaoyi/pyo00005/Entity_Matching/data/mrds.csv', ignore_errors=True).with_columns(
#     pl.all().cast(pl.Utf8)
# )
# usmin_data = pl.read_csv('/home/yaoyi/pyo00005/Entity_Matching/data/USMIN.csv', ignore_errors=True).with_columns(
#     pl.all().cast(pl.Utf8)
# ).drop('OBJECTID')

# # usmin_data = pl.DataFrame()

# merged_data = pl.concat(
#     [ground_truth_full, mrds_data],
#     how='align'
# )

# merged_data = pl.concat(
#     [merged_data, usmin_data],
#     how='align'
# ).drop_nulls('grouping').sort('grouping')


# # merged_data = merged_data.filter(
# #     pl.col('grouping') == 'A626'
# # )

# # merged_data = merged_data.tail(2)

# # merged_data.write_csv('./dummy.csv')

# print(merged_data.shape[0])

# print(ord('A'))


import polars as pl
from itertools import combinations
from random import sample
from math import floor

def testing():
    pl_data = pl.read_csv('/home/yaoyi/pyo00005/Entity_Matching/dummy.csv', infer_schema_length=0)
    pl_data = pl_data[['grouping', 'dep_id']].sample(n=2093, shuffle=True) 

    list_indexes = list(range(2093))
    pl_data = pl_data.with_columns(
        index = pl.Series(list_indexes)
    ).group_by('grouping').agg([pl.all()]).with_columns(
        pl.col('index').list.sort()
    ).with_columns(
        first_item = pl.col('index').list.get(0)
    ).sort('first_item')

    list_combination = list(combinations(list_indexes, 2))

    pl_combination = pl.DataFrame(list_combination, orient='row').with_columns(
        combination_tag = pl.col('column_0').cast(pl.Utf8) + pl.lit('_') + pl.col('column_1').cast(pl.Utf8),
        link_result = pl.lit('0').cast(pl.Int64),
        visited = pl.lit('False')
    )

    list_tags = pl_combination['combination_tag'].to_list()
    list_intiation = pl_combination['link_result'].to_list()

    dict_calculations = dict(zip(list_tags, list_intiation))

    # list_pl_combination = pl_combination.partition_by(
    #     'column_0'
    # )

    run_count = 0
    starting_key = 0
    list_links = []
    list_nolinks = []

    for key, value in dict_calculations.items():
        index_0, index_1 = key.split('_')
        index_0 = int(index_0)
        index_1 = int(index_1)

        if starting_key != index_0:
            list_guaranteed_combination = list(combinations(list_links, 2))
            for i in list_guaranteed_combination:
                c = f'{str(i[0])}_{str(i[1])}'
                dict_calculations[c] = 1

            list_no_links_combination = list(product(list_links, list_nolinks))
            for i in list_no_links_combination:
                c = f'{str(i[0])}_{str(i[1])}'
                dict_calculations[c] = -1

            starting_key = index_0
            list_links = []
            list_nolinks = []

        if dict_calculations[key] == 0:
            df_test = pl_data.filter(
                pl.col('first_item') == index_0
            )

            if df_test.is_empty():
                pass
            else:
                bool_link = index_1 in df_test.item(0, 'index')
                if bool_link:
                    dict_calculations[key] = 1
                    list_links.append(index_1)
                else:
                    dict_calculations[key] = -1
                    list_links.append(index_1)

            run_count += 1

    return run_count

run1 = testing()
run2 = testing()
run3 = testing()
run4 = testing()
run5 = testing()

print((run1 + run2 + run3 + run4 + run5)/5)

# for df in list_pl_combination:
#     print(df)
