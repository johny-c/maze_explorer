# Maze Explorer

A maze exploration game for AI agents.

![Screenshot](https://raw.githubusercontent.com/mryellow/maze_explorer/master/mazeexp/engine/assets/screen_001.jpg)

## TODO:

* [ ] New game modes
* [ ] Terminal state for human, with switch for god-mode
* [ ] Zoomed scrolling view for human players

## Installation

### Source

```bash
git clone https://github.com/mryellow/maze_explorer.git
cd maze_explorer
pip install -e .
```

### Package

```bash
pip install mazeexp
```

## Standalone

`python standalone.py`

### Options

```bash
--mode X # Mode number
--random # Execute random actions step-by-step via `act`
--step # Call the engine step-by-step via `step`
```


## OpenAIGym

[gym-mazeexplorer](https://github.com/mryellow/gym-mazeexplorer)

### Game modes

#### Mode 0 `MazeExplorerEat-v0`

Apples and poison.

Based on [Andrej Karpathy's Javascript environment](https://cs.stanford.edu/people/karpathy/convnetjs/demo/rldemo.html)

##### State

```
[
  [min(wall_range, apple_range, poison_range), apple_range, poison_range],
  ...
]
```

##### Rewards

* ~~`avg(proximity) or 1` Agents don't like seeing walls, especially up close~~
* ~~`*1.1` Forward action bonus~~
* `-10` collision with wall
* `+5` collision with apple
* `-6` collision with poison

##### Terminal

* None

#### Mode 1 `MazeExplorerExplore-v0`

Explore the maze and make it back to spawn before battery runs out.

##### State

```
[wall_range, ..., battery]
```

##### Rewards

* `-100` collision with wall
* `-100` battery out

###### When battery above 50%

* `+1` exploration reward on first visit to tile and for each of it's open neighbours

The `visited` state is not observable in environment and reward is generated by ground-truth.
Thus agent must keep it's own internal state and/or develop a policy which overcomes this unknown.

###### When battery below 50%

* `+200` reward goal state on reaching spawn tile
* No futher exploration rewards

Spawn tile is no different to any other from agents perspective, must remember how to return to it or develop a policy which increases the likelihood of such.

##### Terminal

* Wall collision
* Battery out
* Return to home goal

## Cite

If you use Maze Explorer in your academic research, we would be grateful if you could cite it as follows:

```
@misc{king2017mazeexplorer,
    author = {King},
    title = {Maze Explorer: A maze exploration game for AI agents},
    howpublished={Web page},
    url = {https://github.com/mryellow/maze_explorer},
    year = {2017}
}
```
