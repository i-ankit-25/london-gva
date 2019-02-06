import datetime

from dataflows import Flow, load, dump_to_path, PackageWrapper, ResourceWrapper,printer, unpivot


def set_format_and_name(package: PackageWrapper):
    package.pkg.descriptor['title'] = 'London Gross Value Added (GVA)'
    package.pkg.descriptor['name'] = 'gva'
    # Change path and name for the resource:
    package.pkg.descriptor['resources'][0]['path'] = 'data/gva.csv'
    package.pkg.descriptor['resources'][0]['name'] = 'gva'

    yield package.pkg
    res_iter = iter(package)
    first: ResourceWrapper = next(res_iter)
    yield first.it
    yield from package

def filter_gva(rows):
    for row in rows:
        if row['NUTS code'] is not '':
            yield row

def remove_duplicates(rows):
    seen = set()
    for row in rows:
        line = ''.join('{}{}'.format(key, val) for key, val in row.items())
        if line in seen: continue
        seen.add(line)
        yield row

unpivot_fields = [
    {'name': '1997', 'keys': {'Year': '1997-01-01'}},
    {'name': '1998', 'keys': {'Year': '1998-01-01'}},
    {'name': '1999', 'keys': {'Year': '1999-01-01'}},
    {'name': '2000', 'keys': {'Year': '2000-01-01'}},
    {'name': '2001', 'keys': {'Year': '2001-01-01'}},
    {'name': '2002', 'keys': {'Year': '2002-01-01'}},
    {'name': '2003', 'keys': {'Year': '2003-01-01'}},
    {'name': '2004', 'keys': {'Year': '2004-01-01'}},
    {'name': '2005', 'keys': {'Year': '2005-01-01'}},
    {'name': '2006', 'keys': {'Year': '2006-01-01'}},
    {'name': '2007', 'keys': {'Year': '2007-01-01'}},
    {'name': '2008', 'keys': {'Year': '2008-01-01'}},
    {'name': '2009', 'keys': {'Year': '2009-01-01'}},
    {'name': '2010', 'keys': {'Year': '2010-01-01'}},
    {'name': '2011', 'keys': {'Year': '2011-01-01'}},
    {'name': '2012', 'keys': {'Year': '2012-01-01'}},
    {'name': '2013', 'keys': {'Year': '2013-01-01'}},
    {'name': '20143', 'keys': {'Year': '2014-01-01'}}
]

extra_keys = [
    {'name': 'Year', 'type': 'date'}
]
extra_value = {'name': 'Value', 'type': 'number'}

def london_gva(link):
    Flow(
        load(link,
             sheet=3),
        filter_gva,
        unpivot(unpivot_fields, extra_keys, extra_value),
        remove_duplicates,
        set_format_and_name,
        dump_to_path(),
        printer(num_rows=1)
    ).process()



london_gva('https://data.london.gov.uk/download/gross-value-added-and-gross-disposable-household-income/922c4abe-d75e-4c58-b6ed-9dace9f933a3/GVA-GDHI-nuts3-regions-uk.xls')
