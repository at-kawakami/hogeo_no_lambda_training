import boto3
import json
import pymysql
import rds_config as rds

def lambda_handler(event, context):

    # confirm RDS connection
    rds_host  = rds.db_host
    name = rds.db_username
    password = rds.db_password
    db_name = rds.db_name
    
    conn = pymysql.connect(rds_host, user=name, passwd=password, connect_timeout=5)
    with conn.cursor() as cursor:
        cursor.execute("show databases")
        results = cursor.fetchall()
    
    return {
        'statusCode': 200,
        'body': json.dumps(results)
    }

