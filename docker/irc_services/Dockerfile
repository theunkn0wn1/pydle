FROM buildpack-deps:bionic

RUN apt update && apt install -y cmake
# create an unpriviledged user to make and run irc in
RUN useradd ircd -m --password ircd
# switch to the new user
USER ircd
# switch to the user's working directory
WORKDIR /home/ircd
# retrive anope
RUN git clone https://github.com/anope/anope

WORKDIR anope
COPY config.cache config.cache
#RUN chmod 777 config.cache
# configure it to use its defaults
RUN ./Config -quick
# switch to the build directory
WORKDIR build

# and compile it
RUN make -j 4 install

WORKDIR /home/ircd/services

COPY ./conf/services.conf /home/ircd/services/conf/services.conf

ENTRYPOINT ./bin/services --nofork