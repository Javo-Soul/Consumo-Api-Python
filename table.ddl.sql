CREATE TABLE IF NOT EXISTS public.lista_anime (
    "Titulo_Anime" text COLLATE pg_catalog.default NOT NULL,
    "Episodios" text COLLATE pg_catalog.default,
    "Tipo" text COLLATE pg_catalog.default,
    "Estado" text COLLATE pg_catalog.default,
    CONSTRAINT lista_anime_pkey PRIMARY KEY ("Titulo_Anime")
) TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.lista_anime OWNER to postgres;


CREATE TABLE IF NOT EXISTS public.lista_anime_canciones
(
    "name" text COLLATE pg_catalog."default" NOT NULL,
    "artist" text COLLATE pg_catalog."default",
    "popularity" text COLLATE pg_catalog."default",
    CONSTRAINT lista_animesongs_pkey PRIMARY KEY ("name")
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.lista_anime_canciones
    OWNER to postgres;