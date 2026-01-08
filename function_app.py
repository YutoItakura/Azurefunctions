import azure.functions as func
from sqlalchemy import create_engine, text
import urllib.parse
import datetime
import json
import logging



app = func.FunctionApp()


@app.route(route="http_trigger", auth_level=func.AuthLevel.ANONYMOUS)
def http_trigger(req: func.HttpRequest) -> func.HttpResponse:
    encoded_password = urllib.parse.quote(password)
    connection_string = f"mssql+pymssql://{username}:{encoded_password}@{server}/{database}"

    today = datetime.date.today()
    today_str = today.strftime('%Y-%m-%d')

    engine = create_engine(connection_string)

    try:
        with engine.connect() as conn:
            result = conn.execute(text("SELECT * FROM DISEASES WHERE Date = :date"), {'date': today_str})
            for row in result:
                disease1= row._mapping['DISEASE1']
                disease2= row._mapping['DISEASE2']
                disease3= row._mapping['DISEASE3']
                print(f"Date: {today_str}, Disease1: {disease1}, Disease2: {disease2}, Disease3: {disease3}")
                numdisease=sum([disease1, disease2, disease3])
                if numdisease == 0:
                    diseaselevel=0
                elif numdisease >0 and numdisease <= 3:
                    diseaselevel=0.2
                elif numdisease > 3 and numdisease <= 6:
                    diseaselevel=0.4
                elif numdisease > 6 and numdisease <= 9:
                    diseaselevel=0.6    
                elif numdisease > 9 and numdisease <= 12:
                    diseaselevel=0.8
                elif numdisease > 12:
                    diseaselevel=1.0
        #make json response       
        response_data = {
            "tree1":diseaselevel,
            "leaves1":diseaselevel,
            "tree2":0,
            "leaves2":0,
            "tree3":0,
            "leaves3":0,
            "tree4":0,
            "leaves4":0,
            "tree5":0,
            "leaves5":0,
            "tree6":0,
            "leaves6":0,
            }
        return func.HttpResponse(json.dumps(response_data), mimetype="application/json")
    
    except Exception as e:
        logging.error(f"Error fetching data: {e}")
        return func.HttpResponse(f"Error: {str(e)}", status_code=500)

