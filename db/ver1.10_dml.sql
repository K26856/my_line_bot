insert
into user_status_master(id, description)
values 
("any"    , "using user_status_condition."),
("keep"   , "using next_user_status."),
("0000000", "default status"),
("0001000", "at home"),
("0002000", "Not at home");

insert
into scenario_master(id, description)
values 
("any"    , "using scenario condition."),
("keep"   , "using next_scenario."),
("0000000", "not in scenario");
