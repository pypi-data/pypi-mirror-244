# climafeis
CLI Python application for scraping daily climate data from [Canal CLIMA](https://clima.feis.unesp.br) [UNESP Ilha Solteira](https://www.feis.unesp.br/) using [requests](https://requests.readthedocs.io/en/latest/) and [BeautifulSoup 4](https://www.crummy.com/software/BeautifulSoup/).  

### Installation
1. Make sure Python 3.8 or higher and pip are installed
1. Run `pip install climafeis`

### Development
1. Check Python's version `python -V`
1. Install Python 3.8 or higher and pip, if they aren't already installed:

    - Windows `winget install Python.Python.3.X` (replace X with the desired minor version)
    - Ubuntu based distros `apt install python3 python3-pip`
    - Arch based distros `pacman -S python python-pip`
    - Fedora `dnf install python3 python3-pip`

1. [Install poetry](https://python-poetry.org/docs/#installation) 
1. Clone this repo `git clone https://github.com/joaofauvel/climafeis.git && cd climafeis`
1. Install requirements `poetry install`

### Output headers
| Header     | Description                                           |
| ---------- | ----------------------------------------------------- |
| Date       | Observation date (dd-mm-yyyy)                         |
| Tmean      | Mean temperature (ºC)                                 |
| Tmax       | Max temperature (ºC)                                  |
| Tmin       | Min temperature (ºC)                                  |
| RHmean     | Mean relative humidity (%)                            |
| RHmax      | Max relative humidity (%)                             |
| RHmin      | Min relative humidity (%)                             |
| Pmean      | Mean pressure (kPa)                                   |
| Rn         | Net radiation (MJ/m^2*day)                            |
| Rl         | Liquid radiation (MJ/m^2*day)                         |
| G          | Soil heat flux (MJ/m^2*day)                           |
| PAR        | (μmoles/m^2)                                          |
| ETcat      | Evapotranspiration Class A Tank (mm/day)              |
| ET0pm      | Reference evapotranspiration Penman–Monteith (mm/day) |
| ET0cat     | Reference evapotranspiration Class A Tank (mm/day)    |
| U2max      | Max windspeed at 2 meters (m/s)                       |
| U2mean     | Mean windspeed at 2 meters (m/s)                      |
| U2dir      | Wind direction at 2 meters (º)                        |
| Rain       | Rainfall (mm)                                         |
| Insolation | Solar insolation (h/day)                              |  

[Reference](https://www.fao.org/3/x0490e/x0490e06.htm)

### Usage
Daily data from ILHA_SOLTEIRA station from 30/05/2020 (dd/MM/YYYY) to 03/05/2020  
`climafeis ILHA_SOLTEIRA 30/05/2020 03/06/2020`

Daily data from MARINOPOLIS station from 30/05/2020 to today  
`climafeis MARINOPOLIS 30/05/2020`

Daily data from ILHA_SOLTEIRA station from 30/05/2020 to today, supplying username and password  
`climafeis ILHA_SOLTEIRA 30/05/2020 -U user -P password`  

---

    usage: climafeis [-h] [-U USER] [-P PW] [-o OUT] [-l LOG] [-v] station start [end]

    Scrape daily climate date from Canal CLIMA (https://clima.feis.unesp.br)

    positional arguments:
    station               station name: ILHA_SOLTEIRA, MARINOPOLIS, JUNQUEIROPOLIS, PARANAPUA, IRAPURU, 
                            POPULINA, SANTA_ADELIA_PIONEIROS, SANTA_ADELIA, BONANCA, ITAPURA, DRACENA
    start                 start date dd/MM/YYYY (30/05/2020)
    end                   end date dd/MM/YYYY (03/05/2020). Default: today

    options:
    -h, --help            show this help message and exit
    -U USER, --user USER  override Canal CLIMA user set in the environment variable $USER_CLIMAFEIS
    -P PW, --pw PW        override Canal CLIMA password set in the environment variable $PASSWD_CLIMAFEIS
    -o OUT, --output OUT  output file. Default: <station>.csv
    -l LOG, --log LOG     output log file. Default: stdout
    -v, --verbose
