import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit
from ckan.lib.plugins import DefaultTranslation


class SokigoPlugin(plugins.SingletonPlugin, DefaultTranslation, toolkit.DefaultDatasetForm):
    plugins.implements(plugins.IConfigurer)
    plugins.implements(plugins.ITranslation)
    plugins.implements(plugins.IDatasetForm)

    # IConfigurer

    def update_config(self, config_):
        toolkit.add_template_directory(config_, 'templates')
        toolkit.add_public_directory(config_, 'public')
        toolkit.add_resource('fanstatic', 'sokigo')

    # IDatasetForm
    def _modify_package_schema(self, schema):
        defaults = [toolkit.get_validator('ignore_missing')]
        package_defaults = [toolkit.get_validator('ignore_missing'),
                            toolkit.get_converter('convert_to_extras')]

        mandatory_defaults = [toolkit.get_validator('not_empty'),
                            toolkit.get_converter('convert_to_extras')]

        schema.update({
            'metadata_language': package_defaults,
        })

        schema['resources'].update({
            'resource_language': defaults,
            'completeness': defaults,
            'classification': defaults,
            'update_frequency': defaults,
            'area': defaults,
            'coordinate_system': defaults,
            'scale_factor': defaults,
            'z_min': defaults,
            'z_max': defaults,
        })

        return schema

    def create_package_schema(self):
        schema = super(SokigoPlugin, self).create_package_schema()
        return self._modify_package_schema(schema)

    def update_package_schema(self):
        schema = super(SokigoPlugin, self).update_package_schema()
        return self._modify_package_schema(schema)

    def show_package_schema(self):
        schema = super(SokigoPlugin, self).show_package_schema()
        defaults = [toolkit.get_validator('ignore_missing')]
        package_defaults = [toolkit.get_converter('convert_from_extras'),
                            toolkit.get_validator('ignore_missing')]
        mandatory_defaults = [toolkit.get_validator('not_empty'),
                            toolkit.get_converter('convert_from_extras')]

        schema.update({
            'metadata_language': package_defaults,

        })

        schema['resources'].update({
            'resource_language': defaults,
            'completeness': defaults,
            'classification': defaults,
            'update_frequency': defaults,
            'area': defaults,
            'coordinate_system': defaults,
            'scale_factor': defaults,
            'z_min': defaults,
            'z_max': defaults,
        })
        return schema

    def is_fallback(self):
        return True

    def package_types(self):
        return []