from rest_framework_json_api.schemas.openapi import SchemaGenerator as JSONAPISchemaGenerator, AutoSchema
from apis import __title__, __version__, __author__, __copyright__


class SchemaGenerator(JSONAPISchemaGenerator):
    
    def get_schema(self, request, public):
        """
        Augments the automatically-generated `schema` with some additional
        documentation, servers.
        """
        schema = super().get_schema(request, public)
        schema['info'] = {
            'version': __version__,
            'title': __title__,
            'description':
                '![alt-text](https://cuit.columbia.edu/sites/default/files/logo/CUIT_Logo_286_web.jpg "CUIT logo")'
                '\n'
                '\n'
                '\n'
                'COVID Information Commons (CIC) API'
                '\n'
                '\n' + __copyright__ + '\n',
            'contact': {
                'name': __author__
            }
        }
        schema['servers'] = [
            {'url': 'http://127.0.0.1:8000/v1', 'description': 'local dev'},
            {'url': 'https://cice-dev.paas.cc.columbia.edu/v1', 'description': 'dev server on AWS'}
        ]
        
        return schema

        


