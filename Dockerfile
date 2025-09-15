FROM ubuntu:24.04

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y \
    postfix \
    sasl2-bin \
    libsasl2-modules \
    libsasl2-modules-db \
    mailutils \
    && apt-get clean

RUN mkdir -p /etc/postfix /var/spool/postfix /etc/postfix/sasl /etc/postfix/maps /var/run/saslauthd

COPY master.cf /etc/postfix/master.cf
RUN chmod 644 /etc/postfix/master.cf
COPY main.cf /etc/postfix/main.cf
RUN chmod 644 /etc/postfix/main.cf
COPY smtpd.conf /etc/postfix/sasl/smtpd.conf
RUN chmod 644 /etc/postfix/sasl/smtpd.conf

RUN echo "START=yes" > /etc/default/saslauthd \
    && echo "MECHANISMS=\"sasldb\"" >> /etc/default/saslauthd \
    && echo "OPTIONS=\"-c -m /var/run/saslauthd -r\"" >> /etc/default/saslauthd

RUN mkdir -p /var/spool/postfix/var/run/saslauthd
RUN ln -s /var/run/saslauthd/mux /var/spool/postfix/var/run/saslauthd/mux

# Disable chroot in postfix to communicate with saslauthd
RUN sed -i 's/^\(smtp.*inet.*\)y/\1n/' /etc/postfix/master.cf

EXPOSE 25
EXPOSE 465

# RUN /usr/sbin/postmap /etc/postfix/maps/relay_domains
RUN /usr/sbin/postconf compatibility_level=3.7

COPY start.sh /
CMD /start.sh
