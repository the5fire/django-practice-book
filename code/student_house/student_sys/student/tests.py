# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import Client
from django.test import TestCase

from .models import Student


class StudentTestCase(TestCase):
    def setUp(self):
        Student.objects.create(
            name='test',
            sex=1,
            email='333@dd.com',
            profession='程序员',
            qq='3333',
            phone='32222',
        )

    def test_create_and_unicode(self):
        student = Student.objects.create(
            name='test',
            sex=1,
            email='333@dd.com',
            profession='程序员',
            qq='3333',
            phone='32222',
        )
        student_name = '<Student: test>'
        self.assertEqual(unicode(student), student_name, 'student __unicode__ must be {}'.format(student_name))

    def test_filter(self):
        students = Student.objects.filter(name='test')
        self.assertEqual(students.count(), 1, 'only one is right')

    def test_get_index(self):
        client = Client()
        response = client.get('/')
        self.assertEqual(response.status_code, 200, 'status code must be 200!')

    def test_post_student(self):
        client = Client()
        data = dict(
            name='test_for_post',
            sex=1,
            email='333@dd.com',
            profession='程序员',
            qq='3333',
            phone='32222',
        )
        response = client.post('/', data)
        self.assertEqual(response.status_code, 302, 'status code must be 302!')

        response = client.get('/')
        self.assertTrue(b'test_for_post' in response.content, 'response content must contain `test_for_post`')
