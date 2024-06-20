from hstest import StageTest, CheckResult, dynamic_test, TestedProgram
import ast
import os


class Football(StageTest):

    @dynamic_test()
    def check_data(self):
        if not os.path.exists("../data"):
            return CheckResult.wrong("The data directory is missing")

        if 'database.sqlite' not in os.listdir("../data/database"):
            return CheckResult.wrong("The database.sqlite file is missing from the data directory")

        return CheckResult.correct()

    @dynamic_test()
    def test_output(self):
        pr = TestedProgram()
        out = pr.start()

        answer = ['West Ham United', 47]

        if not out:
            return CheckResult.wrong("Print the list")

        if not ("[" in out) or not ("]" in out):
            return CheckResult.wrong("The output is a list")

        if not out.startswith("[") and not out.endswith("]"):
            return CheckResult.wrong("The output is a list")

        result = ast.literal_eval(out)

        if not len(result) == 2:
            return CheckResult.wrong("Print team name and total number of points")

        if result != answer:
            return CheckResult.wrong("The output is incorrect")

        return CheckResult.correct()
