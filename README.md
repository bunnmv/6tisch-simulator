# Adaption to The 6TiSCH Simulator

* Marcus Bunn (marcus.bunn@posgrad.ufsc.br)

## Key Additions

1. Two roots mode
2. 866Mhz interface
3. Auto connectivity mode
4. AppPeriodicDelayed application

# The 6TiSCH Simulator
Core Developers:

* Yasuyuki Tanaka (yasuyuki.tanaka@inria.fr)
* Keoma Brun-Laguna (keoma.brun@inria.fr)
* Mališa Vučinić (malisa.vucinic@inria.fr)
* Thomas Watteyne (thomas.watteyne@inria.fr)

Contributers:

* Kazushi Muraoka (k-muraoka@eecs.berkeley.edu)
* Nicola Accettura (nicola.accettura@eecs.berkeley.edu)
* Xavier Vilajosana (xvilajosana@eecs.berkeley.edu)
* Esteban Municio (esteban.municio@uantwerpen.be)
* Glenn Daneels (glenn.daneels@uantwerpen.be)

## Publishing

If you publish an academic paper using the results of the 6TiSCH Simulator, please cite:

E. Municio, G. Daneels, M. Vucinic, S. Latre, J. Famaey, Y. Tanaka, K. Brun, K. Muraoka, X. Vilajosana, and T. Watteyne, "Simulating 6TiSCH Networks", Wiley Transactions on Emerging Telecommunications (ETT), 2019; 30:e3494. https://doi.org/10.1002/ett.3494

And

M.Bunn, R.Souza, G.Moritz, "Channel diversity on 6TiSCH networks"

## Scope

6TiSCH is an IETF standardization working group that defines a complete protocol stack for ultra reliable ultra low-power wireless mesh networks.
This simulator implements the 6TiSCH protocol stack, exactly as it is standardized.
It allows you to measure the performance of a 6TiSCH network under different conditions.

Simulated protocol stack

