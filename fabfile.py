# -*- coding: utf-8 -*-

import inspect
from functools import wraps
from os.path import dirname

from fabric.api import execute, local, task as fabric_task
from fabric.context_managers import hide, warn_only


# inspired by: http://stackoverflow.com/a/6618825
def flo(string):
    '''Return the string given by param formatted with the callers locals.'''
    callers_locals = {}
    frame = inspect.currentframe()
    try:
        outerframe = frame.f_back
        callers_locals = outerframe.f_locals
    finally:
        del frame
    return string.format(**callers_locals)


def _wrap_with(color_code):
    '''Color wrapper.
    Example:
        >>> blue = _wrap_with('34')
        >>> print(blue('text'))
        \033[34mtext\033[0m
    '''
    def inner(text, bold=False):
        '''Inner color function.'''
        code = color_code
        if bold:
            code = flo("1;{code}")
        return flo('\033[{code}m{text}\033[0m')
    return inner


black = _wrap_with('30')
red = _wrap_with('31')
green = _wrap_with('32')
yellow = _wrap_with('33')
blue = _wrap_with('34')
magenta = _wrap_with('35')
cyan = _wrap_with('36')
white = _wrap_with('37')
default_color = _wrap_with('0')


def first_paragraph(multiline_str, without_trailing_dot=True, maxlength=None):
    '''Return first paragraph of multiline_str as a oneliner.
    When without_trailing_dot is True, the last char of the first paragraph
    will be removed, if it is a dot ('.').
    Examples:
        >>> multiline_str = 'first line\\nsecond line\\n\\nnext paragraph'
        >>> print(first_paragraph(multiline_str))
        first line second line
        >>> multiline_str = 'first \\n second \\n  \\n next paragraph '
        >>> print(first_paragraph(multiline_str))
        first second
        >>> multiline_str = 'first line\\nsecond line\\n\\nnext paragraph'
        >>> print(first_paragraph(multiline_str, maxlength=3))
        fir
        >>> multiline_str = 'first line\\nsecond line\\n\\nnext paragraph'
        >>> print(first_paragraph(multiline_str, maxlength=78))
        first line second line
        >>> multiline_str = 'first line.'
        >>> print(first_paragraph(multiline_str))
        first line
        >>> multiline_str = 'first line.'
        >>> print(first_paragraph(multiline_str, without_trailing_dot=False))
        first line.
        >>> multiline_str = ''
        >>> print(first_paragraph(multiline_str))
        <BLANKLINE>
    '''
    stripped = '\n'.join([line.strip() for line in multiline_str.splitlines()])
    paragraph = stripped.split('\n\n')[0]
    res = paragraph.replace('\n', ' ')
    if without_trailing_dot:
        res = res.rsplit('.', 1)[0]
    if maxlength:
        res = res[0:maxlength]
    return res


# for decorator with arguments see: http://stackoverflow.com/a/5929165
def print_doc1(*args, **kwargs):
    '''Print the first paragraph of the docstring of the decorated function.
    The paragraph will be printed as a oneliner.
    May be invoked as a simple, argument-less decorator (i.e. ``@print_doc1``)
    or with named arguments ``color``, ``bold``, ``prefix`` of ``tail``
    (eg. ``@print_doc1(color=utils.red, bold=True, prefix=' ')``).
    Examples:
        >>> @print_doc1
        ... def foo():
        ...     """First line of docstring.
        ...
        ...     another line.
        ...     """
        ...     pass
        ...
        >>> foo()
        \033[34mFirst line of docstring\033[0m
        >>> @print_doc1
        ... def foo():
        ...     """First paragraph of docstring which contains more than one
        ...     line.
        ...
        ...     Another paragraph.
        ...     """
        ...     pass
        ...
        >>> foo()
        \033[34mFirst paragraph of docstring which contains more than one line\033[0m
    '''
    # output settings from kwargs or take defaults
    color = kwargs.get('color', blue)
    bold = kwargs.get('bold', False)
    prefix = kwargs.get('prefix', '')
    tail = kwargs.get('tail', '\n')

    def real_decorator(func):
        '''real decorator function'''
        @wraps(func)
        def wrapper(*args, **kwargs):
            '''the wrapper function'''
            try:
                prgf = first_paragraph(func.__doc__)
                print(color(prefix + prgf + tail, bold))
            except AttributeError as exc:
                name = func.__name__
                print(red(flo('{name}() has no docstring')))
                raise(exc)
            return func(*args, **kwargs)
        return wrapper

    invoked = bool(not args or kwargs)
    if not invoked:
        # invoke decorator function which returns the wrapper function
        return real_decorator(func=args[0])

    return real_decorator


