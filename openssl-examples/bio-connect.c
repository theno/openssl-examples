#include "stdio.h"        // printf(), sprintf(), exit()

#include "openssl/bio.h"  // BIO, BIO_NOCLOSE,
                          // BIO_new_connect(), BIO_new_fp(), BIO_do_connect(),
                          // BIO_puts(), BIO_read(), BIO_write(), BIO_free()
#include "openssl/err.h"  // ERR_print_errors_fp()

/* int bio_connect(char *hostname)
 *
 * Send an HTTP request to hostname (port 80) and print the reply to stdout.
 *
 * It follows the example of `man BIO_s_connect` (version: OpenSSL-1.1.0).
 *
 *
 * Documentation of the used types and functions:
 *
 * https://www.openssl.org/docs/man1.1.0/crypto/BIO_new_fp.html
 *
 *     BIO_new_fp()
 *
 * https://www.openssl.org/docs/man1.1.0/crypto/BIO_gets.html
 *
 *     BIO_puts()
 *     BIO_read()
 *     BIO_write()
 *
 * https://www.openssl.org/docs/man1.1.0/crypto/BIO_new.html
 *
 *     BIO_free()
 *
 * https://www.openssl.org/docs/man1.1.0/crypto/BIO_s_connect.html
 *
 *     BIO_new_connect()
 *     BIO_do_connect()
 *
 * https://www.openssl.org/docs/man1.1.0/crypto/ERR_print_errors_fp.html
 *
 *     ERR_print_errors_fp()
 *
 */
int bio_connect(char *hostname)
{
    /* declare BIOs
     * BIO stands for Basic Input Output
     * it is similar to an input/output stream pointer */

    /* connection BIO */
    BIO *cbio;
    /* stdout BIO */
    BIO *out;

    /* addressee of the connection */
    char name[1024];
    /* request */
    char req[1024];
    /* length of the reply to the HTTP request */
    int len;
    /* temporary buffer to outreach the reply from cbio to out
     * (in this example, the BIOs are not chained) */
    char tmpbuf[1024];

    /* create and setup the TCP/IP connection */

    /* name = "<hostname>:<port>" */
    sprintf(name, "%s:%s", hostname, "http");

    cbio = BIO_new_connect(name);
    out = BIO_new_fp(stdout, BIO_NOCLOSE);

    if (BIO_do_connect(cbio) <= 0) {
        fprintf(stderr, "Error connecting to server\n");
        ERR_print_errors_fp(stderr);
        exit(1);
    }

    /* send HTTP request to the server <hostname> */

    sprintf(req, "GET / HTTP/1.1\x0D\x0AHost: %s\x0D\x0A\x43onnection: Close\x0D\x0A\x0D\x0A", hostname);
    BIO_puts(cbio, req);

    /* read HTTP response from server and print to stdout */

    for ( ; ; ) {
        len = BIO_read(cbio, tmpbuf, 1024);
        if (len <= 0) {
            break;
        }
        BIO_write(out, tmpbuf, len);
    }

    /* close TCP/IP connection and free used BIOs */

    BIO_free(cbio);
    BIO_free(out);

    return 0;
}

int main(int argc, char *argv[])
{
    if (argc > 1) {
        bio_connect(argv[1]);
    } else {
        printf("Usage: %s <hostname>\n", argv[0]);
    }
    return 0;
}
