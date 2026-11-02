/*
   FASE 1 - RECONCILED DATABASE
   Global Terrorism Database - schema riconciliato.
 */

DROP SCHEMA IF EXISTS rd CASCADE;
CREATE SCHEMA rd;


CREATE TABLE rd.REGION (
    region_id    INT PRIMARY KEY,
    region_name  VARCHAR(100) NOT NULL,
    CONSTRAINT uq_region_name UNIQUE (region_name)
);

CREATE TABLE rd.COUNTRY (
    country_id    INT PRIMARY KEY,
    country_name  VARCHAR(100) NOT NULL,
    region_id     INT NOT NULL,
    CONSTRAINT fk_country_region FOREIGN KEY (region_id) REFERENCES rd.REGION(region_id)
);

CREATE TABLE rd.GEOGRAPHY (
    loc_id        SERIAL PRIMARY KEY,
    country_id    INT NOT NULL,
    provstate     VARCHAR(255) NOT NULL DEFAULT 'Unknown',
    city          VARCHAR(255) NOT NULL DEFAULT 'Unknown',
    lat_centroid  DECIMAL(9,6),
    lon_centroid  DECIMAL(9,6),
    CONSTRAINT fk_geo_country FOREIGN KEY (country_id) REFERENCES rd.COUNTRY(country_id),
    CONSTRAINT uq_geo_natural UNIQUE (country_id, provstate, city),
    CONSTRAINT ck_geo_lat CHECK (lat_centroid IS NULL OR lat_centroid BETWEEN -90 AND 90),
    CONSTRAINT ck_geo_lon CHECK (lon_centroid IS NULL OR lon_centroid BETWEEN -180 AND 180)
);

CREATE TABLE rd.TERRORIST_GROUP (
    group_id   SERIAL PRIMARY KEY,
    gname      VARCHAR(255) NOT NULL,
    gsubname   VARCHAR(255) NOT NULL DEFAULT '',
    CONSTRAINT uq_group_natural UNIQUE (gname, gsubname)
);

CREATE TABLE rd.ATTACK_TYPE (
    attacktype_id  INT PRIMARY KEY,
    attack_name    VARCHAR(100) NOT NULL,
    attack_macro   VARCHAR(50)  NOT NULL
);

CREATE TABLE rd.WEAPON_TYPE (
    weaptype_id    INT PRIMARY KEY,
    weapon_name    VARCHAR(150) NOT NULL,
    weapon_macro   VARCHAR(50)  NOT NULL
);

CREATE TABLE rd.WEAPON_SUBTYPE (
    weapsubtype_id       INT PRIMARY KEY,
    weapon_subtype_name  VARCHAR(150) NOT NULL,
    weaptype_id          INT NOT NULL,
    CONSTRAINT fk_weapsub_type FOREIGN KEY (weaptype_id) REFERENCES rd.WEAPON_TYPE(weaptype_id)
);

CREATE TABLE rd.TARGET_TYPE (
    targtype_id    INT PRIMARY KEY,
    target_name    VARCHAR(150) NOT NULL,
    target_macro   VARCHAR(50)  NOT NULL
);

CREATE TABLE rd.TARGET_SUBTYPE (
    targsubtype_id       INT PRIMARY KEY,
    target_subtype_name  VARCHAR(150) NOT NULL,
    targtype_id          INT NOT NULL,
    CONSTRAINT fk_targsub_type FOREIGN KEY (targtype_id) REFERENCES rd.TARGET_TYPE(targtype_id)
);