|                                                                                                              |                                             |
|--------------------------------------------------------------------------------------------------------------|---------------------------------------------|
| [RFC6550](https://tools.ietf.org/html/rfc6550), [RFC6552](https://tools.ietf.org/html/rfc6552)               | RPL, non-storing mode, OF0                  |
| [RFC6206](https://tools.ietf.org/html/rfc6206)                                                               | Trickle Algorithm                           |
| [draft-ietf-6lo-minimal-fragment-07](https://tools.ietf.org/html/draft-ietf-6lo-minimal-fragment-07)         | 6LoWPAN Fragment Forwarding                 |
| [RFC6282](https://tools.ietf.org/html/rfc6282), [RFC4944](https://tools.ietf.org/html/rfc4944)               | 6LoWPAN Fragmentation                       |
| [draft-ietf-6tisch-msf-10](https://tools.ietf.org/html/draft-ietf-6tisch-msf-10)                             | 6TiSCH Minimal Scheduling Function (MSF)    |
| [draft-ietf-6tisch-minimal-security-15](https://tools.ietf.org/html/draft-ietf-6tisch-minimal-security-15)   | Constrained Join Protocol (CoJP) for 6TiSCH |
| [RFC8480](https://tools.ietf.org/html/rfc8480)                                                               | 6TiSCH 6top Protocol (6P)                   |
| [RFC8180](https://tools.ietf.org/html/rfc8180)                                                               | Minimal 6TiSCH Configuration                |
| [IEEE802.15.4-2015](https://ieeexplore.ieee.org/document/7460875/)                                           | IEEE802.15.4 TSCH                           |

* connectivity models
    * Pister-hack
    * k7: trace-based connectivity
* miscellaneous
    * Energy Consumption model taken from
        * [A Realistic Energy Consumption Model for TSCH Networks](http://ieeexplore.ieee.org/xpl/login.jsp?tp=&arnumber=6627960&url=http%3A%2F%2Fieeexplore.ieee.org%2Fiel7%2F7361%2F4427201%2F06627960.pdf%3Farnumber%3D6627960). Xavier Vilajosana, Qin Wang, Fabien Chraim, Thomas Watteyne, Tengfei Chang, Kris Pister. IEEE Sensors, Vol. 14, No. 2, February 2014.

## Installation

* Install Python 2.7 (or Python 3)
* Clone or download this repository
* To plot the graphs, you need Matplotlib and scipy. On Windows, Anaconda (http://continuum.io/downloads) is a good one-stop-shop.

While 6TiSCH Simulator has been tested with Python 2.7, it should work with Python 3 as well.

## Getting Started

1. Download the code:
   ```
   $ git clone https://bitbucket.org/6tisch/simulator.git
   ```
1. Install the Python dependencies:
   `cd simulator` and `pip install -r requirements.txt`
2. Execute `runSim.py`:
    * runSim.py
       ```
       $ cd bin
       $ python runSim.py
       ```
        * a new directory having the timestamp value as its name is created under
          `bin/simData/` (e.g., `bin/simData/20181203-161254-775`)
        * raw output data and raw charts are stored in the newly created directory
        
Take a look at `bin/config.json` to see the configuration of the simulations you just ran.

## Code Organization

* `SimEngine/`: the simulator
    * `Connectivity.py`: Simulates wireless connectivity.
    * `SimConfig.py`: The overall configuration of running a simulation campaign.
    * `SimEngine.py`: Event-driven simulation engine at the core of this simulator.
    * `SimLog.py`: Used to save the simulation logs.
    * `SimSettings.py`: The settings of a single simulation, part of a simulation campaign.
    * `Mote/`: Models a 6TiSCH mote running the different standards listed above.
* `bin/`: the scripts for you to run
* `gui/`: files for GUI (see "GUI" section for further information)
* `tests/`: the unit tests, run using `pytest`
* `traces/`: example `k7` connectivity traces

## Configuration

`runSim.py` reads `config.json` in the current working directory.
You can specify a specific `config.json` location with `--config` option.

```
python runSim.py --config=example.json
```

The `config` parameter can contain:

* the name of the configuration file in the current directory, e.g. `example.json`
* a path to a configuration file on the computer running the simulation, e.g. `c:\simulator\example.json`
* a URL of a configuration file somewhere on the Internet, e.g. `https://www.example.com/example.json`

### base format of the configuration file

```
{
    "version":               0,
    "execution": {
        "numCPUs":           1,
        "numRuns":           100
    },
    "settings": {
        "combination": {
            ...
        },
        "regular": {
            ...
        }
    },
    "logging":               "all",
    "log_directory_name":    "startTime",
    "post": [
        "python compute_kpis.py",
        "python plot.py"
    ]
}
```


* the configuration file is a valid JSON file
* `version` is the version of the configuration file format; only 0 for now.
* `execution` specifies the simulator's execution
    * `numCPUs` is the number of CPUs (CPU cores) to be used; `-1` means "all available cores"
    * `numRuns` is the number of runs per simulation parameter combination
* `settings` contains all the settings for running the simulation.
    * `combination` specifies variations of parameters
    * `regular` specifies the set of simulator parameters commonly used in a series of simulations
* `logging` specifies what kinds of logs are recorded; `"all"` or a list of log types
* `log_directory_name` specifies how sub-directories for log data are named: `"startTime"` or `"hostname"`
* `post` lists the post-processing commands to run after the end of the simulation.

See `bin/config.json` to find  what parameters should be set and how they are configured.

## Additional Configs

### Application:

```

"app_backoffWindow":                           6000, 
"app_backoffWindowType":                       "equal",
```

* `app_backoffWindow`: Delays mote generation packet init process by this value in seconds. Orinally as soon as the mote would join the netowork it would start sending packets.
* `app_backoffWindowType`: "equal"|"leadder" - Select if motes start gradually joining the network, "leadder", or if they do it at the same time "equal".

### Deploy & connectivity
```

"deploy":                                      "linear", 
"motes_by_line":                               10,
"mote_distance":                               null, 
"roots":                                       [0],
"band":                                        "2.4Ghz"

```

* `deploy`: Type of deploy on Auto connectivity (linear|random|split-linear)
* `motes_by_line`: How many motes should be deployed on a single line. If numbers of motes are bigger than motes_by_line a additional rows are created until the mote list is complete.
* `mote_distance`: Specifies the distance between each mote, on both coordinates. If motes_by_line is set, mote_distance is overwriten to be square_side_distance/motes_by_line. If motes_by_line is null, mote_distance is used. **Motes_by_line takes precedence**
* `roots`: Array specifying root id's. **Maximumn 2 roots**
* `band`: Operation band, '2.4Ghz'|'868Mhz'


### more on connectivity models

#### using a *Auto* connectivity model

There are 3 different deploy methods available

* random: Same as Random connectivity model
* linear: Deploy motes with linear distance, all spaced with the same distance.
* split-linear: **Two Roots only** divides the deploy on two networks and splits them to left and right of the deploy area.

### more on applications

`AppPeriodic`, `AppBurst` and `AppPeriodicDelayed` are available.

### configuration file format validation

The format of the configuration file you pass is validated before starting the simulation. If your configuration file doesn't comply with the format, an `ConfigfileFormatException` is raised, containing a description of the format violation. The simulation is then not started.


## About 6TiSCH

| what         | where                                                                                                                                  |
|--------------|----------------------------------------------------------------------------------------------------------------------------------------|
| charter      | [http://tools.ietf.org/wg/6tisch/charters](http://tools.ietf.org/wg/6tisch/charters)                                                   |
| data tracker | [http://tools.ietf.org/wg/6tisch/](http://tools.ietf.org/wg/6tisch/)                                                                   |
| mailing list | [http://www.ietf.org/mail-archive/web/6tisch/current/maillist.html](http://www.ietf.org/mail-archive/web/6tisch/current/maillist.html) |
| source       | [https://bitbucket.org/6tisch/](https://bitbucket.org/6tisch/)                                                                         |
