import argparse
import numpy as np
import os
from ConfigParser import ConfigParser

ini = ConfigParser()
ini_path = os.path.join(os.path.dirname(__file__),"conf.ini")
ini.read(ini_path)

URL               = ini.get("1C","url")
TARGET_DB         = ini.get("1C","target_db")
DAYS_BACKSHIFT    = ini.getint("1C","days_backshift")
TARGET_TABLE      = ini.get("1C","target_table")
TARGET_SCHEMA     = ini.get("1C","target_schema")
DELETE_SCRIPT     = ini.get("1C","delete_script")
SELECT_CONFIG_SQL = ini.get("1C","select_config_sql")
DESCRIPTION       = ini.get("1C","description")

def get_request(date_period):
    return '<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:fxc="http://www.fxclub.com"> \
                   <soapenv:Header/> \
                   <soapenv:Body> \
                      <fxc:exchangeWithOLAP> \
                         <fxc:Period>'+ date_period.strftime("%Y-%m-%d") + '</fxc:Period> \
                      </fxc:exchangeWithOLAP> \
                   </soapenv:Body> \
                </soapenv:Envelope>'
    
rename_mapping = {"m:ExpensesItems":"ExpensesItemName", 
                  "m:FactValue":"FactValue", 
                  "m:PlanValue":"PlanValue",
                  "m:Month":"Period"}


def first_day_of_month(date):
    return date.replace(day=1)

def get_arguments():
    parser = argparse.ArgumentParser(description=DESCRIPTION)
    parser.add_argument("--cfg", dest="conf_file")
    return parser.parse_args()

def get_credentials(engine):
    login = engine.execute(SELECT_CONFIG_SQL,       "1C_USER").fetchall()[0][0]
    password = engine.execute(SELECT_CONFIG_SQL,    "1C_PASSWORD").fetchall()[0][0]
    return {"login":login,"password":password}

def is_test(engine):
    sql = ini.get("1C","sql_test")
    try:
        test = engine.execute(sql, "1C_USER").fetchall()[0][0]
    except: test = 0
    if test == 1:
        return True
    else:
        return False

def randomiser(df):
    df["FactValue"] = np.random.randint(10000000, size=len(df))
    df["PlanValue"] = np.random.randint(10000000, size=len(df))
    return df


def benchmark(func):
    """
    Logs execution time
    """
    import time
    def wrapper(*args, **kwargs):
        t = time.clock()
        res = func(*args, **kwargs)
        print("Execution time is: " + str(int(time.clock() - t)) + " s.")
        return res
    return wrapper