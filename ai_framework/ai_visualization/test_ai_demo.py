import time
import unittest
from ai_framework.ai_visualization import AIDemo
from ai_framework.ai_actions import ActionStatus


class TestAIDemo(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        demo_markdown_file_folder = '/Users/jerry/OneDrive/Documents/Obsidian Vault/'
        cls._ai_demo = AIDemo(demo_mode=True, markdown_folder=demo_markdown_file_folder)
        try:
            cls._ai_demo.reset_demo()
            pass
        except:
            pass

    def test_demo_goals(self):
        test_goals = [
            {"goal_state": True}
        ]
        self._ai_demo.demo_goals(test_goals)
        self.assertTrue(True)

    def test_demo_diary_entry(self):
        # make the first diary entry
        goal = {"goal_state": True}
        world_state_before = []
        world_state_after = [
            {"condition_one": True}
        ]
        action_status = ActionStatus.SUCCESS
        diary_entry = {
            "my_goal": goal,
            "the_world_state_before": world_state_before,
            "my_plan": "plan",
            "action_status": action_status,
            "the_world_state_after": world_state_after
        }
        self._ai_demo.demo_diary_entry(diary_entry)

        # make the second diary entry
        world_state_before = [
            {"condition_one": True}
        ]
        world_state_after = [
            {"condition_one": True},
            {"condition_two": True}
        ]
        diary_entry = {
            "my_goal": goal,
            "the_world_state_before": world_state_before,
            "my_plan": "plan",
            "action_status": action_status,
            "the_world_state_after": world_state_after
        }
        self._ai_demo.demo_diary_entry(diary_entry)

        # make the third diary entry
        world_state_before = [
            {"condition_one": True},
            {"condition_two": True}
        ]
        world_state_after = [
            goal,
            {"condition_one": True},
            {"condition_two": True}
        ]
        diary_entry = {
            "my_goal": goal,
            "the_world_state_before": world_state_before,
            "my_plan": "plan",
            "action_status": action_status,
            "the_world_state_after": world_state_after
        }
        self._ai_demo.demo_diary_entry(diary_entry)

        self.assertTrue(True)

    def test_multiple_diary_entries(self):
        for i in range(50):
            self.test_demo_diary_entry()
            self._ai_demo.retire_nodes()
            time.sleep(5)
            update = "[PlanStep(action=<__main__.AcmeTemperatureMonitor object at 0x7f76245a2a90>, services={})]"
            self._ai_demo.update_demo_goals(update)
            time.sleep(10)


if __name__ == '__main__':
    unittest.main()
