CREATE TABLE IF NOT EXISTS address (
    a_id                varchar(40) PRIMARY KEY,
    name                varchar(100) NOT NULL,
    full_address        varchar(400),
    location_link       varchar(200),
    country_code        varchar(3) NOT NULL,
    country_code_3      varchar(3),
    latitude            decimal NOT NULL,
    longitude           decimal NOT NULL,
    state               varchar(60),
    city                varchar(60),
    country             varchar(60),
    postal_code         varchar(20));

CREATE TABLE IF NOT EXISTS event (
    e_id                varchar(40) PRIMARY KEY,
    a_id                varchar(40),
    phone               varchar(20),
    email               varchar(60),
    website             varchar(300),
    update_key          varchar(40),
    name                varchar(100) NOT NULL,
    payment_options     varchar(60),
    start_time          timestamp NOT NULL,
    activity_type       varchar(40),
    large_event_id      varchar(40),
    reg_options         boolean,
    reg_skus            boolean,
    l_id                varchar(40),
    format              varchar(30),
    status              varchar(30),
    tags                varchar(30)[],
    in_calendar         boolean NOT NULL,
    pokemon_url         varchar(150),
    

    FOREIGN KEY (a_id)
        REFERENCES address (a_id));