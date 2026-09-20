import json
from pathlib import Path
import tempfile
import unittest

import menu_receipt as subject


class MenuReceiptTest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        root = Path(self.temp.name)
        self.events = root / "events.tsv"
        self.catalog = root / "catalog.tsv"
        self.receipt = root / "receipt.json"
        self.events.write_text(
            "event_key\tsequence\ttext_key\toriginal_length\toriginal_sha256\tcaller\tbackground\tforeground\trow\tcolumn\n"
            "race.screen.prompt\t1\tmenu.pick_race\t9\t"
            "e932f4664fa9d32f95c406fe026368eb2e88dcbdadab01fc684d95abddef0c93\t"
            "37F1:158C\t0\t13\t2\t1\n",
            encoding="utf-8",
        )
        self.catalog.write_text("key\ttranslation\tsource\nmenu.pick_race\t選擇種族\truntime\n", encoding="utf-8")
        self.data = {
            "state_start": 99_999_999,
            "stopped_at": 100_300_000,
            "bios_input": "Enter(scan=0x1c,ascii=0x0d,queued_at=100010000)",
            "events": [{
                "entry_step": 100_033_190, "post_call_step": 100_040_266,
                "caller": {"segment": 0x37F1, "offset": 0x158C}, "original_length": 9,
                "original_sha256": "e932f4664fa9d32f95c406fe026368eb2e88dcbdadab01fc684d95abddef0c93",
                "background": 0, "foreground": 13, "row": 2, "column": 1,
            }],
        }
        self._write()

    def tearDown(self):
        self.temp.cleanup()

    def _write(self):
        self.receipt.write_text(json.dumps(self.data), encoding="utf-8")

    def test_accepts_exact_guarded_receipt(self):
        subject.verify(self.receipt, self.events, self.catalog)

    def test_rejects_hash_guard_order_and_extra_fields(self):
        mutations = [
            ("hash", lambda e: e.update(original_sha256="0" * 64)),
            ("guard order", lambda e: e.update(post_call_step=e["entry_step"])),
            ("extra field", lambda e: e.update(original_text="Pick Race")),
        ]
        for name, mutate in mutations:
            with self.subTest(name=name):
                saved = json.loads(json.dumps(self.data))
                mutate(self.data["events"][0])
                self._write()
                with self.assertRaises(ValueError):
                    subject.verify(self.receipt, self.events, self.catalog)
                self.data = saved


if __name__ == "__main__":
    unittest.main()
