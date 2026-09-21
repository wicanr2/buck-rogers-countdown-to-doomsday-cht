import tempfile, unittest
from pathlib import Path
from skill_action_bar_text_safe_rects import validate

ROOT=Path(__file__).resolve().parents[1]
EVENTS=ROOT/"text/skill-action-bar-events.tsv"; TEXT=ROOT/"text/skill-action-bar.zh-TW.tsv"; RECTS=ROOT/"text/skill-action-bar-text-safe-rects.tsv"

class SkillActionBarRectsTest(unittest.TestCase):
    def test_formal(self): self.assertEqual(validate(EVENTS,TEXT,RECTS),16)
    def reject(self,old,new):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/"r.tsv"; p.write_text(RECTS.read_text().replace(old,new,1),encoding="utf-8")
            with self.assertRaises(ValueError): validate(EVENTS,TEXT,p)
    def test_rejects_geometry(self): self.reject("career.action.add.normal\t0\t192\t32","career.action.add.normal\t0\t184\t32")
    def test_rejects_missing(self): self.reject("career.action.add.normal","orphan")
    def test_rejects_capacity(self): self.reject("\t4\t1\tsingle-line-reject","\t1\t1\tsingle-line-reject")
    def test_rejects_cross_action_overlap(self): self.reject("career.action.done.normal\t104","career.action.done.normal\t32")

if __name__=="__main__": unittest.main()
