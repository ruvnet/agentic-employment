import unittest
from backend.app.services.agent_service import create_agent

class TestAgentService(unittest.TestCase):
    def test_create_agent(self):
        agent_name = "TestAgent"
        agent_type = "Conversational"
        result = create_agent(agent_name, agent_type)
        self.assertEqual(result, f"Agent '{agent_name}' of type '{agent_type}' created successfully.")

if __name__ == '__main__':
    unittest.main()
