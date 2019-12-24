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
```bash
cat > ~/.credentials/xmg_config.json << EOF
{
    "XeroApiConfig":{
        "consumer_key": "XXXXXXXXXX",
        "rsa_key_path": "~/.credentials/privatekey.pem"
    }
}
EOF
```

Use [the instructions for the pyxero API](https://github.com/freakboy3742/pyxero) to generate your private application credentials

To Generate a single xml file
```bash
xero_map_gen --config-dir ~/.credentials --config-path xmg_config.json --filter-contact-groups 'Support Clients (monthly)'
```

Create a script if you are generating multiple csv files like so

```bash
#!/bin/bash
cd /mnt/c/Users/User/Desktop/Maps/

rm warnings.txt
xero_map_gen --filter-contact-groups 'Direct' --filter-states 'NT' --dump-path "stockists_nt_$(date +'%Y-%m-%d').csv" --config-path ~/.credentials/xmg_config.json "${@:2}" 
xero_map_gen --filter-contact-groups 'Direct|Victoria' --filter-states 'VIC' --dump-path "stockists_vic_$(date +'%Y-%m-%d').csv" --config-path ~/.credentials/xmg_config.json "${@:2}" && \
xero_map_gen --filter-contact-groups 'Direct|Country NSW|Sydney Metro' --filter-states 'NSW|ACT' --dump-path "stockists_nsw_$(date +'%Y-%m-%d').csv" --config-path ~/.credentials/xmg_config.json "${@:2}" && \
xero_map_gen --filter-contact-groups 'Direct|QLD'  --filter-states 'QLD' --dump-path "stockists_qld_$(date +'%Y-%m-%d').csv" --config-path ~/.credentials/xmg_config.json "${@:2}" && \
xero_map_gen --filter-contact-groups 'Direct|South Australia' --filter-states 'SA' --dump-path "stockists_sa_$(date +'%Y-%m-%d').csv" --config-path ~/.credentials/xmg_config.json "${@:2}" && \
xero_map_gen --filter-contact-groups 'Direct' --filter-states 'WA' --dump-path "stockists_wa_$(date +'%Y-%m-%d').csv" --config-path ~/.credentials/xmg_config.json "${@:2}" && \
xero_map_gen --filter-contact-groups 'Direct' --filter-states 'TAS' --dump-path "stockists_tas_$(date +'%Y-%m-%d').csv" --config-path ~/.credentials/xmg_config.json "${@:2}" && \
read -n 1 -p "Maps Succesfully Generated, press enter to continue"
```
