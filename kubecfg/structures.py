# -*- coding: utf-8 -*-
import copy
import json
import os


class Stack(object):
    components = {}

    def __init__(self, name):
        self.name = name

    def create_component(self, name):
        if name in self.components.keys():
            raise Exception(
                'Component with name {} already exists'.format(name)
            )

        component = Component(stack=self.name, name=name)
        self.components[name] = component
        return component

    def save(self, target_directory):
        if not os.path.exists(target_directory):
            os.makedirs(target_directory)
        for component_name, component in self.components.items():
            for item_type, item in component.serialize():
                fname = '-'.join((self.name, component_name, item_type))
                fpath = '{}/{}.json'.format(target_directory, fname)
                with open(fpath, 'w') as fout:
                    json.dump(item, fout, indent=2, sort_keys=True)
                    fout.write('\n')



class Component(object):
    controller = None

    def __init__(self, stack, name):
        self.stack = stack
        self.name = name
        self.services = []

    def add_controller(self, replicas, containers):
        rc = ReplicationController(
            name=self.name,
            stack=self.stack,
            replicas=replicas,
            containers=containers
        )
        self.controller = rc
        return rc

    def add_service(self, ports, service_type, controller=None):
        service = Service(
            name=self.name,
            stack=self.stack,
            ports=ports,
            service_type=service_type,
            controller=controller,
        )
        self.services.append(service)
        return service

    def serialize(self):
        data = []
        if self.controller:
            data.append(('controller', self.controller.serialize()))
        data += [('service', s.serialize()) for s in self.services]
        return data


class BaseStructure(object):
    apiVersion = 'v1'
    labels = {}
    kind = None

    def __init__(self, stack, name, *args, **kwargs):
        self.stack = stack
        self.name = name

    def serialize(self):
        data = {
            'apiVersion': self.apiVersion,
            'kind': self.kind,
            'spec': {},
            'metadata': {
                'name': self.name,
                'labels': {
                    'stack': self.stack,
                    'component': self.name,
                }
            }
        }

        if self.labels:
            for key, value in self.labels.items():
                data['metadata']['labels'][key] = value
        return data


class ReplicationController(BaseStructure):
    kind = 'ReplicationController'

    def __init__(self, stack, name, replicas, containers, labels=None):
        super(ReplicationController, self).__init__(stack, name)
        self.replicas = replicas
        self.containers = {c.name: c for c in containers}
        self.labels = labels or {}

    def serialize(self):
        data = super(ReplicationController, self).serialize()
        data['spec']['replicas'] = self.replicas
        data['spec']['template'] = {
            'metadata': {
                'name': self.name,
                'labels': {
                    key: val for key, val
                    in self.labels.items()
                    }
            },
            'spec': {
                'containers': [i.serialize() for i in self.containers.values()]
            }
        }
        data['spec']['template']['metadata']['labels']['stack'] = self.stack
        data['spec']['template']['metadata']['labels']['component'] = self.name
        return data


class Service(BaseStructure):
    kind = 'Service'

    def __init__(self, stack, name, ports, service_type=None, controller=None,
                 selectors=None, *args, **kwargs):
        super(Service, self).__init__(stack, name, *args, **kwargs)
        self.ports = ports
        self.service_type = service_type
        self.controller = controller
        self.selectors = selectors

    def serialize(self):
        data = super(Service, self).serialize()
        if self.ports:
            data['spec'].setdefault('ports', [])
            for port in self.ports:
                data['spec']['ports'].append(port.serialize())

        if self.controller or self.selectors:
            data['spec'].setdefault('selector', {})

        if self.controller:
            data['spec']['selector']['stack'] = self.stack
            data['spec']['selector']['component'] = self.name

        if self.selectors:
            for key, val in self.selectors.items():
                data['spec']['selector'][key] = val

        if self.service_type:
            data['spec']['type'] = self.service_type

        return data


class Container(object):
    command = None
    args = None
    image = None
    env = None
    cpu_limit = None
    memory_limit = None

    def __init__(self, defaults=None, **kwargs):
        # TODO: env would all get overwritten
        options = defaults.copy() if defaults else {}
        options.update(**kwargs)
        for key, val in options.items():
            setattr(self, key, val)

    def serialize(self):
        data = {}
        if self.command and not isinstance(self.command, (list, tuple)):
            self.command = [self.command]

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


class Port(object):
    port = None
    target_port = None
    node_port = None
    protocol = None

    def __init__(self, port, target_port=None, node_port=None, protocol=None):
        self.port = port
        self.target_port = target_port
        self.node_port = node_port
        self.protocol = protocol

    def serialize(self):
        data = {'port': self.port}

        if self.target_port:
            data['targetPort'] = self.target_port

        if self.node_port:
            data['nodePort'] = self.node_port

        if self.protocol:
            data['protocol'] = self.protocol

        return data
