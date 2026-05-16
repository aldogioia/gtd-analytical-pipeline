-- ==============================================================================
-- PHASE 1: DATA WAREHOUSE SCHEMA CREATION (PostgreSQL - Star Schema)
-- ==============================================================================

CREATE SCHEMA IF NOT EXISTS dwh;

-- 1. DIMENSION TABLES (Denormalizzate)

CREATE TABLE dwh.dim_time (
    date_sk SERIAL PRIMARY KEY,      -- Surrogate Key   
    full_date DATE,
    is_approximate_date BOOLEAN,
    iyear INT NOT NULL,
    quarter INT,
    imonth INT,
    month_name VARCHAR(20),
    iday INT
);

CREATE TABLE dwh.dim_geography (
    geo_sk SERIAL PRIMARY KEY,       -- Surrogate Key
    city VARCHAR(255),
    provstate VARCHAR(255),
    country_name VARCHAR(255),
    region_name VARCHAR(255),
    latitude DECIMAL(9,6),
    longitude DECIMAL(9,6)
);

CREATE TABLE dwh.dim_group (
    group_sk SERIAL PRIMARY KEY,     -- Surrogate Key
    gname VARCHAR(255),
    gsubname VARCHAR(255)
);

CREATE TABLE dwh.dim_attack_type (
    attack_sk SERIAL PRIMARY KEY,
    attack_name VARCHAR(255)
);

CREATE TABLE dwh.dim_weapon (
    weapon_sk SERIAL PRIMARY KEY,
    weapon_name VARCHAR(255)
);

CREATE TABLE dwh.dim_target (
    target_sk SERIAL PRIMARY KEY,
    target_name VARCHAR(255)
);

-- 2. FACT TABLE (Il Fatto Centrale)

CREATE TABLE dwh.fact_event (
    event_sk SERIAL PRIMARY KEY,     -- Surrogate Key
    eventid BIGINT NOT NULL,         -- Business Key (Dal DB originale)
    
    -- Chiavi Esterne Dimensionali
    date_sk INT REFERENCES dwh.dim_time(date_sk),
    geo_sk INT REFERENCES dwh.dim_geography(geo_sk),
    group_sk INT REFERENCES dwh.dim_group(group_sk),
    attack_sk INT REFERENCES dwh.dim_attack_type(attack_sk),
    
    -- Misure
    nkill INT,
    nkillter INT,
    nwound INT,
    propvalue DECIMAL(18,2)
);

-- 3. BRIDGE TABLES (Per la gestione delle dimensioni Multi-Valore)

CREATE TABLE dwh.bridge_event_weapon (
    event_sk BIGINT REFERENCES dwh.fact_event(event_sk),
    weapon_sk INT REFERENCES dwh.dim_weapon(weapon_sk),
    PRIMARY KEY (event_sk, weapon_sk)
);

CREATE TABLE dwh.bridge_event_target (
    event_sk BIGINT REFERENCES dwh.fact_event(event_sk),
    target_sk INT REFERENCES dwh.dim_target(target_sk),
    PRIMARY KEY (event_sk, target_sk)
);