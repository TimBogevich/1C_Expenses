from sqlalchemy import create_engine
from sqlalchemy import sql
from sqlalchemy.orm import sessionmaker
import r_conf_file




def get_connection(confile,target_db):
    r_conf_file.r_conf_file(confile)   #Read params from file
    connection_string = "mssql+pymssql://"+ r_conf_file.mssql_srv_login +":"+ r_conf_file.mssql_srv_pwd +"@"+ r_conf_file.mssql_srv_adr +":1433/"+ target_db
    return create_engine(connection_string)

