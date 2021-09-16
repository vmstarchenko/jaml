import pathlib
import yaml


class TestFile:
    def __init__(self, template, path):
        self.template = template
        self.path = pathlib.Path(path)
        self.tests = yaml.safe_load(self.path.read_text())

    def run(self, update_new=False, update_all=False):
        for test in self.tests:
            try:
                output = self.template(test['input'])
            except Exception as e:
                output = f'exception: {type(e).__name__}'

            expected_output = test.get('output')
            if (update_new and expected_output is None) or update_all:
                test['output'] = output
                continue

            if expected_output is None:
                raise ValueError('Expected output not defined and update_new == False')

            if expected_output != output:
                raise ValueError(f'Expected output != real output: {expected_output} != {output}')

        if update_new or update_all:
            self.path.write_text(yaml.dump(self.tests))
