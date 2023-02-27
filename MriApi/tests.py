from django.test import TestCase, RequestFactory, Client
from django.urls import reverse
from rest_framework.test import force_authenticate
from rest_framework import status
from .views import ProfileAPIView
from .models import User, License, Doctors, Research, Patient
from django.core.files.uploadedfile import SimpleUploadedFile
from .serializers import PatientSerializer


# Create your tests here.

class ProfileAPIViewTest(TestCase):
    def setUp(self) -> None:
        self.factory = RequestFactory()
        self.view = ProfileAPIView.as_view()
        self.user = User.objects.create(username='tester', email="test@test.com", password='testpass',
                                        linecse=License.objects.create())
        self.doctor = Doctors.objects.create(name='doc1', second_name='doc2', third_name='doc3', profession='doc4',
                                             licence=self.user.linecse)

    def test_get(self):
        request = self.factory.get("accounts/profile/")
        force_authenticate(request, user=self.user)
        response = self.view(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_put(self):
        request = self.factory.put('accounts/profile/',
                                   {"name": "John", "second_name": "doc2", "third_name": "doc3", "profession": "doc4"},
                                   content_type='application/json')
        force_authenticate(request, user=self.user)
        response = self.view(request)
        self.assertEqual(response.data,
                         {"name": "John", "second_name": "doc2", "third_name": "doc3", "profession": "doc4"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class StartAPIVIewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create(username='tester', email="test@test.com", password='testpass',
                                        linecse=License.objects.create())

    def test_post(self):
        url = reverse('start')
        data1 = {"name": "John", "second_name": "doc2", "third_name": "doc3", "pass_number": "doc4"}
        data2 = {"name": "John", "second_name": "doc2", "third_name": "doc3"}
        self.client.force_login(user=self.user)
        response1 = self.client.post(url, data=data1, content_type='application/json')
        response2 = self.client.post(url, data=data2, content_type='application/json')

        self.assertEqual(response1.data, {"id": 4, "name": "John", "second_name": "doc2", "third_name": "doc3",
                                          "pass_number": "doc4"})
        self.assertEqual(response1.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response2.status_code, status.HTTP_400_BAD_REQUEST)


class CreateArchiveAPIViewTest(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        self.user = User.objects.create(username='tester', email="test@test.com", password='testpass',
                                        linecse=License.objects.create())
        self.doctor = Doctors.objects.create(name='doc1', second_name='doc2', third_name='doc3', profession='doc4',
                                             licence=self.user.linecse)
        self.patient = Patient.objects.create(name='name1', second_name='name2', third_name='name2',
                                              pass_number='name3')
        self.research = Research.objects.create(doctor=self.doctor, patient=self.patient)

    def test_put(self):
        url = reverse('archive')
        session = self.client.session
        session['research_id'] = self.research.id
        session.save()
        self.client.force_login(user=self.user)
        response = self.client.put(url)
        print(response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(len(response.data['file']) > 0)


class CreateReportAPIViewTest(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        self.user = User.objects.create(username='tester', email="test@test.com", password='testpass',
                                        linecse=License.objects.create())
        self.doctor = Doctors.objects.create(name='doc1', second_name='doc2', third_name='doc3', profession='doc4',
                                             licence=self.user.linecse)
        self.patient = Patient.objects.create(name='name1', second_name='name2', third_name='name2',
                                              pass_number='name3')
        self.research = Research.objects.create(doctor=self.doctor, patient=self.patient)

    def test_put(self):
        url = reverse('report')
        session = self.client.session
        session['research_id'] = self.research.id
        session.save()
        self.client.force_login(user=self.user)
        response = self.client.put(url)
        print(response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(len(response.data['report']) > 0)


class ResearchAPIViewTest(TestCase):
    def setUp(self) -> None:
        self.image = SimpleUploadedFile(
            'image.jpg', content=b'filec_ontent', content_type='image/jpeg'
        )

        self.client = Client()
        self.user = User.objects.create(username='tester', email="test@test.com", password='testpass',
                                        linecse=License.objects.create())

        self.doctor = Doctors.objects.create(name='doc1', second_name='doc2', third_name='doc3', profession='doc4',
                                             licence=self.user.linecse)
        self.patient = Patient.objects.create(name='name1', second_name='name2', third_name='name2',
                                              pass_number='name3')
        self.research = Research.objects.create(doctor=self.doctor, patient=self.patient)

    def test_post(self):
        url = reverse('research')
        session = self.client.session
        session['patient'] = PatientSerializer(self.patient).data
        session.save()
        self.client.force_login(user=self.user)
        response = self.client.post(url, {'images': self.image})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
