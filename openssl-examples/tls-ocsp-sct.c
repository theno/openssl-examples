#include "openssl/bio.h"
#include "openssl/err.h"
#include "openssl/ssl.h"

int tls_handshake(char *hostname)
{
    /* SSL context structure */
    SSL_CTX *ctx;
    /* SSL connection structure */
    SSL *ssl;
    /* connection BIO (basic input output) */
    BIO *cbio;

    /* addressee <hostname> of the connection */
    char name[1024];
    /* request */
    char req[1024];
    /* response */
    char resp[1024];
    int len;

    /* Set up the OpenSSL library */

    SSL_load_error_strings();
    SSL_library_init();

    /* create SSL context structure and load the trust store
     * (accepted root ca-certificates) */

    ctx = SSL_CTX_new(SSLv23_client_method());
    if(! ctx) {
        // TODO error
    }

    if(! SSL_CTX_load_verify_locations(ctx,
                                       "/etc/ssl/certs/ca-certificates.crt",
                                       NULL)) {
        // TODO error
    }

    /* Setup the SSL connection */

    cbio = BIO_new_ssl_connect(ctx);
    BIO_get_ssl(cbio, &ssl);

    /* Set flag SSL_MODE_AUTO_RETRY */
    SSL_set_mode(ssl, SSL_MODE_AUTO_RETRY);

    /* Connect to server <hostname> */

    /* name = "<hostname>:<port>" */
    sprintf(name, "%s:%s", hostname, "https");

    BIO_set_conn_hostname(cbio, name);

    if(BIO_do_connect(cbio) <= 0) {
        // TODO error
    }

    /* Check the certificate */

    if(SSL_get_verify_result(ssl) != X509_V_OK) {
        // TODO error
    }
}
