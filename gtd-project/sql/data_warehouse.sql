/*
   FASE 1 - DATA WAREHOUSE (STAR SCHEMA)
   Traduzione logica dello schema di fatto DFM "ATTENTATO".
*/

DROP SCHEMA IF EXISTS dwh CASCADE;
CREATE SCHEMA dwh;



-- DIMENSIONI

CREATE TABLE dwh.dim_time (
    date_sk      INT PRIMARY KEY,
    full_date    DATE,
    iyear        INT          NOT NULL,
    decade       VARCHAR(10)  NOT NULL,
    quarter      SMALLINT,
    imonth       SMALLINT,
    month_name   VARCHAR(20)  NOT NULL,
    iday         SMALLINT,
    day_of_week  SMALLINT,
    day_name     VARCHAR(20)  NOT NULL,
    is_weekend   BOOLEAN,
    CONSTRAINT uq_dim_time_date UNIQUE (full_date)
);

CREATE TABLE dwh.dim_geography (
    geo_sk        SERIAL PRIMARY KEY,
    loc_nk        INT,
    city          VARCHAR(255) NOT NULL,
    provstate     VARCHAR(255) NOT NULL,
    country_name  VARCHAR(100) NOT NULL,
    region_name   VARCHAR(100) NOT NULL,
    lat_centroid  DECIMAL(9,6),
    lon_centroid  DECIMAL(9,6),
    CONSTRAINT uq_dim_geo_nk UNIQUE (loc_nk)
);

CREATE TABLE dwh.dim_country (
    country_sk    SERIAL PRIMARY KEY,
    country_nk    INT,
    country_name  VARCHAR(100) NOT NULL,
    region_name   VARCHAR(100) NOT NULL,
    CONSTRAINT uq_dim_country_nk UNIQUE (country_nk)
);

CREATE TABLE dwh.dim_group (
    group_sk                SERIAL PRIMARY KEY,
    group_nk                INT,
    gname                   VARCHAR(255) NOT NULL,
    gsubname                VARCHAR(255) NOT NULL DEFAULT '',
    is_unknown_perpetrator  BOOLEAN NOT NULL DEFAULT FALSE,
    CONSTRAINT uq_dim_group_nk UNIQUE (group_nk)
);

CREATE TABLE dwh.dim_attack_type (
    attack_sk      SERIAL PRIMARY KEY,
    attack_nk      INT,
    attack_name    VARCHAR(100) NOT NULL,
    attack_macro   VARCHAR(50)  NOT NULL,
    CONSTRAINT uq_dim_attack_nk UNIQUE (attack_nk)
);

CREATE TABLE dwh.dim_weapon (
    weapon_sk       SERIAL PRIMARY KEY,
    weapon_nk       INT,
    weapon_subtype  VARCHAR(150) NOT NULL,
    weapon_name     VARCHAR(150) NOT NULL,
    weapon_macro    VARCHAR(50)  NOT NULL,
    CONSTRAINT uq_dim_weapon_nk UNIQUE (weapon_nk)
);

CREATE TABLE dwh.dim_target (
    target_sk       SERIAL PRIMARY KEY,
    target_nk       INT,
    target_subtype  VARCHAR(150) NOT NULL,
    target_name     VARCHAR(150) NOT NULL,
    target_macro    VARCHAR(50)  NOT NULL,
    CONSTRAINT uq_dim_target_nk UNIQUE (target_nk)
);


CREATE TABLE dwh.dim_quality (
    quality_sk               SERIAL PRIMARY KEY,
    date_accuracy            VARCHAR(20) NOT NULL,
    nkill_source             VARCHAR(20) NOT NULL,
    nwound_source            VARCHAR(20) NOT NULL,
    perp_fatalities_source   VARCHAR(20) NOT NULL,
    claim_of_responsibility  VARCHAR(20) NOT NULL,
    perpetrator_attribution  VARCHAR(20) NOT NULL,
    doubt_terrorism          VARCHAR(20) NOT NULL,
    inclusion_criteria       VARCHAR(20) NOT NULL,
    CONSTRAINT uq_dim_quality UNIQUE (
        date_accuracy, nkill_source, nwound_source, perp_fatalities_source,
        claim_of_responsibility, perpetrator_attribution, doubt_terrorism,
        inclusion_criteria)
);

