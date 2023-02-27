from io import BytesIO, StringIO

from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.parsers import FileUploadParser, MultiPartParser, FormParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from django.core.files.base import ContentFile
from .models import Research, User, License, Doctors, Patient, Images
from .serializers import (ResearchSerializer, UserSerializer, DoctorsSerializer, PatientSerializer,
                          ResearchOnlySerializer, ImagesSerializers)
from django.core.files.uploadedfile import InMemoryUploadedFile


# Create your views here.
class ResearchAPIView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ResearchOnlySerializer
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, *args, **kwargs):
        licence_number, doctor = get_data_session(request)
        patient = Patient.objects.get(id=request.session['patient']['id'])
        research_obj = Research.objects.create(doctor=doctor, patient=patient)
        arr = []
        print(request.data)
        print(request.FILES.getlist('images'))
        for i in request.FILES.getlist('images'):
            arr.append(Images.objects.create(research=research_obj, image=i, masked=i))
        images_serialized = ImagesSerializers(arr, many=True)
        research_serialized = ResearchOnlySerializer(research_obj)
        request.session['research_id'] = research_serialized.data['id']
        return Response({'research': research_serialized.data, 'images': images_serialized.data})


class CreateReportAPIView(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ResearchOnlySerializer

    def put(self, request, *args, **kwargs):
        print(request.session['research_id'])
        research_object = Research.objects.get(id=request.session['research_id'])
        images_arr = Images.objects.filter(research=research_object)
        masked_arr = images_arr.values_list('masked', flat=True)
        with StringIO() as buffer:
            for i in masked_arr:
                buffer.write(i + '\n')
            research_object.report = InMemoryUploadedFile(buffer, None, 'Report.txt', 'text/plain', buffer.tell(), None)
            research_object.save()
        serialized_research = ResearchOnlySerializer(research_object)
        return Response(serialized_research.data)


class CreateArchiveAPIView(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ResearchOnlySerializer

    def put(self, request, *args, **kwargs):
        print(request.session['research_id'])
        research_object = Research.objects.get(id=request.session['research_id'])
        images_arr = Images.objects.filter(research=research_object)
        masked_arr = images_arr.values_list('masked', flat=True)
        with StringIO() as buffer:
            for i in masked_arr:
                buffer.write(i + '\n')
            research_object.file = InMemoryUploadedFile(buffer, None, 'Archive.txt', 'text/plain', buffer.tell(),
                                                        None)
            research_object.save()
        serialized_research = ResearchOnlySerializer(research_object)
        return Response(serialized_research.data)


class StartAPIView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = PatientSerializer

    def perform_create(self, serializer):
        patient = serializer.save()
        self.request.session['patient'] = serializer.data


def get_data_session(request):
    data: User
    data = request.user
    license_number = request.user.linecse.number
    doctor = Doctors.objects.get(licence=data.linecse)
    return license_number, doctor


class ProfileAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        license_number, doctor = get_data_session(request)
        research_list = Research.objects.filter(doctor=doctor)
        return Response({'licence_number': license_number,
                         'doctor': DoctorsSerializer(doctor).data,
                         'research_list': ResearchSerializer(research_list, many=True).data})

    def put(self, request):
        license_number, doctor = get_data_session(request)
        serializer = DoctorsSerializer(doctor, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
