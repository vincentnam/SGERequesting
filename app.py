from flask import Flask, render_template, request

import pyodbc
import pandas as pd
import time
import datetime


app = Flask(__name__)


@app.route('/')
def hello_world():
    return render_template("index.html")

@app.route('/request', methods=["POST"])
def test():
    data = request.form.to_dict()
    # return data
    # return str(data.to_dict())
    start_time = time.time()
    # Cnx à la base
    date_debut = data["trip-start"]
    date_fin = data["trip-end"]
    db = pyodbc.connect(
        'driver={SQL Server};server=127.0.0.1,20001\MSSQLQERVER;DATABASE=BigData;UID=sa;PWD=neoData2.password.SGE.MsSQL;')

    # recuperer liste des colonnes adequates du fichier criteres
    file = r"C:\Users\SGE\Desktop\Integration_Conso\Extraction_CPT_clients_annee_courante\critères pour INES V4.xlsx"
    # cols = [3, 4, 5]
    # xls = pd.ExcelFile(file)

    # return date_fin,date_debut
    # df = xls.parse(skiprows=1, index_col=None, usecols=cols)
    # df['Date_début'] = pd.to_datetime(df.Date_début).dt.strftime('%Y-%m-%d')
    # df['Date_fin'] = pd.to_datetime(df.Date_fin).dt.strftime('%Y-%m-%d')
    query = f"""select TS, Jour, Time, Name, Id_CPT, Value from BigData.dbo.Table_Index_Histo where Id_CPT=? 
        and Jour >= '{date_debut}' and Jour <'{date_fin}' order by TS  """

    record = pd.read_sql(query, db, params={data[id]})

    # error = open(r"C:\Users\SGE\Desktop\Integration_Conso\Extraction_CPT_clients_annee_courante\Clients\erreur.txt",
    #              "w")
    return record
    data = pd.DataFrame([])

    for i in range(len(df)):
        print("criteres à la ligne", i)
        dt_d = df['Date_début'][i]
        dt_f = df['Date_fin'][i]

        # selectionner les donnes selon les criteres dans le fichier excel

        # si aucun enregistrement est retourné selectionner les donnes de l'année courante sinon retourne msg d'erreur dans le log
        if record.empty:
            query = f"""select TS, Jour, Time,Name, Id_CPT, Value from BigData.dbo.Table_Index_Histo  where Id_CPT=? and YEAR(TS)=YEAR(GETDATE()) order by TS  """
            record = pd.read_sql(query, db, params={df['Choix ID_CPT'][i]})
            if record.empty:
                print(str(df['Choix ID_CPT'][i]))
                error.write("Le compteur " + str(df['Choix ID_CPT'][i]) + " est introuvable dans la base histo \n")
            else:
                data = data.append(record)

        else:

            data = data.append(record)

    df_dict = {}

    for id_cdt in data['Id_CPT'].unique():
        id_df = data[data['Id_CPT'] == id_cdt]
        df_dict[id_cdt] = id_df

    def save_xlsx(df_dict, path):
        """
        Save a dictionary of dataframes to an excel file, with each dataframe as a seperate page
        """

        with pd.ExcelWriter(path) as writer:
            for key in df_dict:
                df_dict[key].to_excel(writer, key, index=False)

        writer.save()

    out = r"C:\Users\SGE\Desktop\Integration_Conso\Extraction_CPT_clients_annee_courante\Clients\extraction.xlsx"
    save_xlsx(df_dict, out)

    print("Temps d execution : %s secondes ---" % (time.time() - start_time))


if __name__ == '__main__':
    app.run()

