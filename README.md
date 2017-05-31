
----
___Please contribute and send pull requests with commented code-examples or OpenSSL programming links.___

----

# OpenSSL Examples

__Commented__ and __explained__ C-code examples which show how to use the API
of OpenSSL.


## Usage

The (bash) commands to run this code will be executed by [Fabric][9] tasks:

```
fab -l

Available commands:

    clean                 Remove temporary files and compiled binaries not
                          under version control.

    dev_check_urls        Devel-task: Find broken URLs in
                          `links.md` and `README.md`.
    dev_functional_tests  Devel-task: Run all examples, check urls, and
                          run external examples.
    dev_push_ci           Devel-task: Push to remote origin repo and trigger
                          Travis CI rebuilds

    dex                   Download more external OpenSSL code examples.
    dex_intro_openssl     Compile and run external example
                                          `downloaded-examples/intro-openssl`

    run                   Compile and run all examples of this repository.
    run_bio_connect       Compile and run `openssl-examples/bio-connect.c`.
    run_tls_connect       Compile and run `openssl-examples/tls-connect.c`.
    run_tls_extension_18  Compile and run `openssl-examples/tls-extension-18.c`
```

Show task details, e.g.:
```
fab -d dex
```

Compile and run the examples:

```bash
fab run

fab run_tls_connect
fab run_tls_extension_18
```

Hide the output in order to see only the commands used to run the
examples:

```bash
fab <example-task> --hide output
```

You can copy the commands and execute them manually.

Download more external (unfortunately outdated) code examples:

```bash
fab dex
```


## More Documentation of the OpenSSL API

It ist hard to find well explaned introducing documentation of the
OpenSSL [API][4] which is [not][5] out[dated][6].

At least, here are some links:

__[OpenSSL Programming Links](./links.md)__


## Motivation: Outdated Directory `demos` in OpenSSL

From the [`README`][1] of the `demos` dir:

    "Don't expect any of these programs to work with current OpenSSL releases"

This is true, for example running `bio/client-arg.c` compiled with gcc ends in
a frustrating segfault.

A complex API should be accompanied by usage examples.  These examples have to
be well explained and commented and must not end in a segfault or any other
error.  Even no examples is better than short commented non-working demo code.

Conclusion:  The `demos` dir in OpenSSL should be removed in order to not to
dount OpenSSL beginners!  More constructive: __It should be replaced by an
examples directory with working, explained and commented code.__

Goal of this repo is to become a suite of well-commented working code examples
under test which show and explane how to use the OpenSSL API in order to
replace\* the `demos` dir of OpenSSL.

**Please send pull requests with commented code-examples to achieve this
goal!**


## Consideration: OpenSSL Wiki

The official OpenSSL [wiki][2] is in danger to become outdated, too (for
example this useless, non-versioned, redundand\*\* [API listing][8]).
As the OpenSSL source code repository has [moved to github][7] it remains to be
hoped that the wiki will be moved [to it][3], too.  As more closer
documentation is to its source code, the more up-to-date it will be.


----

\*) It is up to the OpenSSL developers team to decide to delete or to replace
the `demos` dir.

\*\*) Usefull, versioned, official API listing:
https://www.openssl.org/docs/manmaster/man3/

[1]: https://github.com/openssl/openssl/blob/master/demos/README
[2]: https://wiki.openssl.org/index.php/Main_Page
[3]: https://github.com/openssl/openssl/wiki
[4]: https://www.openssl.org/docs/manmaster/man3/
[5]: http://shop.oreilly.com/product/9780596002701.do
[6]: http://shop.oreilly.com/product/9780596003944.do
[7]: https://www.openssl.org/blog/blog/2016/10/12/f2f-rt-github/
[8]: https://wiki.openssl.org/index.php/Documentation_Index
[9]: http://www.fabfile.org/installing.html
