from __future__ import division, print_function, unicode_literals

# This code is so you can run the samples without installing the package
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../..'))
#

from random import randint

import mazeexp as mx

def main(argv):

    mode_id = 0
    if '-m' in argv or '--mode' in argv:
        indexes = [i for i,x in enumerate(argv) if x == '-m' or x == '--mode']
        mode_id = int(argv[indexes[0]+1])
        print('Changed mode to ' + str(mode_id))

    engine = mx.MazeExplorer(mode_id)

    if '-r' in argv or '--random' in argv:
        print('Random test agent...')

        engine.create_scene()

        while not engine.director.window.has_exit:
            action = randint(0, engine.actions_num-1)
            observation, reward, terminal, info = engine.act(action)
            #print(observation)
            #print(action, [min(observation),max(observation)], reward, terminal)
    elif '-s' in argv or '--step' in argv:
        print('Step by step...')
        engine.create_scene()
        while not engine.director.window.has_exit:
            engine.step()
    else:
        engine.run()

if __name__ == "__main__":
   main(sys.argv[1:])
