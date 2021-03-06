import datetime
import re
from datetime import datetime

import click

from course_selection import TKUCourseSelector
from data_parsing import parse_data


@click.command()
@click.option('--studid', prompt='Student ID', envvar='STUDID')
@click.option('--password', prompt=True, hide_input=True, envvar='PASSWD')
@click.argument('script', type=click.File('r'), default='course_list.txt')
def cli(studid, password, script):
    while True:
        try:
            course_selector = TKUCourseSelector()
            course_selector.login(studid, password)
            sequence_add(course_selector, script)
        except AssertionError as error:
            click.echo(f'[{datetime.now().isoformat()}] {error}')


command_pattern = re.compile('(?P<operation>[+-]{1}) *(?P<course_id>\d{4})')


def sequence_add(course_selector, script):
    for command in script:
        match = command_pattern.match(command)
        if match:
            operation = match.group('operation')
            course_id = match.group('course_id')

            if operation == '+':
                func = course_selector.add_course
            elif operation == '-':
                func = course_selector.del_course

            resp = func(course_id)

            click.echo(
                f"course_id: {course_id}\nmsg: {parse_data(resp.text)['msg']}\n")

        else:
            click.echo('Invalid input\n')


if __name__ == "__main__":
    cli()
