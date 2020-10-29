# Doctor-Doctor
A portal for doctor and patient


# Dependencies
Django 3.0.8
Python 3.7.7

table Patient
    Notes:
    - Customer ka patient history
    - age
    - name
    - address
    - phone
    - gender
    - email
    - dob
    - blood group
    - allergies
    - any major illness diagnosed before
    - List of medication you are currently taking 
    - marital status - single, married, divorsed, windowed
    - date of joining
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
    - name
    - dob
    - address
    - speciality/degree
    - gender
    - college
    - experience

table prescription
    - date
    - all meds
    - patient
    - doc
