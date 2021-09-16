import jiml


def test_load_template():
    jiml.load_template('key: {{ value }}')
