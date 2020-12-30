import base64
import psycopg2


# 解密方法
def base64decode(str):
    return base64.b64decode(str).decode()


# 加密方法
def base64encode(str):
    return base64.b64encode(str.encode("utf-8")).decode()
