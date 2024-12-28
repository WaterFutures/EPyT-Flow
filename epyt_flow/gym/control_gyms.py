"""
Module provides functions for registering and creating control environments.
"""
from .scenario_control_env import ScenarioControlEnv


environments = {}


def register(env_name: str, env: ScenarioControlEnv) -> None:
    """
    Registers a new environment under a given name.

    Parameters
    ----------
    env_name : `str`
        Name of the environment -- must be unique among all environments.
    env : :class:`~epyt_flow.gym.scenario_control_env.ScenarioControlEnv`
        Environment.
    """
    if env_name in environments:
        raise ValueError(f"Environment '{env_name}' already exists.")
    if not issubclass(env, ScenarioControlEnv):
        raise TypeError("'env' must be a subclass of " +
                        "'epyt_flow.gym.ScenarioControlEnv'")

    environments[env_name] = env


def make(env_name: str, **kwds) -> ScenarioControlEnv:
    """
    Creates an instance of a registered environment.

    Parameters
    ----------
    env_name : `str`
        Name of the environment.

    Returns
    -------
    :class:`~epyt_flow.gym.scenario_control_env.ScenarioControlEnv`
        Environment.
    """
    if env_name not in environments:
        raise ValueError(f"Unknown environment '{env_name}'.")

    return environments[env_name](**kwds)
