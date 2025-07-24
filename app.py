

from flask import Flask, render_template, redirect, url_for, request
from models import db, Patient, Doctor, Appointment, Billing
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///hospital_db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

with app.app_context():
    db.create_all()


@app.route('/')
def home():
    return render_template('home.html')

# --------PATIENTS ROUTES-----------


@app.route('/patients')
def list_patients():
    patients = Patient.query.all()
    return render_template('Patient/patients.html', patients=patients)


@app.route('/patients/add', methods=['POST', 'GET'])
def add_patient():
    if request.method == 'POST':
        name = request.form['name']
        age = request.form['age']
        gender = request.form['gender']
        contact = request.form['contact']
        address = request.form['address']
        patient = Patient(name=name, age=age, gender=gender,
                          contact=contact, address=address)
        db.session.add(patient)
        db.session.commit()
        return redirect(url_for('list_patients'))
    return render_template('Patient/add_patient.html')


@app.route('/patient/update/<int:id>', methods=['GET', 'POST'])
def update_patient(id):
    patient = Patient.query.get_or_404(id)
    if request.method == 'POST':
        patient.name = request.form['name']
        patient.age = request.form['age']
        patient.contact = request.form['contact']
        patient.address = request.form['address']
        db.session.commit()
        return redirect(url_for('list_patients'))
    return render_template('Patient/update_patient.html', patient=patient)


@app.route('/patient/delete/<int:id>')
def delete_patient(id):
    patient = Patient.query.get_or_404(id)
    db.session.delete(patient)
    db.session.commit()
    return redirect(url_for('list_patients'))

# ------------DOCTORS ROUTES-------------


@app.route('/doctors')
def list_doctors():
    doctors = Doctor.query.all()
    return render_template('Doctor/doctors.html', doctors=doctors)


@app.route('/doctor/add', methods=['GET', 'POST'])
def add_doctor():
    if request.method == 'POST':
        name = request.form['name']
        specialization = request.form['specialization']
        contact = request.form['contact']
        doctor = Doctor(
            name=name, specialization=specialization, contact=contact)
        db.session.add(doctor)
        db.session.commit()
        return redirect(url_for('list_doctors'))
    return render_template('Doctor/add_doctor.html')


@app.route('/doctor/update/<int:id>', methods=['GET', 'POST'])
def update_doctor(id):
    doctors = Doctor.query.get_or_404(id)
    if request.method == 'POST':
        doctors.name = request.form['name']
        doctors.specialization = request.form['specialization']
        db.session.commit()
        return redirect(url_for('list_doctors'))
    return render_template('Doctor/update_doctor.html', doctor=doctors)


@app.route('/doctor/delete/<int:id>')
def delete_doctor(id):
    doctors = Doctor.query.get_or_404(id)
    db.session.delete(doctors)
    db.session.commit()
    return redirect(url_for('list_doctors'))


# ---------APPOINTMENTS ROUTES----------

@app.route('/appointments')
def list_appointments():
    appointments = Appointment.query.all()
    patients = Patient.query.all()
    doctors = Doctor.query.all()
    return render_template('Appointment/appointments.html', appointments=appointments,
                           patients=patients, doctors=doctors)


@app.route('/appointment/add', methods=['POST', 'GET'])
def add_appointment():
    if request.method == 'POST':
        patient_id = request.form['patient_id']
        doctor_id = request.form['doctor_id']
        appointment_date = request.form['appointment_date']
        appointment_time = request.form['appointment_time']
        new_appointment = Appointment(patient_id=patient_id, doctor_id=doctor_id,
                                      appointment_date=appointment_date, appointment_time=appointment_time)
        db.session.add(new_appointment)
        db.session.commit()
        return redirect(url_for('list_appointments'))
    return render_template('Appointment/add_appointment.html')


@app.route('/appointment/update/<int:id>', methods=['GET', 'POST'])
def update_appointment(id):
    appointment = Appointment.query.get_or_404(id)
    if request.method == 'POST':
        appointment.patient_id = request.form['patient_id']
        appointment.doctor_id = request.form['doctor_id']
        appointment.appointment_date = request.form['appointment_date']
        appointment.appointment_time = request.form['appointment_time']
        db.session.commit()
        return redirect(url_for('list_appointments'))
    return render_template('Appointment/update_appointment.html', appointment=appointment)


@app.route('/appointment/delete/<int:id>')
def delete_appointment(id):
    appointment = Appointment.query.get_or_404(id)
    db.session.delete(appointment)
    db.session.commit()
    return redirect(url_for('list_appointments'))


@app.route('/about')
def about():
    return render_template('about.html')


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
