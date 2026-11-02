/* livello superiore della gerarchia geografica */
ALTER TABLE rd.REGION
    ADD COLUMN IF NOT EXISTS macro_area VARCHAR(60) NOT NULL DEFAULT 'Unknown';

/* raggruppamento narrativo delle classi d'arma */
ALTER TABLE rd.WEAPON_TYPE
    ADD COLUMN IF NOT EXISTS weapon_group VARCHAR(40) NOT NULL DEFAULT 'Altre armi';



ALTER TABLE dwh.dim_country
    ADD COLUMN IF NOT EXISTS macro_area VARCHAR(60) NOT NULL DEFAULT 'Unknown';

ALTER TABLE dwh.dim_geography
    ADD COLUMN IF NOT EXISTS macro_area VARCHAR(60) NOT NULL DEFAULT 'Unknown';

ALTER TABLE dwh.dim_weapon
    ADD COLUMN IF NOT EXISTS weapon_group VARCHAR(40) NOT NULL DEFAULT 'Altre armi';
