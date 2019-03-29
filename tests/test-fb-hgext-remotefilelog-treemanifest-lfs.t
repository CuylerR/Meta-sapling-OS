
  $ . "$TESTDIR/library.sh"

  $ enable lfs treemanifest pushrebase
  $ setconfig treemanifest.treeonly=True
  $ hginit master

  $ cd master
  $ setconfig remotefilelog.server=True treemanifest.server=True remotefilelog.shallowtrees=True
  $ mkdir dir
  $ echo x > dir/x
  $ hg commit -qAm x1
  $ hg book master
  $ cd ..

  $ hgcloneshallow ssh://user@dummy/master shallow --config extensions.fastmanifest= --config fastmanifest.usetrees=True --config extensions.treemanifest= --config treemanifest.treeonly=True
  streaming all changes
  1 files to transfer, 124 bytes of data
  transferred 124 bytes in * seconds (*) (glob)
  searching for changes
  no changes found
  updating to branch default
  fetching tree '' 287ee6e53d4fbc5fab2157eb0383fdff1c3277c8
  2 trees fetched over * (glob)
  1 files updated, 0 files merged, 0 files removed, 0 files unresolved
  1 files fetched over 1 fetches - (1 misses, 0.00% hit ratio) over * (glob)

  $ cd shallow
  $ enable fastmanifest remotenames
  $ setconfig fastmanifest.usetrees=True
  $ setconfig treemanifest.sendtrees=True treemanifest.treeonly=True
  $ echo >> dir/x
  $ hg commit -m "Modify dir/x"
  $ hg push --to master
  pushing rev 6b73ab2c9773 to destination ssh://user@dummy/master bookmark master
  searching for changes
  remote: pushing 1 changeset:
  remote:     6b73ab2c9773  Modify dir/x
  updating bookmark master
  $ hg --cwd ../master log -G -l 1 --stat
  o  changeset:   1:6b73ab2c9773
  |  bookmark:    master
  ~  tag:         tip
     user:        test
     date:        Thu Jan 01 00:00:00 1970 +0000
     summary:     Modify dir/x
  
      dir/x |  1 +
      1 files changed, 1 insertions(+), 0 deletions(-)
  
