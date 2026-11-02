"""Settings remain portable and never contain a built-in password."""
import os
import unittest
from pathlib import Path
from unittest.mock import patch
from gtd_pipeline.config import DatabaseSettings, PathSettings


class ConfigurationTests(unittest.TestCase):
    def test_default_password_is_empty(self):
        with patch.dict(os.environ, {}, clear=True):
            self.assertEqual(DatabaseSettings().password, "")

    def test_environment_password_is_encoded(self):
        with patch.dict(os.environ, {"GTD_DB_PASSWORD": "a b@c"}, clear=True):
            self.assertIn(":a+b%40c@", DatabaseSettings().url)

    def test_sql_paths_survive_cli_relocation(self):
        paths = PathSettings()
        self.assertEqual(paths.root, Path(__file__).resolve().parents[1])
        self.assertTrue(paths.ddl_reconciled.is_file())
        self.assertTrue(paths.ddl_warehouse.is_file())
        self.assertTrue((paths.sql_dir / "export.sql").is_file())
