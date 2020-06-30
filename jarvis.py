import click
import requests
from addict import Dict

@click.command()
@click.option('--source', prompt=True)
@click.option('--dest', prompt=True)
@click.option('--date', prompt=True, type=click.DateTime(['%Y-%m-%d']))
@click.option('--count', prompt=True, type=click.IntRange(1, 10))
@click.option('--site', '-s', multiple=True, default=["easemytrip", "expedia"])
@click.option('--all', default=False)
@click.argument('api', type=click.Choice(['scrape', 'report']))
def cli(api, site, source, dest, date, count, all):
    date = date.date()
    base = 'https://codetrippers.herokuapp.com/api/'
    if(api == 'scrape'):
        # tell the server to scrape the data
        url = base + ''
        site = list(site)
        payload = Dict()
        payload.source = source
        payload.dest = dest
        payload.date = date
        payload.sites = site        
        payload.count = count
        r = requests.post(url, data=payload)
        click.echo(r.url)
        click.echo(r.json())
    else:
        # generate report
        url = base + ''
        site = list(site)
        payload = Dict()
        payload.source = source
        payload.dest = dest
        payload.date = date
        payload.sites = site        
        payload.count = count
        r = requests.get(url, params=payload)
        click.echo(r.url)
        click.echo(r.json())

if __name__ == '__main__':
    cli()