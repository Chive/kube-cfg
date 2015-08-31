# kubecfg

> **Warning:** this is experimental / pre alpha code!

## Usage

### Define your Stack

> ``$ vi example.py``

```python
from kubecfg.structures import (
    Application, Tier, ReplicationController, Container
)

frontend = Tier('frontend')
app = Application('nginx-web', tiers=[frontend])

web_container = Container(
    name='nginx',
    image='nginx',
)

redis_container = Container(
    name='redis',
    image='redis'
)

frontend_rc = ReplicationController(
    'web-rc',
    replicas=2,
    containers=[web_container, redis_container]
)

frontend.controllers.append(frontend_rc)

app.write('out')
```

### Run it

```bash
$ python example.py
$ ls out
nginx-web-frontend-controllers-web-rc.json
```

> ``$ cat out/nginx-web-frontend-controllers-web-rc.json``

```json
{
  "apiVersion": "v1",
  "kind": "ReplicationController",
  "metadata": {
    "labels": {
      "name": "web-rc"
    },
    "name": "web-rc"
  },
  "spec": {
    "replicas": 2,
    "template": {
      "metadata": {
        "labels": {
          "component": "web-rc"
        },
        "name": "web-rc"
      },
      "spec": {
        "containers": [
          {
            "image": "nginx",
            "name": "nginx"
          },
          {
            "image": "redis",
            "name": "redis"
          }
        ]
      }
    }
  }
}
```
