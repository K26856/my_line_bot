create table if not exists user_status_master(
    id text primary key,
    description text not null
);

create table if not exists scenario_master(
    id text primary key,
    description text not null
);

create table if not exists user_info(
    user_id text primary key,
    status text not null default "0000000",
    scenario text not null default "0000000",
    foreign key(status) references user_status_master(id),
    foreign key(scenario) references scenario_master(id)
);

create table if not exists patterns(
    user_status_condition text not null,
    scenario_condition text not null,
    recieve text not null,
    response text not null,
    next_user_status text not null,
    next_scenario text not null,
    primary key(user_status_condition, scenario_condition, recieve, response),
    foreign key(user_status_condition) references user_status_master(id),
    foreign key(scenario_condition) references scenario_master(id),
    foreign key(next_user_status) references user_status_master(id),
    foreign key(next_scenario) references scenario_master(id)
);
