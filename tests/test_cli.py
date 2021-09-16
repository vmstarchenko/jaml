import jiml.cli


def write_file(path, text):
    path.write_text(text)
    return path


def test_argparse(tmp_path):
    tmpl = write_file(tmp_path / 't.yaml', 'key: {{ var }}')
    inp = write_file(tmp_path / 'i.json', '{"var": "Hello!"}')
    out = tmp_path / 'o.json'

    jiml.cli.main(jiml.cli.parse_args(
        '-t', str(tmpl),
        '-i', str(inp),
        '-o', str(out),
    ))
