-- PHASE 1: DATA WAREHOUSE SCHEMA CREATION
DROP SCHEMA IF EXISTS dwh CASCADE;
CREATE SCHEMA dwh;

-- 1. DIMENSION TABLES
CREATE TABLE dwh.dim_time (
    date_sk SERIAL PRIMARY KEY,      
    full_date DATE,
    is_approximate_date BOOLEAN,
    iyear INT NOT NULL,
    quarter INT,
    imonth INT,
    month_name VARCHAR(20),
    iday INT
);
CREATE TABLE dwh.dim_geography (
    geo_sk SERIAL PRIMARY KEY,       
    city VARCHAR(255),
    provstate VARCHAR(255),
    country_name VARCHAR(255),
    region_name VARCHAR(255),
    latitude DECIMAL(9,6),
    longitude DECIMAL(9,6)
);
CREATE TABLE dwh.dim_group (
    group_sk SERIAL PRIMARY KEY,     
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

-- 2. FACT TABLE
CREATE TABLE dwh.fact_event (
    event_sk SERIAL PRIMARY KEY,     
    eventid BIGINT NOT NULL,         
    
    -- Chiavi Esterne Dimensionali
    date_sk INT REFERENCES dwh.dim_time(date_sk),
    geo_sk INT REFERENCES dwh.dim_geography(geo_sk),
    group_sk INT REFERENCES dwh.dim_group(group_sk),
    attack_sk INT REFERENCES dwh.dim_attack_type(attack_sk),
    
    -- Misure e Flag
    nkill INT,
    nkillter INT,
    nwound INT,
    propvalue DECIMAL(18,2),
    nkillter_reported INT,
    is_nkill_imputed INT,
    is_nwound_imputed INT
);

-- 3. BRIDGE TABLES
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