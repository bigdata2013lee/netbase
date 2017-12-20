echo "mongodb restarting...."
p1=/data/main
p2=/data/perf
/opt/mongodb/bin/mongod  --shutdown  --dbpath=$p1/db
/opt/mongodb/bin/mongod  --shutdown  --dbpath=$p2/db
[ -d $p1/db/journal ] && rm -rf $p1/db/journal
[ -d $p2/db/journal ] && rm -rf $p2/db/journal
[ -d $p3/db/journal ] && rm -rf $p3/db/journal
[ -f $p1/db/mongod.lock ] && rm -rf $p1/db/mongod.lock
[ -f $p2/db/mongod.lock ] && rm -rf $p2/db/mongod.lock
[ -f $p3/db/mongod.lock ] && rm -rf $p3/db/mongod.lock

/opt/mongodb/bin/mongod  --fork --auth  --dbpath=$p1/db --logpath=$p1/mongodb.log --port=27017
/opt/mongodb/bin/mongod  --fork --auth  --dbpath=$p2/db  --logpath=$p2/mongodb.log --port=27018
echo "seccessuly"
