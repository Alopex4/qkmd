#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import re
import email
import random
import urllib
import urllib3
import argparse
from datetime import datetime

import requests
from pyquery import PyQuery as pq
from pygments import highlight
from pygments.lexers import get_lexer_by_name
from pygments.formatters.terminal import TerminalFormatter

__version__ = 0.1

USER_AGENTS = (
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.7; rv:11.0) Gecko/20100101 Firefox/11.0',
    'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:22.0) Gecko/20100 101 Firefox/22.0',
    'Mozilla/5.0 (Windows NT 6.1; rv:11.0) Gecko/20100101 Firefox/11.0',
    ('Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_4) AppleWebKit/536.5 (KHTML, like Gecko) '
     'Chrome/19.0.1084.46 Safari/536.5'),
    ('Mozilla/5.0 (Windows; Windows NT 6.1) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.46'
     'Safari/536.5'),
)

SUPORT_LANGUAGE = ('actionscript', 'apache', 'applescript', 'asp', 'brainfuck',
                   'c', 'cfm', 'clojure', 'cmake', 'coffee-script',
                   'coffeescript, coffee', 'cpp', 'c++', 'cs', 'csharp', 'css',
                   'csv', 'bash', 'diff', 'elixir', 'erb', 'go', 'haml',
                   'http', 'java', 'javascript', 'json', 'jsx', 'less',
                   'lolcode', 'make', 'markdown', 'matlab', 'nginx',
                   'objectivec', 'pascal', 'php', 'perl', 'python', 'profile',
                   'rust', 'salt,', 'shell, sh, zsh, bash', 'sql', 'scss',
                   'sql', 'svg', 'swift', 'rb, jruby, ruby', 'smalltalk',
                   'vim, viml', 'volt', 'vhdl', 'vue', 'xml', 'yaml')

HEAD = r'^'
SCHEME = r'(https?|ftp)'
SLASH = r'://'
HOST_NAME = r'([a-zA-Z0-9._]){1,}/?.*'
TAIL = r'$'
URI = HEAD + SCHEME + SLASH + HOST_NAME + TAIL

FORMAT_SCHEME = {
    'link': '[{title}]({url})  \n',
    'date': "> _# date: {date}_ \n>\n",
    'quote': "> _# comment: {comment}_ \n>\n",
    'code': "> ```{language}\n{code}> ``` \n",
    'result': "{link}{date}{comment}{codes}"
}

# [Suppress InsecureRequestWarning](https://stackoverflow.com/a/28002687/8057310)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def _set_proxy():
    os.environ['http_proxy'] = 'http://127.0.0.1:8123'
    os.environ['https_proxy'] = 'https://127.0.0.1:8123'


def get_proxies():
    proxies = urllib.request.getproxies()
    filtered_proxies = {}
    for key, value in proxies.items():
        if key.startswith('http'):
            if not value.startswith('http'):
                filtered_proxies[key] = 'http://%s' % value
            else:
                filtered_proxies[key] = value
    return filtered_proxies


def get_verify(url):
    if 'https' in url:
        return True
    return False


def _emergency_reslove(url):
    http = urllib3.PoolManager()
    result = http.request('Get', url)
    if result.status == requests.codes.ok:
        return result.data
    else:
        return None


def _reslove(url):
    with requests.Session() as s:
        try:
            result = s.get(
                url,
                headers={
                    'User-Agent': random.choice(USER_AGENTS),
                    'Accept-Encoding': 'identity, deflate, compress, gzip'
                },
                proxies=get_proxies(),
                verify=get_verify(url),
                timeout=2,
            )
        # except requests.exceptions.Timeout:
        except requests.ReadTimeout:
            _tips_msg('request read timeout')
            return
        except requests.exceptions.SSLError:
            _tips_msg('request error')
            return
        if result.status_code in (requests.codes.NOT_FOUND,
                                  requests.codes.forbidden):
            return _emergency_reslove(url)
        elif result.status_code == requests.codes.ok:
            return result.content
        else:
            return None


def _local_resolve(url):
    # False --> can't local relosve
    # True --> can local reslove
    try:
        r = requests.head(url, timeout=2)
    except (requests.ConnectionError, requests.ConnectTimeout,
            requests.ReadTimeout):
        return False
    return True


def resolve_process(url):
    # if _local_resolve(url) == None:
    #     return None
    if not _local_resolve(url):
        _set_proxy()
    result = _reslove(url)
    return result


def is_validURL(url):
    # url_parttern = re.compile(r'^(https?|ftp)://([a-zA-Z0-9._]){1,}/.*$', re.I)
    url_parttern = re.compile(URI, re.I)
    if url_parttern.match(url):
        return True
    return False


def get_title(page):
    html = pq(page)
    title = html.find("title").html().strip()
    return title


def _tips_msg(tips):
    tips = "<< {} >>".format(tips)
    print(tips)


