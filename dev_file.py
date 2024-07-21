import os
import argparse
import logging
import pickle

import polars as pl
from serialization.text_based import *
from LLM_based.prompt_generation import design_prompt
from LLM_based.llama3_based import *
# from LLM_based.gpt_based import *

def main():
    gbw = pl.read_csv('/home/yaoyi/pyo00005/Entity_Matching/data/GBW_MRDS.csv', ignore_errors=True).select(
        pl.col(['OBJECTID', 'COMB_DEP_IDs']).cast(pl.Utf8)
    ).with_columns(
        pl.col('COMB_DEP_IDs').str.split('|')
    ).explode(
        'COMB_DEP_IDs'
    ).with_columns(
        pl.col('COMB_DEP_IDs').str.strip_chars()
    ).rename(
        {'COMB_DEP_IDs': 'dep_id',
        'OBJECTID': 'grouping'}
    )

    idmt = pl.read_csv('/home/yaoyi/pyo00005/Entity_Matching/data/MineralSites.csv', ignore_errors=True).select(
        pl.col(['OID_','source_ID']).cast(pl.Utf8)
    ).with_columns(
        pl.col('source_ID').str.split(';')
    ).explode(
        'source_ID'
    ).with_columns(
        pl.col('source_ID').str.strip_chars()
    ).rename(
        {'source_ID': 'dep_id'}
    ).with_columns(
        grouping = pl.lit('A') + pl.col('OID_')
    ).filter(
        pl.col('dep_id').str.contains(r'MRDS|USMIN')
    ).drop(
        'OID_'
    )

    mrds_mapping = pl.read_csv('/home/yaoyi/pyo00005/Entity_Matching/data/MRDS(1).csv', ignore_errors=True).with_columns(pl.all().cast(pl.Utf8))
    dict_mrds = dict(zip(mrds_mapping['source_ID'], mrds_mapping['dep_id']))
    usmin_mapping = pl.read_csv('/home/yaoyi/pyo00005/Entity_Matching/data/USMIN(1).csv', ignore_errors=True).with_columns(pl.all().cast(pl.Utf8))
    dict_usmin = dict(zip(usmin_mapping['source_ID'], usmin_mapping['Site_ID']))
    dict_mrds.update(dict_usmin)

    idmt = idmt.with_columns(
        pl.col('dep_id').replace(dict_mrds)
    )

    ground_truth_full = pl.concat(
        [gbw, idmt],
        how='diagonal_relaxed'
    )

    mrds_data = pl.read_csv('/home/yaoyi/pyo00005/Entity_Matching/data/mrds.csv', infer_schema_length=0).with_columns(
        pl.all().cast(pl.Utf8)
    )
    usmin_data = pl.read_csv('/home/yaoyi/pyo00005/Entity_Matching/data/USMIN.csv', ignore_errors=True).with_columns(
        pl.all().cast(pl.Utf8)
    ).drop('OBJECTID')

    merged_data = pl.concat(
        [ground_truth_full, mrds_data],
        how='align'
    )

    merged_data = pl.concat(
        [merged_data, usmin_data],
        how='align'
    ).drop_nulls('grouping').sort('grouping')
    merged_data.write_csv('./dummy.csv')

    pl_data = merged_data.drop('grouping')
    pl_data = text_serialization(pl_data, unique_id_col='dep_id', method='attribute_value_pairs')
    pl_data.write_csv('./completed.csv')

    list_strings = pl_data['serialized_string'].to_list()
    list_grouping = merged_data['grouping'].to_list()


    entity_name = 'Mine'
    prompt = design_prompt(bool_simple=False, bool_free=False, entity_object=entity_name.lower())

    # matches = match_gpt(list_strings[0], list_strings[1], prompt)
    # print(matches)
    matches, ground_truth = run_on_llama(list_strings, list_grouping, prompt)

if __name__ == "__main__":
    main()