CREATE TABLE dwh.fact_event (
    event_sk            SERIAL PRIMARY KEY,
    eventid             BIGINT NOT NULL,

    date_sk             INT NOT NULL,
    geo_sk              INT NOT NULL,
    attack_country_sk   INT NOT NULL,
    target_nat_sk       INT NOT NULL,
    group_sk            INT NOT NULL,
    attack_sk           INT NOT NULL,
    quality_sk          INT NOT NULL,

    latitude            DECIMAL(9,6),
    longitude           DECIMAL(9,6),

    nkill               INT,
    nkillter            INT,
    nwound              INT,
    nperps              INT,
    propvalue           DECIMAL(18,2),
    is_success          SMALLINT,
    is_suicide          SMALLINT,
    is_extended         SMALLINT,
    is_multiple         SMALLINT,
    is_transnational    SMALLINT,

    nkill_victims       INT GENERATED ALWAYS AS
                        (GREATEST(COALESCE(nkill,0) - COALESCE(nkillter,0), 0)) STORED,
    casualties          INT GENERATED ALWAYS AS
                        (COALESCE(nkill,0) + COALESCE(nwound,0)) STORED,

    n_weapon_types      SMALLINT NOT NULL DEFAULT 1,
    n_target_types      SMALLINT NOT NULL DEFAULT 1,

    CONSTRAINT uq_fact_eventid   UNIQUE (eventid),
    CONSTRAINT fk_fact_time      FOREIGN KEY (date_sk)           REFERENCES dwh.dim_time(date_sk),
    CONSTRAINT fk_fact_geo       FOREIGN KEY (geo_sk)            REFERENCES dwh.dim_geography(geo_sk),
    CONSTRAINT fk_fact_country   FOREIGN KEY (attack_country_sk) REFERENCES dwh.dim_country(country_sk),
    CONSTRAINT fk_fact_natlty    FOREIGN KEY (target_nat_sk)     REFERENCES dwh.dim_country(country_sk),
    CONSTRAINT fk_fact_group     FOREIGN KEY (group_sk)          REFERENCES dwh.dim_group(group_sk),
    CONSTRAINT fk_fact_attack    FOREIGN KEY (attack_sk)         REFERENCES dwh.dim_attack_type(attack_sk),
    CONSTRAINT fk_fact_quality   FOREIGN KEY (quality_sk)        REFERENCES dwh.dim_quality(quality_sk),
    CONSTRAINT ck_fact_flags     CHECK (is_success IS NULL OR is_success IN (0,1))
);


CREATE TABLE dwh.bridge_event_weapon (
    event_sk   INT NOT NULL,
    weapon_sk  INT NOT NULL,
    is_primary BOOLEAN NOT NULL DEFAULT FALSE,
    PRIMARY KEY (event_sk, weapon_sk),
    CONSTRAINT fk_bew_fact   FOREIGN KEY (event_sk)  REFERENCES dwh.fact_event(event_sk) ON DELETE CASCADE,
    CONSTRAINT fk_bew_weapon FOREIGN KEY (weapon_sk) REFERENCES dwh.dim_weapon(weapon_sk)
);

CREATE TABLE dwh.bridge_event_target (
    event_sk   INT NOT NULL,
    target_sk  INT NOT NULL,
    is_primary BOOLEAN NOT NULL DEFAULT FALSE,
    PRIMARY KEY (event_sk, target_sk),
    CONSTRAINT fk_bet_fact   FOREIGN KEY (event_sk)  REFERENCES dwh.fact_event(event_sk) ON DELETE CASCADE,
    CONSTRAINT fk_bet_target FOREIGN KEY (target_sk) REFERENCES dwh.dim_target(target_sk)
);


CREATE UNIQUE INDEX uq_bew_primary ON dwh.bridge_event_weapon (event_sk) WHERE is_primary;
CREATE UNIQUE INDEX uq_bet_primary ON dwh.bridge_event_target (event_sk) WHERE is_primary;


CREATE VIEW dwh.dim_attack_country AS
SELECT country_sk   AS attack_country_sk,
       country_name AS attack_country,
       region_name  AS attack_region
FROM dwh.dim_country;

CREATE VIEW dwh.dim_target_nationality AS
SELECT country_sk   AS target_nat_sk,
       country_name AS target_nationality,
       region_name  AS target_nat_region
FROM dwh.dim_country;


-- INDICI PER LO STAR JOIN
CREATE INDEX idx_fact_date     ON dwh.fact_event (date_sk);
CREATE INDEX idx_fact_geo      ON dwh.fact_event (geo_sk);
CREATE INDEX idx_fact_country  ON dwh.fact_event (attack_country_sk);
CREATE INDEX idx_fact_natlty   ON dwh.fact_event (target_nat_sk);
CREATE INDEX idx_fact_group    ON dwh.fact_event (group_sk);
CREATE INDEX idx_fact_attack   ON dwh.fact_event (attack_sk);
CREATE INDEX idx_fact_quality  ON dwh.fact_event (quality_sk);
CREATE INDEX idx_bew_weapon    ON dwh.bridge_event_weapon (weapon_sk);
CREATE INDEX idx_bet_target    ON dwh.bridge_event_target (target_sk);
