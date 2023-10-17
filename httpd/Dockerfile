FROM quay.io/centos/centos:stream8

RUN dnf install -y epel-release httpd \
 && dnf clean all \
 && rm -rf /var/cache/yum

# Download from: https://github.com/OpenIDC/mod_auth_openidc/releases
# "hiredis" in epel-release is required as a dependency.
COPY mod_auth_openidc-2.4.14.4-1.el8.x86_64.rpm /tmp
RUN dnf install -y /tmp/mod_auth_openidc-2.4.14.4-1.el8.x86_64.rpm \
 && rm /tmp/mod_auth_openidc-2.4.14.4-1.el8.x86_64.rpm

COPY my-proxy.conf /etc/httpd/conf.d/

EXPOSE 80

CMD ["httpd", "-D", "FOREGROUND"]

