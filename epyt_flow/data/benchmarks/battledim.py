from datetime import datetime

from ..networks import load_ltown
from ...simulation.events import AbruptLeakage, IncipientLeakage
from ...simulation import ScenarioConfig


def load_battledim(evaluation:bool, download_dir:str=None) -> ScenarioConfig:
    """
    The Battle of the Leakage Detection and Isolation Methods (*BattLeDIM*) 2020, organized by
    S. G. Vrachimis, D. G. Eliades, R. Taormina, Z. Kapelan, A. Ostfeld, S. Liu, M. Kyriakou, 
    P. Pavlou, M. Qiu, and M. M. Polycarpou, as part of the 2nd International CCWI/WDSA Joint 
    Conference in Beijing, China, aims at objectively comparing the performance of methods for 
    the detection and localization of leakage events, relying on SCADA measurements of flow and 
    pressure sensors installed within water distribution networks.

    See https://github.com/KIOS-Research/BattLeDIM for details.


    This method supports two different scenario configurations:
        - *Training/Historical configuration:* https://github.com/KIOS-Research/BattLeDIM/blob/master/Dataset%20Generator/dataset_configuration_historical.yalm
        - *Test/Evaluation configuraton:* https://github.com/KIOS-Research/BattLeDIM/blob/master/Dataset%20Generator/dataset_configuration_evaluation.yalm

    Parameters
    ----------
    evaluation : `bool`
        If True, the evaluation scenario is returned, otherwise the historical 
        (i.e. training) scenario is returned.
    download_dir : `str`
        Path to the L-TOWN.inp file -- if None, the temp folder will be used.
        If the path does not exist, the .inp will be downloaded to the give path.

        The default is None.
    
    Returns
    -------
    :class:`epyt_flow.simulation.scenario_config.ScenarioConfig`
        Complete scenario configuration for this benchmark.
    """

    # Load L-Town network including the sensor placement
    if download_dir is not None:
        ltown_config = load_ltown(download_dir=download_dir, include_default_sensor_placement=True)
    else:
        ltown_config = load_ltown(include_default_sensor_placement=True)

    # Set simulation duration
    general_params = {"simulation_duration": 365,   # One year
                      "hydraulic_time_step": 300}   # 5min time steps

    # Add events
    if evaluation is True:
        start_time = datetime.strptime("2019-01-01 00:00", "%Y-%m-%d %H:%M")
        #end_time = datetime.strptime("2019-12-31 23:55", "%Y-%m-%d %H:%M")

        leaks_config = \
        """p257, 2019-01-01 00:00, 2019-12-31 23:55, 0.011843, incipient, 2019-01-01 00:00
        p427, 2019-01-01 00:00, 2019-12-31 23:55, 0.0090731, incipient, 2019-01-01 00:00
        p810, 2019-01-01 00:00, 2019-12-31 23:55, 0.010028, incipient, 2019-01-01 00:00
        p654, 2019-01-01 00:00, 2019-12-31 23:55, 0.0087735, incipient, 2019-01-01 00:00
        p523, 2019-01-15 23:00, 2019-02-01 09:50, 0.020246, abrupt, 2019-01-15 23:00
        p827, 2019-01-24 18:30, 2019-02-07 09:05, 0.02025, abrupt, 2019-01-24 18:30
        p280, 2019-02-10 13:05, 2019-12-31 23:55, 0.0095008, abrupt, 2019-02-10 13:05
        p653, 2019-03-03 13:10, 2019-05-05 12:10, 0.016035, incipient, 2019-04-21 19:00
        p710, 2019-03-24 14:15, 2019-12-31 23:55, 0.0092936, abrupt, 2019-03-24 14:15
        p514, 2019-04-02 20:40, 2019-05-23 14:55, 0.014979, abrupt, 2019-04-02 20:40
        p331, 2019-04-20 10:10, 2019-12-31 23:55, 0.014053, abrupt, 2019-04-20 10:10
        p193, 2019-05-19 10:40, 2019-12-31 23:55, 0.01239, incipient, 2019-07-25 03:20
        p277, 2019-05-30 21:55, 2019-12-31 23:55, 0.012089, incipient, 2019-08-11 15:05
        p142, 2019-06-12 19:55, 2019-07-17 09:25, 0.019857, abrupt, 2019-06-12 19:55
        p680, 2019-07-10 08:45, 2019-12-31 23:55, 0.0097197, abrupt, 2019-07-10 08:45
        p586, 2019-07-26 14:40, 2019-09-16 03:20, 0.017184, incipient, 2019-08-28 07:55
        p721, 2019-08-02 03:00, 2019-12-31 23:55, 0.01408, incipient, 2019-09-23 05:40
        p800, 2019-08-16 14:00, 2019-10-01 16:35, 0.018847, incipient, 2019-09-07 21:05
        p123, 2019-09-13 20:05, 2019-12-31 23:55, 0.011906, incipient, 2019-11-29 22:10
        p455, 2019-10-03 14:00, 2019-12-31 23:55, 0.012722, incipient, 2019-12-16 05:25
        p762, 2019-10-09 10:15, 2019-12-31 23:55, 0.01519, incipient, 2019-12-03 01:15
        p426, 2019-10-25 13:25, 2019-12-31 23:55, 0.015008, abrupt, 2019-10-25 13:25
        p879, 2019-11-20 11:55, 2019-12-31 23:55, 0.013195, incipient, 2019-12-31 23:55"""
    else:
        start_time = datetime.strptime("2018-01-01 00:00", "%Y-%m-%d %H:%M")
        #end_time = datetime.strptime("2018-12-31 23:55", "%Y-%m-%d %H:%M")

        leaks_config = \
        """p257, 2018-01-08 13:30, 2018-12-31 23:55, 0.011843, incipient, 2018-01-25 08:30
        p461, 2018-01-23 04:25, 2018-04-02 11:40, 0.021320, incipient, 2018-03-27 20:35
        p232, 2018-01-31 02:35, 2018-02-10 09:20, 0.020108, incipient, 2018-02-03 16:05
        p427, 2018-02-13 08:25, 2018-12-31 23:55, 0.0090731, incipient, 2018-05-14 19:25
        p673, 2018-03-05 15:45, 2018-03-23 10:25, 0.022916, abrupt, 2018-03-05 15:45
        p810, 2018-07-28 03:05, 2018-12-31 23:55, 0.010028, incipient, 2018-11-02 22:25
        p628, 2018-05-02 14:55, 2018-05-29 21:20, 0.022318, incipient, 2018-05-16 08:00
        p538, 2018-05-18 08:35, 2018-06-02 06:05, 0.021731, abrupt, 2018-05-18 08:35
        p866, 2018-06-01 09:05, 2018-06-12 03:00, 0.018108, abrupt, 2018-06-01 09:05
        p31, 2018-06-28 10:35, 2018-08-12 17:30, 0.016389, incipient, 2018-08-03 02:45
        p654, 2018-07-05 03:40, 2018-12-31 23:55, 0.0087735, incipient, 2018-09-16 21:05
        p183, 2018-08-07 02:35, 2018-09-01 17:10, 0.015853, abrupt, 2018-08-07 02:35
        p158, 2018-10-06 02:35, 2018-10-23 13:35, 0.019364, abrupt, 2018-10-06 02:35
        p369, 2018-10-26 02:05, 2018-11-08 20:25, 0.019363, abrupt, 2018-10-26 02:05"""

    leakages = []
    for leak in leaks_config.splitlines():
        # Parse entry
        items = [i.strip() for i in leak.split(",")]
        leaky_pipe_id = items[0]
        leak_start_time = int((datetime.strptime(items[1], "%Y-%m-%d %H:%M") - start_time)\
                            .total_seconds())
        leak_end_time = int((datetime.strptime(items[2], "%Y-%m-%d %H:%M") - start_time)\
                            .total_seconds())
        leak_diameter = float(items[3])
        leak_type = items[4]
        leak_peak_time = int((datetime.strptime(items[5], "%Y-%m-%d %H:%M") - start_time)\
                            .total_seconds())

        # Create leak config
        if leak_type == "incipient":
            leak = IncipientLeakage(link_id=leaky_pipe_id, diameter=leak_diameter,
                                    start_time=leak_start_time, end_time=leak_end_time,
                                    peak_time=leak_peak_time)
        elif leak_type == "abrupt":
            leak = AbruptLeakage(link_id=leaky_pipe_id, diameter=leak_diameter,
                                 start_time=leak_start_time, end_time=leak_end_time)

        leakages.append(leak)

    # Build final scenario
    return ScenarioConfig(f_inp_in=ltown_config.f_inp_in, general_params=general_params,
                          sensor_config=ltown_config.sensor_config, system_events=leakages)
