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
    
def get_accounting_data(start_year, end_year):
    db = MySQLdb.connect(host='127.0.0.1', user='root', database='boekhouding')
    cursor = db.cursor()
    print("\n(ID, inkomsten, uitgaven, btw, inkomsten_belasting, kwartaal, inkomst_datum)")
    for year in range(int(start_year), int(end_year) + 1):
        querry = "select * from {0} order by inkomst_datum asc;".format("Y" + str(year))
        cursor.execute(querry)
        for entries in cursor:
            print(entries)

def get_personal_file(lastName):
    db = MySQLdb.connect(host='127.0.0.1', user='root', database='patientinfo')
    cursor = db.cursor()
    querry = """
        select distinct patients.patientID, patients.firstName, patients.lastName, patients.address, 
        patients.placeOfResidence, patients.dateOfBirth, patients.bsn, behandelingen.behandelDesc, 
        behandelgeschiedenis.treatmentDate, tandartsen.dentistLastName from patients inner join behandelgeschiedenis 
        on patients.patientID = behandelgeschiedenis.patientID inner join behandelingen on behandelingen.behandelID = 
        behandelgeschiedenis.behandelID inner join tandartsen on tandartsen.dentistID = behandelgeschiedenis.dentistID 
        where patients.lastName = "{0}" order by treatmentDate desc;""".format(lastName)
    cursor.execute(querry)
    print("\n(patientID, firstName, lastName, address, placeOfResidence, dateOfBirth, bsn behandelDesc, treatmentDate, dentistLastName)")
    for entries in cursor:
        print(entries)


if __name__ == "__main__":
    choice = input("Select an option:\n\n[1] Get patient history\n[2] Get accounting data\n[3] Get personal file\n\nChoice: ")
    if choice == "1":
        get_patient_history()
    elif choice == "2":
        start_year = input("First year in desired range: ")
        end_year = input("Last year in desired range: ")
        get_accounting_data(start_year, end_year)
    elif choice == "3":
        lastName = input("Enter last name: ")
        get_personal_file(lastName)