create table if not exists status_master(
    id text primary key,
    description text not null
);

create table if not exists user_status(
    line_id text primary key,
    status_id text not null,
    foreign key(status_id) references status_master(id)
);

create table if not exists patterns(
    pre_status text not null,
    recieve text not null,
    response text not null,
    post_status text not null,
    primary key(pre_status, recieve, response),
    foreign key(pre_status) references status_master(id),
    foreign key(post_status) references status_master(id)
);
