"""
WSGI config for carlifornia project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "carlifornia.settings")

application = get_wsgi_application()

# ML registry
import inspect
from apps.ml.registry import MLRegistry
from apps.ml.price_prediction.random_forest import RandomForestRegressor

try:
    registry = MLRegistry() # create ML registry
    # random forest regressor
    rf = RandomForestRegressor()
    # add to ML registry
    registry.add_model(
        endpoint_name="price_prediction",
        model_object=rf,
        model_name="random forest",
        model_status="production",
        model_version="0.0.1",
        owner="Jared",
        model_description="Simple random forest with pre- and post processing",
        model_code=inspect.getsource(RandomForestRegressor)
    )

except Exception as e:
    print("Exception while loading the models to the registry,", str(e))