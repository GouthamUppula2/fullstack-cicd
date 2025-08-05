from models import Patient
from app import app, db
import pytest
_


@pytest.fixture
def client():
    # Set up test config
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
            yield client
            db.session.remove()
            db.drop_all()


def test_add_patient(client):
    response = client.post('/patients/add', data={
        'name': 'John Doe',
        'age': 30,
        'gender': 'Male',
        'contact': '1234567890',
        'address': '123 Main Street'
    }, follow_redirects=True)
    assert response.status_code == 200
    assert b'John Doe' in response.data


def test_list_patients(client):
    patient = Patient(name='Jane Doe', age=25, gender='Female',
                      contact='9876543210', address='456 Elm Street')
    db.session.add(patient)
    db.session.commit()

    response = client.get('/patients')
    assert response.status_code == 200
    assert b'Jane Doe' in response.data


def test_update_patient(client):
    # Create and commit a patient
    patient = Patient(name='Old Name', age=40, gender='Other',
                      contact='1112223333', address='Old Address')
    db.session.add(patient)
    db.session.commit()

    # Update patient
    response = client.post(f'/patients/{patient.id}/update', data={
        'name': 'New Name',
        'age': 41,
        'gender': 'Other',
        'contact': '4445556666',
        'address': 'New Address'
    }, follow_redirects=True)

    assert response.status_code == 200
    assert b'New Name' in response.data


def test_delete_patient(client):
    patient = Patient(name='Delete Me', age=60, gender='Male',
                      contact='0000000000', address='To Be Deleted')
    db.session.add(patient)
    db.session.commit()

    response = client.post(
        f'/patients/{patient.id}/delete', follow_redirects=True)
    assert response.status_code == 200
    assert b'Delete Me' not in response.data
