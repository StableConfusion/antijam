# Env

## Step

args:
- `action`: `{"light_{i}": 0 or 1}`

returns:
- `observation`: `{"light_{i}": observation tensor}`
- `reward`: `{"light_{i}": mean car speed}`
- `terminated`: `{"light_{i}": False, "__all__": False}`
- `info`: `{"light_{i}": {}}`

observation tensor NxMx5:
- map: 1 where road
- cars: 1 where car
- this agent: 1 at current light agent position
- light state A: 1 where lights are in state A
- light state B: 1 where lights are in state B
