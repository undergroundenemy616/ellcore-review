from dotenv import load_dotenv
import os

load_dotenv()
"""
FastAPI во многом сфокусирован на работе с Pydantic, и этот фактор делает Pydantic естественным выбором 
для управления конфигурацией в проекте FastAPI. Вот несколько причин, по которым использование Pydantic 
для конфигурации может быть предпочтительнее, чем просто помещение переменных в глобальный файл:

1. Типизация и валидация данных: Pydantic обеспечивает строгую типизацию и валидацию данных. 
Это значит, что ваши конфигурационные параметры будут не только хорошо структурированы, 
но и автоматически проверяться на правильность.

2. Десериализация и сериализация: Pydantic упрощает десериализацию данных из различных форматов, 
таких как JSON, и их сериализацию обратно в эти форматы. Это упрощает работу с конфигурационными данными.

https://github.com/zhanymkanov/fastapi-best-practices#10-use-pydantics-basesettings-for-configs
"""


DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASS = os.getenv("DB_PASS")
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))
