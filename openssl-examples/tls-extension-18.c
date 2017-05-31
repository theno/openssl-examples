#include "stdio.h"
#include "string.h"
#include "stdlib.h"

#include "openssl/ssl.h"
#include "openssl/bio.h"
#include "openssl/err.h"

/* for istext(), dup_bio_out() */
//#include "openssl/apps.h"

# define B_FORMAT_TEXT   0x8000
# define FORMAT_TEXT    (1 | B_FORMAT_TEXT)     /* Generic text */


static int istext(int format)
{
    return (format & B_FORMAT_TEXT) == B_FORMAT_TEXT;
}


BIO *dup_bio_out(int format)
{
    BIO *b = BIO_new_fp(stdout,
                        BIO_NOCLOSE | (istext(format) ? BIO_FP_TEXT : 0));
    return b;
}

static int serverinfo_cli_parse_cb(SSL *s, unsigned int ext_type,
                                   const unsigned char *in, size_t inlen,
                                   int *al, void *arg)
{
    char pem_name[100];
    unsigned char ext_buf[4 + 65536];
    static BIO *bio_c_out = NULL;

    BIO *bio_c_msg = NULL;

    static int c_debug = 0;
    static int c_quiet = 0;
    int c_msg = 0;

    //bio_c_out = BIO_new(BIO_s_null());
    if (bio_c_out == NULL) {
        if (c_quiet && !c_debug) {
            bio_c_out = BIO_new(BIO_s_null());
            if (c_msg && !bio_c_msg)
                bio_c_msg = dup_bio_out(FORMAT_TEXT);
        } else if (bio_c_out == NULL)
            bio_c_out = dup_bio_out(FORMAT_TEXT);
    }

    /* Reconstruct the type/len fields prior to extension data */
    ext_buf[0] = ext_type >> 8;
    ext_buf[1] = ext_type & 0xFF;
    ext_buf[2] = inlen >> 8;
    ext_buf[3] = inlen & 0xFF;
    memcpy(ext_buf + 4, in, inlen);

    BIO_snprintf(pem_name, sizeof(pem_name), "SERVERINFO FOR EXTENSION %d",
                 ext_type);
    PEM_write_bio(bio_c_out, pem_name, "", ext_buf, 4 + inlen);
    return 1;
}

int main()
{
    /* head bio object */
    BIO* bio;

    /* ssl bio layer */
    SSL* ssl;

    /* socket */
    SSL_CTX* ctx;

    int p;

    //char* request = "GET / HTTP/1.1\x0D\x0AHost: www.verisign.com\x0D\x0A\x43onnection: Close\x0D\x0A\x0D\x0A";
    char* request = "GET / HTTP/1.1\x0D\x0AHost: ritter.vg\x0D\x0A\x43onnection: Close\x0D\x0A\x0D\x0A";
    char r[1024];

    /* Set up the library */
    SSL_library_init();
    SSL_load_error_strings();

    /* https://www.openssl.org/docs/man1.1.0/crypto/OpenSSL_add_all_algorithms.html */
    /* https://www.openssl.org/docs/man1.0.2/crypto/OpenSSL_add_all_algorithms.html */
    OpenSSL_add_all_algorithms();

    /* Set up the SSL context */
    ctx = SSL_CTX_new(SSLv23_client_method());
    if(! ctx) {
        fprintf(stderr, "Error creating SSL context");
        ERR_print_errors_fp(stderr);
        SSL_CTX_free(ctx);
        return 0;
    }

    /* Load the trust store */

    if(! SSL_CTX_load_verify_locations(ctx, "/etc/ssl/certs/ca-certificates.crt", NULL))
    {
        fprintf(stderr, "Error loading trust store\n");
        ERR_print_errors_fp(stderr);
        SSL_CTX_free(ctx);
        return 0;
    }

    if (!SSL_CTX_add_client_custom_ext(ctx,
                                       18,
                                       NULL, NULL, NULL,
                                       serverinfo_cli_parse_cb, NULL)) {
        fprintf(stderr, "Unable to add custom extension 18\n");
        ERR_print_errors_fp(stderr);
        SSL_CTX_free(ctx);
        return 0;
        //BIO_printf(bio_err,
        //           "Warning: Unable to add custom extension %u, skipping\n",
        //           18);
    }

    /* Setup the connection */

    bio = BIO_new_ssl_connect(ctx);


    /* Set the SSL_MODE_AUTO_RETRY flag */
    BIO_get_ssl(bio, & ssl);
    SSL_set_mode(ssl, SSL_MODE_AUTO_RETRY);

    /* Create and setup the connection */

    BIO_set_conn_hostname(bio, "ritter.vg:https");

    if(BIO_do_connect(bio) <= 0)
    {
        fprintf(stderr, "Error attempting to connect\n");
        ERR_print_errors_fp(stderr);
        BIO_free_all(bio);
        SSL_CTX_free(ctx);
        return 0;
    }

    /* Check the certificate */

    if(SSL_get_verify_result(ssl) != X509_V_OK)
    {
        fprintf(stderr,
                "Certificate verification error: %i\n",
                (int) SSL_get_verify_result(ssl));
        BIO_free_all(bio);
        SSL_CTX_free(ctx);
        return 0;
    }

    /* Send the request */

    BIO_write(bio, request, strlen(request));

    /* Read in the response */

    for(;;)
    {
        p = BIO_read(bio, r, 1023);
        if(p <= 0) break;
        r[p] = 0;
        printf("%s", r);
    }

    /* Close the connection and free the context */

    BIO_free_all(bio);
    SSL_CTX_free(ctx);
    return 0;
}
