FROM eclipse-temurin:21
WORKDIR /minecraft

# update
RUN apt update && apt upgrade -y
CMD [ "java", "-Xms4G", "-Xmx20G", "-jar", "-Dfml.readTimeout=180", "-Dfml.queryResult=confirm", "@java9args.txt", "lwjgl3ify-forgePatches.jar", "nogui" ]