def _get_title_link(url):
    if not is_validURL(url):
        _tips_msg('Check the URL again (eg: http://www.google.com/)')
        return None
    else:
        page = resolve_process(url)
        if page:
            title = get_title(page)
        else:
            _tips_msg('`link` can\'t resolve')
            return None
        format_link = FORMAT_SCHEME['link'].format(title=title, url=url)
    return format_link


def _get_comment(comment):
    format_comment = ''
    if comment:
        comment = ' '.join(comment).capitalize()
        format_comment = FORMAT_SCHEME['quote'].format(comment=comment)
    return format_comment


def _get_date(date):
    format_date = ''
    if date:
        dt = datetime.now()
        date = email.utils.format_datetime(dt)
        format_date = FORMAT_SCHEME['date'].format(date=date)
    return format_date


def _exit_file(path):
    if os.path.exists(path):
        return True
    return False


def _format_codes(language, format_codes):
    format_codes = FORMAT_SCHEME['code'].format(
        language=language, code=format_codes)
    return format_codes


def _get_codes(language, file_path):
    codes = ''
    if file_path and _exit_file(file_path):
        with open(file_path, mode='r') as f:
            for line in f.readlines():
                one_line = '> ' + line
                codes = codes + one_line
    return codes


def _get_color_code(color, language, code):
    format_color_code = code
    if color:
        lexter = get_lexer_by_name(language)
        format_color_code = highlight(
            code, lexter, TerminalFormatter(bg='dark'))

    if language:
        format_color_code = _format_codes(language, format_color_code)
    return format_color_code


def _export_string(link, date, comment, language, codes, color=False):
    color_codes = _get_color_code(color, language, codes)
    export_string = FORMAT_SCHEME['result'].format(
        link=link, date=date, comment=comment, codes=color_codes)
    return export_string


def export_format(link, date, comment, codes, args):
    language = args['language']
    is_color = args['color']
    is_print = args['print']
    file_path = args['save']

    if is_print:
        print_string = _export_string(
            link, date, comment, language, codes, color=is_color)
        _tips_msg('print out')
        print(print_string)

    if file_path:
        output_string = _export_string(link, date, comment, language, codes)
        try:
            with open(file_path, 'a') as f:
                f.write(output_string + '\n')
                _tips_msg('success: store in ' + '`' + str(file_path) + '`')
        except (FileNotFoundError, PermissionError) as e:
            _tips_msg('save error')
            _tips_msg(e)


def qkmd(args):
    url = args['link']
    title = args['title']
    if title:
        title = ' '.join(args['title']).strip()
    if url and title:
        format_link = FORMAT_SCHEME['link'].format(title=title, url=url)
    else:
        format_link = _get_title_link(url)

    if format_link:
        format_date = _get_date(args['date'])

        format_comment = _get_comment(args['comment'])

        language, file_path = args['language'], args['source']
        format_codes = _get_codes(language, file_path)

        export_format(format_link, format_date, format_comment, format_codes,
                      args)


def get_parser():
    parser = argparse.ArgumentParser(
        description=
        'Quickly formatting markdown `link`, convenient your daily life/work.')
    parser.add_argument(
        'link',
        type=str,
        nargs='?',
        help='generate the markdown format link',
    )
    parser.add_argument(
        '-d',
        '--date',
        help='append `RFC 2822` date format',
        action='store_true')
    parser.add_argument(
        '-v',
        '--version',
        help='display current version of `qkmd`',
        action='store_true')
    parser.add_argument(
        '-c',
        '--comment',
        metavar='comment',
        help='give the link a simple comment',
        type=str,
        nargs='*')
    parser.add_argument(
        '-l',
        '--language',
        metavar='language',
        help='specific the code language',
        # Case insensitive
        type=str.lower,
        choices=SUPORT_LANGUAGE,
        default=None)
    parser.add_argument(
        '-s',
        '--source',
        metavar='source-code-file',
        help='give the source code snip file',
        type=str,
        default=None)
    parser.add_argument(
        '-C',
        '--color',
        help='source code syntax hightline',
        action='store_true')
    parser.add_argument(
        '-t',
        '--title',
        metavar='title',
        nargs='*',
        type=str.lower,
        help='add title manually')
    parser.add_argument(
        '-o',
        '--save',
        metavar='output-file',
        type=str,
        help='save the markdown to a file')
    parser.add_argument(
        '-P',
        '--print',
        action='store_false',
        help='turn off print the markdown format in screen')

    return parser


def command_runner():
    parser = get_parser()
    args = vars(parser.parse_args())
    # print(args)
    if args['version']:
        print(__version__)
        return

    # if color turn on, source and language must give together
    # if color turn off, source and language appear/disapper together
    if args['color']:
        if not (args['source'] and args['language']):
            parser.error('color option require --source and --language')
    elif bool(args['source']) ^ bool(args['language']):
        parser.error('--source and --language must be given together')

    if not args['link']:
        return parser.print_help()
    else:
        qkmd(args)


if __name__ == '__main__':
    command_runner()
