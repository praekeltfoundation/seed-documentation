# Identity service

## Create identity

- 'create_identity' invoked with address parameter `{"msisdn": "+27820001001"}` results in base payload:

        "data": {
            "details": {
                "default_addr_type": "msisdn",
                "addresses": {
                    "msisdn": {
                        "+27820001001": { "default": true }
                    }
                }
            }
        }

- communicate_through_id and/or operator_id added to base payload (specific to **HelloMama**):

        "data": {
            "details": {
                "default_addr_type": "msisdn",
                "addresses": {
                    "msisdn": {
                        "+27820001001": { "default": true }
                    }
                }
            },
            "communicate_through": "cb245673-aa41-4302-ac47-9092222222",
            "operator": "cb245673-aa41-4302-ac47-00000000007"
        }

## Update identity
(whole identity object that includes changed fields passed as argument to 'update_identity')

#### Change of number (msisdn) examples
- HELLOMAMA

        'data': {
            "id": "3f7c8851-5204-43f7-af7f-005059992222",
            "version": 1,
            "details": {
                "default_addr_type": "msisdn",
                "addresses": {
                    "msisdn": {
                        "+2345059992222": {}  // new msisdn
                    }
                },
                "receiver_role": "mother",
                "linked_to": null,
                "preferred_msg_type": "audio",
                "preferred_language": "ibo_NG",
                "preferred_msg_days": "tue_thu",
                "preferred_msg_times": "9_11"
            },
            "created_at": "2016-08-05T06:13:29.693272Z",
            "updated_at": "2016-08-05T06:13:29.693298Z",
        }

- FAMILYCONNECT

        'data':  {
            "id": "cb245673-aa41-4302-ac47-0000000333",
            "version": 1,
            "details": {
                "default_addr_type": "msisdn",
                "addresses": {
                    "msisdn": {
                        "+256720000222": {}  // new msisdn
                    }
                },
                "role": "trusted_friend",
                "mother_id": "identity-uuid-09",
                "preferred_msg_type": "text"
            },
            "created_at": "2016-08-05T06:13:29.693272Z",
            "updated_at": "2016-08-05T06:13:29.693298Z",
        }

- NURSECONNECT

        "data": {
            "url": "http://is/api/v1/identities/cb245673-aa41-4302-ac47-00000001003/",
            "id": "cb245673-aa41-4302-ac47-00000001003",
            "version": 1,
            "details": {
                "default_addr_type": "msisdn",
                "addresses": {
                    "msisdn": {
                        "+27820001003": {"inactive": true},  // old number
                        "+27820001001": {"default": true}  // new number
                    }
                },
                "nurseconnect": {
                    "faccode": "123456",
                    "facname": "WCL clinic",
                    "id_type": "sa_id",
                    "sa_id_no": "5101025009086",
                    "dob": "1951-01-02",
                    "redial_sms_sent": true
                }
            },
            "created_at": "2016-08-05T06:13:29.693272Z",
            "updated_at": "2016-08-05T06:13:29.693298Z",
        }

Here's a more complex example where number changed from 27820001005 to previously opted out 27820001012:

    "data": {
        "url": "http://is/api/v1/identities/cb245673-aa41-4302-ac47-00000001005/",
        "id": "cb245673-aa41-4302-ac47-00000001005",
        "version": 1,
        "details": {
            "default_addr_type": "msisdn",
            "addresses": {
                "msisdn": {
                    "+27820001005": { "inactive": true },
                    "+27820001012": {
                        "default": true,
                        "optedout": true  // this will be unset by is.optin
                    }
                }
            },
            "nurseconnect": {
                "faccode": "123456",
                "facname": "WCL clinic",
                "id_type": "sa_id",
                "sa_id_no": "5101025009086",
                "dob": "1964-07-11"
            }
        },
        "created_at": "2016-08-05T06:13:29.693272Z",
        "updated_at": "2016-08-05T06:13:29.693298Z",
    }

#### Change of facility code/name example

- NURSECONNECT

        "data": {
            "url": "http://is/api/v1/identities/cb245673-aa41-4302-ac47-00000001003/",
            "id": "cb245673-aa41-4302-ac47-00000001003",
            "version": 1,
            "details": {
                "default_addr_type": "msisdn",
                "addresses": {
                    "msisdn": {
                        "+27820001003": {}
                    }
                },
                "nurseconnect": {
                    "faccode": "234567",
                    "facname": "OLT clinic",
                    "id_type": "sa_id",
                    "sa_id_no": "5101025009086",
                    "dob": "1951-01-02",
                    "redial_sms_sent": true
                }
            },
            "created_at": "2016-08-05T06:13:29.693272Z",
            "updated_at": "2016-08-05T06:13:29.693298Z",
        }


## Optout identity

- HELLOMAMA

        data: { 	
        	"optout_type": "stop",  // default is 'stop'
            "identity": "3f7c8851-5204-43f7-af7f-005059997777",
            "reason": "miscarriage",  // | “other” | “stilborn” | “baby_death” | “not_useful”  (default is ’unknown’)
            "address_type": "msisdn",  // default is ‘msisdn’
            "address": "+2345059997777",
            "request_source": "ussd_public",  // | “voice_public”
            "requestor_source_id": "0170b7bb-978e-4b8a-35d2-662af5b6daee"
        }

- FAMILYCONNECT

        data: { 	
        	"optout_type": "stop",
            "identity": "3f7c8851-5204-43f7-af7f-005059997777",
            "reason": "miscarriage",  // | “other” | “stilborn” | “baby_death” | “not_useful”  (default is ’unknown’)
            "address_type": "msisdn",
            "address": "+2345059997777",
            "request_source": "ussd_public" // | “voice_public”
            "requestor_source_id": "0170b7bb-978e-4b8a-35d2-662af5b6daee"
        }

- NURSECONNECT

        "data": {
            "optout_type": "stop",
            "identity": "cb245673-aa41-4302-ac47-00000001003",
            "reason": "unknown",
            "address_type": "msisdn",
            "address": "+27820001003",
            "request_source": "sms_nurse",
            "requestor_source_id": "0170b7bb-978e-4b8a-35d2-662af5b6daee"
        }

- MOMCONNECT

        "data": {
            "optout_type": "stop",
            "identity": "cb245673-aa41-4302-ac47-00000001002",
            "reason": "unknown",
            "address_type": "msisdn",
            "address": "+27820001002",
            "request_source": "sms_inbound",  // | "ussd_pmtct" | "sms_pmtct"
            "requestor_source_id": "0170b7bb-978e-4b8a-35d2-662af5b6daee"
        }
