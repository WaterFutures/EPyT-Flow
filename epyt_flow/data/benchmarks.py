import os
import json
from datetime import datetime
import scipy
import numpy as np

from .networks import load_ltown, load_net1, load_hanoi, download_if_necessary
from .leakdb_data import net1_leakages, hanoi_leakages
from ..utils import get_temp_folder
from ..simulation import WaterDistributionNetworkScenarioSimulator
from ..simulation.events import AbruptLeakage, IncipientLeakage
from ..simulation import ScenarioConfig
from ..uncertainty import ModelUncertainty, UniformUncertainty


def load_leakdb(scenarios_id:list[int], use_net1:bool=True,
                path_to_inp:str=None) -> list[ScenarioConfig]:
    """
    LeakDB (Leakage Diagnosis Benchmark) by Vrachimis, S. G., Kyriakou, M. S., Eliades, D. G. 
    and Polycarpou, M. M. (2018), is a realistic leakage dataset for water distribution networks. 
    The dataset is comprised of 1000 artificially created but realistic leakage 
    scenarios, on different water distribution networks, under varying conditions.

    See https://github.com/KIOS-Research/LeakDB/ for details.

    .. note::
        Note that due to the randomness in the demand creation as well as in the model 
        uncertainties, the generated scenarios will differ between different runs, and 
        will also differ from the "official" data set available at 
        https://github.com/KIOS-Research/LeakDB/. 
        However, the leakages (i.e. location and profile) will be always the same and be 
        consistent with the "official" data set.

    This implementation is based on 
    https://github.com/KIOS-Research/LeakDB/blob/master/CCWI-WDSA2018/Dataset_Generator_Py3/demandGenerator.py
    and https://github.com/KIOS-Research/LeakDB/blob/master/CCWI-WDSA2018/Dataset_Generator_Py3/leakDataset.py

    Parameters
    ----------
    scenarios_id : `list[int]`
        List of scenarios ID that are to be loaded -- there is a total number of 1000 scenarios.
    use_net1 : `bool`
        If True, Net1 network will be used, otherwise the Hanoi network will be used.

        The default is True.
    path_to_inp : `str`
        Path to the Net1.inp or Hanoi.inp file -- if None, the temp folder will be used.
        If the path does not exist, the .inp will be downloaded to the give pat.

        The default is None.
    """
    scenarios_inp = []

    # Load the network
    load_network = load_net1 if use_net1 is True else load_hanoi
    download_dir = path_to_inp if path_to_inp is not None else get_temp_folder()
    network_config = load_network(download_dir)

    # Set simulation duration
    general_params = {"simulation_duration": 365,   # One year
                      "hydraulic_time_step": 1800}  # 30min time steps

    # Add demand patterns
    # Taken from https://github.com/KIOS-Research/LeakDB/blob/master/CCWI-WDSA2018/Dataset_Generator_Py3/demandGenerator.py
    def gen_dem(tmp_path):
        week_pat = scipy.io.loadmat(os.path.join(tmp_path, "weekPat_30min.mat"))
        a_w = week_pat['Aw']
        nw = week_pat['nw']
        year_offset = scipy.io.loadmat(os.path.join(tmp_path, "yearOffset_30min.mat"))
        a_y = year_offset['Ay']
        ny = year_offset['ny']

        # Create yearly component
        days = 365

        t = (288/6)*days    # one year period in five minute intervals
        w = 2*np.pi/t
        k = np.arange(1, days*288/6+1 ,1)   # number of time steps in time series
        n = ny[0][0]    # number of fourier coefficients
        h_y = [1]*len(k)

        for i in range(1, n+1):
            h_y = np.column_stack((h_y, np.sin(i*w*k), np.cos(i*w*k)))

        unc_y = 0.1
        a_y_r = a_y*(1-unc_y + 2*unc_y*np.random.rand(int(a_y.shape[0]), int(a_y.shape[1])))
        year_offset = np.dot(h_y, a_y_r)

        # Create weekly component
        t = (288/6)*7   #one week period in five minute intervals
        w = 2*np.pi/t
        k = np.arange(1, days*288/6+1 ,1)   # number of time steps in time series
        n = nw[0][0]    # number of fourier coefficients
        h_w = [1]*len(k)
        for i in range(1,n+1):
            h_w = np.column_stack((h_w, np.sin(i*w*k), np.cos(i*w*k)))

        unc_w = 0.1
        a_w_r = a_w*(1-unc_w + 2*unc_w*np.random.rand(int(a_w.shape[0]), int(a_w.shape[1])))
        week_year_pat = np.dot(h_w, a_w_r)

        # Create random component
        unc_r = 0.05
        random = np.random.normal(0,(-unc_r+2*unc_r),
                                  (int(week_year_pat.shape[0]), int(week_year_pat.shape[1])))

        # Create demand
        if use_net1 is True:
            base = 1
            variation = 0.75 + np.random.normal(0,0.07)  # from 0 to 1
        else:
            base=0.5
            variation = np.random.normal(0,0.07)
        dem = base * (year_offset+1) * (week_year_pat*variation+1) * (random+1)
        dem = dem.tolist()
        dem_final = []
        for d in dem:
            dem_final.append(d[0])

        return dem_final

    week_pattern_url = "https://github.com/KIOS-Research/LeakDB/raw/master/CCWI-WDSA2018/"+\
        "Dataset_Generator_Py3/weekPat_30min.mat"
    year_offset_url = "https://github.com/KIOS-Research/LeakDB/raw/master/CCWI-WDSA2018/"+\
        "Dataset_Generator_Py3/yearOffset_30min.mat"

    download_if_necessary(os.path.join(get_temp_folder(), "weekPat_30min.mat"), week_pattern_url)
    download_if_necessary(os.path.join(get_temp_folder(), "yearOffset_30min.mat"), year_offset_url)

    for s_id in scenarios_id:   # Create new .inp files with demands if necessary
        f_inp_in = os.path.join(download_dir,
                                f"{'Net1' if use_net1 is True else 'Hanoi'}_LeakDB_ID={s_id}.inp")
        scenarios_inp.append(f_inp_in)

        if not os.path.exists(f_inp_in):
            with WaterDistributionNetworkScenarioSimulator(f_inp_in=network_config.f_inp_in) as wdn:
                wdn.epanet_api.setTimeHydraulicStep(general_params["hydraulic_time_step"])
                wdn.epanet_api.setTimeSimulationDuration(general_params["simulation_duration"]*\
                                                         24*3600)
                wdn.epanet_api.setTimePatternStep(general_params["hydraulic_time_step"])

                wdn.epanet_api.deletePatternsAll()

                reservoir_nodes_id = wdn.epanet_api.getNodeReservoirNameID()
                for node_id in network_config.sensor_config.nodes:
                    if node_id in network_config.sensor_config.tanks or \
                        node_id in reservoir_nodes_id:
                        continue

                    node_idx = wdn.epanet_api.getNodeIndex(node_id)
                    base_demand = wdn.epanet_api.getNodeBaseDemands(node_idx)[1][0]

                    my_demand_pattern = np.array(gen_dem(get_temp_folder()))

                    wdn.set_node_demand_pattern(node_id=node_id, base_demand=base_demand,
                                                demand_pattern_id=f"demand_{node_id}",
                                                demand_pattern=my_demand_pattern)

                wdn.epanet_api.saveInputFile(f_inp_in)

    # Create uncertainties
    class MyUniformUncertainty(UniformUncertainty):
        """
        Custom uniform uncertainty for LeakDB scenarios.
        """
        def __init__(self, **kwds):
            super().__init__(**kwds)

        def apply(self, data:float) -> float:
            z = data * np.random.uniform(low=self.min, high=self.max)
            l = data - z
            u = data + z
            return l + np.random.uniform() * (u - l)

    model_uncertainty = ModelUncertainty(pipe_length_uncertainty=MyUniformUncertainty(low=0,
                                                                                      high=0.25),
                                         pipe_diameter_uncertainty=MyUniformUncertainty(low=0,
                                                                                        high=0.25),
                                         pipe_roughness_uncertainty=MyUniformUncertainty(low=0,
                                                                                         high=0.25),
                                         demand_base_uncertainty=MyUniformUncertainty(low=0,
                                                                                      high=0.25))

    # Create sensor config (place pressure and flow sensors everywhere)
    sensor_config = network_config.sensor_config
    sensor_config.pressure_sensors = sensor_config.nodes
    sensor_config.flow_sensors = sensor_config.links

    # Add leakages
    leaks_all = []

    if use_net1 is True:
        leaks_info = json.loads(net1_leakages)
    else:
        leaks_info = json.loads(hanoi_leakages)

    for s_id in scenarios_id:
        leaks_data = []

        if str(s_id) in leaks_info:
            for leak in leaks_info[str(s_id)]:
                if leak["leak_type"] == "incipient":
                    leaks_data.append(IncipientLeakage(node_id=leak["node_id"],
                                                       link_id=None,
                                                       diameter=leak["leak_diameter"],
                                                       start_time=leak["leak_start_time"],
                                                       end_time=leak["leak_end_time"],
                                                       peak_time=leak["leak_peak_time"]))
                else:
                    leaks_data.append(AbruptLeakage(node_id=leak["node_id"],
                                                    link_id=None,
                                                    diameter=leak["leak_diameter"],
                                                    start_time=leak["leak_start_time"],
                                                    end_time=leak["leak_end_time"]))

        leaks_all.append(leaks_data)

    # Build final scenarios
    return [ScenarioConfig(f_inp_in=f_inp_in, general_params=general_params,
                          sensor_config=sensor_config, model_uncertainty=model_uncertainty,
                          system_events=leaks) for f_inp_in, leaks in zip(scenarios_inp, leaks_all)]


def load_battledim(evaluation:bool, path_to_ltown:str=None) -> ScenarioConfig:
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
    path_to_ltown : `str`
        Path to the L-TOWN.inp file -- if None, the temp folder will be used.
        If the path does not exist, the .inp will be downloaded to the give path.

        The default is None.
    
    Returns
    -------
    :class:`epyt_flow.simulation.scenario_config.ScenarioConfig`
        Complete scenario configuration for this benchmark.
    """

    # Load L-Town network including the sensor placement
    if path_to_ltown is not None:
        ltown_config = load_ltown(download_dir=path_to_ltown, include_default_sensor_placement=True)
    else:
        ltown_config = load_ltown(include_default_sensor_placement=True)

    # Set simulation duration
    general_params = {"simulation_duration": 365,   # One year
                      "hydraulic_time_step": 300}   # 5min time steps

    # Add events
    if evaluation is True:
        start_time = datetime.strptime("2019-01-01 00:00", "%Y-%m-%d %H:%M")
        end_time = datetime.strptime("2019-12-31 23:55", "%Y-%m-%d %H:%M")

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
        end_time = datetime.strptime("2018-12-31 23:55", "%Y-%m-%d %H:%M")

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
