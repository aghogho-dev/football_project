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

        answer = [
            ['SV Werder Bremen', 76],
            ['TSG 1899 Hoffenheim', 76],
            ['VfL Wolfsburg', 67]
        ]

        if not out:
            return CheckResult.wrong("Print the list of lists")

        if not ("[[" in out) or not ("]]" in out):
            return CheckResult.wrong("The output is a list of lists")

        if not out.startswith("[[") and not out.endswith("]]"):
            return CheckResult.wrong("The output is a list of lists")

        result = ast.literal_eval(out)

        if not len(result) == 3:
            return CheckResult.wrong("Print the top 3 German teams with most draws")

        for row in result:
            if len(row) != 2:
                return CheckResult.wrong("The list should contain the team name and the total number of draws")

        if set(i for i, _ in result) != set(j for j, _ in answer):
            return CheckResult.wrong("There is at least one incorrect team returned")

        for v, k in zip(answer, result):
            if v != k:
                return CheckResult.wrong("The teams with most draws should come first"
                                         "\nIf you teams have same number of draws, sort alphabetically")

        return CheckResult.correct()