CREATE TABLE rd.EVENT (
    eventid               BIGINT PRIMARY KEY,

    iyear                 SMALLINT NOT NULL,
    imonth                SMALLINT,
    iday                  SMALLINT,
    full_date             DATE,
    is_approximate_date   BOOLEAN NOT NULL DEFAULT FALSE,

    loc_id                INT NOT NULL,
    latitude              DECIMAL(9,6),
    longitude             DECIMAL(9,6),
    specificity           SMALLINT,
    vicinity              BOOLEAN,

    group_id              INT NOT NULL,
    claimed               BOOLEAN,
    guncertain1           BOOLEAN,
    nperps                INT,

    attacktype_id         INT NOT NULL,

    natlty_id             INT NOT NULL DEFAULT -1,

    success               BOOLEAN,
    suicide               BOOLEAN,
    extended              BOOLEAN,
    multiple              BOOLEAN,
    nkill                 INT,
    nkillter              INT,
    nwound                INT,
    property              BOOLEAN,
    propextent            SMALLINT,
    propvalue             DECIMAL(18,2),

    crit1                 BOOLEAN,
    crit2                 BOOLEAN,
    crit3                 BOOLEAN,
    doubtterr             BOOLEAN,

    nkillter_reported     BOOLEAN,
    is_nkill_imputed      BOOLEAN,
    is_nwound_imputed     BOOLEAN,

    CONSTRAINT fk_event_geo     FOREIGN KEY (loc_id)        REFERENCES rd.GEOGRAPHY(loc_id),
    CONSTRAINT fk_event_group   FOREIGN KEY (group_id)      REFERENCES rd.TERRORIST_GROUP(group_id),
    CONSTRAINT fk_event_attack  FOREIGN KEY (attacktype_id) REFERENCES rd.ATTACK_TYPE(attacktype_id),
    CONSTRAINT fk_event_natlty  FOREIGN KEY (natlty_id)     REFERENCES rd.COUNTRY(country_id),

    CONSTRAINT ck_event_month   CHECK (imonth IS NULL OR imonth BETWEEN 0 AND 12),
    CONSTRAINT ck_event_day     CHECK (iday   IS NULL OR iday   BETWEEN 0 AND 31),
    CONSTRAINT ck_event_year    CHECK (iyear BETWEEN 1970 AND 2100),
    CONSTRAINT ck_event_spec    CHECK (specificity IS NULL OR specificity BETWEEN 1 AND 5),
    CONSTRAINT ck_event_lat     CHECK (latitude  IS NULL OR latitude  BETWEEN -90 AND 90),
    CONSTRAINT ck_event_lon     CHECK (longitude IS NULL OR longitude BETWEEN -180 AND 180),
    CONSTRAINT ck_event_nkill   CHECK (nkill     IS NULL OR nkill     >= 0),
    CONSTRAINT ck_event_nkillt  CHECK (nkillter  IS NULL OR nkillter  >= 0),
    CONSTRAINT ck_event_nwound  CHECK (nwound    IS NULL OR nwound    >= 0),
    CONSTRAINT ck_event_nperps  CHECK (nperps    IS NULL OR nperps    >= 0),
    CONSTRAINT ck_event_propval CHECK (propvalue IS NULL OR propvalue >= 0),
    CONSTRAINT ck_event_propext CHECK (propextent IS NULL OR propextent BETWEEN 1 AND 4)
);

CREATE TABLE rd.EVENT_WEAPON (
    eventid         BIGINT NOT NULL,
    weapsubtype_id  INT    NOT NULL,
    weap_order      SMALLINT NOT NULL,
    PRIMARY KEY (eventid, weapsubtype_id),
    CONSTRAINT fk_ew_event   FOREIGN KEY (eventid)        REFERENCES rd.EVENT(eventid) ON DELETE CASCADE,
    CONSTRAINT fk_ew_weapon  FOREIGN KEY (weapsubtype_id) REFERENCES rd.WEAPON_SUBTYPE(weapsubtype_id),
    CONSTRAINT ck_ew_order   CHECK (weap_order BETWEEN 1 AND 4)
);

CREATE TABLE rd.EVENT_TARGET (
    eventid         BIGINT NOT NULL,
    targsubtype_id  INT    NOT NULL,
    targ_order      SMALLINT NOT NULL,
    PRIMARY KEY (eventid, targsubtype_id),
    CONSTRAINT fk_et_event   FOREIGN KEY (eventid)        REFERENCES rd.EVENT(eventid) ON DELETE CASCADE,
    CONSTRAINT fk_et_target  FOREIGN KEY (targsubtype_id) REFERENCES rd.TARGET_SUBTYPE(targsubtype_id),
    CONSTRAINT ck_et_order   CHECK (targ_order BETWEEN 1 AND 3)
);

CREATE INDEX idx_event_loc      ON rd.EVENT (loc_id);
CREATE INDEX idx_event_group    ON rd.EVENT (group_id);
CREATE INDEX idx_event_attack   ON rd.EVENT (attacktype_id);
CREATE INDEX idx_event_natlty   ON rd.EVENT (natlty_id);
CREATE INDEX idx_event_year     ON rd.EVENT (iyear);
CREATE INDEX idx_event_fulldate ON rd.EVENT (full_date);
CREATE INDEX idx_geo_country    ON rd.GEOGRAPHY (country_id);
CREATE INDEX idx_ew_weapon      ON rd.EVENT_WEAPON (weapsubtype_id);
CREATE INDEX idx_et_target      ON rd.EVENT_TARGET (targsubtype_id);
