from __future__ import division, print_function, unicode_literals

import numpy as np
import pyglet
#from pyglet.gl import *

import cocos
from cocos.director import director

import config
from message import MessageLayer
from world import WorldLayer

class MazeExplorer():
    """
    Wrapper for game engine
    """

    def __init__(self, visible = True):
        config.settings['window']['visible'] = visible

        self.director = director
        self.director.init(**config.settings['window'])
        #pyglet.font.add_directory('.') # adjust as necessary if font included
        self.z = 0

        self.actions_num = len(config.settings['world']['bindings'])
        # Sensors, plus one for battery indicator
        self.observation_num = config.settings['player']['sensors']['num'] + 1

    def create_scene(self):
        """
        Attach a new engine to director
        """
        self.scene = cocos.scene.Scene()
        self.z = 0

        palette = config.settings['view']['palette']
        #Player.palette = palette
        r, g, b = palette['bg']
        self.scene.add(cocos.layer.ColorLayer(r, g, b, 255), z=self.z)
        self.z += 1
        message_layer = MessageLayer()
        self.scene.add(message_layer, z=self.z)
        self.z += 1
        self.world_layer = WorldLayer(fn_show_message=message_layer.show_message)
        self.scene.add(self.world_layer, z=self.z)
        self.z += 1

        self.director._set_scene(self.scene)

    def act(self, action):
        """
        Take one action for one step
        """
        assert isinstance(action, int)
        assert action < self.actions_num, "%r (%s) invalid"%(action, type(action))

        # Reset other buttons
        for k in self.world_layer.buttons:
            self.world_layer.buttons[k] = 0

        key = sorted(self.world_layer.buttons.keys())[action]

        # Set action for next step
        self.world_layer.buttons[key] = 1

        # Act in the environment
        self.step()

        # Create observation from sensor proximities
        observation = [o.proximity_norm() for o in self.world_layer.player.sensors]
        # Include battery level in state
        observation.append(self.world_layer.player.stats['battery']/100)

        # Return reward and reset for next step
        reward = self.world_layer.player.stats['reward']
        self.world_layer.player.stats['reward'] = 0

        return observation, reward, self.world_layer.player.game_over, {}

    def step(self):
        """
        Step the engine one tick
        """
        self.director.window.switch_to()
        self.director.window.dispatch_events()
        self.director.window.dispatch_event('on_draw')
        self.director.window.flip()

        # Ticking before events caused glitches.
        pyglet.clock.tick()

        #for window in pyglet.app.windows:
        #    window.switch_to()
        #    window.dispatch_events()
        #    window.dispatch_event('on_draw')
        #    window.flip()

    def run(self):
        """
        Run in real-time
        """
        self.create_scene()
        return self.director.run(self.scene)
