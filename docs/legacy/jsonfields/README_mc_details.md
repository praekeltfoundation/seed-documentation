# MomConnect

## Identity details blob

- when registered for all services on MomConnect, an identity's details blob might look as follow:

        "details": {
            "default_addr_type": "msisdn",
            "addresses": {
                "msisdn": {
                    "+27820001008": {"default": true}
                }
            },
            "lang_code": "eng_ZA",
            "consent": true,
            "sa_id_no": "5101025009086",
            "mom_dob": "2051-01-02",
            "source": "clinic",
            "last_mc_reg_on": "clinic",
            "chw": {
                "redial_sms_sent": false
            },
            "clinic": {
                "redial_sms_sent": true
            },
            "public": {
                "redial_sms_sent": false
            },
            "nurseconnect": {
                "faccode": "123456",
                "facname": "WCL clinic",
                "id_type": "sa_id",
                "sa_id_no": "5101025009086",
                "dob": "1951-01-02",
                "redial_sms_sent": false
            }
        }
