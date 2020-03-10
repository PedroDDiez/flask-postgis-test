from ..main import app
from ..api import api


@app.route("/")
def hello():
    # This could also be returning an index.html
    return '''
    <h1>Flask and PostGis Test: </h1>
    <p>Take a look at these urls:</p> 
    <ul>
        <li>Turnover by month and gender: 
            <a href="/v0/turnover/by-month-gender?point=40.36,-3.66">/v0/turnover/by-month-gender?point=40.36,-3.66</a>
        </li>
        <li>Turnover by age and gender: 
            <a href="/v0/turnover/by-age-gender?point=40.36,-3.66">/v0/turnover/by-age-gender?point=40.36,-3.66</a>
        </li>
        <li>Total Turnover: 
            <a href="/v0/turnover/total?point=40.36,-3.66">/v0/turnover/total?point=40.36,-3.66</a>
        </li>
        <li>Map of Comunidad de Madrid: 
            <a href="/v0/map/turnover/com_madrid.geo.json">/v0/map/turnover/com_madrid.geo.json</a>
        </li>  
    </ul>
    '''
