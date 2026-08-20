from pathlib import Path
import re
import unittest


ROOT = Path(__file__).resolve().parents[1]
SKILL = (ROOT / "SKILL.md").read_text(encoding="utf-8")


class SkillContractTests(unittest.TestCase):
    def test_zero_beginner_positioning_and_neutral_goal_question(self):
        self.assertIn("# 零基础 A2 语言教练", SKILL)
        self.assertIn("你学韩语最想先做到什么？", SKILL)
        self.assertIn("旅行只是可选路线之一", SKILL)

    def test_free_environment_precedes_course_route(self):
        environment = SKILL.index("## 先准备免费声音环境")
        course = SKILL.index("## 运行零基础 A2 快速路线")
        self.assertLess(environment, course)
        self.assertIn("不得要求 API Key、信用卡、云端付费 TTS、订阅或按量计费服务", SKILL)

    def test_windows_system_speech_is_not_edge_tts(self):
        self.assertIn("System.Speech.Synthesis.SpeechSynthesizer", SKILL)
        self.assertIn("不要把 Windows 系统语音称为 Edge TTS", SKILL)

    def test_recording_upload_is_not_a_required_or_scored_path(self):
        self.assertIn("默认不要求用户上传 MP3 或录音", SKILL)
        self.assertIn("不使用百分制", SKILL)
        self.assertNotIn("## 分析用户录音", SKILL)
        self.assertNotIn("内容准确 `0–30`", SKILL)

    def test_internal_skill_resources_are_paths_not_dead_markdown_links(self):
        self.assertIsNone(re.search(r"\[[^]]+\]\([^)]+\)", SKILL))


if __name__ == "__main__":
    unittest.main()
