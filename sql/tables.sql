create table if not exists users (
    id serial primary key,
    username text not null unique,
    password text not null,
    created_at timestamp not null default current_timestamp,
    last_login timestamp not null default current_timestamp,
    is_logged_in boolean not null default false
);

create table if not exists sources (
    id serial primary key,
    name text not null unique,
    domian text not null unique
);

create table if not exists books (
    id serial primary key,
    title text not null,
    author text not null,
    source_id int not null,
    introduction text not null,
    tags text not null default '',
    store_path text not null,
    created_at timestamp not null default current_timestamp,
    last_updated timestamp not null default current_timestamp,
    is_complete boolean not null default false,
    latest_chapter text default null,
    foreign key (source_id) references sources(id)
);

create table if not exists bookshelf(
    user_id int not null,
    book_id int not null,
    is_read_begin boolean not null default false,
    is_read_end boolean not null default false,
    reading_progress decimal(5, 2) not null default 0.00,
    latest_read_chapter_name text not null default '',
    latest_read_time timestamp not null default current_timestamp,
    latest_read_chapter_index int not null default 0,
    primary key (user_id, book_id)
    foreign key (user_id) references users(id),
    foreign key (book_id) references book(id)
);


