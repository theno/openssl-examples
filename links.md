# OpenSSL Programming Links

It is hard to find explaining documentation and well commented code-examples
about programming with OpenSSL which are not outdated and running with
current OpenSSL versions.

Current OpenSSL versions:
 * since 2016-08-26: OpenSSL-1.1.0 (until 2018-08-31)
 * since 2015-01-22: OpenSSL-1.0.2 (until 2019-12-31; LTS [Long Term Support])

OpenSSL-1.0.2 is API\* stable to OpenSSL-1.0.0 (released on 2010-03-29).

Code-examples older than this dates need to be checked if they are outdated.
If a documentation or code-example is about OpenSSL-0.9.x it is outdated.

## Official

* Docs: https://www.openssl.org/docs/
* OpenSSL-API: https://www.openssl.org/docs/manpages.html
  * master: https://www.openssl.org/docs/manmaster/
    * Short explanations: https://www.openssl.org/docs/manmaster/man7/
  * OpenSSL-1.1.0
    * ssl library: https://www.openssl.org/docs/man1.1.0/ssl/
    * crypto library: https://www.openssl.org/docs/man1.1.0/crypto/
  * OpenSSL-1.0.2
    * ssl library: https://www.openssl.org/docs/man1.0.2/ssl/
    * crypto library: https://www.openssl.org/docs/man1.0.2/crypto/
* Release Strategy: https://www.openssl.org/policies/releasestrat.html  
  Explains which OpenSSL versions are currently supported and will be in future
* Demos (outdated): https://github.com/openssl/openssl/tree/master/demos
* source dir `apps`: https://github.com/openssl/openssl/tree/master/apps  
  How OpenSSL itself uses its API
  * `s_client.c`:
    https://github.com/openssl/openssl/blob/master/apps/s_client.c
* OpenSSL-Wiki: https://wiki.openssl.org/index.php/Main_Page
  * Getting Started  
    https://wiki.openssl.org/index.php/Libcrypto_API#Getting_Started
* OpenSSL-Blog: Engine Building
  * Lesson 1: A Minimum Useless Engine  
    https://www.openssl.org/blog/blog/2015/10/08/engine-building-lesson-1-a-minimum-useless-engine/
  * Lesson 2: An Example MD5 Engine  
    https://www.openssl.org/blog/blog/2015/11/23/engine-building-lesson-2-an-example-md5-engine/

## Books

* __Network Security With OpenSSL__ (outdated, from 2002)  
  http://shop.oreilly.com/product/9780596002701.do  
  "The" OpenSSL-Book, but outdated
  * Example-Code: http://examples.oreilly.com/9780596002701/
* Secure Programming Cookbook for C and C++ (outdated, from 2003)  
  http://shop.oreilly.com/product/9780596003944.do  
  Chapter 9. Networking
  * Example-Code: http://examples.oreilly.com/9780596003944/

## Articles

* __Secure programming with the OpenSSL API__ (from 2004, updated 2012)  
  https://www.ibm.com/developerworks/linux/library/l-openssl/index.html  
  recommended by many users
* SSL Programming Tutorial (from 2006)  
  http://h41379.www4.hpe.com/doc/83final/ba554_90007/ch04s03.html
* An Introduction to OpenSSL Programming (from 2001)
  * Part I: https://www.linuxjournal.com/article/4822
  * Part II: https://www.linuxjournal.com/article/5487
* OpenSSL: Implementierung innerhalb eines Client- und Server-Programms
  (C++, from 2010)  
  https://heise.de/-1050619
* OpenSSL-WikiBook: https://en.wikibooks.org/wiki/OpenSSL
  * OpenSSL/Initialization: https://en.wikibooks.org/wiki/OpenSSL/Initialization

## Presentations

 * Programming with OpenSSL and libcrypto in examples (from 2014)  
   https://people.freebsd.org/~syrinx/presentations/openssl/OpenSSL-Programming-20140424-01.pdf
 * Programming OpenSSL (outdated, from 2001)  
   https://www.cs.utah.edu/~swalton/Documents/Articles/Programming-OpenSSL.pdf

## Code-Examples

 * `sslconnect.c`: How to make a basic SSL/TLS connection (from 2014)  
   http://fm4dd.com/openssl/sslconnect.htm
 * openSSL Tutorial (outdated, about OpenSSL-0.9.6c)  
   http://rudeserver.com/ssl/openssltutorial.html
 * Stackoverflow:  
   https://stackoverflow.com/questions/tagged/openssl+c
   * Programmatically verify certificate chain using OpenSSL API  
     https://stackoverflow.com/questions/16291809
   * How do you verify a public key was issued by your private CA?  
     https://stackoverflow.com/questions/3412032
   * Client and Server communication using ssl c/c++ - SSL protocol don't works 
     https://stackoverflow.com/questions/11705815
   * How to compile .c file with OpenSSL includes?  
     https://stackoverflow.com/questions/3368683
   * How to use OpenSSL in GCC?  
     https://stackoverflow.com/questions/1894013
 * PyOpenSSL Client Example (Python)  
   https://github.com/pyca/pyopenssl/blob/master/examples/sni/client.py

## Repositories

* Examples  
  https://github.com/search?l=C&o=desc&q=openssl+example&s=forks&type=Repositories&utf8=%E2%9C%93
  * https://github.com/darrenjs/openssl_examples
  * https://github.com/lazyp/openssl-bio-example/blob/master/src/openssl_client.c
  * https://github.com/conradoplg/openssl_examples/blob/master/src/tls_client.c
  * https://github.com/IamLupo/openssl-examples/tree/master/sslv3/basic
* Demos  
  https://github.com/search?l=C&q=openssl+demos&type=Repositories&utf8=%E2%9C%93
* Howto  
  https://github.com/search?utf8=%E2%9C%93&q=openssl+howto&type=Repositories
  * https://github.com/mdaxini/howto-openssl


----

\*) In OpenSSL, API (Application Programming Interface) is named as ABI
    (Application Binary Interface).
