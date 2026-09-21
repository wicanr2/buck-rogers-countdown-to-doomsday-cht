import json
from pathlib import Path
import tempfile
import unittest

import name_prompt_request_receipt as subject


class NamePromptRequestReceiptTest(unittest.TestCase):
    def receipt(self, *, echo: bool) -> dict:
        events = [{
            "entry_step": 101919217,
            "post_call_step": 101931640,
            "caller": {"segment": 1891, "offset": 2086},
            "original_length": 16,
            "original_sha256": subject.PROMPT_HASH,
            "background": 0,
            "foreground": 13,
            "row": 24,
            "column": 0,
        }]
        if echo:
            events.append({
                "entry_step": 102050850,
                "post_call_step": 102051824,
                "caller": {"segment": 1891, "offset": 2479},
                "original_length": 1,
                "original_sha256": subject.ECHO_HASH,
                "background": 0,
                "foreground": 15,
                "row": 24,
                "column": 17,
            })
        return {
            "stopped_at": 102100000 if echo else 102000000,
            "events": events,
            "requests": [{"event_key": "character.name.prompt",
                          "text_key": "character.name.prompt", "translation_runes": 5}],
            "catalog_misses": 1 if echo else 0,
        }

    def test_accepts_matching_pair(self):
        with tempfile.TemporaryDirectory() as directory:
            paths = [Path(directory) / str(i) for i in range(2)]
            value = self.receipt(echo=True)
            for path in paths:
                path.write_text(json.dumps(value), encoding="utf-8")
            subject.validate_pair(*paths, events=2, misses=1,
                                  stopped_at=102100000, expect_echo=True)

    def test_rejects_echo_as_request(self):
        with tempfile.TemporaryDirectory() as directory:
            paths = [Path(directory) / str(i) for i in range(2)]
            value = self.receipt(echo=True)
            value["requests"].append({"event_key": "echo", "text_key": "echo",
                                      "translation_runes": 1})
            for path in paths:
                path.write_text(json.dumps(value), encoding="utf-8")
            with self.assertRaises(ValueError):
                subject.validate_pair(*paths, events=2, misses=1,
                                      stopped_at=102100000, expect_echo=True)


if __name__ == "__main__":
    unittest.main()
