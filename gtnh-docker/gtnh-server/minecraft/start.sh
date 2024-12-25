#!/bin/sh
# Start the Minecraft server
java -Xms4G -Xmx20G -jar -Dfml.readTimeout=180 @java9args.txt lwjgl3ify-forgePatches.jar nogui