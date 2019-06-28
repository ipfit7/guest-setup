import MySQLdb

def get_patient_history():
    db = MySQLdb.connect(host='127.0.0.1', user='root', database='patientinfo')
    cursor = db.cursor()
    querry = """select patients.firstName, patients.lastName, behandelgeschiedenis.behandelID,
    behandelingen.behandelDesc, behandelgeschiedenis.treatmentDate from patients inner join 
    behandelgeschiedenis on patients.bsn = behandelgeschiedenis.patientID inner join behandelingen 
    on behandelingen.behandelID = behandelgeschiedenis.behandelID;"""
    cursor.execute(querry)
    for entries in cursor:
        print(entries)

if __name__ == "__main__":
    get_patient_history()