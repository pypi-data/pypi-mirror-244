import argparse
import os
from datetime import date
from enum import Enum
import logging

import bs4
import numpy as np
import pandas as pd
import requests


class Station(Enum):
    ILHA_SOLTEIRA = 1
    MARINOPOLIS = 2
    JUNQUEIROPOLIS = 3
    PARANAPUA = 4
    IRAPURU = 9
    POPULINA = 10
    SANTA_ADELIA_PIONEIROS = 11
    SANTA_ADELIA = 12
    BONANCA = 13
    ITAPURA = 14
    DRACENA = 19


class ParsingError(Exception):
    pass


def login(user: str, pw: str) -> requests.Session:
    url = 'http://clima.feis.unesp.br/valida.php'
    payload = {'usuario': user, 'senha': pw, 'enviar': 'Enviar'}
    logging.debug(f'logging in at {url} with payload {payload}')
    s = requests.Session()
    r = s.post(url, data=payload)
    r.raise_for_status()
    logging.debug(f'response status {r.status_code}')
    return s


# Fmt data: dd/MM/YYYY (03/06/2020)
def fetch_daily(session: requests.Session, dataini: str, datafim: str, estacao: Station) -> pd.DataFrame:
    url = 'http://clima.feis.unesp.br/recebe_formulario.php'
    payload = {'requireddataini': dataini, 'requireddatafim': datafim, 'estacao': estacao.value,
               'RadioGroup1': 'dados_diario', 'enviar': 'Enviar'}
    logging.debug(f'POST request for fetching daily data at {url} with payload {payload}')
    r = session.post(url, payload)
    r.raise_for_status()
    logging.debug(f'response status {r.status_code}')
    soup = bs4.BeautifulSoup(r.content, 'html5lib')
    table_daily: bs4.element.Tag = soup.find_all('table')[1]
    df = parse_daily(table_daily.prettify())
    return df


def parse_daily(daily_data: str) -> pd.DataFrame:
    headers = {0: 'Tmean', 1: 'Tmax', 2: 'Tmin',
               3: 'RHmean', 4: 'RHmax', 5: 'RHmin',
               6: 'Pmean', 7: 'Rn', 8: 'Rl', 9: 'G',
               10: 'PAR', 11: 'ETcat', 12: 'ET0pm', 13: 'ET0cat', 14: 'U2max',
               15: 'U2mean', 16: 'U2dir', 17: 'Rain', 18: 'Insolation'}
    
    logging.debug('reading table from html table daily_data')
    dfs = pd.read_html(daily_data, index_col=0, parse_dates=True, flavor='html5lib')
    try:
        # due to the html table structure in this page, it is necessary to concatenate 
        # along the columns to create a single table 
        df = pd.concat(dfs, axis=1, sort=False, ignore_index=True)
    except pd.errors.InvalidIndexError:
        logging.error('unable to parse response, credentials might be wrong')
        raise ParsingError('unable to parse response, check your login credentials')
    # trimming html table 'junk'
    df = df[2:-11]
    # filtering target column indices
    df = df[[i for i in range(19)]]
    df = df.rename(columns=pd.Series(headers))
    df.index.name = 'Date'
    df = df.replace('-', np.nan)
    return df


def main() -> None:
    parser = argparse.ArgumentParser(description='Scrape daily climate date from Canal CLIMA (https://clima.feis.unesp.br)')
    parser.add_argument('station', type=str,
                        help="""station name: ILHA_SOLTEIRA, MARINOPOLIS, JUNQUEIROPOLIS, PARANAPUA, IRAPURU, 
                        POPULINA, SANTA_ADELIA_PIONEIROS, SANTA_ADELIA, BONANCA, ITAPURA, DRACENA""")
    parser.add_argument('start', type=str, help='Start date dd/MM/YYYY (30/05/2020)')
    parser.add_argument('end', nargs='?', default=date.today().strftime('%d/%m/%Y'), type=str,
                        help='end date dd/MM/YYYY (03/05/2020). Default: today')
    parser.add_argument('-U', '--user', type=str,
                        help='override Canal CLIMA user set in the environment variable $USER_CLIMAFEIS')
    parser.add_argument('-P', '--pw', type=str,
                        help='override Canal CLIMA password set in the environment variable $PASSWD_CLIMAFEIS')
    parser.add_argument('-o', '--output', metavar='OUT', type=str,
                        help='output file. Default: <station>.csv')
    parser.add_argument('-l', '--log', type=str, help='output log file. Default: stdout')
    parser.add_argument('-v', '--verbose', action='count', default=1)
    args = parser.parse_args()
    args.verbose = 40 - (10*args.verbose) if args.verbose > 0 else 0
    FORMAT = '%(asctime)s %(levelname)s: %(message)s'
    DATEFMT = '%Y-%m-%d %H:%M:%S'
    logging.basicConfig(level=args.verbose, format=FORMAT, datefmt=DATEFMT, filename=args.log)

    if args.user or args.pw:
        logging.info('attempting login with overriden user and password parameters')
        s = login(args.user, args.pw)
    else:
        logging.info('attempting login with credentials stored in environment variables')
        s = login(os.environ['USER_CLIMAFEIS'], os.environ['PASSWD_CLIMAFEIS'])
    logging.info('fetching daily data')
    df = fetch_daily(s, args.start, args.end, Station[args.station])
    outputf = f'{args.output}.csv' if args.output else f'{args.station}.csv'
    logging.info(f'writing to {outputf}')
    df.to_csv(outputf)


if __name__ == '__main__':
    main()
