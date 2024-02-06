.. _usage:

*****
Usage
*****

Quick example
-------------

.. code-block:: python

    from epyt_flow.data.networks import load_hanoi
    from epyt_flow.simulation import WaterDistributionNetworkScenarioSimulator
    from epyt_flow.simulation.sensor_config import SENSOR_TYPE_NODE_PRESSURE,\
        SENSOR_TYPE_LINK_FLOW


    if __name__ == "__main__":
        # Load Hanoi network
        network_config = load_hanoi()

        # Create scenario
        with WaterDistributionNetworkScenarioSimulator(scenario_config=network_config) as sim:
            # Set simulation duration to two days
            sim.set_general_parameters(simulation_duration=2)

            # Place pressure sensors at nodes "13", "16", "22", and "30"
            sim.set_sensors(SENSOR_TYPE_NODE_PRESSURE, sensor_locations=["13", "16", "22", "30"])

            # Place a flow sensor at link/pipe ""
            sim.set_sensors(SENSOR_TYPE_LINK_FLOW, sensor_locations=["1"])

            # Run entire simulation
            res = sim.run_simulation()

            # Show sensor readings over the entire simulation
            print(res.get_data())
