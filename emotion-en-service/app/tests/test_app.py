import unittest

from app.emotion import predict_emotion


class ServiceCase(unittest.TestCase):

    def test_service_short_text(self):
        result_dict = predict_emotion("This is great and I am happy")
        self.assertGreater(result_dict['joy'], 0.7)

    def test_service_long_text(self):
        result_dict = predict_emotion("Bad day. This is a long text." * 100)
        self.assertGreater(result_dict['disgust'], 0.3)

    def test_service_empty_text(self):
        result_dict = predict_emotion("")
        self.assertEqual(result_dict, {})

    def test_service_none_text(self):
        result_dict = predict_emotion(None)
        self.assertEqual(result_dict, {})


if __name__ == '__main__':
    unittest.main()