def print_full_name(*args, **kwargs):
    '''Decorator, print the full name of the decorated function.
    May be invoked as a simple, argument-less decorator (i.e. ``@print_doc1``)
    or with named arguments ``color``, ``bold``, or ``prefix``
    (eg. ``@print_doc1(color=utils.red, bold=True, prefix=' ')``).
    '''
    color = kwargs.get('color', default_color)
    bold = kwargs.get('bold', False)
    prefix = kwargs.get('prefix', '')
    tail = kwargs.get('tail', '')

    def real_decorator(func):
        '''real decorator function'''
        @wraps(func)
        def wrapper(*args, **kwargs):
            '''the wrapper function'''
            first_line = ''
            try:
                first_line = func.__module__ + '.' + func.__qualname__
            except AttributeError:
                first_line = func.__name__
            print(color(prefix + first_line + tail, bold))
            return func(*args, **kwargs)
        return wrapper

    invoked = bool(not args or kwargs)
    if not invoked:
        # invoke decorator function which returns the wrapper function
        return real_decorator(func=args[0])

    return real_decorator


def supported(*args, **kwargs):
    '''Only execute decorated task-function if the OpenSSL version is supported.

    Keyword-Args:
        openssl_versions: List of OpenSSL version strings

    Example:

        @task
        @supported(openssl_versions=['OpenSSL-1.1.0', 'OpenSSL-1.0.2'])
        def run_openssl_example_xyz():
            ...
    '''
    supported_versions = kwargs.get('openssl_versions', [])

    def real_decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            with hide('running'):
                cur = local('openssl version', capture=True)
            for ver in supported_versions:
                if cur.startswith(ver.replace('-', ' ')):
                    return func(*args, **kwargs)
            print(flo('Example does not support {cur} ' + yellow('(skip)')))
            return
        return wrapper

    # if the decorated function is actually invoked
    invoked = bool(not args or kwargs)
    if not invoked:
        return real_decorator(func=args[0])
    return real_decorator


def task(func):
    '''Composition of decorator functions for inherent self-documentation on
    task execution.

    On execution, each task prints out its name and its first docstring line.
    '''
    prefix = '\n# '
    tail = '\n'
    return fabric_task(print_full_name(
        color=magenta, prefix=prefix, tail=tail)(print_doc1(func)))


@task
def clean(deldex=None):
    '''Remove temporary files and compiled binaries not under version control.

    Args:
        deldex: Also delete directory `downloaded-examples`.
    '''
    basedir = dirname(__file__)

    print(cyan('delete files not under version control'))
    ignore_filter = r"grep -v downloaded-examples | grep -v '\.c$' |"
    local("bash -c '" +
          flo('cd {basedir}  &&  '
              'git check-ignore **/* | {ignore_filter} xargs rm -rvf') +
          "'")

    print(cyan('\ndelete temp files and dirs for editing'))
    local(flo(
        'rm -rf  '
        '{basedir}/.cache  '
        '{basedir}/.ropeproject  '
    ))

    if deldex is not None:
        print(cyan('\ndelete dir `downloaded-examples` (deldex)'))
        local(flo('rm -rf {basedir}/downloaded-examples'))


# ## Travis CI related tasks

@print_full_name(color=cyan, prefix='\n## ', tail='\n')
def incorporate_examples_into_openssl():
    # git remote add upstream git://github.com/openssl/openssl.git
    pass
    # * reset openssl fork from previous changes
    # * update openssl fork from orig openssl
    # * for each branch (1.1.0, 1.0.2, master) apply changes and push to origin
    #   which triggers the Travis CI rebuild


