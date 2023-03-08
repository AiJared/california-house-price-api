from django.test import TestCase

from apps.ml.price_prediction.random_forest import RandomForestRegressor

class MLTests(TestCase):
    def test_rf_model(self):
        input_data = {
            "longitude": -122.22,
            "latitude": 37.86,
            "housing_median_age": 21,
            "total_rooms": 7099,
            "total_bedrooms": 1106.0,
            "population": 2401,
            "households": 1138,
            "median_income": 8.3014,
            "ocean_proximity": 0
        }
        my_model = RandomForestRegressor()
        response = my_model.compute_prediction(input_data)
        self.assertEqual("OK", response["status"])
        self.assertTrue("predicted_value" in response)
        self.assertAlmostEqual(358500, response["predicted_value"], places=5)