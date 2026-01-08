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
    connection_string = (f"mssql+pymssql://{username}:{encoded_password}@{server}/{database}"
                         f"?charset=utf8")

    today = datetime.date.today()
    olddatetime=today - datetime.timedelta(days=7)
    today_str = today.strftime('%Y-%m-%d')
    olddatetime_str = olddatetime.strftime('%Y-%m-%d')

    engine = create_engine(connection_string)
    data=[]

    try:
        with engine.connect() as conn:
            result = conn.execute(text("SELECT * FROM DISEASES WHERE Date = :date1 OR Date = :date2"), {'date1': today_str,'date2': olddatetime_str})
            for row in result:
                date= row._mapping['Date']
                cameraid= row._mapping['CameraID']
                disease1= row._mapping['DISEASE1']
                disease2= row._mapping['DISEASE2']
                disease3= row._mapping['DISEASE3']
                print(f"Date: {date}, CameraID: {cameraid} Disease1: {disease1}, Disease2: {disease2}, Disease3: {disease3}")
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
                data.append({
                    "Date":str(date),
                    "CameraID": cameraid,
                    "Disease1": disease1,
                    "Disease2": disease2,
                    "Disease3": disease3,
                    "DiseaseLevel": diseaselevel
                })
         
        response_data = {
            "data": data
            }
        return func.HttpResponse(json.dumps(response_data), mimetype="application/json")
    
    except Exception as e:
        logging.error(f"Error fetching data: {e}")
        return func.HttpResponse(f"Error: {str(e)}", status_code=500)

