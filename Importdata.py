#region import package
import subprocess
import sys
from datetime import datetime

def instalar(paquete):
    subprocess.check_call([sys.executable, "-m", "pip", "install", paquete])
def librerias(paquete):
    for paquete in paquete:
        try:
            __import__(paquete)
        except ImportError:
            instalar(paquete)

lib_mysql = ["mysql-connector-python"]
librerias(lib_mysql)
lib_pandas = ["pandas"]
librerias(lib_pandas)

import mysql.connector
from mysql.connector import errorcode
import pandas as pd
pd.options.display.max_columns = None

#endregion
#region conección_mysql
def conneccion_mysql():
    import tkinter as tk
    from tkinter import simpledialog, messagebox
    root = tk.Tk()
    root.withdraw()
    username = simpledialog.askstring("Input", "Ingrese su nombre de usuario de MySQL:")
    password = simpledialog.askstring("Input", "Ingrese su contraseña de MySQL:", show='*')

    try:
        cnx = mysql.connector.connect(user=username, password=password, host='localhost')
        cursor = cnx.cursor()
        cursor.execute("USE CASOS_COVID")
        messagebox.showinfo("Éxito", "Conexión exitosa a MySQL.")
        return cnx
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            messagebox.showerror("Error", "Acceso denegado. Verifica tu usuario y contraseña.")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            messagebox.showerror("Error", f"La base de datos no existe.")
        else:
            messagebox.showerror("Error", str(err))
cnx = conneccion_mysql()
#endregion
# Leer el archivo CSV
csv = pd.read_csv("Casos_positivos_de_COVID-19-Cund-Boy.csv", delimiter=';')


def insert_status(cnx, status_name):
    if pd.isna(status_name):
        return None

    cursor = cnx.cursor()
    # Check if status already exists
    query = "SELECT id_status FROM status WHERE name = %s"
    cursor.execute(query, (status_name,))
    result = cursor.fetchone()
    if result:
        return result[0]
    else:
        # Insert new status
        query = "INSERT INTO status (name) VALUES (%s)"
        cursor.execute(query, (status_name,))
        cnx.commit()
        # Retrieve the id_status of the newly inserted status
        query = "SELECT id_status FROM status WHERE name = %s"
        cursor.execute(query, (status_name,))
        result = cursor.fetchone()
        return result[0] if result else None
def insert_type_contagion(cnx, type_contagion_name):
    cursor = cnx.cursor()
    # Check if type_contagion already exists
    query = "SELECT id_type_contagion FROM type_contagion WHERE name = %s"
    cursor.execute(query, (type_contagion_name,))
    result = cursor.fetchone()
    if result:
        return result[0]
    else:
        # Insert new type_contagion
        query = "INSERT INTO type_contagion (name) VALUES (%s)"
        cursor.execute(query, (type_contagion_name,))
        cnx.commit()
        return cursor.lastrowid

def insert_gender(cnx, gender_name):
    cursor = cnx.cursor()
    # Check if gender already exists
    query = "SELECT id_gender FROM gender WHERE name = %s"
    cursor.execute(query, (gender_name,))
    result = cursor.fetchone()
    if result:
        return result[0]
    else:
        # Insert new gender
        query = "INSERT INTO gender (name) VALUES (%s)"
        cursor.execute(query, (gender_name,))
        cnx.commit()
        return cursor.lastrowid

def insert_department(cnx, department_id, department_name):
    cursor = cnx.cursor()
    query = "SELECT id_department FROM department WHERE id_department = %s"
    cursor.execute(query, (department_id,))
    result = cursor.fetchone()
    if result:
        return result[0]
    else:
        # Insert new department
        query = "INSERT INTO department (id_department, name) VALUES (%s, %s)"
        cursor.execute(query, (department_id, department_name))
        cnx.commit()
        return department_id

def insert_municipality(cnx, municipality_id, municipality_name, department_id):
    cursor = cnx.cursor()
    query = "SELECT id_municipality FROM municipality WHERE id_municipality = %s"
    cursor.execute(query, (municipality_id,))
    result = cursor.fetchone()
    if result:
        return result[0]
    else:
        # Insert new municipality
        query = "INSERT INTO municipality (id_municipality, name, id_department) VALUES (%s, %s, %s)"
        cursor.execute(query, (municipality_id, municipality_name, department_id))
        cnx.commit()
        return municipality_id
def insert_case(cnx, case_data):
    cursor = cnx.cursor()
    # Check if case already exists
    query = "SELECT id_case FROM cases WHERE id_case = %s"
    cursor.execute(query, (case_data['id_case'],))
    result = cursor.fetchone()
    if not result:
        # Insert new case
        query = """
        INSERT INTO cases (id_case, id_municipality, age, id_status, id_type_contagion, id_gender, date_symptom, date_death, date_diagnosis, date_recovery)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        case_data = {key: (None if pd.isna(value) else value) for key, value in case_data.items()}
        fechas = ['date_symptom', 'date_death', 'date_diagnosis', 'date_recovery']
        for columnas in fechas:
            if case_data[columnas] is not None:
                case_data[columnas] = datetime.strptime(case_data[columnas], '%d/%m/%Y').strftime('%Y-%m-%d')
        cursor.execute(query, (
            case_data['id_case'], case_data['id_municipality'],
            case_data['age'], case_data['id_status'], case_data['id_type_contagion'],
            case_data['id_gender'], case_data['date_symptom'],
            case_data['date_death'], case_data['date_diagnosis'], case_data['date_recovery']
        ))
        cnx.commit()

for index, row in csv.iterrows():
    status_id = insert_status(cnx, row['status'])
    type_contagion_id = insert_type_contagion(cnx, row['type_contagion'])
    gender_id = insert_gender(cnx, row['gender'])
    # Obtener id_department y name_department del CSV
    department_id = row['id_department']
    department_name = row['name_department']
    department_id = insert_department(cnx, department_id, department_name)
    municipality_id = row['id_municipality']
    municipality_name = row['name_municipality']
    id_department = row['id_department']
    municipality_id = insert_municipality(cnx, municipality_id, municipality_name, id_department)


casos= csv
cursorn = cnx.cursor()
def merge_ids (casos, tablas):
    sql_query = f"SELECT * FROM {tablas}"
    cursorn.execute(sql_query)
    results = cursorn.fetchall()
    tabla = pd.DataFrame(results, columns=[desc[0] for desc in cursorn.description])
    tabla.rename(columns={'name': tablas}, inplace=True)
    casos = pd.merge(casos, tabla, on=tablas, how='inner')
    return casos
tablas = ['gender', 'status', 'type_contagion']
for tabla in tablas:
    casos = merge_ids(casos, tabla)
for index, row in casos.iterrows():
   case_data = {
        'id_case': row['id_case'],
        'id_municipality': row['id_municipality'],
        'age': row['age'],
        'id_status': row['id_status'],
        'id_type_contagion': row['id_type_contagion'],
        'id_gender': row['id_gender'],
        'date_symptom': row['date_symptom'],
        'date_death': row['date_death'],
        'date_diagnosis': row['date_diagnosis'],
        'date_recovery': row['date_recovery']
   }
   insert_case(cnx, case_data)

cnx.close()