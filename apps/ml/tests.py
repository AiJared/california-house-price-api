from django.test import TestCase
import inspect

from apps.ml.registry import MLRegistry
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
        self.assertAlmostEqual(358500, response["predicted_value"], places=3)

    def test_registry(self):
        registry = MLRegistry()
        self.assertEqual(len(registry.endpoints), 0)
        endpoint_name = "price_prediction"
        model_object = RandomForestRegressor()
        model_name = "random forest"
        model_status = "production"
        model_version = "0.0.1"
        model_owner = "Jared"
        model_description = "Random Forest with simple pre- and post processing"
        model_code = inspect.getsource(RandomForestRegressor)
        # add to registry
        registry.add_model(endpoint_name, model_object, model_name, model_status,
                           model_version, model_owner, model_description, model_code)
        # there should be one endpoint available
        self.assertEqual(len(registry.endpoints), 1)