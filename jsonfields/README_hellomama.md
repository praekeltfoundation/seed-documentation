# HelloMama Hub
HelloMama Hub (Registration and Change) service

## Registration Information

    data: {
        stage: "prebirth",  // | "postbirth"
        mother_id: “cb245673-aa41-4302-ac47-10000000001",
        data: {
            msg_receiver: “cb245673-aa41-4302-ac47-10000000002",
            receiver_id: “cb245673-aa41-4302-ac47-10000000002",
            operator_id: “cb245673-aa41-4302-ac47-10000000003",
            gravida: “3”,
            language: "ibo_NG",
            msg_type: “text”
    		// if user_id
    		user_id:  "cb245673-aa41-4302-ac47-00000000002",  // ?
    		// if msg_type === ‘audio’
    		voice_times: ”9_11”, // “2_5”
    		voice_days: “tue_thu”,  // “mon_wed”
    		// if pregnancy_status === ‘prebirth’
    		last_period_date: “20150212”,
    		// if pregancy_status === ‘post birth’
    		baby_dob: “20160713”
        }
    }

## Change Information

    // switch to baby messages
    data: {
        mother_id": "3f7c8851-5204-43f7-af7f-005059992222",
        "action": "change_baby",
        "data": {}
    }

    // change message format (voice to text or vice versa)
    data: {
        "mother_id": "3f7c8851-5204-43f7-af7f-005059992222",
        "action": "change_messaging",
        "data": {
            "msg_type": “audio”,  // | “text”
            "voice_days": “tue_thu”,  // “mon_wed” | null
            "voice_times": ”9_11”  // “2_5” | null
        }
    }

    // change language
    'data': {
        "mother_id": "3f7c8851-5204-43f7-af7f-005059992222",
        "action": "change_language",
        "data": {
            "household_id": null,
            "new_language": "pcm_NG"
        }
    }

    // unsubscribe household (part of optout process)
    data: {
        "mother_id": "3f7c8851-5204-43f7-af7f-005059992222",
        "action": "unsubscribe_household_only",
        "data": {
            "household_id": "3f7c8851-5204-43f7-af7f-005059993333",
            "reason": “other” // “miscarriage” | “not_useful” | “stillborn” | “baby_death”
        }
    }

    // unsubscribe mother (part of optout process)
    data: {
        "mother_id": "3f7c8851-5204-43f7-af7f-005059992222",
        "action": "unsubscribe_mother_only",
        "data": {
            "household_id": "3f7c8851-5204-43f7-af7f-005059993333",
            "reason": “not_useful” // | “other”
        }
    }

    // subscribe to loss messages
    data: {
        "mother_id": "3f7c8851-5204-43f7-af7f-005059992222",
        "action": "change_loss",
        "data": {
            "reason": “miscarriage”
        }
    }
