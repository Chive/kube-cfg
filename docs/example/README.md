# Example

## Define your stack

See [``definition.py``](https://github.com/Chive/kubecfg/blob/master/docs/example/definition.py)

## Execute ``kubecfg``

```bash
$ python definition.py
$ ls out
example-web-controller.json  example-web-service.json
```

## View output and use with ``kubectl``

### Controller

> [``out/example-web-controller.json``](https://github.com/Chive/kubecfg/blob/master/docs/example/out/example-web-controller.json)

```bash
$ kubectl create -f out/example-web-controller.json
```

### Service

> [``out/example-web-service.json``](https://github.com/Chive/kubecfg/blob/master/docs/example/out/example-web-service.json)

```bash
$ kubectl create -f out/example-web-service.json
```
