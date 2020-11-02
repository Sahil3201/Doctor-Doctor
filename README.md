# Doctor-Doctor
A portal for doctor and patient


# Dependencies
Django 3.0.8
Python 3.7.7

Notes:
table CustomUser
    - name
    - dob
    - address
    - gender
    - date of joining
    - email

table Patient
    - phone
    - blood group
    - allergies
    - marital status - single, married, divorsed, windowed

    - Patient history
    - List of medication you are currently taking 
    - occupation
    - Patient social history[alcohol/drugs/tobacco]

    past medical history
    - [dropdown]


    emergency contact
    - name
    - contact number
    - relationship

    insurance
    - id
    - company name
    - validity


table Doctor Record
    - speciality/degree
    - college
    - experience

table prescription
    - date
    - all meds
    - patient   <foreign key>
    - doc       <foreign key>

table appointment
    - doc
    - patient
    - rest of appointment details

features:
    - appointments
    - doc profile public
    - patient profile visible only to doc
    ML models
        - xray chest corona check
