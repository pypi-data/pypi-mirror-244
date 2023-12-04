import random
import sys
import json
from datetime import datetime
from time import sleep
import travel.util.validation_util as validation_util
from migration.connector.source.mysql.source import MysqlSource
from migration.connector.source.pg.source import PGSource
from concurrent.futures import ThreadPoolExecutor, CancelledError, wait, ALL_COMPLETED
from migration.connector.destination.clickzetta.destination import ClickZettaDestination
import logging
logging.basicConfig(level=logging.INFO)

global_result_map = {}

def _format_job_id():
    unique_id = str(datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f'))
    format_unique_id = unique_id.replace('-', '').replace(':', '').replace('.', '').replace(' ', '') \
                       + str(random.randint(10000, 99999))
    return format_unique_id


def write_validation_table_result(source_df_result, destination_df_result, out_path, source_table, destination_table, uid:str):
    print(f'processing {source_table} and {destination_table}')
    try:
        if source_df_result.equals(destination_df_result):
            with open(f'{out_path}/{uid}_result.txt', 'a') as f:
                f.write(
                    f'{source_table} result is equal with {destination_table} result.\n')
        else:
            with open(f'{out_path}/{uid}_result.txt', 'a') as f:
                f.write(
                    f'{source_table} result is not equal with {destination_table} result. \n')
            diff_result = source_df_result.sort_index().sort_index(axis=1).compare(destination_df_result.sort_index().sort_index(axis=1),
                                                                                   result_names=(source_table,
                                                                                                 destination_table))
            with open(f'{out_path}/{uid}_diff_result.csv', 'a') as f:
                f.write(diff_result.to_csv(index=True))
    except Exception as e:
        raise e

def check_validation(source, destination, source_table, destination_table, out_path, uid, validation_type, check_schema=0, pk_cols=None):
    source_df_result = None
    destination_df_result = None
    if check_schema:
        check_schema_result = validation_util.schema_table_validation(source, destination, source_table, destination_table)
        only_in_source_cols = check_schema_result['only_in_source_cols']
        only_in_destination_cols = check_schema_result['only_in_dest_cols']
        if len(only_in_source_cols) > 0 or len(only_in_destination_cols) > 0:
            with open(f'{out_path}/{uid}_diff_schema_result.txt', 'a') as f:
                f.write(
                    f'{source_table} has columns {only_in_source_cols} not in {destination_table}.\n')
                f.write(
                    f'{destination_table} has columns {only_in_destination_cols} not in {source_table}.\n')
    if int(validation_type) == 0:
        source_df_result, destination_df_result = validation_util.gen_basic_validation_table_result(source, destination, source_table, destination_table)
    elif int(validation_type) == 1:
        source_df_result, destination_df_result = validation_util.multidimensional_validation_table(source, destination, source_table, destination_table)
    elif int(validation_type) == 2:
        diff_result = validation_util.data_diff_table_validation(source, destination, source_table, destination_table)
        if len(diff_result) == 0:
            with open(f'{out_path}/{uid}_result.txt', 'a') as f:
                f.write(
                    f'{source_table} result is equal with {destination_table} result.\n')
        else:
            with open(f'{out_path}/{uid}_result.txt', 'a') as f:
                f.write(
                    f'{source_table} result is not equal with {destination_table} result. \n')

            with open(f'{out_path}/{uid}_diff_result.csv', 'a') as f:
                for line in diff_result:
                    f.write(line)
            return
    elif int(validation_type) == 3:
        source_df_result, destination_df_result = validation_util.count_table_validation(source, destination, source_table, destination_table)
    elif int(validation_type) == 4:
        source_count, dest_count, abs_count = validation_util.count_table_validation_without_df(source, destination, source_table, destination_table)
        assert pk_cols is not None, 'pk_cols is None'
        if abs_count > 0:
            check_timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
            result_dict = validation_util.pk_id_table_validation_with_count(source, destination, source_table, destination_table, pk_cols, abs_count)
            result_dict['source_count'] = source_count
            result_dict['dest_count'] = dest_count
            result_dict['check_timestamp'] = check_timestamp
            map_key = f'{source_table}_{destination_table}'
            if map_key not in global_result_map:
                global_result_map[map_key] = []
            global_result_map[map_key].append(result_dict)
        return
    else:
        raise Exception(f"Unsupported validation type {validation_type}")
    write_validation_table_result(source_df_result, destination_df_result, out_path, source_table, destination_table, uid)

def validate(source, destination, source_tables, destination_tables, validation_type, out_path, executor, check_schema=0):
    if len(source_tables) != len(destination_tables):
        raise Exception("Source tables and destination tables should have the same length")
    uid = _format_job_id()
    try:
        for source_table, destination_table in zip(source_tables, destination_tables):
            executor.submit(check_validation, source, destination, source_table, destination_table, out_path, uid, validation_type, check_schema)
    except Exception as e:
        raise e
def real_time_validate(source, destination, source_tables, destination_tables,
                       validation_type, out_path, executor, check_schema=0, check_times=1, wait_time_sce=1, pk_cols=None):
    if len(source_tables) != len(destination_tables):
        raise Exception("Source tables and destination tables should have the same length")
    uid = _format_job_id()
    try:
        for i in range(check_times):
            future_results = []
            for source_table, destination_table in zip(source_tables, destination_tables):
                future = executor.submit(check_validation, source, destination, source_table, destination_table, out_path, uid, validation_type, check_schema, pk_cols)
                future_results.append(future)
            wait(future_results, None, return_when=ALL_COMPLETED)
            sleep(wait_time_sce)
        with open(f'{out_path}/{uid}_real_time_result.txt', 'a') as f:
            for key, value in global_result_map.items():
                f.write(f"{key}:\n")
                only_in_source_list = []
                only_in_dest_list = []
                only_in_source_map = {}
                only_in_dest_map = {}
                for index, result_dict in enumerate(value):
                    f.write(f"check {index + 1} times, check timestamp: {result_dict['check_timestamp']}:\n")
                    f.write(f"source count: {result_dict['source_count']}\n")
                    f.write(f"dest count: {result_dict['dest_count']}\n")
                    f.write(f"only_in_source_pk_count: {result_dict['only_in_source']}\n")
                    f.write(f"only_in_dest_pk_count: {result_dict['only_in_dest']}\n")
                    f.write(f"only_in_source_pks: {result_dict['only_in_source_list']}\n")
                    only_in_source_list.extend(result_dict['only_in_source_list'])
                    f.write(f"only_in_dest_pks: {result_dict['only_in_dest_list']}\n")
                    only_in_dest_list.extend(result_dict['only_in_dest_list'])
                for item in only_in_source_list:
                    if item not in only_in_source_map:
                        only_in_source_map[item] = 1
                    else:
                        only_in_source_map[item] += 1
                for item in only_in_dest_list:
                    if item not in only_in_dest_map:
                        only_in_dest_map[item] = 1
                    else:
                        only_in_dest_map[item] += 1
                f.write("conclusion:\n")
                f.write(f"only_in_source_pks: {only_in_source_map}\n")
                f.write(f"only_in_dest_pks: {only_in_dest_map}\n")
                f.write("\n")
                global_result_map.pop(key)
    except Exception as e:
        print('real-time validation error:', e)
        raise e
def get_source_connection_params(source_engine_conf):
    host = source_engine_conf['host']
    port = source_engine_conf['port']
    username = source_engine_conf['username']
    password = source_engine_conf['password']
    db_type= source_engine_conf['db_type']
    database = source_engine_conf['database']
    return {
        'host': host,
        'port': port,
        'user': username,
        'password': password,
        'db_type': db_type,
        'database': database,
    }

def get_destination_connection_params(destination_engine_conf):
    service = destination_engine_conf['service']
    workspace = destination_engine_conf['workspace']
    instance = destination_engine_conf['instance']
    vcluster = destination_engine_conf['vcluster']
    username = destination_engine_conf['username']
    password = destination_engine_conf['password']
    schema = destination_engine_conf['schema']
    instance_id = destination_engine_conf['instanceId']

    return {
        'service': service,
        'workspace': workspace,
        'instance': instance,
        'vcluster': vcluster,
        'username': username,
        'password': password,
        'schema': schema,
        'instanceId': instance_id,
    }

def construct_source_engine(connection_dict: dict):
    db_type = connection_dict['db_type']
    if db_type == 'mysql':
        return MysqlSource(connection_dict)
    elif db_type == 'postgres':
        return PGSource(connection_dict)
    else:
        raise Exception(f"Unsupported db type {db_type}")

def construct_destination_engine(connection_dict: dict):
    return ClickZettaDestination(connection_dict)


def get_source_tables(source_tables_file):
    source_tables = []
    with open(source_tables_file, 'r') as f:
        lines = f.readlines()
        for line in lines:
            source_tables.append(line.strip())
    return source_tables

def get_destination_tables(destination_tables_file):
    destination_tables = []
    with open(destination_tables_file, 'r') as f:
        lines = f.readlines()
        for line in lines:
            destination_tables.append(line.strip())
    return destination_tables


if __name__ == '__main__':
    source_engine_conf = sys.argv[1]
    destination_engine_conf = sys.argv[2]
    source_tables_file = sys.argv[3]
    destination_tables_file = sys.argv[4]
    validation_type = sys.argv[5]
    out_path = sys.argv[6]
    concurrency = int(sys.argv[7])
    check_schema = 0
    pk_cols = None
    check_times = 1
    wait_time_sce = 1
    if len(sys.argv) == 9:
        check_schema = sys.argv[8]
    if int(validation_type) == 4:
        check_schema = sys.argv[8]
        pk_cols = sys.argv[9].strip()
        check_times = int(sys.argv[10])
        wait_time_sce = int(sys.argv[11])
    try:
        executor = ThreadPoolExecutor(max_workers=concurrency)
        source_engine_conf = json.load(open(source_engine_conf))
        source = construct_source_engine(get_source_connection_params(source_engine_conf))
        destination_engine_conf = json.load(open(destination_engine_conf))
        destination = construct_destination_engine(get_destination_connection_params(destination_engine_conf))
        source_tables = get_source_tables(source_tables_file)
        destination_tables = get_destination_tables(destination_tables_file)
        if int(validation_type) == 4:
            real_time_validate(source, destination, source_tables, destination_tables, validation_type, out_path, executor, check_schema, check_times, wait_time_sce, pk_cols)
        else:
            validate(source, destination, source_tables, destination_tables, validation_type, out_path, executor, check_schema)
        executor.shutdown(wait=True)
    except Exception as e:
        print('validation error:', e)
        raise e