@task
def dev_push_ci():
    '''Devel-task: Push to remote origin repo and also trigger Travis CI
    rebuilds for branches of current OpenSSLs with this openssl-examples
    incorporated using an OpenSSL repository fork.

    Pushing to remote origin triggers a Travis CI rebuild which runs the meta
    tests only (c.f. file `.travis.yml`).
    '''
    basedir = dirname(__file__)

    print(cyan('## push master branch to remote origin\n'))
    local(flo('cd {basedir}  &&  git push origin master'))

    incorporate_examples_into_openssl()


@task
def dev_check_urls():
    '''Devel-task: Find broken URLs in `links.md` and `README.md`.'''
    basedir = dirname(__file__)
    for filename in ['links.md', 'README.md']:
        urls = local('bash -c "' +
                     flo(
                         'grep http {basedir}/{filename} | '
                         r"sed 's/http/\nhttp/g' | "
                         'grep ^http | '
                         r"sed 's/\(^http[^ <]*\)\(*\)/\1/g' | "
                         'sort -u'
                     ) +
                     '"', capture=True).split('\n')
        for url in urls:
            url = url.strip()
            cert_check = ''
            if url in ['linuxjournal']:
                cert_check = '--no-check-certificate'
            local(flo('wget --spider --server-response {cert_check} "{url}"'))


@task
def dev_functional_tests(run_only=None):
    '''Devel-task: Run all examples, check urls, and run external examples.

    Keyword-Args:
        run_only:
            'examples': Only run openssl-examples of this repository
            'meta':     Only check for broken urls, and install and run
                        external examples
            None:       Run all tests

    This task is used by the Travis Continuous Integration (CI) setup.
    '''
    if run_only is not None:
        print(flo('only run tests: {run_only}'))
    else:
        print('run all tests')

    if not run_only or run_only == 'examples':
        # run all examples of this repository
        execute(run)

    if not run_only or run_only == 'meta':
        execute(dev_check_urls)
        # run external examples
        execute(dex)
        execute(dex_intro_openssl)


# ## tasks for external examples

@task
def dex():
    '''Download more external OpenSSL code examples.

    Only download if the target dir not exists.

    Touched files and dirs:

        > tree -L 1 downloaded-examples

        downloaded-examples
        ├── demos
        ├── intro-openssl
        ├── NSwO-1.3
        ├── spc-1.1
        └── codingstyle.md

    dex is a fantasy-acronym for downloaded_example.
    '''
    basedir = dirname(__file__)
    examples_basedir = flo('{basedir}/downloaded-examples')
    local(flo('mkdir -p {examples_basedir}'))

    print(cyan('\n## demos directory of OpenSSL src\n'))
    local(flo('cd {examples_basedir}  &&  '
              '[ -d demos ] && echo skip OpenSSL demos directory || '
              'svn export '
              'https://github.com/openssl/openssl/trunk/demos  demos'))

    print(cyan('\n## Network Security with OpenSSL\n'))
    local(flo('cd {examples_basedir}  &&  '
              '[ -d NSwO-1.3 ] && echo skip Network Security with OpenSSL || '
              'wget '
              'http://examples.oreilly.com/9780596002701/NSwO-1.3.tar.gz && '
              'tar xf NSwO-1.3.tar.gz'))

    print(cyan('\n## Secure Programming Cookbook\n'))
    local(flo('cd {examples_basedir}  &&  '
              '[ -d spc-1.1 ] && echo skip Secure Programming Cookbook || '
              'wget '
              'http://examples.oreilly.com/9780596003944/spc-1.1.tar.gz && '
              'tar xf spc-1.1.tar.gz'))

    print(cyan('\n## Secure programming with the OpenSSL API\n'))
    local(flo('cd {examples_basedir}  &&  '
              '[ -d intro-openssl ] && '
              'echo skip Secure Programming with the OpenSSL API || ('
              'wget '
              'http://download.boulder.ibm.com'
              '/ibmdl/pub/software/dw/linux/l-openssl/intro-openssl.zip && '
              'mkdir intro-openssl && '
              'cd intro-openssl && '
              'unzip ../intro-openssl.zip && '
              """sed -i 's/\\r$//' *.c"""
              ')'))

    print(cyan('\n## OpenSSL Coding Style\n'))
    local(flo('cd {examples_basedir}  &&  '
              '[ -e codingstyle.md ] && echo skip download codingstyle.txt || ('
              'wget -O codingstyle.md  '
              'https://www.openssl.org/policies/codingstyle.txt && '
              r"sed -i 's/\s\s\+Chapter.\+:\s\+Deleted//g' codingstyle.md && "
              r"sed -i 's/\s\s\+OpenSSL/# OpenSSL/g' codingstyle.md && "
              r"sed -i 's/\s\s\+Chapter/## Chapter/g' codingstyle.md && "
              r"sed -i 's/\s\s\+Chapter/## Chapter/g' codingstyle.md && "
              r"sed -i 's/\s\s\+Appendix/## Appendix/g' codingstyle.md && "
              'cat --squeeze-blank codingstyle.md > codingstyle.tmp.md && '
              'mv codingstyle.tmp.md  codingstyle.md'
              ')'))


