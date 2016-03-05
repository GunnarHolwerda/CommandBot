from unittest import TestCase
from discord_commands.dankmemes_command.dankmemes_command import DankMemesCommand


class TestDankMemesCommand(TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        self.command = None

    def test_run(self):
        self.command = DankMemesCommand("test")
        result = self.command.run()

        should_be_result = "TEST\nE\nS\nT\n"

        self.assertEqual(result, should_be_result)

    def test_run_space_option(self):
        self.command = DankMemesCommand("test $space=true")
        result = self.command.run()

        should_be_result = "T E S T \n \nE\n \nS\n \nT\n \n"

        self.assertEqual(result, should_be_result)
