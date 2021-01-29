from flask import Flask, render_template, request, send_file
from io import BytesIO
import pyodbc
import pandas as pd
import time
import datetime

PORT = 8001

app = Flask(__name__)


@app.route('/')
def hello_world():
    return render_template("index.html")

@app.route('/request', methods=["POST"])
def test():
    data = request.form.to_dict()

    start_time = time.time()
    now = datetime.date.today().strftime('%Y-%m-%d')
    try :
        date_debut = data["trip-start"]
        date_fin = data["trip-end"]
        id_cpt =  data["id"]
    except:
        return "Il faut remplir la totalité des champs."

    db = pyodbc.connect(
        'driver={ODBC Driver 17 for SQL Server};server=127.0.0.1,20001;DATABASE=BigData;UID=sa;PWD=neoData2.password.SGE.MsSQL;')

    query = f"""select TS, Jour, Time, Name, Id_CPT, Value from BigData.dbo.Table_Index_Histo where Id_CPT=? 
        and Jour >= '{date_debut}' and Jour <'{date_fin}' order by TS  """

    record = pd.read_sql(query, db, params={id_cpt})




    #create an output stream
    output = BytesIO()
    writer = pd.ExcelWriter(output, engine='xlsxwriter')

    #taken from the original question
    record.to_excel(writer, startrow = 0, merge_cells = False, sheet_name = "Réponse de requête")
    # workbook = writer.book
    # worksheet = writer.sheets["Sheet_1"]
    # format = workbook.add_format()
    # format.set_bg_color('#eeeeee')
    # worksheet.set_column(0,9,28)

    #the writer has done its job
    writer.close()

    #go back to the beginning of the stream
    output.seek(0)

    #finally return the file
    return send_file(output, attachment_filename="Requete_BD_SGE_"+now+"_"+id_cpt+".xlsx", as_attachment=True)



if __name__ == '__main__':
    app.run(port=PORT)

