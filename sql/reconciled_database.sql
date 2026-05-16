-- ==============================================================================
-- PHASE 1: RECONCILED DATABASE SCHEMA CREATION (PostgreSQL)
-- ==============================================================================

DROP SCHEMA IF EXISTS rd CASCADE;
CREATE SCHEMA rd;

-- 1. BASE DIMENSIONAL TABLES (Lookup Tables from Codebook)
CREATE TABLE rd.REGION (
    region_id INT PRIMARY KEY,
    region_name VARCHAR(255) NOT NULL
);

CREATE TABLE rd.ATTACK_TYPE (
    attacktype_id INT PRIMARY KEY,
    attack_name VARCHAR(255) NOT NULL
);

CREATE TABLE rd.WEAPON (
    weaptype_id INT PRIMARY KEY,
    weapon_name VARCHAR(255) NOT NULL
);

CREATE TABLE rd.TARGET (
    targtype_id INT PRIMARY KEY,
    target_name VARCHAR(255) NOT NULL
);

-- 2. TABLES WITH FOREIGN KEYS (Hierarchies and Master Data)
CREATE TABLE rd.COUNTRY (
    country_id INT PRIMARY KEY,
    country_name VARCHAR(255) NOT NULL,
    region_id INT,
    FOREIGN KEY (region_id) REFERENCES rd.REGION(region_id)
);

CREATE TABLE rd.GEOGRAPHY (
    loc_id SERIAL PRIMARY KEY,
    country_id INT,
    provstate VARCHAR(255),
    city VARCHAR(255),
    latitude DECIMAL(9,6),
    longitude DECIMAL(9,6),
    FOREIGN KEY (country_id) REFERENCES rd.COUNTRY(country_id)
);

CREATE TABLE rd.TERRORIST_GROUP (
    group_id SERIAL PRIMARY KEY,
    gname VARCHAR(255) NOT NULL,
    gsubname VARCHAR(255),
    claimed BOOLEAN
);

-- 3. CORE ENTITY (Preliminary Fact)
CREATE TABLE rd.EVENT (
    eventid BIGINT PRIMARY KEY,
    iyear INT NOT NULL,
    imonth INT,
    iday INT,
    full_date DATE,
    is_approximate_date BOOLEAN,
    success BOOLEAN,
    suicide BOOLEAN,
    nkill INT,
    nkillter INT,
    nwound INT,
    propvalue DECIMAL(18,2),
    nkillter_reported INT,   -- <--- NUOVA COLONNA AGGIUNTA
    loc_id INT,
    group_id INT,
    attacktype_id INT,
    FOREIGN KEY (loc_id) REFERENCES rd.GEOGRAPHY(loc_id),
    FOREIGN KEY (group_id) REFERENCES rd.TERRORIST_GROUP(group_id),
    FOREIGN KEY (attacktype_id) REFERENCES rd.ATTACK_TYPE(attacktype_id)
);

-- 4. BRIDGE TABLES (M:N Multiplicity Management)
CREATE TABLE rd.EVENT_WEAPON (
    eventid BIGINT,
    weaptype_id INT,
    PRIMARY KEY (eventid, weaptype_id),
    FOREIGN KEY (eventid) REFERENCES rd.EVENT(eventid),
    FOREIGN KEY (weaptype_id) REFERENCES rd.WEAPON(weaptype_id)
);

CREATE TABLE rd.EVENT_TARGET (
    eventid BIGINT,
    targtype_id INT,
    PRIMARY KEY (eventid, targtype_id),
    FOREIGN KEY (eventid) REFERENCES rd.EVENT(eventid),
    FOREIGN KEY (targtype_id) REFERENCES rd.TARGET(targtype_id)
);