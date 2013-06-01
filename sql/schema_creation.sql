--- Elucidata SQL Database Creation
-- Author: Max Bainrot
-- Date: 1st June 2013

-- Table: coordinate
-- DROP TABLE coordinate;

CREATE TABLE coordinate
(
  id serial NOT NULL,
  lat real,
  "long" real,
  CONSTRAINT coordinate_pkey PRIMARY KEY (id)
);


-- Table: dataset
-- DROP TABLE dataset;

CREATE TABLE dataset
(
  id text NOT NULL,
  api_url text,
  revision_date integer,
  revision_id text,
  "Name" text,
  "Provider" text,
  CONSTRAINT pkey_id PRIMARY KEY (id)
);

-- Table: "group"
-- DROP TABLE "group";

CREATE TABLE "group"
(
  dataset_id text NOT NULL,
  "group" text NOT NULL,
  CONSTRAINT pkey_group PRIMARY KEY (dataset_id, "group"),
  CONSTRAINT fkey_dataset_id FOREIGN KEY (dataset_id)
      REFERENCES dataset (id)
      ON UPDATE NO ACTION ON DELETE CASCADE
);

-- Table: point
-- DROP TABLE point;

-- Table: resource_map
-- DROP TABLE resource_map;

CREATE TABLE resource_map
(
  id text NOT NULL,
  dataset_id text,
  type text,
  name text,
  resource_url text,
  CONSTRAINT resource_map_pkey PRIMARY KEY (id),
  CONSTRAINT fkey_dataset_id FOREIGN KEY (dataset_id)
      REFERENCES dataset (id)
      ON UPDATE NO ACTION ON DELETE CASCADE
);

CREATE TABLE point
(
  map_id text NOT NULL,
  coord_id integer NOT NULL,
  weight integer,
  CONSTRAINT point_pkey PRIMARY KEY (map_id, coord_id),
  CONSTRAINT point_coord_id_fkey FOREIGN KEY (coord_id)
      REFERENCES coordinate (id)
      ON UPDATE NO ACTION ON DELETE NO ACTION,
  CONSTRAINT point_map_id_fkey FOREIGN KEY (map_id)
      REFERENCES resource_map (id)
      ON UPDATE NO ACTION ON DELETE CASCADE
);

-- Table: resource_text
-- DROP TABLE resource_text;

CREATE TABLE resource_text
(
  id text NOT NULL,
  dataset_id text,
  column_headers text,
  row_headers text,
  type text,
  "Name" text,
  resource_url text,
  wordcount integer,
  CONSTRAINT pkey_rt_id PRIMARY KEY (id),
  CONSTRAINT fkey_dataset_id FOREIGN KEY (dataset_id)
      REFERENCES dataset (id)
      ON UPDATE NO ACTION ON DELETE CASCADE
);

-- Table: resouce_word
-- DROP TABLE resouce_word;

CREATE TABLE resouce_word
(
  text_id text NOT NULL,
  word text NOT NULL,
  frequency integer,
  CONSTRAINT pkey PRIMARY KEY (text_id, word),
  CONSTRAINT fkey_resource_id FOREIGN KEY (text_id)
      REFERENCES resource_text (id)
      ON UPDATE NO ACTION ON DELETE CASCADE
);





-- Index: fki_fkey_dataset_id
-- DROP INDEX fki_fkey_dataset_id;

CREATE INDEX fki_fkey_dataset_id
  ON resource_map
  USING btree
  (dataset_id COLLATE pg_catalog."default");




-- Table: tag
-- DROP TABLE tag;

CREATE TABLE tag
(
  dataset_id text NOT NULL,
  tag text NOT NULL,
  CONSTRAINT pkey_tag PRIMARY KEY (dataset_id, tag),
  CONSTRAINT fkey_dataset_id FOREIGN KEY (dataset_id)
      REFERENCES dataset (id)
      ON UPDATE NO ACTION ON DELETE CASCADE
);
