create table if not exists words(
    id integer primary key,
    word text unique
);

create table if not exists sentences(
    id_sentence text unique not null
);

create table if not exists chains2(
    pre_word_id1 integer not null,
    pre_word_id2 integer not null,
    next_word_id integer not null,
    word_count integer default 1,
    primary key(pre_word_id1, pre_word_id2, next_word_id),
    foreign key(pre_word_id1) references words(id),
    foreign key(pre_word_id2) references words(id),
    foreign key(next_word_id) references words(id)
);

create table if not exists chains3(
    pre_word_id1 integer not null,
    pre_word_id2 integer not null,
    pre_word_id3 integer not null,
    next_word_id integer not null,
    word_count integer default 1,
    primary key(pre_word_id1, pre_word_id2, pre_word_id3, next_word_id),
    foreign key(pre_word_id1) references words(id),
    foreign key(pre_word_id2) references words(id),
    foreign key(pre_word_id3) references words(id),
    foreign key(next_word_id) references words(id)
);

create table if not exists chains4(
    pre_word_id1 integer not null,
    pre_word_id2 integer not null,
    pre_word_id3 integer not null,
    pre_word_id4 integer not null,
    next_word_id integer not null,
    word_count integer default 1,
    primary key(pre_word_id1, pre_word_id2, pre_word_id3, pre_word_id4, next_word_id),
    foreign key(pre_word_id1) references words(id),
    foreign key(pre_word_id2) references words(id),
    foreign key(pre_word_id3) references words(id),
    foreign key(pre_word_id4) references words(id),
    foreign key(next_word_id) references words(id)
);

create table if not exists chains5(
    pre_word_id1 integer not null,
    pre_word_id2 integer not null,
    pre_word_id3 integer not null,
    pre_word_id4 integer not null,
    pre_word_id5 integer not null,
    next_word_id integer not null,
    word_count integer default 1,
    primary key(pre_word_id1, pre_word_id2, pre_word_id3, pre_word_id4, pre_word_id5, next_word_id),
    foreign key(pre_word_id1) references words(id),
    foreign key(pre_word_id2) references words(id),
    foreign key(pre_word_id3) references words(id),
    foreign key(pre_word_id4) references words(id),
    foreign key(pre_word_id5) references words(id),
    foreign key(next_word_id) references words(id)
);
