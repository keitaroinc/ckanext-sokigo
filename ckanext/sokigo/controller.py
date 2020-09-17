import ckan.lib.helpers as h
import ckan.plugins as p
import ckan.model as m
import ckan.plugins.toolkit as t
import ckan.logic as l

import ckan.lib.navl.dictization_functions as dict_fns
from ckan.common import c
from ckan.controllers.package import PackageController
from ckan.controllers.home import CACHE_PARAMETERS

tuplize_dict = l.tuplize_dict
clean_dict = l.clean_dict
parse_params = l.parse_params
flatten_to_string_key = l.flatten_to_string_key


class CopyController(PackageController):

    def copy(self, id):
        context = {
            'model': m,
            'session': m.Session,
            'user': p.toolkit.c.user or p.toolkit.c.author,
            'auth_user_obj': p.toolkit.c.userobj,
            'save': 'save' in t.request.params,
        }

        # check permissions
        try:
            t.check_access('package_create', context)
        except t.NotAuthorized:
            t.abort(401, t._('Unauthorized to copy this package'))

        data_dict = {'id': id}
        data = t.get_action('package_show')(None, data_dict)

        # change dataset title and name
        data['name'] = '{}-copy'.format(data['name'])
        while True:
            try:
                _ = t.get_action('package_show')(None, {'name_or_id': data['name']})
            except l.NotFound:
                break
            else:
                import random
                data['name'] = '{}-copy-{}'.format(data['name'], random.randint(1, 100))

        data['title'] = 'Copy of {0}'.format(data['title'])

        # remove unnecessary attributes from the dataset
        remove_atts = ['id', 'revision_id', 'metadata_created', 'metadata_modified',
                       'resources', 'revision_timestamp']
        for attr in remove_atts:
            if attr in data:
                del data[attr]

        if data and 'type' in data:
            package_type = data['type']
        else:
            package_type = self._guess_package_type(True)

        data = data or clean_dict(dict_fns.unflatten(tuplize_dict(parse_params(
            t.request.params, ignore_keys=CACHE_PARAMETERS))))
        c.resources_json = h.json.dumps(data.get('resources', []))

        # convert tags if not supplied in data
        if data and not data.get('tag_string'):
            data['tag_string'] = ', '.join(
                h.dict_list_reduce(data.get('tags', {}), 'name'))

        # if we are creating from a group then this allows the group to be
        # set automatically
        data['group_id'] = t.request.params.get('group') or \
                           t.request.params.get('groups__0__id')

        # in the phased add dataset we need to know that
        # we have already completed stage 1
        stage = ['active']
        if data.get('state', '').startswith('draft'):
            stage = ['active', 'complete']

        form_snippet = self._package_form(package_type=package_type)
        form_vars = {'data': data, 'errors': {},
                     'error_summary': {},
                     'action': 'new', 'stage': stage,
                     'dataset_type': package_type, }

        c.errors_json = h.json.dumps({})

        # override form action to use built-in package controller
        c.form_action = t.url_for(controller='package', action='new')

        self._setup_template_variables(context, {}, package_type=package_type)
        new_template = self._new_template(package_type)
        extra_vars = {'form_vars': form_vars,
                      'form_snippet': form_snippet,
                      'dataset_type': package_type}

        return t.render(new_template, extra_vars=extra_vars)
