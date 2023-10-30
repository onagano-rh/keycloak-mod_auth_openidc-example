FROM quay.io/keycloak/keycloak:22.0

ENV KEYCLOAK_ADMIN=admin
ENV KEYCLOAK_ADMIN_PASSWORD=password

COPY keycloak.conf /opt/keycloak/conf/keycloak.conf

CMD ["start-dev"]

