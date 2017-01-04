# FamilyConnect Hub
FamilyConnect Hub (Registration and Change) service

## Registration Information

Healthworker registration

    data: {
        stage: 'prebirth',
        mother_id: "cb245673-aa41-4302-ac47-10000000001",
        data: {
            hoh_id: "cb245673-aa41-4302-ac47-10000000002",
            receiver_id: "cb245673-aa41-4302-ac47-10000000002",
            operator_id: "cb245673-aa41-4302-ac47-10000000003",
            language: “xog_UG”,
            msg_type: "text",
            last_period_date: “20150421”,
            msg_receiver: “trusted_friend”,
            hoh_name: “Isaac”,  // household head name,
            hoh_surname: “Mbire”,
            mama_name: “Mary”,
            mama_surname: “Nalule”,
            mama_id_type: ”other”,
    		// if state_id_type === ‘ugandan_id’
    		mama_id_no: “444”,
    		// else
    		mama_dob = “19820513”
        }    
    }

Public registration

    data: {
        stage: 'prebirth',
        mother_id: "cb245673-aa41-4302-ac47-10000000001",
        data: {
            hoh_id: "cb245673-aa41-4302-ac47-10000000002",
            receiver_id: "cb245673-aa41-4302-ac47-10000000002",
            operator_id: null,
            language: “eng_UG”,
            msg_type: "text",
            last_period_date: “20150421”,
            msg_receiver: “mother_to_be”,
        }
    }

## Change Information

    // change language
    data: {
        "mother_id": uuid,
        "action": "change_language",
        "data": {
            "new_language": “xog_UG”
        }
    }

    // switch to loss messages
    data: {
        "mother_id": uuid,
        "action": "change_loss",
        "data": {
            "reason": “miscarriage” // | “stillborn” | “baby_death”  
        }
    }

    // unsubscribe mother
    data: {
        "mother_id": uuid,
        "action": "unsubscribe",
        "data": {
            "reason": “other” // “not_useful”
        }
    }
