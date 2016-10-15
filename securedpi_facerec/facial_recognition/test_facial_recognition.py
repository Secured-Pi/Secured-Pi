"""Test Facial Recognition."""

import os


def test_train_recognizer():
    """Assert that the recognizer runs and creates the yml file."""
    from facial_recognition import train_recognizer
    if os.path.isfile('test_brain.yml'):
        os.remove('test_brain.yml')
    train_recognizer(img_path='training', save_file='test_brain.yml')
    assert os.path.isfile('test_brain.yml')


def test_test_individual():
    """Assert that the test is performed and returns an expected result."""
    from facial_recognition import test_individual, train_recognizer
    train_recognizer(img_path='training', save_file='test_brain.yml')
    x = test_individual('test_training/member-1-testing')
    assert x[1] == 0.0
    assert x[0] == 1
