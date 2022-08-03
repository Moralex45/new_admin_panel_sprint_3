CREATE SCHEMA IF NOT EXISTS content;
ALTER ROLE app SET search_path TO "content", "public";