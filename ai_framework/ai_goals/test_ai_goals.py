import unittest
from ai_framework.ai_goals import AIGoal


class TestAIGoals(unittest.TestCase):
    def test_goal_prioritization(self):
        # test that the goals sort in the proper priority order

        goals = [
            AIGoal("third_goal", True, 0.75, 0.0),
            AIGoal("fourth_goal", True, 0.5, 0.5),
            AIGoal("first_goal", True, 0.65, 0.8),
            AIGoal("second_goal", True, 1, 0)
        ]
        sorted_goals = sorted(goals, reverse=True)

        self.assertEqual(sorted_goals[0].goal_state_name, "first_goal")
        self.assertEqual(sorted_goals[1].goal_state_name, "second_goal")
        self.assertEqual(sorted_goals[2].goal_state_name, "third_goal")
        self.assertEqual(sorted_goals[3].goal_state_name, "fourth_goal")

    def test_goal_deferral(self):
        # goals with low time sensitivity are deferrable but not deferred by default
        time_insensitive_goal = AIGoal("goal", True, 1, 0.5)
        self.assertEqual(time_insensitive_goal.deferrable, True)
        self.assertEqual(time_insensitive_goal.deferred, False)

        # goals with high time sensitivity are not deferrable and not deferred by default
        time_sensitive_goal = AIGoal("goal", True, 1, 0.51)
        self.assertEqual(time_sensitive_goal.deferrable, False)
        self.assertEqual(time_sensitive_goal.deferred, False)

        # you can only defer a deferrable goal
        time_insensitive_goal.deffer()
        self.assertEqual(time_insensitive_goal.deferred, True)
        time_sensitive_goal.deffer()
        self.assertEqual(time_sensitive_goal.deferred, False)

        # pursuing a goal means that it is no longer deferred
        time_insensitive_goal.pursue()
        self.assertEqual(time_insensitive_goal.deferred, False)


if __name__ == '__main__':
    unittest.main()
