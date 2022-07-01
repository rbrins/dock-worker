# Dock Worker

See [post at dc864](https://www.dc864.org/2022/07/exfiltrating-information-with-docker/) that describes the proof of concept.

Idea is to use docker hub as a repository to exfiltrate data, using containers. This could be epsecially useful in a devops environment that relies on docker. 

Note: this is strictly a Proof-of-concept and has not been seen in the wild to my knowledge. To operationalize this for your red teaming exercise, add your docker hub credentials, create a repository on docker hub (and probably should be private if you are doing this for a client), then unpload the load function onto the victim machine, and the unload function for the attacker machine.
