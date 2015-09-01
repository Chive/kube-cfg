from kubecfg.structures import Stack, Container, Port

stack = Stack(name='example')

web = stack.create_component(name='web')
web.add_controller(
    replicas=1,
    containers=[
        Container(
            name='nginx',
            image='nginx',
            ports=[8000],
        ),
        Container(
            name='redis',
            image='redis',
        ),
    ],
)

web.add_service(
    service_type='LoadBalancer',
    controller=web.controller,
    ports=[Port(port=80, target_port=8000, protocol='TCP')],
)

stack.save('out')
