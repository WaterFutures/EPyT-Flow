"""
Module provides functions for loading LeakDB scenarios.
"""
import os
import json
import scipy
import numpy as np

from ..networks import load_net1, load_hanoi, download_if_necessary
from .leakdb_data import net1_leakages, hanoi_leakages
from ...utils import get_temp_folder
from ...simulation import WaterDistributionNetworkScenarioSimulator
from ...simulation.events import AbruptLeakage, IncipientLeakage
from ...simulation import ScenarioConfig
from ...uncertainty import ModelUncertainty, UniformUncertainty


# Taken from https://github.com/KIOS-Research/LeakDB/blob/master/CCWI-WDSA2018/Dataset_Generator_Py3/demandGenerator.py
def __gen_dem(download_dir, use_net1):
    week_pat = scipy.io.loadmat(os.path.join(download_dir, "weekPat_30min.mat"))
    a_w = week_pat['Aw']
    nw = week_pat['nw']
    year_offset = scipy.io.loadmat(os.path.join(download_dir, "yearOffset_30min.mat"))
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

def load_leakdb(scenarios_id:list[int], use_net1:bool=True,
                download_dir:str=None) -> list[ScenarioConfig]:
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
    use_net1 : `bool`, optional
        If True, Net1 network will be used, otherwise the Hanoi network will be used.

        The default is True.
    download_dir : `str`, optional
        Path to the Net1.inp or Hanoi.inp file -- if None, the temp folder will be used.
        If the path does not exist, the .inp will be downloaded to the give path.

        The default is None.
    """
    scenarios_inp = []

    # Load the network
    load_network = load_net1 if use_net1 is True else load_hanoi
    download_dir = download_dir if download_dir is not None else get_temp_folder()
    network_config = load_network(download_dir)

    # Set simulation duration
    general_params = {"simulation_duration": 365,   # One year
                      "hydraulic_time_step": 1800}  # 30min time steps

    # Add demand patterns
    week_pattern_url = "https://github.com/KIOS-Research/LeakDB/raw/master/CCWI-WDSA2018/"+\
        "Dataset_Generator_Py3/weekPat_30min.mat"
    year_offset_url = "https://github.com/KIOS-Research/LeakDB/raw/master/CCWI-WDSA2018/"+\
        "Dataset_Generator_Py3/yearOffset_30min.mat"

    download_if_necessary(os.path.join(download_dir, "weekPat_30min.mat"), week_pattern_url)
    download_if_necessary(os.path.join(download_dir, "yearOffset_30min.mat"), year_offset_url)

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

                    my_demand_pattern = np.array(__gen_dem(download_dir, use_net1))

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
