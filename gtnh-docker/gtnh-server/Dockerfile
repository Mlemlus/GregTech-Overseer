FROM eclipse-temurin:21
WORKDIR /minecraft

# update, install unzip
RUN apt update && apt upgrade -y
RUN apt install -y unzip && apt clean

# install the server from gtnh_server.zip
COPY gtnh_server.zip /minecraft/gtnh_server.zip 
RUN if [ -f /minecraft/gtnh_server.zip ]; then \
    unzip /minecraft/gtnh_server.zip -d /minecraft && rm /minecraft/gtnh_server.zip; \
    fi
# accept the Faustian bargain
RUN echo "eula=true" > /minecraft/eula.txt

# if you have a backup called backup.zip, recover the backup
COPY backup.zip /minecraft/backup.zip
RUN if [ -f /minecraft/backup.zip ]; then \
    unzip /minecraft/backup.zip && rm /minecraft/backup.zip; \
    fi

# Copy the custom prepared configs
COPY minecraft /minecraft

# Make the start script executable
RUN chmod +x /minecraft/start.sh

# set the entrypoint to the start script
ENTRYPOINT ["/minecraft/start.sh"]

