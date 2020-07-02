import click
import requests
from addict import Dict


def _generate_output(data):
    for res in data:
        if True:
            yield res.__str__() + '\n\n'

def check():
    data = {
    "origin": "DEL",
    "destination":"BOM",
    "departureDate":"2020-07-07",
    "arrivalDate": null,
    "adults":"1",
    "children":"0",
    "infants":"0",
    "isDomestic":"true",
    "isOneway":"true",
    "airline":"undefined",
    "cabin":"0",
    "currencyCode":"INR"
    }
    r = requests.get(url, data=data)
    print(r.json())

def calc(data):
    report = Dict()
    discounts = 0
    types = set()
    flights = set()
    for res in data:
        discounts += 1 if res.get('discount') > 0 else 0
        if res.get('flightName'):
            flights.add(res.get('flightName'))
        if res.get('couponCode'):
            types.add(res.get('couponCode'))
        pass
    report.discounts = discounts
    report.types_of_discounts = types if len(types) else ''
    report.flights = flights if len(flights) else ''
    return report

@click.command()
@click.option('--source', prompt=True)
@click.option('--dest', prompt=True)
@click.option('--ddate', prompt=True, type=click.DateTime(['%Y-%m-%d']))
@click.option('--adate', prompt=True, type=click.DateTime(['%Y-%m-%d']))
@click.option('--count', prompt=True, type=click.IntRange(1, 10))
@click.option('--site', '-s', multiple=True, default=["easemytrip", "expedia"])
@click.option('--all', default=False)
@click.option('--oneway', default=True)
@click.argument('api', type=click.Choice(['scrape', 'report']))
def cli(api, site, source, dest, ddate, adate, count, all, oneway):
    adate = adate.date()
    ddate = ddate.date()
    adate = adate.strftime('%Y-%m-%d')
    ddate = ddate.strftime('%Y-%m-%d')
    # base = 'https://codetrippers.herokuapp.com/api/'
    base = 'https://flights-easemytrip.herokuapp.com'
    if(api == 'scrape'):
        # tell the server to scrape the data
        url = base + '/getFlights'
        site = list(site)
        payload = Dict()
        payload.origin = source
        payload.destination = dest
        payload.departureDate = ddate
        payload.arrivalDate = adate
        # payload.sites = site        
        payload.adults = count
        payload.isOneway = 'true' if oneway else 'false'
        r = requests.post(url, data=payload.to_dict())
        click.secho('\n' + payload.origin + ' -> ' + payload.destination, fg='green')
        click.secho('Report generated: ', fg='yellow')
        data = r.json()
        report = calc(data)
        for key in report:
            click.secho('\t' + key + ': ' + report[key].__str__(), fg = 'blue')
        click.secho('\nHead', fg='yellow')
        click.echo_via_pager(_generate_output(data))
    else:
        # generate report
        url = base + ''
        site = list(site)
        payload = Dict()
        payload.source = source
        payload.dest = dest
        payload.date = ddate
        payload.sites = site        
        payload.count = count
        r = requests.get(url, params=payload)
        click.echo(r.url)
        click.echo_via_pager(_generate_output(r.json()))

if __name__ == '__main__':
    cli()
