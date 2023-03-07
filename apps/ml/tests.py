from django.test import TestCase

from apps.ml.price_prediction.random_forest import RandomForestRegressor

class MLTests(TestCase):
    def test_rf_model(self):
        input_data = {
            "longitude": -122.23,
            "latitude": 37.88,
            "housing_median_age": 41,
            "total_rooms": 880,
            "total_bedrooms": 129.0,
            "population": 322,
            "households": 126,
            "median_income": 8.3252,
            "ocean_proximity": 0
        }
        my_model = RandomForestRegressor()
        response = my_model.compute_prediction(input_data)
        self.assertEqual("OK", response["status"])
        self.assertTrue("predicted_value" in response)
        self.assertAlmostEqual(452600, response["predicted_value"], places=3)