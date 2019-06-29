import MySQLdb

def get_patient_history():
    db = MySQLdb.connect(host='127.0.0.1', user='root', database='patientinfo')
    cursor = db.cursor()
    querry = """select distinct patients.lastName, behandelingen.behandelDesc, behandelgeschiedenis.treatmentDate, 
        tandartsen.dentistLastName from patients inner join behandelgeschiedenis on patients.patientID = 
        behandelgeschiedenis.patientID inner join behandelingen on behandelingen.behandelID = 
        behandelgeschiedenis.behandelID inner join tandartsen on tandartsen.dentistID = 
        behandelgeschiedenis.dentistID order by treatmentDate desc;"""
    cursor.execute(querry)
    for entries in cursor:
        print(entries)

if __name__ == "__main__":
    get_patient_history()