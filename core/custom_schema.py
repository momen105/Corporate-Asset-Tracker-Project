from drf_spectacular.generators import SchemaGenerator
from drf_spectacular.views import SpectacularAPIView


class CustomSchema(SchemaGenerator):
    def get_schema(self, request=None, public=False):
        schema = super().get_schema(request, public)

        # Define a list of excluded paths with method mapping
        excluded_paths = {
            "/add-employee/{id}/": ["post"],
            "/create-organization/": ["put", "delete"],
            "/create-organization/{id}/": ["put", "post"],
            "/create-device/": ["put", "delete"],
            "/create-device/{id}/": ["put", "post"],
            "/delegate-device/": ["put", "delete"],
            "/delegate-device/{id}/": ["put", "post"],
            "/device-receive/{id}/": ["post"],
            "/device-return/{id}/": ["put"],
        }

        # Loop through excluded paths and methods and remove them from schema
        for path, methods in excluded_paths.items():
            if path in schema["paths"]:
                for method in methods:
                    if method in schema["paths"][path]:
                        del schema["paths"][path][method]

        return schema


class CustomSpectacularAPIView(SpectacularAPIView):
    generator_class = CustomSchema
