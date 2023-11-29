DROP SCHEMA IF EXISTS projet CASCADE;
CREATE SCHEMA projet;

-----------------------------------------------------
-- table_api_key
-----------------------------------------------------
DROP TABLE IF EXISTS projet.table_cles_api CASCADE ;
CREATE TABLE projet.table_cles_api(
    id_utilisateur                SERIAL, 
    cle_api                         TEXT,
    type_utilisateur                TEXT,
    PRIMARY KEY (id_utilisateur, cle_api)
);

-----------------------------------------------------
-- historique_consommateur
-----------------------------------------------------
DROP TABLE IF EXISTS projet.historique_consommateur CASCADE ;
CREATE TABLE projet.historique_consommateur(
    id_utilisateur                 INT,
    cle_api                       TEXT,
    date_requete             TIMESTAMP,
    duree                          INT,
    date_visionnage          TIMESTAMP,
    resolution                     INT,
    type_connexion                TEXT,
    materiel                      TEXT,
    empreinte_carbone             REAL,
    ville                         TEXT,
    pays                          TEXT,
    PRIMARY KEY (cle_api, date_requete),
    FOREIGN KEY (id_utilisateur, cle_api) 
        REFERENCES projet.table_cles_api (id_utilisateur, cle_api)
        ON DELETE CASCADE
);