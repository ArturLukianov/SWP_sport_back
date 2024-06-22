from django.db import transaction
from sport.models import Student


def update_students(student_data_list):
    updated_students = []
    with transaction.atomic():
        for student_data in student_data_list:
            student_email = student_data['email']
            try:
                student = Student.objects.get(user__email=student_email)
                del student_data['email']
            except Student.DoesNotExist:
                student = None
            if not student:
                continue
            for attr, value in student_data.items():
                setattr(student, attr, value)
            student.save()
            updated_students.append(student_email)
    return updated_students
