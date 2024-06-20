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
            ['West Ham United', 40, '2013/2014'],
            ['Crystal Palace', 45, '2013/2014'],
            ['West Ham United', 47, '2014/2015'],
            ['Crystal Palace', 48, '2014/2015'],
            ['West Ham United', 62, '2015/2016'],
            ['Crystal Palace', 42, '2015/2016']
        ]

        if not out:
            return CheckResult.wrong("Print the list of lists")

        if not ("[[" in out) or not ("]]" in out):
            return CheckResult.wrong("The output is a list of lists")

        if not out.startswith("[[") and not out.endswith("]]"):
            return CheckResult.wrong("The output is a list of lists")

        result = ast.literal_eval(out)

        if not len(result) == 6:
            return CheckResult.wrong("The entries should be 6")

        for row in result:
            if len(row) != 3:
                return CheckResult.wrong("Each row should contain 3 items")

        if set(i for _, i, _ in result) != set(j for _, j, _ in answer):
            return CheckResult.wrong("There is at least one incorrect score returned")

        if set(i for i, _, _ in result) != set(j for j, _, _ in answer):
            return CheckResult.wrong("There is at least one incorrect team returned")

        if set(i for _, _, i in result) != set(j for _, _, j in answer):
            return CheckResult.wrong("There is at least one incorrect season returned")

        for v, k in zip(answer, result):
            if v != k:
                return CheckResult.wrong("The order is important"
                                         "\nAlternate between West Ham United and Crystal Palace")

        return CheckResult.correct()
