# Xero-Map-Generator
Generates a Google Maps import file from a Contact Group in Xero

[![Build Status](https://travis-ci.org/derwentx/Xero-Map-Generator.svg?branch=master)](https://travis-ci.org/derwentx/Xero-Map-Generator)
[![Say thanks icon](https://img.shields.io/badge/Say%20Thanks-!-1EAEDB.svg)](https://saythanks.io/to/derwentx)


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

## Examples

```
xero_map_gen --filter-contact-groups 'Gordon Cohen Agencies|Joli Agencies|KAS Agencies' --filter-states 'NSW|ACT' --dump-file "stockists_nsw_$(date +'%Y-%m-%d').csv" --config-file ~/.credentials/xmg_config.json
xero_map_gen --filter-contact-groups 'Joli Agencies'  --filter-states 'QLD' --dump-file "stockists_qld_$(date +'%Y-%m-%d').csv" --config-file ~/.credentials/xmg_config.json
xero_map_gen --filter-contact-groups 'Louise Cargill' --dump-file "stockists_vic_$(date +'%Y-%m-%d').csv" --config-file ~/.credentials/xmg_config.json
xero_map_gen --filter-contact-groups 'Jenny Atkins' --dump-file "stockists_sa_$(date +'%Y-%m-%d').csv" --config-file ~/.credentials/xmg_config.json
xero_map_gen --filter-contact-groups 'Direct' --filter-states 'TAS' --dump-file "stockists_tas_$(date +'%Y-%m-%d').csv" --config-file ~/.credentials/xmg_config.json
xero_map_gen --filter-contact-groups 'Direct' --filter-states 'WA' --dump-file "stockists_wa_$(date +'%Y-%m-%d').csv" --config-file ~/.credentials/xmg_config.json
xero_map_gen --filter-contact-groups 'Direct' --filter-states 'NT' --dump-file "stockists_nt_$(date +'%Y-%m-%d').csv" --config-file ~/.credentials/xmg_config.json
```
