# Env

## Step

args:
- action: TODO

returns:
- observation
- reward
- terminated
- truncated
- info

observation: tensor[n, m, 5]
channels:
- map: 1 where road
- cars: 1 where car
- this agent: 1 at current light agent position
- light state A: 1 where lights are in state A
- light state B: 1 where lights are in state B
