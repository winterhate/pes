import csv
import requests
from io import StringIO
import datetime


def dispDigest():
    d = digest()
    return (
        f"Tak štěk pes dnes, {d['pes_date']:%d.%m.%Y}:\n"
        f"Stupeň:            {d['pes_tier']}\n" 
        f"Skóre:             {d['pes_value']}\n"
        f"R:                 {d['pes_simple_r']:.2f}\n"
        f"Testy:             {d['tests_daily']}\n"
        f"Nově pozitivní:    {d['infected_daily']}\n"
        f"Podíl pozitivních: {d['positive_share']*100:.2f}%\n"
        f"Hospitalizovaní:   {d['in_hospital']}\n"
        f"Aktivní případy:   {d['active_cases']}\n"
    )


def digest():
    pes = pesData()[-1]
    overview = overviewData()[-1]
    return {
        'pes_date': datetime.datetime.strptime(pes['datum_zobrazeni'], '%Y-%m-%d').date(),
        'pes_value': int(pes['body']),
        'pes_tier': tier(int(pes['body'])),
        'pes_simple_r': float(pes['simple_r']),
        'deaths_total': int(overview['umrti']),
        'active_cases': int(overview['aktivni_pripady']),
        'in_hospital': int(overview['aktualne_hospitalizovani']),
        'infected_daily': int(overview['potvrzene_pripady_vcerejsi_den']),
        'tests_daily': int(overview['provedene_testy_vcerejsi_den']),
        'positive_share': int(overview['potvrzene_pripady_vcerejsi_den'])
                          / int(overview['provedene_testy_vcerejsi_den'])
    }


def tier(points):
    if points < 21:
        return 1
    elif points < 41:
        return 2
    elif points < 61:
        return 3
    elif points < 74:
        return 4
    else:
        return 5


pesDataUrl = 'https://share.uzis.cz/s/BRfppYFpNTddAy4/download?path=%2F&files=pes_CR.csv'


def pesData():
    return collectCsvRows(pesDataUrl, ';')


overviewDataUrl = 'https://onemocneni-aktualne.mzcr.cz/api/v2/covid-19/zakladni-prehled.csv'


def overviewData():
    return collectCsvRows(overviewDataUrl, ',')


def collectCsvRows(url, delimiter):
    return collectRows(csv.DictReader(asIterable(requests.get(url)), delimiter=delimiter))


def collectRows(reader):
    rows = []
    for row in reader:
        rows.append(row)
    return rows


def asIterable(response):
    asText = removeBom(response.text)
    return StringIO(asText)


def removeBom(text):
    return text[1:]
