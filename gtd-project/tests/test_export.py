"""Every dimensional table still has a nonempty export query."""
import unittest
from gtd_pipeline.cli.export import parse_export_script
from gtd_pipeline.config import PathSettings


class ExportTests(unittest.TestCase):
    def test_all_eleven_tables_are_exported(self):
        queries = parse_export_script((PathSettings().sql_dir / "export.sql").read_text())
        self.assertEqual(len(queries), 11)
        self.assertIn("fact_event", queries)
        self.assertIn("bridge_event_weapon", queries)
        self.assertIn("bridge_event_target", queries)
        self.assertTrue(all(query.strip() for query in queries.values()))

    def test_empty_export_block_is_rejected(self):
        with self.assertRaises(ValueError):
            parse_export_script("--@table: missing\n;")

    def test_directives_allow_a_space_after_comment_marker(self):
        queries = parse_export_script("-- @table: fact_event\nSELECT 1;\n--@table: dim_time\nSELECT 2;")
        self.assertEqual(list(queries), ["fact_event", "dim_time"])
