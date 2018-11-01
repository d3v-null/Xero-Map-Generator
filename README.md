# Xero-Map-Generator
Generates a Google Maps import file from a Contact Group in Xero

[![Build Status](https://travis-ci.org/derwentx/Xero-Map-Generator.svg?branch=master)](https://travis-ci.org/derwentx/Xero-Map-Generator)
[![Maintainability](https://api.codeclimate.com/v1/badges/8fde8d3562484457ae4b/maintainability)](https://codeclimate.com/github/derwentx/Xero-Map-Generator/maintainability)
[![Test Coverage](https://api.codeclimate.com/v1/badges/8fde8d3562484457ae4b/test_coverage)](https://codeclimate.com/github/derwentx/Xero-Map-Generator/test_coverage)
[![Known Vulnerabilities](https://snyk.io/test/github/derwentx/Xero-Map-Generator/badge.svg)](https://snyk.io/test/github/derwentx/Xero-Map-Generator)
[![Say thanks icon](https://img.shields.io/badge/Say%20Thanks-!-1EAEDB.svg)](https://saythanks.io/to/derwentx)

```
        _  __    __  ___   ______
       | |/ /   /  |/  /  / ____/
       |   /   / /|_/ /  / / __
      /   |   / /  / /  / /_/ /
     /_/|_|  /_/  /_/   \____/

```

## Coverage

![codecoverage-svg-sunburst]( https://codecov.io/gh/derwentx/Xero-Map-Generator/branch/master/graphs/sunburst.svg)

## Usage

Create a config file with your API credentials
```
cat > ~/.credentials/xmg_config.json << EOF
{
    "XeroApiConfig":{
        "consumer_key": "XXXXXXXXXX",
        "rsa_key_path": "~/.credentials/privatekey.pem"
    }
}
EOF
```

Create a script if you are generating multiple csv files like so

```
xero_map_gen --filter-contact-groups 'ACME Agencies|Joli Agencies|KAS Agencies' --filter-states 'NSW|ACT' --dump-path "stockists_nsw_$(date +'%Y-%m-%d').csv" --config-path ~/.credentials/xmg_config.json && \
xero_map_gen --filter-contact-groups 'Foo Agencies'  --filter-states 'QLD' --dump-path "stockists_qld_$(date +'%Y-%m-%d').csv" --config-path ~/.credentials/xmg_config.json && \
xero_map_gen --filter-contact-groups 'Bar Agencies' --dump-path "stockists_vic_$(date +'%Y-%m-%d').csv" --config-path ~/.credentials/xmg_config.json && \
xero_map_gen --filter-contact-groups 'Foobar Agencies' --dump-path "stockists_sa_$(date +'%Y-%m-%d').csv" --config-path ~/.credentials/xmg_config.json && \
xero_map_gen --filter-contact-groups 'Direct' --filter-states 'TAS' --dump-path "stockists_tas_$(date +'%Y-%m-%d').csv" --config-path ~/.credentials/xmg_config.json && \
xero_map_gen --filter-contact-groups 'Direct' --filter-states 'WA' --dump-path "stockists_wa_$(date +'%Y-%m-%d').csv" --config-path ~/.credentials/xmg_config.json && \
xero_map_gen --filter-contact-groups 'Direct' --filter-states 'NT' --dump-path "stockists_nt_$(date +'%Y-%m-%d').csv" --config-path ~/.credentials/xmg_config.json
read -p "Maps Succesfully Generated, press enter to continue"
```
