from dotenv import load_dotenv
from datetime import timedelta
import os

load_dotenv()

print('Loading.....')
class Config:
        #### General Configuration
        ENABLE_CORS=os.getenv('ENABLE_CORS')
        SWAGGER_UI_DOC_EXPANSION = 'list'
        SECRET_KEY=os.getenv('SECRET_KEY')

        #### Neo4j Configuration
        NEO4J_URI=os.getenv('NEO4J_URI')
        NEO4J_USERNAME=os.getenv('NEO4J_USERNAME')
        NEO4J_PASSWORD=os.getenv('NEO4J_PASSWORD')
        NEO4J_DATABASE=os.getenv('NEO4J_DATABASE')

        #### JWT Configuration
        JWT_SECRET_KEY=os.getenv('SECRET_KEY')
        JWT_ACCESS_TOKEN_EXPIRES=timedelta(minutes=int(os.getenv('JWT_EXP_MINS')))
