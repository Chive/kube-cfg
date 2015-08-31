# -*- coding: utf-8 -*-
import copy
import json
import os


class BaseStructure(object):
    apiVersion = 'v1'
    labels = {}
    kind = None

    def __init__(self, name):
        self.name = name

    def serialize(self):
        data = {
            'apiVersion': self.apiVersion,
            'kind': self.kind,
            'spec': {},
            'metadata': {
                'name': self.name,
                'labels': {
                    'name': self.name,
                }
            }
        }

        if self.labels:
            data.setdefault('metadata', {})
            data['metadata'].setdefault('labels', {})
            for key, value in self.labels.items():
                data['metadata']['labels'][key] = value

        return data


class Application(object):
    def __init__(self, name, tiers):
        self.name = name
        self.tiers = tiers

    def serialize(self):
        return {
            tier.name: tier.serialize()
            for tier in self.tiers
        }

    def write(self, target_directory):
        for tier, sections in self.serialize().items():
            for section, components in sections.items():
                for component_name, component_config in components.items():
                    fname = '-'.join((self.name, tier, section, component_name))
                    fpath = '{}/{}.json'.format(target_directory, fname)
                    if not os.path.exists(target_directory):
                        os.makedirs(target_directory)
                    with open(fpath, 'w') as f:
                        json.dump(
                            component_config, f,
                            indent=2, sort_keys=True
                        )


class Tier(object):
    def __str__(self):
        return self.name

    def __init__(self, name):
        self.name = name
        self.controllers = list()
        self.services = list()

    def serialize(self):
        return {
            'controllers': {i.name: i.serialize() for i in self.controllers},
            'services': {i.name: i.serialize() for i in self.services},
        }



class ReplicationController(BaseStructure):
    kind = 'ReplicationController'

    def __init__(self, name, replicas, containers=None, template_labels=None):
        super(ReplicationController, self).__init__(name)
        self.replicas = replicas
        self.containers = containers or []
        self.template_labels = template_labels or {}

    def serialize(self):
        data = super(ReplicationController, self).serialize()
        data['spec']['replicas'] = self.replicas
        data['spec']['template'] = {
            'metadata': {
                'name': self.name,
                'labels': {
                    key: val for key, val
                    in self.template_labels.items()
                }
            },
            'spec': {
                'containers': [i.serialize() for i in self.containers]
            }
        }
        data['spec']['template']['metadata']['labels']['component'] = self.name
        return data


class Service(BaseStructure):
    kind = 'Service'
    ports = []
    selectors = {}
    type = None

    def serialize(self):
        data = super(Service, self).serialize()
        if self.ports:
            data['spec'].setdefault('ports', [])
            for port in self.ports:
                data['spec']['ports'].append({'port': port})

        if self.selectors:
            data['spec'].setdefault('selector', {})
            for key, val in self.selectors:
                data['spec']['selector'][key] = val

        if self.type:
            data['type'] = self.type

        return data


class Container(object):
    cpu_limit = None
    memory_limit = None

    def __init__(self, name, command=None, args=None, image=None, env=None):
        self.name = name
        self.command = command
        self.args = args
        self.image = image
        self.env = env

    def serialize(self):
        data = {}
        for attr in ['name', 'command', 'args', 'image']:
            if getattr(self, attr, None):
                data[attr] = getattr(self, attr)

        if self.env:
            data['env'] = [
                {'name': key, 'value': val}
                for key, val in self.env.items()
            ]

        if self.cpu_limit or self.memory_limit:
            data.setdefault('resources', {})
            data['resources'].setdefault('limits', [])

            if self.cpu_limit:
                data['resources']['limits'].append(
                    {'cpu': self.cpu_limit}
                )

            if self.memory_limit:
                data['resources']['limits'].append(
                    {'memory': self.memory_limit}
                )

        return data

    def copy(self):
        return copy.deepcopy(self)
