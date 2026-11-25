class Patient:
    def __init__(self, Patient_ID, Name, Date_of_birth):
        self.Patient_ID = Patient_ID
        self.Name = Name
        self.Date_of_birth = Date_of_birth
        self.record = MedicalRecord(Patient_ID)
        self.room = None 
        self.appointments = []
        self.Prescriptions = []
        self.bills = []
        self.lab_tests = []
        
    @property
    def patient_ID(self):
        return self.Patient_ID
    
    @property
    def name(self):
        return self.Name
    
    @property
    def date_of_birth(self):
        return self.Date_of_birth
    
    def Register(self):
        print(f'Patient {self.Name} Registered')
        
class Doctor:
    def __init__(self, Doctor_ID, Name, Specialty):
        self.Doctor_ID = Doctor_ID
        self.Name = Name
        self.Specialty = Specialty 
        self.appointments = []
        self.Prescriptions = []
        
    def Examine_The_Patient(self, patient, diagnosis):
        patient.record.add_entry(diagnosis)
        print(f'Dr. {self.Name} Examined {patient.name} with {diagnosis}')
        
    def make_prescription(self, prescription_ID, patient, medicines, instructions):
        p = Prescription (prescription_ID, self, patient, medicines, instructions)
        p.Issue()
        return p     
        
class Appointment:
    def __init__(self, Appointment_ID, Doctor, Patient, Date_time):
        self.Appointment_ID = Appointment_ID
        self.Doctor = Doctor
        self.Patient = Patient
        self.Date_time = Date_time
        self.status = "New"
        
    def schedule(self):
        self.status = 'Schedule'
        self.Doctor.appointments.append(self)
        self.Patient.appointments.append(self)
        
    def cancel(self):
        self.status = 'Cancelled'
        
class Medicine:
    def __init__(self, Medicine_ID, Name, Dosage, Stock=0):
        self.Medicine_ID = Medicine_ID
        self.Name = Name
        self.Dosage = Dosage
        self.Stock = Stock
        
    def Check_Stock(self):
        return self.Stock 
    
    def Update_Stock(self, amount):
        self.Stock += amount
        
class Prescription:
    def __init__(self, Prescription_ID, Doctor, Patient, Medicines, Instructions):
        self.Prescription_ID = Prescription_ID
        self.Doctor = Doctor
        self.Patient = Patient
        self.Medicines = Medicines
        self.Instructions = Instructions
        self.Date_Issued = None
        
    def Issue(self):
        from datetime import date
        self.Date_Issued = date.today()
        self.Doctor.Prescriptions.append(self)
        self.Patient.Prescriptions.append(self)
        
    def print_prescription(self):
        meds = ", ".join(m.Name for m in self.Medicines)
        print(f"Prescription #{self.Prescription_ID} | {self.Doctor.Name} -> "
              f"{self.Patient.Name} | {meds} | {self.Instructions}")
        
class Treatment:
    def __init__(self, treatment_ID, Description):
        self.treatment_ID = treatment_ID
        self.Description = Description
        self.status = "Not Started"
        self.Prescriptions = []
        
    def start_treatment(self):
        self.status = "In Progress"
    
    def complete_treatment(self):
        self.status = "Completed"
    
class Hospital_Room:
    def __init__(self, Room_Number, Room_type):
        self.Room_Number = Room_Number
        self.Room_type = Room_type
        self.available = True
    
    def assign_patient(self, patient):
        if not self.available:
            print("Room is Occupied.")
            return
        patient.room = self
        self.available = False
    
    def release_room(self):
        self.available = True

class MedicalRecord:
    def __init__(self, Record_ID):
        self.Record_ID = Record_ID
        self.diagnosis = ""
        self.history = []
    
    def add_entry(self, diagnosis):
        self.diagnosis = diagnosis
        self.history.append(diagnosis)
    
    def view_record(self):
        print(f"Diagnosis: {self.diagnosis} | History: {self.history}")
        
class Lab_test:
    def __init__(self, Test_ID, Test_Name):
        self.Test_ID = Test_ID
        self.Test_Name = Test_Name
        self.result = ""
    
    def record_result(self, result):
        self.result = result
    
    def get_report(self):
        return f"{self.Test_Name}: {self.result or 'pending'}"
    
class Bill:
    def __init__(self, bill_ID):
        self.bill_ID = bill_ID
        self.amount = 0.0
        self.paid = False
    
    def calculate_total(self, items):
        self.amount = sum(items)
        return self.amount
    
    def pay_bill(self):
        self.paid = True
    
if __name__ == "__main__":
    doctor = Doctor(1, "Ahmed", "Cardiology")
    from datetime import date
    patient = Patient(100, "Sara", date(1990, 5, 17))
    patient.Register()

    Appointment(1, doctor, patient, "2026-12-01 10:30").schedule()
    doctor.Examine_The_Patient(patient, "Mild hypertension")

    aspirin = Medicine(10, "Aspirin", "75mg", Stock=50)
    doctor.make_prescription(500, patient, [aspirin], "One tablet daily").print_prescription()

    Hospital_Room(204, "Private").assign_patient(patient)

    test = Lab_test(7, "Lipid Panel")
    patient.lab_tests.append(test)
    test.record_result("Normal")
    print(test.get_report())

    bill = Bill(900)
    print("Total:", bill.calculate_total([150, 75.5, 40]))
    bill.pay_bill()
    patient.record.view_record()