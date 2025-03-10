"""
Module provides tests to test the visualization output. Stops and shows plots
if SHOW_PLOTS=True.
"""

import pytest
import numpy as np

from epyt_flow.data.benchmarks import load_leakdb_scenarios
from epyt_flow.data.networks import load_hanoi, load_ctown
from epyt_flow.simulation import ScenarioSimulator
from epyt_flow.visualization import ScenarioVisualizer, epanet_colors, epyt_flow_colors

SHOW_PLOTS = False


@pytest.fixture()
def setup_simulator():
    network_config = load_ctown()
    wdn = ScenarioSimulator(scenario_config=network_config)
    yield wdn
    wdn.close()


def test_animation(setup_simulator):
    vis = ScenarioVisualizer(setup_simulator)
    vis.color_links(parameter='flow_rate', statistic='time_step', pit=(1, 200),
                    colormap='Blues')
    vis.resize_links(parameter='diameter', statistic='time_step', pit=(1, 200),
                     line_widths=(1, 5))
    vis.hide_nodes()
    if SHOW_PLOTS:
        vis.show_animation()
    else:
        vis.show_animation(return_animation=True)


def test_animation_with_colorbar(setup_simulator):
    vis = ScenarioVisualizer(setup_simulator)
    vis.color_links(parameter='flow_rate', statistic='time_step', pit=(1, 200),
                    colormap='Blues', show_colorbar=True)
    vis.resize_links(parameter='diameter', statistic='time_step', pit=(1, 200),
                     line_widths=(1, 5))
    vis.hide_nodes()
    if SHOW_PLOTS:
        vis.show_animation()
    else:
        vis.show_animation(return_animation=True)


def test_animation_with_labels(setup_simulator):
    vis = ScenarioVisualizer(setup_simulator)
    vis.color_links(parameter='flow_rate', statistic='time_step', pit=(1, 200),
                    colormap='Blues')
    vis.resize_links(parameter='diameter', statistic='time_step', pit=(1, 200),
                     line_widths=(1, 5))
    vis.add_labels('all')
    if SHOW_PLOTS:
        vis.show_animation()
    else:
        vis.show_animation(return_animation=True)

    vis = ScenarioVisualizer(setup_simulator)
    vis.color_links(parameter='flow_rate', statistic='time_step', pit=(1, 200),
                    colormap='Blues')
    vis.resize_links(parameter='diameter', statistic='time_step', pit=(1, 200),
                     line_widths=(1, 5))
    vis.add_labels(['valves', 'tanks'])
    if SHOW_PLOTS:
        vis.show_animation()
    else:
        vis.show_animation(return_animation=True)


def test_animation_sensor_config_labels():
    network_config, = load_leakdb_scenarios(scenarios_id=["1"], use_net1=False)
    wdn = ScenarioSimulator(scenario_config=network_config)
    wdn.set_pressure_sensors(sensor_locations=["13", "16", "22", "30"])
    wdn.set_flow_sensors(sensor_locations=["1"])
    vis = ScenarioVisualizer(wdn)
    vis.color_links(parameter='flow_rate', statistic='time_step', pit=(0, 50),
                    colormap='Blues')
    vis.resize_links(parameter='diameter', statistic='time_step', pit=(0, 50),
                     line_widths=(1, 5))
    vis.add_labels('sensor_config')
    if SHOW_PLOTS:
        vis.show_animation()
    else:
        vis.show_animation(return_animation=True)
    wdn.close()


def test_custom_table_animation(setup_simulator):
    timesteps = 50
    links = 444

    t = np.linspace(0, 2 * np.pi, timesteps)

    frequencies = np.linspace(1, 3, links)
    phases = np.linspace(0, np.pi, links)
    amplitudes = np.linspace(0.5, 1.5, links)

    custom_data_table = np.array([a * np.sin(f * t + p) for f, p, a in
                                  zip(frequencies, phases, amplitudes)]).T

    vis = ScenarioVisualizer(setup_simulator,
                             color_scheme=epyt_flow_colors)
    vis.color_links(data=custom_data_table, parameter='custom_data',
                    statistic='time_step', pit=(0, -1))
    vis.resize_links(data=custom_data_table, parameter='custom_data',
                     statistic='time_step', pit=(0, -1), line_widths=(1, 5))

    if SHOW_PLOTS:
        vis.show_animation()
    else:
        vis.show_animation(return_animation=True)


def test_color_scheme_serialization(setup_simulator):
    attrs = epanet_colors.get_attributes()
    assert isinstance(attrs, dict), ("get_attributes does not return"
                                     " dictionary for serialization")
