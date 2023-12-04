import importlib
import os
from typing import Any

from aws_lambda_powertools.utilities.typing import LambdaContext

from topless.actions.dispatcher import Dispatcher
from topless.app import Topless
from topless.models import BaseModel
from topless.models.orm.mapper import generate_orm_mapping


class Bootstrap:
    def __init__(self, app: Topless, app_path=None):
        self.app = app
        self.app_path = app_path

        self.boot()

    def boot(self):
        for service in self.app.services:
            directory = os.path.join(self.app_path, service)

            for root, _, files in os.walk(directory):
                for file in files:
                    if file.endswith(".py") and not file.startswith("__"):
                        module_path = os.path.join(root, file)
                        path_name = module_path.replace(directory, service)
                        module_name = path_name.replace(os.sep, ".")[0:-3]

                        importlib.import_module(module_name)

        self.map_models()

    def map_models(self):
        for model in BaseModel._registry:
            model.orm_mapper = generate_orm_mapping(self.app.get_mapper(), model)

    def handle(self, event, context: LambdaContext):
        return Dispatcher(self.app, event, context).run()
