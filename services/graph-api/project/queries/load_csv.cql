WITH $url AS url 
CALL apoc.load.csv(url, {
    skip:0, 
    header:true, 
    mapping:{
        individual_id: {type:'int'},
        individual_id: {type:'int'},
        minor: {type:'bool'},
        age: {type:'str'},
        male: {type:'bool'},
        nationality: {type:'str'},
        number_previous_arrests: {type: 'str'},
        perpetrator_affiliation: {type: 'str'},
        perpetrator_affiliation_detail: {type: 'str'},
        war_tribunal: {type: 'bool'},
        violence: {type: 'str'},
        method: {type: 'str'},
        interrogation: {type: 'bool'},
        torture: {type: 'bool'},
        mistreatment: {type: 'bool'},
        press: {type: 'bool'},
        start_date_daily: {type: 'date'},
        end_date_daily: {type: 'date'},
        start_date_monthly: {type: 'date'},
        end_date_monthly: {type: 'date'},
        page: {type: 'str'},
        additional_comments: {type: 'str'}}
    })
YIELD lineNo, map, list
MERGE (v:Victim {
    individual_id: map.individual_id,
    group_id: map.group_id,
    first_name: map.first_name,
    last_name: map.last_name,
    age: map.age,
    minor: map.minor,
    male: map.male,
    nationality: map.nationality,
    number_previous_arrests: map.number_previous_arrests,
    occupation: map.occupation,
    occupation_detail: map.occupation_detail,
    victim_affiliation: map.victim_affiliation,
    victim_affiliation_detail: map.victim_affiliation_detail,
    targeted: map.targeted
    })
MERGE (p:Perpetrator {
    perpetrator_affiliation: map.perpetrator_affiliation,
    perpetrator_affiliation_detail: map.perpetrator_affiliation_detail,
    war_tribunal: map.war_tribunal
})
MERGE (e:ViolenceEvent {
    violence: map.violence,
    method: map.method,
    interrogation: map.interrogation,
    torture: map.torture,
    mistreatment: map.mistreatment,
    press: map.press,
    start_date_daily: map.start_date_daily,
    end_date_daily: map.end_date_daily,
    start_date_monthly: map.start_date_monthly,
    end_date_monthly: map.end_date_monthly,
    page: map.page,
    additional_comments: map.additional_comments
})