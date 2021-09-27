from dotenv import load_dotenv
import os

load_dotenv('.env')

DATABASE_CREDENTIALS = {
    'host': os.getenv('POSTGRES_HOST'),
    'port': os.getenv('POSTGRES_PORT'),
    'database': os.getenv('POSTGRES_DATABASE'),
    'user': os.getenv('POSTGRES_USER'),
    'password': os.getenv('POSRGRES_PASSWORD')
}
