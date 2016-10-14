"""Test Facial Recognition."""


def setup_test_recognizer():
    import cv2
    dummy_recognizer = cv2.face.createLBPHFaceRecognizer
    return dummy_recognizer()


def test_train_recognizer():
    recognizer = setup_test_recognizer()



def test_test_individual():
    pass
