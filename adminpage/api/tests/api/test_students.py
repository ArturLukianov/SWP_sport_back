from datetime import date

import pytest
from django.conf import settings
from rest_framework import status
from rest_framework.test import APIClient

from sport.models import Student

frozen_time = date(2020, 1, 2)


@pytest.fixture
@pytest.mark.freeze_time(frozen_time)
def setup(
    student_factory,
    user_factory,
):
    admin_email = "user@foo.bar"
    admin_password = "pass"
    user_factory(
        email=admin_email,
        password=admin_password,
        is_staff=True,
        is_superuser=True,
    )
    client = APIClient()
    client.login(
        username=admin_email,
        password=admin_password,
    )

    student1 = student_factory(
        email="student1@foo.bar",
        password="pass",
    )
    student1.student.telegram = "@initial_tg_1"
    student1.save()

    student2 = student_factory(
        email="student2@foo.bar",
        password="pass",
    )
    student2.student.telegram = "@initial_tg_2"
    student2.save()

    return student1, student2, client


@pytest.mark.django_db
@pytest.mark.freeze_time(frozen_time)
def test_1_student_batch_update(setup):
    student1, student2, client = setup

    data = {
        'students': [
            {'email': 'student2@foo.bar', 'telegram': '@test_tg'}
        ]
    }

    response = client.put(f"/{settings.PREFIX}api/v2/students/batch-update",
                          data=data, format='json')

    assert response.status_code == status.HTTP_200_OK
    assert len(response.data['students']) == 1
    assert Student.objects.filter(telegram='@test_tg').exists()
    assert Student.objects.filter(telegram='@initial_tg_1').exists()
    assert not Student.objects.filter(telegram='@initial_tg_2').exists()


@pytest.mark.django_db
@pytest.mark.freeze_time(frozen_time)
def test_multiple_students_batch_update(setup):
    student1, student2, client = setup

    data = {
        'students': [
            {'email': 'student1@foo.bar', 'telegram': '@test_tg_1'},
            {'email': 'student2@foo.bar', 'telegram': '@test_tg_2'}
        ]
    }

    response = client.put(f"/{settings.PREFIX}api/v2/students/batch-update",
                          data=data, format='json')

    assert response.status_code == status.HTTP_200_OK
    assert len(response.data['students']) == 2
    assert Student.objects.filter(telegram='@test_tg_1').exists()
    assert Student.objects.filter(telegram='@test_tg_2').exists()
    assert not Student.objects.filter(telegram='@initial_tg_1').exists()


@pytest.mark.django_db
@pytest.mark.freeze_time(frozen_time)
def test_non_existing_students_batch_update(setup):
    _, _, client = setup

    data = {
        'students': [
            {'email': 'student11@foo.bar', 'telegram': '@test_tg_11'},
            {'email': 'student2@foo.bar', 'telegram': '@test_tg_12'}
        ]
    }

    response = client.put(f"/{settings.PREFIX}api/v2/students/batch-update",
                          data=data, format='json')

    assert response.status_code == status.HTTP_200_OK
    assert Student.objects.filter(telegram='@test_tg_12').exists()
    assert response.data['students'] == ['student2@foo.bar']
