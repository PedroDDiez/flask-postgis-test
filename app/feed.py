# docker-compose exec web bash -c "python feed.py"


from sqlalchemy import *
import pandas as pd

# Set up connection with db
engine = create_engine('postgresql://docker:docker@db:5432/gis')
# Load data from csv and loads it into db
try:
    pd.read_csv('feed/postal_codes.csv').to_sql('postal_codes', con=engine)
    print('postal_codes table populated')
except:
    print('Could not populate postal_codes table')

try:
    pd.read_csv('feed/paystats.csv').to_sql('paystats', con=engine)
    print('paystats table populated')
except:
    print('Could not populate paystats table')
