create table if not exists words(
    id integer primary key,
    word text unique
);

create table if not exists markov(
    pre_word integer,
    pre_word2 integer,
    next_word integer,
    word_count integer default 1,
    primary key(pre_word, pre_word2, next_word),
    foreign key(pre_word) references words(id),
    foreign key(pre_word2) references words(id),
    foreign key(next_word) references words(id)
);
