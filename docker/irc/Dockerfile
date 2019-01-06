FROM python:3.6

RUN apt update
RUN apt install build-essential libssl-dev curl cmake -y

# create an unpriviledged user to make and run irc in
RUN useradd ircd -m --password ircd
# switch to the new user
USER ircd
# switch to the user's working directory
WORKDIR /home/ircd

# fetch unreal sources
RUN wget --trust-server-names https://www.unrealircd.org/unrealircd4/unrealircd-4.2.1.1.tar.gz
#unpack
RUN tar xzvf unrealircd-4.2.1.1.tar.gz
# switch to our new working directory
WORKDIR /home/ircd/unrealircd-4.2.1.1

# run default configuration
RUN ./Config
# build unreal
RUN make -j 4
# and install it
RUN make install

# change to unreal's install directory directory
WORKDIR ../unrealircd


# where the fun lays... (Script to simulate network issues)
COPY ./boomstick.py .
# where the buzzkill lays (Script to undo network issue simulation)
COPY ./sponge.py .

WORKDIR conf/ssl

RUN openssl req -new -sha256 -newkey rsa:4096 -keyout server.key.pem -out server.req.pem -subj "/C=US/ST=WA/O=Pydle/CN=irc.unknown.com" -nodes && openssl req -x509 -key server.key.pem -in server.req.pem -days 1 -out server.cert.pem
WORKDIR ..
COPY ./ircd.conf unrealircd.conf
WORKDIR ..

ENTRYPOINT ./unrealircd start; tail -f logs/ircd.log