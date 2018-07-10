
# Xero-Map-Generator
Generates a Google Maps import file from a Contact Group in Xero

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
xero_map_gen --filter-contact-groups 'Direct' --filter-states 'TAS' --dump-file "stockists_tas_$(date +'%Y-%m-%d').csv" --config-file ~/.credentials/xmg_config.json
```
