import os

from api.helpers.config_generator import EnvInstaller

# Parse a .env file and then load all the variables found as environment variables.
EnvInstaller()

PORT = os.environ.get('PORT')

TARGET = os.environ.get('TARGET')
VERSION_APP = os.environ.get('VERSION_APP')


# MONGO
MONGO_HOST = os.environ.get('MONGO_HOST')
MONGO_PORT = os.environ.get('MONGO_PORT')
MONGO_USER = os.environ.get('MONGO_USER')
MONGO_PASSWORD = os.environ.get('MONGO_PASSWORD')
MONGO_DB = os.environ.get('MONGO_DB')
MONGO_AUTH_SOURCE = os.environ.get('MONGO_AUTH_SOURCE')
MONGO_AUTH_MECHANISM = os.environ.get('MONGO_AUTH_MECHANISM')


def get_url():
    result = f"mongodb://{MONGO_USER}:{MONGO_PASSWORD}@{MONGO_HOST}:{MONGO_PORT}/{MONGO_DB}" \
             f"?authSource={MONGO_AUTH_SOURCE}&authMechanism={MONGO_AUTH_MECHANISM}"
    if TARGET == 'dev':
        result = f'mongodb://{MONGO_HOST}:{MONGO_PORT}'
    return result


MONGO_URL = get_url()

# CLICKHOUSE
CLICKHOUSE_HOST = os.environ.get('CLICKHOUSE_HOST')
CLICKHOUSE_PORT = os.environ.get('CLICKHOUSE_PORT')
CLICKHOUSE_USER = os.environ.get('CLICKHOUSE_USER')
CLICKHOUSE_PASSWORD = os.environ.get('CLICKHOUSE_PASSWORD')
CLICKHOUSE_PROTOCOL = os.environ.get('CLICKHOUSE_PROTOCOL')

def get_clickhouse_url():
    return f'clickhouse+http://{CLICKHOUSE_USER}:{CLICKHOUSE_PASSWORD}@{CLICKHOUSE_HOST}:{CLICKHOUSE_PORT}'


class REDIS_PARAMS:
    """ Redis params """
    REDIS_HOST = os.environ.get('REDIS_HOST')
    REDIS_PORT = os.environ.get('REDIS_PORT')


class REDIS_CACHE_EX:
    """ Redis cach time live (sec) """
    group_risk_statistic_full = os.environ.get('cache_ex_group_risk_statistic_full')
    default = os.environ.get('cache_ex_default')
    one_day: int = 86400
    one_hour = 3600


class MONGO_COLLECTIONS:
    CREWS_NSI_MULTES = 'nsi_multes'
    NSI_ROADS = 'nsi_roads'
    NSI_DEPOS = 'nsi_depos'
    NSI_CREWS = 'nsi_crews'
    CREWS_NSI_COLUMNS = 'nsi_columns'
    CREWS_DATAS = "crews_datas"
    CREWS_TRIPS = "crews_trips"
    CREWS_PREDICT_DYNAMICS = "crews_predicts_dynmcs"
    CREWS_PREDICT_VIOLS = "crews_predicts_stats"
    CREWS_GROUP_RISK = 'crews_risk_groups'
    CREWS_GROUP_RISK_REPORT = 'crews_risk_groups_report'
    CREWS_GROUP_RISK_JY_STRUCTURE = 'group_risk_journal_structure'
    CREWS_GROUP_RISK_TYPES = 'group_risk_type'
    CREWS_GROUP_RISK_NAMES = 'group_risk_names'
    CREWS_GROUP_RISK_SOURCE = 'group_risk_source'
    PREDICTS_AGGRS = 'crews_predicts_aggrs'
    PREDICTS_DYNMCS = 'crews_predicts_dynmcs'
    CREWS_MERY = 'crews_datas'
    ANALYTICS = 'crews_datas'


class MONGO_KEYS:
    class GROUP_RISK:
        class JOURNAL:
            ROAD_ID = "ROAD_ID"
            DEPO_ID = "DEPO_ID"
            COL_ID = "COL_ID"
            COL_NUM = "COL_CODE"
            TAB_NUM8 = "TAB_NUM8"
            FIO = "FIO"
            PROF_NAME = "PROF_NAME"
            GROUP_DATE_IN = "GROUP_DATE_IN"
            GROUP_DATE_OUT = "GROUP_DATE_OUT"
            GROUP_TYPE_ID = "GROUP_TYPE"
            GROUP_NAME_ID = "GROUP_NAME"
            SOURCE_SYSTEM_ID = "SOURCE_SYSTEM"
            STATUS = "STATUS"
            EVENTS = "EVENTS"
            COUNT_EVENTS = "COUNT_EVENTS"
            REASON = "REASON"
            DELETION_REASON = "DELETION_REASON"
            PREDICT = "PREDICT"
            TERM = "TERM"
            DATE = "DATE"
            LIABLE_DATE = "LIABLE_DATE"
            UP_MARKER = "UP_MARKER"
            COUNT_DAYS = "COUNT_DAYS"
            ID_KEY = "ID_KEY"


