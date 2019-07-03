import MySQLdb
import libarchive.public
import libarchive.constants
import csv
import os
import shutil
import hashlib

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
    for year in range(int(start_year), int(end_year) + 1):
        querry = "select * from {0} order by inkomst_datum asc;".format("Y" + str(year))
        cursor.execute(querry)
    with open("boekhouding.csv", "w") as f:
        writer = csv.writer(f)
        writer.writerows(cursor)
    write_hashes(hash_file("boekhouding.csv"))
    zip_files(["boekhouding.csv"], "boekhouding")

def get_personal_file(lastName):
    db = MySQLdb.connect(host='127.0.0.1', user='root', database='patientinfo')
    folder = "./dummy-data/data/patient_dossiers/"
    cursor = db.cursor()
    querry = """
        select distinct patients.patientID, patients.firstName, patients.lastName, patients.address, 
        patients.placeOfResidence, patients.dateOfBirth, patients.bsn, behandelingen.behandelDesc, 
        behandelgeschiedenis.treatmentDate, tandartsen.dentistLastName from patients inner join behandelgeschiedenis 
        on patients.patientID = behandelgeschiedenis.patientID inner join behandelingen on behandelingen.behandelID = 
        behandelgeschiedenis.behandelID inner join tandartsen on tandartsen.dentistID = behandelgeschiedenis.dentistID 
        where patients.lastName = "{0}" order by treatmentDate desc;""".format(lastName)
    cursor.execute(querry)
    entries = [n for n in cursor]
    dossier = [f for f in os.listdir(folder) if str(entries[0][0]) in f]
    shutil.copyfile("{0}/{1}".format(folder, dossier[0]), "./{0}".format(dossier[0]))
    with open("{0}".format(dossier[0].replace(".docx", ".csv")), "w") as export:
        writer = csv.writer(export)
        writer.writerows(entries)
    write_hashes(hash_file(dossier[0], lastName))
    write_hashes(hash_file(dossier[0].replace(".docx", ".csv"), lastName))
    zip_files([dossier[0].replace(".docx", ".csv"), dossier[0]], lastName)

def hash_file(file, lastname=None):
    file_hash = ""
    BUFF_SIZE = 65536
    sha1 = hashlib.sha1()
    md5 = hashlib.md5()
    with open("{0}".format(file), "rb") as f:
        while True:
            data = f.read(BUFF_SIZE)
            if not data:
                break
            sha1.update(data)
            md5.update(data)
    file_hash = "SHA1: {0}\t{1}\nMD5: {2}\t{3}\n".format(sha1.hexdigest(), file, md5.hexdigest(), file)
    return file_hash

def write_hashes(hash):
    with open("hashes.txt", "a") as f:
        f.write(hash)

def zip_files(files: [], lastname=None):
    if not lastname:
        lastname = "export"
    libarchive.public.create_file("{0}.zip".format(lastname), libarchive.constants.ARCHIVE_FORMAT_ZIP,
        files=files)
    write_hashes(hash_file("{0}.zip".format(lastname)))

def get_personel_file():
    db = MySQLdb.connect(host='127.0.0.1', user='root', database='patientinfo')
    cursor = db.cursor()
    querry = "select * from tandartsen;"
    cursor.execute(querry)
    with open("personeelsbestand.csv", "w") as f:
        writer = csv.writer(f)
        writer.writerows(cursor)
    write_hashes(hash_file("personeelsbestand.csv"))
    zip_files(["personeelsbestand.csv"])

if __name__ == "__main__":
    choice = input("Select an option:\n\n[1] Get patient history\n[2] Get accounting data\n[3] Get patient file\n[4] Get personel file\n\nChoice: ")
    if choice == "1":
        get_patient_history()
    elif choice == "2":
        start_year = input("First year in desired range: ")
        end_year = input("Last year in desired range: ")
        get_accounting_data(start_year, end_year)
    elif choice == "3":
        lastName = input("Enter last name: ")
        get_personal_file(lastName)
    elif choice == "4":
        get_personel_file()