create table if not exists templates(
    message text not null,
    word_num_condition integer not null,
    primary key(message)
);
