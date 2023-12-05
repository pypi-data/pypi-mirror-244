import json
import os.path
import sys

import jinja2

USAGE_STR = 'USAGE: python render_website.py [pages json] [templates] [output]'
NUM_ARGS = 3


def main():
    if len(sys.argv) != NUM_ARGS + 1:
        print(USAGE_STR)
        sys.exit(1)

    json_loc = sys.argv[1]
    templates_loc = sys.argv[2]
    output_loc = sys.argv[3]

    env = jinja2.Environment(loader=jinja2.FileSystemLoader(templates_loc))

    with open(json_loc) as f:
        pages = json.load(f)['pages']

    for page in pages:
        template = env.get_template(page['src'])
        rendered = template.render(
            sections=filter(lambda x: x['index'], pages),
            current_section=page['section'],
            enable_pyscript=page['pyscript'],
            title=page['label']
        )
        
        with open(os.path.join(output_loc, page['src']), 'w') as f:
            f.write(rendered)


if __name__ == '__main__':
    main()
