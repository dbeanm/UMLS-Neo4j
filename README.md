# UPDATE Neo4j 4.x bulk import and docker
Work in progress to optimise but working.

In neo4j 4.x you can't copy databases around as files/directories any more. 

Also if you run with docker and do `docker exec -it [container name] bash` and then run the import, you end up with databases that cannot be started, are unavailable, permissions errors, etc.

This is because you're running as `root` when you `docker exec` which leaves you with databases owned by `root` when they need to be owned by `neo4j`

To bulk import with neo4j-admin and end up with a working database:

1. start neo4j container with import and data volumes mapped to host
2. `sudo docker exec -it --user=neo4j [container name] bash`
 - now you are the neo4j user 
 - run the neo4j-admin import command loading into [database name]
 - exit
4. stop the container
5. start a new container with at least the data volume mapped and set `--env NEO4J_dbms_active__database=[database name]`
6. in the neo4j browser, hard refresh and log in
- should now be connected to [database name]

# Neo4j 3.x
1. Preprocess MRCONSO and MRREL with preprocess.py
2. Copy the output into neo4j_import directory
3. Use neo4j-admin bulk importer but note:
  - Can only import into an offline db
  - Does not create any constraints or index, have to do that afterwards as it's a huge performance increase



`
bin/neo4j-admin import --nodes import/MRCONSO.processed.csv --relationships import/MRREL.processed.csv --database umls.db
`

Output:
`
IMPORT DONE in 6m 1s 43ms.
Imported:
  3590365 nodes
  105332256 relationships
  7180730 properties
Peak memory usage: 1.35 GB
`

Now stop the docker machine and delete or rename the (empty) graph.db that was created. Rename the umls.db that the import created to graph.db and start a new docker container (The alternative is to mount a config file in neo4j to use a different db name. TODO simplify this).

`
docker run -it --publish=7474:7474 --publish=7687:7687 --volume=/mnt/datastore/my_neo4j_data:/data --volume=/mnt/datastore/neo4j_plugins:/var/lib/neo4j/plugins --volume=/mnt/datastore/neo4j_import:/var/lib/neo4j/import -e NEO4J_dbms_security_procedures_unrestricted=apoc.\\\* neo4j:3.4.0
`

Now create the index from web interface
`CREATE INDEX ON :Concept(CUI)`
This index speeds up finding nodes by cui from ~ 1500ms to 30ms
