.. _usage:

***********
Basic Usage
***********

Quick example
-------------

.. raw:: html

    <a target="_blank" href="https://colab.research.google.com/github/WaterFutures/EPyT-Flow/blob/main/docs/examples/basic_usage.ipynb">
    <img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"/>
    </a>

.. code-block:: python

    from epyt_flow.data.benchmarks import load_leakdb_scenarios
    from epyt_flow.simulation import ScenarioSimulator
    from epyt_flow.utils import to_seconds


    if __name__ == "__main__":
        # Load first Hanoi scenario from LeakDB
        network_config, = load_leakdb_scenarios(scenarios_id=["1"], use_net1=False)

        # Create scenario
        with ScenarioSimulator(scenario_config=network_config) as sim:
            # Set simulation duration to two days
            sim.set_general_parameters(simulation_duration=to_seconds(days=2))

            # Place pressure sensors at nodes "13", "16", "22", and "30"
            sim.set_pressure_sensors(sensor_locations=["13", "16", "22", "30"])

            # Place a flow sensor at link/pipe "1"
            sim.set_flow_sensors(sensor_locations=["1"])

            # Run entire simulation
            scada_data = sim.run_simulation()

            # Print & plot sensor readings over the entire simulation
            print(f"Pressure readings: {scada_data.get_data_pressures()}")
            scada_data.plot_pressures()

            print(f"Flow readings: {scada_data.get_data_flows()}")
            scada_data.plot_flows()


More examples
-------------

More complete examples can be found in the `examples` folder in the GitHub repository
and also in the provided :ref:`Jupyter notebooks <tut.examples>`.
