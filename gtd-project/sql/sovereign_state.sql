
DROP TABLE IF EXISTS dwh.dim_sovereign_state CASCADE;

CREATE TABLE dwh.dim_sovereign_state (
    sovereign_sk     SERIAL PRIMARY KEY,
    member           VARCHAR(100) NOT NULL,   -- membro di dim_country (paese o nazionalita')
    sovereign_state  VARCHAR(100) NOT NULL,   -- livello superiore della gerarchia
    valid_from       SMALLINT     NOT NULL,   -- anno di inizio validita', incluso
    valid_to         SMALLINT     NOT NULL,   -- anno di fine validita', incluso; 9999 = corrente
    is_current       SMALLINT     NOT NULL DEFAULT 1,
    scd_type         SMALLINT     NOT NULL,   -- 1 = una sola versione, 2 = versionata nel tempo
    note             VARCHAR(255) NOT NULL DEFAULT '',

    CONSTRAINT uq_sovereign_version UNIQUE (member, valid_from),
    CONSTRAINT ck_sovereign_interval CHECK (valid_to >= valid_from)
);

CREATE INDEX idx_sovereign_member ON dwh.dim_sovereign_state (member, valid_from, valid_to);

-- Popolamento dalla staging prodotta dalla Fase 2
INSERT INTO dwh.dim_sovereign_state
       (member, sovereign_state, valid_from, valid_to, is_current, scd_type, note)
SELECT member, sovereign_state, valid_from, valid_to, is_current, scd_type, COALESCE(note, '')
FROM   staging.dim_sovereign_state;

CREATE OR REPLACE FUNCTION dwh.sovereign_of(p_member VARCHAR, p_year SMALLINT)
RETURNS VARCHAR
LANGUAGE sql STABLE AS $$
    SELECT COALESCE(
        (SELECT s.sovereign_state
         FROM   dwh.dim_sovereign_state s
         WHERE  s.member = p_member
           AND  p_year BETWEEN s.valid_from AND s.valid_to
         LIMIT  1),
        p_member);
$$;

ALTER TABLE dwh.fact_event
    ADD COLUMN IF NOT EXISTS is_transnational_raw SMALLINT;

UPDATE dwh.fact_event f
SET    is_transnational_raw = f.is_transnational
WHERE  f.is_transnational_raw IS NULL;

UPDATE dwh.fact_event f
SET    is_transnational = CASE
         WHEN nat.country_name IS NULL OR nat.country_name = 'Unknown' THEN 0
         WHEN dwh.sovereign_of(geo.country_name, t.iyear::SMALLINT)
              = dwh.sovereign_of(nat.country_name, t.iyear::SMALLINT) THEN 0
         ELSE 1 END
FROM   dwh.dim_time    t,
       dwh.dim_country geo,
       dwh.dim_country nat
WHERE  t.date_sk            = f.date_sk
  AND  geo.country_sk       = f.attack_country_sk
  AND  nat.country_sk       = f.target_nat_sk;

-- Controllo di riconciliazione
SELECT COUNT(*) FILTER (WHERE is_transnational_raw = 1)                         AS trans_grezzo,
       COUNT(*) FILTER (WHERE is_transnational     = 1)                         AS trans_corretto,
       COUNT(*) FILTER (WHERE is_transnational_raw = 1 AND is_transnational = 0) AS falsi_positivi
FROM   dwh.fact_event;
