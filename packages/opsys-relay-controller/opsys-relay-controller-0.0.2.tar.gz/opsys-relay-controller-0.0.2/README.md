# README

This README would normally document whatever steps are necessary to get your application up and running.

### What is this repository for?

- This repository is a part of opsys automation infrastructure
- This repository is relay controller implementation for relay device

### How do I get set up?

- pip install opsys-relay-controller

### Unit Testing

- python -m unittest -v

### Usage Example

```
from opsys_relay_controller.relay_controller import RelayController

relay = RelayController()  ### KMTronic USB relay, 8 switches
or
relay = RelayController(relay_type='KMTRONIC_1')  ### KMTronic USB relay, 1 switch

relay.connect()
relay.switch_on(switch_number=3)
relay.switch_off(switch_number=3)
relay.disconnect()
```
