from rest_framework import serializers
from sport.models import Student


class StudentSerializer(serializers.ModelSerializer):
    id = serializers.CharField(source='user.id')
    name = serializers.CharField(source='full_name')
    email = serializers.EmailField(source='user.email')
    medical_group = serializers.CharField(source='medical_group.name')

    class Meta:
        model = Student
        fields = ('id', 'name', 'email', 'medical_group')


class StudentAttendanceSerializer(serializers.Serializer):
    attendance = serializers.JSONField()


class StudentUpdateSerializer(serializers.ModelSerializer):
    email = serializers.CharField()

    class Meta:
        model = Student
        fields = ['email', 'gender', 'course', 'medical_group',
                  'enrollment_year', 'telegram', 'student_status',
                  'sport', 'comment']


class BatchStudentUpdateSerializer(serializers.Serializer):
    students = StudentUpdateSerializer(many=True)
