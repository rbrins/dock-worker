#!/usr/bin/env python3

import docker
import os
import time
import shutil

def load(repository, data2Load, username, password, registry: str="docker.io"):

    dockWorker = docker.DockerClient(base_url='unix:///var/run/docker.sock/')

    shiftCheckIn = dockWorker.login(username, password, registry)

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

    shiftCheckIn = dockWorker.login(username, password, registry)

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
