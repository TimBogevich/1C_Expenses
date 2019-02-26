import requests
import json
import pandas as pd
import xmltodict
from requests_ntlm import HttpNtlmAuth
from pandas.io.json import json_normalize
from datetime import datetime
from datetime import timedelta
from db_connector import *
from vars import *
from dateutil.relativedelta import relativedelta



@benchmark
def main():
    args = get_arguments()
    date_from = datetime.now() - timedelta(days=DAYS_BACKSHIFT)
    date_from = first_day_of_month(date_from)
    date_to = datetime.now()
    engine = get_connection(args.conf_file,TARGET_DB)
    credentials = get_credentials(engine)
    while date_from <= date_to:
        res = requests.post(URL, 
                            data = get_request(date_from), 
                            auth=HttpNtlmAuth(credentials["login"],credentials["password"])).content
        dict = xmltodict.parse(res)
        dict = dict["soap:Envelope"]["soap:Body"]["m:exchangeWithOLAPResponse"]["m:return"]["m:StringValue"]
        df = json_normalize(dict)
        df = df[:-1]
        df = df.rename(columns = rename_mapping)
        date = df["Period"].min()
        if is_test(engine):
            df = randomiser(df)
        print(date + " is loading to OLAP")
        engine.execute(DELETE_SCRIPT, date)
        df.to_sql(name=TARGET_TABLE,
                  con=engine,
                  if_exists="append",
                  schema=TARGET_SCHEMA,
                  index=False)
        date_from = date_from + relativedelta(months=+1)
    print("Loaded successfuly")

if __name__ == '__main__':
    main()