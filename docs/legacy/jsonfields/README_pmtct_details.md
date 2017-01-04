# PMTCT

## Identity details blob

- on hybrid - transferred from old to new system:

        "details": {
            "default_addr_type": "msisdn",
            "addresses": {
                "msisdn": {
                    "+27820000777": { "default": true }
                }
            },
            "mom_dob": "1954-05-29",
            "lang_code": "eng_ZA",
            "vumi_contact_key":"3e99804c1f1c4c9790517923bb8b318b",
            "source": "pmtct"
        }

- created and/or updated on new system:

        "details": {
            "default_addr_type": "msisdn",
            "addresses": {
                "msisdn": {
                    "+27820000111": {}
                }
            },
            "consent": true,
            "mom_dob": "1981-04-26",
            "pmtct": {
                "lang_code": "eng_ZA"
            },
            "source": "pmtct"
        }
