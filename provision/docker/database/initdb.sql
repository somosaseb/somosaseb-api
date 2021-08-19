\echo
\echo 'Creating default local database'

create user aseb with encrypted password 'aseb';
alter user aseb with createdb superuser;
create database aseb_core with owner aseb;

\c aseb_core

create extension citext;
create extension unaccent;
create extension ltree;
create extension fuzzystrmatch;
create extension pg_trgm;
