"""
Copyright (c) 2020 Keitaro AB

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as
published by the Free Software Foundation, either version 3 of the
License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

import ckan.plugins as p
import ckan.plugins.toolkit as t
from ckan.lib.plugins import DefaultTranslation


class SokigoPlugin(p.SingletonPlugin, t.DefaultDatasetForm, DefaultTranslation):
    p.implements(p.IConfigurer)
    p.implements(p.ITranslation)
    p.implements(p.IDatasetForm)
    p.implements(p.IRoutes, inherit=True)

    # IConfigurer

    def update_config(self, config_):
        t.add_template_directory(config_, 'templates')
        t.add_public_directory(config_, 'public')
        t.add_resource('fanstatic', 'sokigo')

    # IRoutes

    def before_map(self, map):

        map.connect('copy', '/dataset/copy/{id}',
                    controller='ckanext.sokigo.controller:CopyController',
                    action='copy')
        map.connect('copy_resources', '/dataset/copy/{id}/resources',
                    controller='ckanext.sokigo.controller:CopyController',
                    action='copy_resources')

        return map

    # IDatasetForm

    def _modify_package_schema(self, schema):
        defaults = [t.get_validator('ignore_missing')]
        package_defaults = [t.get_validator('ignore_missing'),
                            t.get_converter('convert_to_extras')]

        mandatory_defaults = [t.get_validator('not_empty'),
                            t.get_converter('convert_to_extras')]

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
        defaults = [t.get_validator('ignore_missing')]
        package_defaults = [t.get_converter('convert_from_extras'),
                            t.get_validator('ignore_missing')]
        mandatory_defaults = [t.get_validator('not_empty'),
                            t.get_converter('convert_from_extras')]

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
