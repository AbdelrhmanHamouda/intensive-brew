---
title: YAML configuration
description: YAML configuration breakdown
---

# YAML configuration
In order to generate a valid [LocustTest] custom resource, a valid yaml configuration should be prepared.

The following sections will break-down the supported configuration and provide the full YAML spec at the end.

!!! Note
        Although all following examples are for a single test, _Intensive Brew_ supports having several _test_ configurations in the same `.yaml` file.


## Locust configuration

This sections highlight all the available options that would impact the configuration of _Locust_. 

### Test entry point

`entry_point: str` is a **mandatory** field that allows _Intensive Brew_ to know which `.py` file to use as an entry to _locust_.

```yaml title="test-config.yaml"
configurations:
  ...
  test_name:
    entry_point: "<path>/demo.py" # (1)!
```

1. The provided `path` must be relative to the location of `test-config.yaml`.

### Test load requirements

`vanilla_specs: object` is a **mandatory** section that can be used to configure:

- Number of users
- Users spawn rate
- Test duration
- Target host of the test

```yaml title="test-config.yaml"
configurations:
  ...
  test_name:
    ...
    vanilla_specs:
      # * Number of users
      users: int
      # * Users spawn rate
      spawn_rate: int
      # * Test duration
      run_time: str # (1)!
      # * Test target URL 
      target_host: str
```

1. This field support different was of expressing duration e.g. (`300s`, `20m`, `3h`, `1h30m`, etc.). Default value is `30s`.

### Custom load shapes

`custom_load_shapes: bool` is an **optional** flag that enables the support of _Locust_ "**_[Custom Load Shapes]_**" feature. This feature doesn't follow the traditional way of declaring users, spawn rate and test run duration.

!!! important
    - When this flag is set to **_true_**, the `vanilla_specs` section becomes **optional** and is ignored even if provided.
    - Additional configuration like **test target host** is expected to be passed through custom config files or directly coded into the test.

```yaml title="test-config.yaml"
configurations:
  ...
  test_name:
    ...
    # * Enable "custom load shapes" support. Default: false
    custom_load_shapes: true
```

## Cluster nodes configuration

This sections highlight all the available options that would impact the configuration of the deployed cluster nodes.

### Locust container image

`image: str`  is an **optional** flag that instructs _Intensive Brew_ to populate the `image` field in _LocustTest_. Default is to use the latest _[Locust]_ image.

```yaml title="test-config.yaml"
configurations:
  ...
  test_name:
    ...
    image: str
```

### Kubernetes test configuration map

`configmap: str` is an **optional** flag that instructs _Intensive Brew_ to populate the `configMap` field in _LocustTest_. This is a feature supported by the _Locust Operator_ where it is possible to [deploy tests as k8s `configMap`] and then having it mounted on the load generation pods.

```yaml title="test-config.yaml"
configurations:
  ...
  test_name:
    ...
    configmap: <valid k8s configMap name>
```

### Worker replicas count

`worker_replicas: int` is an **optional** flag that instructs _Intensive Brew_ to populate the `workerReplicas` field in _LocustTest_. Default value is 5.

```yaml title="test-config.yaml"
configurations:
  ...
  test_name:
    ...
    worker_replicas: int
```

### Kubernetes Affinity

It is an **optional** section that instructs _Intensive Brew_ to populate the `affinity` field in _LocustTest_. The spec is structured in a similar way as the _Operator_. 

```yaml title="test-config.yaml"
configurations:
  ...
  test_name:
    ...
    affinity:
      nodeAffinity:
        requiredDuringSchedulingIgnoredDuringExecution: # (1)!
          <label-key>: <label-value> 
```

1. Can contain as many entries as desired.

### Kubernetes pod taint tolerations

It is an **optional** flag that instructs _Intensive Brew_ to populate the `tolerations` field in _LocustTest_. The spec is structured in a similar way as the _Operator_.

