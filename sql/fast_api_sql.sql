-- Create table posts
CREATE TABLE IF NOT EXISTS public.posts (
	id serial not null,
	title character varying not null,
	content character varying not null,
	published boolean not null default true,
	created_at timestamp with time zone not null default NOW(),
	primary key (id)
);

alter table if exists public.posts
owner to postgres;