@task
def dex_intro_openssl():
    '''Compile and run external example `downloaded-examples/intro-openssl/`
    written by Kenneth Ballard.

    https://www.ibm.com/developerworks/linux/library/l-openssl/index.html
    '''
    basedir = dirname(__file__)
    example_dir = flo('{basedir}/downloaded-examples/intro-openssl')

    print(cyan('## Compile `nossl.c`\n'))
    local(flo('cd {example_dir}  &&  '
              'gcc -Wall nossl.c -o nossl -lssl -lcrypto'))

    print(cyan('\n## Run `nossl`\n'))
    local(flo('cd {example_dir}  &&  '
              './nossl > nossl_output  &&  head nossl_output'))

    print(cyan('\n## Compile `withssl.c`\n'))
    local(flo('cd {example_dir}  &&  '
              'gcc -Wall withssl.c -o withssl -lssl -lcrypto'))

    # raises a segmentation fault
    print(cyan('\n## Run `withssl` -- raises segmentation fault\n'))
    with warn_only():
        local(flo('cd {example_dir}  &&  '
                  './withssl > withssl_output  &&  head withssl_output'))


# ## tasks to run the c-code examples

@task
def run():
    '''Compile and run all examples of this repository.'''
    execute(run_bio_connect)
    execute(run_tls_connect)
    execute(run_tls_extension_18)


def compile_and_run(example, args='', libs='-lssl -lcrypto'):
    basedir = dirname(__file__)
    example_dir = flo('{basedir}/openssl-examples')

    print(cyan(flo('## Compile `{example}.c`\n')))
    local(flo('cd {example_dir}  &&  '
              'gcc -Wall {example}.c -o {example} {libs}'))

    print(cyan(flo('\n## Run `{example}`\n')))
    local(flo('cd {example_dir}  &&  '
              './{example} {args} > {example}_output  &&  '
              'head {example}_output'))


@task
@supported(openssl_versions=['OpenSSL-1.1.0', 'OpenSSL-1.0.2'])
def run_bio_connect():
    '''Compile and run `openssl-examples/bio-connect.c`.'''
    compile_and_run('bio-connect', args='editorconfig.org', libs='-lcrypto')


@task
@supported(openssl_versions=['OpenSSL-1.1.0', 'OpenSSL-1.0.2'])
def run_tls_connect():
    '''Compile and run `openssl-examples/tls-connect.c`.'''
    compile_and_run('tls-connect', args='editorconfig.org')


@task
@supported(openssl_versions=['OpenSSL-1.1.0', 'OpenSSL-1.0.2'])
def run_tls_extension_18():
    '''Compile and run `openssl-examples/tls-extension-18.c`.'''
    compile_and_run('tls-extension-18')
