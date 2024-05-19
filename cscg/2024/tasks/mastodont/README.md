# Mastodon't

Welcome to the Mastodon't challenge. We were quite unlucky at picking
a commit hash at random (3d8bd093b9197659563070d2c763988428063406)
so we are told to be vulnerable to CVE-2023-36460. 
Luckily there are no public exploits. 

Have fun! 

# Login
User: pwn@mastodont.challenge.cscg.live
Pass: cscg2024

# Local Setup
* Add a `/etc/hosts` entry for `mastodon.local` pointing to `127.0.0.1`
* Run the local setup (traefik as proxy) via: `docker compose -f docker-compose.yml -f docker-compose-local.yml up`
* Visit https://mastodon.local
* Note on non x86 CPUs (i.e Apple silicon):
  * Remove all references to the reproducible containers
     * remove pinned @sha hashes on the ruby and node base images 
     * remove the two ADD's of repro-sources-list.sh to the build containers
* The challenge is not dependant on the cpu arch. 

# Tips
* Read the CVE description, associated patches and implications carefully.
* The intended solution does not use MP3.
* Find a way to reach ImageMagick. 
* In case you are struggling in the very end, be mindful of caching and just 
write your exploit with a minimal amount of requests. Good luck.
