ALTER TABLE ab_user ADD COLUMN ref_code VARCHAR(256);

UPDATE alembic_version SET version_num='24fa4244490e' WHERE alembic_version.version_num = 'bce6265cd604';