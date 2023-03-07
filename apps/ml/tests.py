from django.test import TestCase

from apps.ml.price_prediction.random_forest import RandomForestRegressor

class MLTests(TestCase):
    def test_rf_model(self):
        input_data = {
            
        }