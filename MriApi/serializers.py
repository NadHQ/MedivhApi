from rest_framework import serializers

from .models import Research, User, License, Doctors, Patient, Images


class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = ['id', 'name', 'second_name', 'third_name', 'pass_number']


class ResearchOnlySerializer(serializers.ModelSerializer):
    class Meta:
        model = Research
        fields = ['id', 'doctor', 'patient', 'date_research', 'file', 'report']


class ResearchSerializer(serializers.ModelSerializer):
    patient = PatientSerializer()

    class Meta:
        model = Research
        fields = ['id', 'doctor', 'patient', 'date_research', 'file', 'report']


class LicenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = License
        fields = ['number']


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['linecse']


class DoctorsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Doctors
        fields = ['name', 'second_name', 'third_name', 'profession']


class ImagesSerializers(serializers.ModelSerializer):
    class Meta:
        model = Images
        fields = ['image', 'masked']
