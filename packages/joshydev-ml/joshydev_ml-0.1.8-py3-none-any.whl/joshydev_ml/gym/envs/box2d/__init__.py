try:
    import Box2D
    from joshydev_ml.gym.envs.box2d.lunar_lander import LunarLander
    from joshydev_ml.gym.envs.box2d.lunar_lander import LunarLanderContinuous
    from joshydev_ml.gym.envs.box2d.bipedal_walker import BipedalWalker, BipedalWalkerHardcore
    from joshydev_ml.gym.envs.box2d.car_racing import CarRacing
except ImportError:
    Box2D = None
