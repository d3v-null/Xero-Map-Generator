
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
python main.py --map-contact-group 'Gordon Cohen Agencies' --dump-file "stockists_nsw_$(date +'%Y-%m-%d').csv" --config-file ~/.credentials/xmg_config.json
```