```yaml title="test-config.yaml"
configurations:
  ...
  tolerations: # (1)!
      - key: <string value>
        operator: <"Exists", "Equal">
        value: <string value>
        effect: <"NoSchedule", "PreferNoSchedule", "NoExecute">
      ...
```

1. Can contain as many entries as desired.

## Expert mode

`expert_mode: obj` is an **optional** section that grants direct control over what the _LocustTest_ fields for `masterCommandSeed` & `workerCommandSeed` will contain.

!!! important
    - When this section is set, all other sections from the ["Locust configuration"](#locust-configuration) section becomes **optional** and is ignored even if provided.

!!! warning
    - Activating this mode will suppress any processing of the data and directly pass the command "as-is".
    - If you find yourself using this mode frequently, consider opening a [feature request] to support your use case instead.  

```yaml title="test-config.yaml"
configurations:
  ...
  test_name:
    # ! USE WITH CAUTION
    expert_mode:
      # * Enable expert mode. Default: false
      enabled: bool
      # * Commands to pass "as-is"
      masterCommandSeed: str
      workerCommandSeed: str
```

## Full YAML spec

```yaml title="test-config.yaml"

configurations:
  # Test name
  load_test:
  
    #  Entry point script
    entry_point: str # (1)!
    
    # Load requirements
    vanilla_specs: 
      # Number of users
      users: int # (2)!
      # Users spawn rate
      spawn_rate: int # (3)!
      # Test duration
      run_time: str # (4)!
      # Test target URL 
      target_host: str # (5)!
    
    # Custom load shapes support.
    custom_load_shapes: bool
    
    # Locust container image
    image: str # (8)!
    
    # Test configuration map
    configmap: str # (6)!

    # Worker replicas
    worker_replicas: int # (7)!

    # Kubernetes affinity
    affinity: # (9)!
      nodeAffinity:
        requiredDuringSchedulingIgnoredDuringExecution: 
          <label-key>: <label-value>

    # Kubernetes pod taint toleration      
    tolerations: # (10)!
      - key: <string value>
        operator: <"Exists", "Equal">
        value: <string value>
        effect: <"NoSchedule", "PreferNoSchedule", "NoExecute">
    
    # ! USE WITH  CAUTION
    expert_mode:
      # Enable expert mode. Default: false
      enabled: bool
      # Commands to pass "as-is"
      masterCommandSeed: str
      workerCommandSeed: str
```

1. This field maps to the `--locustfile` locust switch and appears in `masterCommandSeed` & `workerCommandSeed` of the _LocustTest custom resource_.
2. This field maps to the `--users` locust switch and appears in `masterCommandSeed` of the _LocustTest custom resource_.
3. This field maps to the `--spawn-rate` locust switch and appears in `masterCommandSeed` of the _LocustTest custom resource_.
4. This field maps to the `--run-time` locust switch and appears in `masterCommandSeed` of the _LocustTest custom resource_.
5. This field maps to the `--host` locust switch and appears in `masterCommandSeed` of the _LocustTest custom resource_.
6. This field maps to the `configMap`  section of the _LocustTest custom resource_.
7. This field maps to the `workerReplicas`  section of the _LocustTest custom resource_.
8. This field maps to the `image`  section of the _LocustTest custom resource_.
9. This field directly maps to the `affinity`  section of the _LocustTest custom resource_.
10. This field directly maps to the `tolerations`  section of the _LocustTest custom resource_.




[//]: # (Links)
[LocustTest]: https://abdelrhmanhamouda.github.io/locust-k8s-operator/getting_started/#step-2-write-a-valid-custom-resource-for-locusttest-crd
[Custom Load Shapes]: https://docs.locust.io/en/stable/custom-load-shape.html
[deploy tests as k8s `configMap`]: https://abdelrhmanhamouda.github.io/locust-k8s-operator/getting_started/#step-4-deploy-test-as-a-configmap
[feature request]: https://github.com/AbdelrhmanHamouda/intensive-brew/issues
[Locust]: https://hub.docker.com/r/locustio/locust#!