from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
INDEX = (ROOT / "index.html").read_text(encoding="utf-8")

class HomepageArtworkVisibilityTests(unittest.TestCase):
    def test_native_service_cards_have_suite_artwork(self):
        for service in ("notes", "memos", "tasks", "contacts"):
            block = INDEX.split(f'data-service="{service}"', 1)[1].split("</article>", 1)[0]
            self.assertIn('assets/goreecloud-logo.svg', block)
    def test_native_platform_cards_have_suite_artwork(self):
        for label in ("GoreeCloud Notify", "GoreeCloud Monitoring", "GoreeCloud Search"):
            before = INDEX.split(f'<h3>{label}</h3>', 1)[0][-900:]
            self.assertIn('assets/goreecloud-logo.svg', before)
    def test_beszel_has_reviewed_artwork(self):
        block = INDEX.split('<h3>Beszel</h3>', 1)[0][-900:]
        self.assertIn('assets/platform/beszel.svg', block)

if __name__ == "__main__": unittest.main()
