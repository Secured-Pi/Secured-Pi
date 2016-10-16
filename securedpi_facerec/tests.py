"""Test Facial Recognition."""

from django.test import TestCase
import os


class FaceRecTestCase(TestCase):
    """Create test class for Event model."""

    def setUp(self):
        self.HERE = os.path.dirname(os.path.abspath(__file__))

    # Create your tests here.
    def test_train_recognizer(self):
        """Assert that the recognizer runs and creates the yml file."""
        from securedpi_facerec.facial_recognition import facial_recognition
        if os.path.isfile('test_brain.yml'):
            os.remove('test_brain.yml')
        facial_recognition.train_recognizer(image_path=os.path.join(self.HERE, 'facial_recognition/test_training'), save_file='test_brain.yml')
        assert os.path.isfile('test_brain.yml')

    def test_test_individual(self):
        """Assert that the test is performed and returns an expected result."""
        from securedpi_facerec.facial_recognition import facial_recognition
        facial_recognition.train_recognizer(image_path=os.path.join(self.HERE, 'facial_recognition/test_training'), save_file='test_brain.yml')
        x = facial_recognition.test_individual('securedpi_facerec/facial_recognition/test_training/member-1-testing', recog_model='test_brain.yml')
        assert x[1] == 0.0
        assert x[0] == 1
