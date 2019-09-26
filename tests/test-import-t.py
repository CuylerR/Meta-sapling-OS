# Copyright (c) Facebook, Inc. and its affiliates.
# Copyright (c) Mercurial Contributors.
#
# This software may be used and distributed according to the terms of the
# GNU General Public License version 2 or any later version.

from __future__ import absolute_import

from testutil.dott import feature, sh, testtmp  # noqa: F401


feature.require("false")  # test not passing
sh % "setconfig 'extensions.treemanifest=!'"
sh % ". helpers-usechg.sh"

sh % "hg init a"
sh % "mkdir a/d1"
sh % "mkdir a/d1/d2"
sh % "echo line 1" > "a/a"
sh % "echo line 1" > "a/d1/d2/a"
sh % "hg --cwd a ci -Ama" == r"""
    adding a
    adding d1/d2/a"""

sh % "echo line 2" >> "a/a"
sh % "hg --cwd a ci -u someone -d '1 0' '-msecond change'"

# import with no args:

sh % "hg --cwd a import" == r"""
    abort: need at least one patch to import
    [255]"""

# generate patches for the test

sh % "hg --cwd a export tip" > "exported-tip.patch"
sh % "hg --cwd a diff '-r0:1'" > "diffed-tip.patch"


# import exported patch
# (this also tests that editor is not invoked, if the patch contains the
# commit message and '--edit' is not specified)

sh % "hg clone -r0 a b" == r"""
    adding changesets
    adding manifests
    adding file changes
    added 1 changesets with 2 changes to 2 files
    new changesets 80971e65b431
    updating to branch default
    2 files updated, 0 files merged, 0 files removed, 0 files unresolved"""
sh % "'HGEDITOR=cat' hg --cwd b import ../exported-tip.patch" == "applying ../exported-tip.patch"

# message and committer and date should be same

sh % "hg --cwd b tip" == r"""
    changeset:   1:1d4bd90af0e4
    tag:         tip
    user:        someone
    date:        Thu Jan 01 00:00:01 1970 +0000
    summary:     second change"""
sh % "rm -r b"


# import exported patch with external patcher
# (this also tests that editor is invoked, if the '--edit' is specified,
# regardless of the commit message in the patch)

sh % "cat" << r"""
from __future__ import print_function
print('patching file a')
file('a', 'wb').write('line2\n')
""" > "dummypatch.py"
sh % "hg clone -r0 a b" == r"""
    adding changesets
    adding manifests
    adding file changes
    added 1 changesets with 2 changes to 2 files
    new changesets 80971e65b431
    updating to branch default
    2 files updated, 0 files merged, 0 files removed, 0 files unresolved"""
sh % "'HGEDITOR=cat' hg --config 'ui.patch=$PYTHON ../dummypatch.py' --cwd b import --edit ../exported-tip.patch" == r"""
    applying ../exported-tip.patch
    second change


    HG: Enter commit message.  Lines beginning with 'HG:' are removed.
    HG: Leave message empty to abort commit.
    HG: --
    HG: user: someone
    HG: branch 'default'
    HG: changed a"""
sh % "cat b/a" == "line2"
sh % "rm -r b"


# import of plain diff should fail without message
# (this also tests that editor is invoked, if the patch doesn't contain
# the commit message, regardless of '--edit')

sh % "hg clone -r0 a b" == r"""
    adding changesets
    adding manifests
    adding file changes
    added 1 changesets with 2 changes to 2 files
    new changesets 80971e65b431
    updating to branch default
    2 files updated, 0 files merged, 0 files removed, 0 files unresolved"""
sh % "cat" << r"""
env | grep HGEDITFORM
cat \$1
""" > "$TESTTMP/editor.sh"
sh % "'HGEDITOR=cat' hg --cwd b import ../diffed-tip.patch" == r"""
    applying ../diffed-tip.patch


    HG: Enter commit message.  Lines beginning with 'HG:' are removed.
    HG: Leave message empty to abort commit.
    HG: --
    HG: user: test
    HG: branch 'default'
    HG: changed a
    abort: empty commit message
    [255]"""

# Test avoiding editor invocation at applying the patch with --exact,
# even if commit message is empty

sh % "echo a" >> "b/a"
sh % "hg --cwd b commit -m ' '"
sh % "hg --cwd b tip -T '{node}\\n'" == "d8804f3f5396d800812f579c8452796a5993bdb2"
sh % "hg --cwd b export -o ../empty-log.diff ."
sh % "hg --cwd b update -q -C '.^1'"
sh % "hg --cwd b debugstrip -q tip"
sh % "'HGEDITOR=cat' hg --cwd b import --exact ../empty-log.diff" == "applying ../empty-log.diff"
sh % "hg --cwd b tip -T '{node}\\n'" == "d8804f3f5396d800812f579c8452796a5993bdb2"

sh % "rm -r b"


# import of plain diff should be ok with message

sh % "hg clone -r0 a b" == r"""
    adding changesets
    adding manifests
    adding file changes
    added 1 changesets with 2 changes to 2 files
    new changesets 80971e65b431
    updating to branch default
    2 files updated, 0 files merged, 0 files removed, 0 files unresolved"""
sh % "hg --cwd b import -mpatch ../diffed-tip.patch" == "applying ../diffed-tip.patch"
sh % "rm -r b"


# import of plain diff with specific date and user
# (this also tests that editor is not invoked, if
# '--message'/'--logfile' is specified and '--edit' is not)

sh % "hg clone -r0 a b" == r"""
    adding changesets
    adding manifests
    adding file changes
    added 1 changesets with 2 changes to 2 files
    new changesets 80971e65b431
    updating to branch default
    2 files updated, 0 files merged, 0 files removed, 0 files unresolved"""
sh % "hg --cwd b import -mpatch -d '1 0' -u 'user@nowhere.net' ../diffed-tip.patch" == "applying ../diffed-tip.patch"
sh % "hg -R b tip -pv" == r"""
    changeset:   1:ca68f19f3a40
    tag:         tip
    user:        user@nowhere.net
    date:        Thu Jan 01 00:00:01 1970 +0000
    files:       a
    description:
    patch


    diff -r 80971e65b431 -r ca68f19f3a40 a
    --- a/a	Thu Jan 01 00:00:00 1970 +0000
    +++ b/a	Thu Jan 01 00:00:01 1970 +0000
    @@ -1,1 +1,2 @@
     line 1
    +line 2"""
sh % "rm -r b"


# import of plain diff should be ok with --no-commit
# (this also tests that editor is not invoked, if '--no-commit' is
# specified, regardless of '--edit')

sh % "hg clone -r0 a b" == r"""
    adding changesets
    adding manifests
    adding file changes
    added 1 changesets with 2 changes to 2 files
    new changesets 80971e65b431
    updating to branch default
    2 files updated, 0 files merged, 0 files removed, 0 files unresolved"""
sh % "'HGEDITOR=cat' hg --cwd b import --no-commit --edit ../diffed-tip.patch" == "applying ../diffed-tip.patch"
sh % "hg --cwd b diff --nodates" == r"""
    diff -r 80971e65b431 a
    --- a/a
    +++ b/a
    @@ -1,1 +1,2 @@
     line 1
    +line 2"""
sh % "rm -r b"


# import of malformed plain diff should fail

sh % "hg clone -r0 a b" == r"""
    adding changesets
    adding manifests
    adding file changes
    added 1 changesets with 2 changes to 2 files
    new changesets 80971e65b431
    updating to branch default
    2 files updated, 0 files merged, 0 files removed, 0 files unresolved"""
sh % "sed 's/1,1/foo/'" << open("diffed-tip.patch").read() > "broken.patch"
sh % "hg --cwd b import -mpatch ../broken.patch" == r"""
    applying ../broken.patch
    abort: bad hunk #1
    [255]"""
sh % "rm -r b"


# hg -R repo import
# put the clone in a subdir - having a directory named "a"
# used to hide a bug.

sh % "mkdir dir"
sh % "hg clone -r0 a dir/b" == r"""
    adding changesets
    adding manifests
    adding file changes
    added 1 changesets with 2 changes to 2 files
    new changesets 80971e65b431
    updating to branch default
    2 files updated, 0 files merged, 0 files removed, 0 files unresolved"""
sh % "cd dir"
sh % "hg -R b import ../exported-tip.patch" == "applying ../exported-tip.patch"
sh % "cd .."
sh % "rm -r dir"


# import from stdin

sh % "hg clone -r0 a b" == r"""
    adding changesets
    adding manifests
    adding file changes
    added 1 changesets with 2 changes to 2 files
    new changesets 80971e65b431
    updating to branch default
    2 files updated, 0 files merged, 0 files removed, 0 files unresolved"""
sh % "hg --cwd b import -" << open(
    "exported-tip.patch"
).read() == "applying patch from stdin"
sh % "rm -r b"


# import two patches in one stream

sh % "hg init b"
sh % "hg --cwd a export '0:tip'" | "hg --cwd b import -" == "applying patch from stdin"
sh % "hg --cwd a id" == "1d4bd90af0e4 tip"
sh % "hg --cwd b id" == "1d4bd90af0e4 tip"
sh % "rm -r b"


# override commit message

sh % "hg clone -r0 a b" == r"""
    adding changesets
    adding manifests
    adding file changes
    added 1 changesets with 2 changes to 2 files
    new changesets 80971e65b431
    updating to branch default
    2 files updated, 0 files merged, 0 files removed, 0 files unresolved"""
sh % "hg --cwd b import -m override -" << open(
    "exported-tip.patch"
).read() == "applying patch from stdin"
sh % "hg --cwd b tip" | "grep override" == "summary:     override"
sh % "rm -r b"

sh % "cat" << r"""
import email.Message, sys
msg = email.Message.Message()
patch = open(sys.argv[1], 'rb').read()
msg.set_payload('email commit message\n' + patch)
msg['Subject'] = 'email patch'
msg['From'] = 'email patcher'
file(sys.argv[2], 'wb').write(msg.as_string())
""" > "mkmsg.py"


# plain diff in email, subject, message body

sh % "hg clone -r0 a b" == r"""
    adding changesets
    adding manifests
    adding file changes
    added 1 changesets with 2 changes to 2 files
    new changesets 80971e65b431
    updating to branch default
    2 files updated, 0 files merged, 0 files removed, 0 files unresolved"""
sh % "'$PYTHON' mkmsg.py diffed-tip.patch msg.patch"
sh % "hg --cwd b import ../msg.patch" == "applying ../msg.patch"
sh % "hg --cwd b tip" | "grep email" == r"""
    user:        email patcher
    summary:     email patch"""
sh % "rm -r b"


# plain diff in email, no subject, message body

sh % "hg clone -r0 a b" == r"""
    adding changesets
    adding manifests
    adding file changes
    added 1 changesets with 2 changes to 2 files
    new changesets 80971e65b431
    updating to branch default
    2 files updated, 0 files merged, 0 files removed, 0 files unresolved"""
sh % "grep -v '^Subject:' msg.patch" | "hg --cwd b import -" == "applying patch from stdin"
sh % "rm -r b"


# plain diff in email, subject, no message body

sh % "hg clone -r0 a b" == r"""
    adding changesets
    adding manifests
    adding file changes
    added 1 changesets with 2 changes to 2 files
    new changesets 80971e65b431
    updating to branch default
    2 files updated, 0 files merged, 0 files removed, 0 files unresolved"""
sh % "grep -v '^email ' msg.patch" | "hg --cwd b import -" == "applying patch from stdin"
sh % "rm -r b"


# plain diff in email, no subject, no message body, should fail

sh % "hg clone -r0 a b" == r"""
    adding changesets
    adding manifests
    adding file changes
    added 1 changesets with 2 changes to 2 files
    new changesets 80971e65b431
    updating to branch default
    2 files updated, 0 files merged, 0 files removed, 0 files unresolved"""
sh % "egrep -v '^(Subject|email)' msg.patch" | "hg --cwd b import -" == r"""
    applying patch from stdin
    abort: empty commit message
    [255]"""
sh % "rm -r b"


# hg export in email, should use patch header

sh % "hg clone -r0 a b" == r"""
    adding changesets
    adding manifests
    adding file changes
    added 1 changesets with 2 changes to 2 files
    new changesets 80971e65b431
    updating to branch default
    2 files updated, 0 files merged, 0 files removed, 0 files unresolved"""
sh % "'$PYTHON' mkmsg.py exported-tip.patch msg.patch"
sh % "cat msg.patch" | "hg --cwd b import -" == "applying patch from stdin"
sh % "hg --cwd b tip" | "grep second" == "summary:     second change"
sh % "rm -r b"


# subject: duplicate detection, removal of [PATCH]
# The '---' tests the gitsendmail handling without proper mail headers

sh % "cat" << r"""
import email.Message, sys
msg = email.Message.Message()
patch = open(sys.argv[1], 'rb').read()
msg.set_payload('email patch\n\nnext line\n---\n' + patch)
msg['Subject'] = '[PATCH] email patch'
msg['From'] = 'email patcher'
file(sys.argv[2], 'wb').write(msg.as_string())
""" > "mkmsg2.py"


# plain diff in email, [PATCH] subject, message body with subject

sh % "hg clone -r0 a b" == r"""
    adding changesets
    adding manifests
    adding file changes
    added 1 changesets with 2 changes to 2 files
    new changesets 80971e65b431
    updating to branch default
    2 files updated, 0 files merged, 0 files removed, 0 files unresolved"""
sh % "'$PYTHON' mkmsg2.py diffed-tip.patch msg.patch"
sh % "cat msg.patch" | "hg --cwd b import -" == "applying patch from stdin"
sh % "hg --cwd b tip --template '{desc}\\n'" == r"""
    email patch

    next line"""
sh % "rm -r b"


# Issue963: Parent of working dir incorrect after import of multiple
# patches and rollback

# We weren't backing up the correct dirstate file when importing many
# patches: import patch1 patch2; rollback

sh % "echo line 3" >> "a/a"
sh % "hg --cwd a ci '-mthird change'"
sh % "hg --cwd a export -o '../patch%R' 1 2"
sh % "hg clone -qr0 a b"
sh % "hg --cwd b parents --template 'parent: {rev}\\n'" == "parent: 0"
sh % "hg --cwd b import -v ../patch1 ../patch2" == r"""
    applying ../patch1
    patching file a
    committing files:
    a
    committing manifest
    committing changelog
    created 1d4bd90af0e4
    applying ../patch2
    patching file a
    committing files:
    a
    committing manifest
    committing changelog
    created 6d019af21222"""
sh % "hg --cwd b rollback" == r"""
    repository tip rolled back to revision 0 (undo import)
    working directory now based on revision 0"""
sh % "hg --cwd b parents --template 'parent: {rev}\\n'" == "parent: 0"

# Test that "hg rollback" doesn't restore dirstate to one at the
# beginning of the rolled back transaction in not-"parent-gone" case.

# invoking pretxncommit hook will cause marking '.hg/dirstate' as a file
# to be restored when rolling back, after DirstateTransactionPlan (see wiki
# page for detail).

sh % "hg --cwd b commit -m foobar"
sh % "hg --cwd b update 0 -q"
sh % "hg --cwd b import ../patch1 ../patch2 --config 'hooks.pretxncommit=true'" == r"""
    applying ../patch1
    applying ../patch2"""
sh % "hg --cwd b update -q 1"
sh % "hg --cwd b rollback -q"
sh % "hg --cwd b parents --template 'parent: {rev}\\n'" == "parent: 1"

sh % "hg --cwd b update -q -C 0"
sh % "hg --cwd b debugstrip -q 1"

sh % "rm -rf b"

# importing a patch in a subdirectory failed at the commit stage

sh % "echo line 2" >> "a/d1/d2/a"
sh % "hg --cwd a ci -u someoneelse -d '1 0' '-msubdir change'"

# hg import in a subdirectory

sh % "hg clone -r0 a b" == r"""
    adding changesets
    adding manifests
    adding file changes
    added 1 changesets with 2 changes to 2 files
    new changesets 80971e65b431
    updating to branch default
    2 files updated, 0 files merged, 0 files removed, 0 files unresolved"""
sh % "hg --cwd a export tip" > "tmp"
sh % "sed -e 's/d1\\/d2\\///'" << open("tmp").read() > "subdir-tip.patch"
sh % "'dir=`pwd`'"
sh % "cd b/d1/d2 '2>&1'" > "/dev/null"
sh % "hg import ../../../subdir-tip.patch" == "applying ../../../subdir-tip.patch"
sh % "cd '$dir'"

# message should be 'subdir change'
# committer should be 'someoneelse'

sh % "hg --cwd b tip" == r"""
    changeset:   1:3577f5aea227
    tag:         tip
    user:        someoneelse
    date:        Thu Jan 01 00:00:01 1970 +0000
    summary:     subdir change"""

# should be empty

sh % "hg --cwd b status"


# Test fuzziness (ambiguous patch location, fuzz=2)

sh % "hg init fuzzy"
sh % "cd fuzzy"
sh % "echo line1" > "a"
sh % "echo line0" >> "a"
sh % "echo line3" >> "a"
sh % "hg ci -Am adda" == "adding a"
sh % "echo line1" > "a"
sh % "echo line2" >> "a"
sh % "echo line0" >> "a"
sh % "echo line3" >> "a"
sh % "hg ci -m change a"
sh % "hg export tip" > "fuzzy-tip.patch"
sh % "hg up -C 0" == "1 files updated, 0 files merged, 0 files removed, 0 files unresolved"
sh % "echo line1" > "a"
sh % "echo line0" >> "a"
sh % "echo line1" >> "a"
sh % "echo line0" >> "a"
sh % "hg ci -m brancha"
sh % "hg import --config 'patch.fuzz=0' -v fuzzy-tip.patch" == r"""
    applying fuzzy-tip.patch
    patching file a
    Hunk #1 FAILED at 0
    1 out of 1 hunks FAILED -- saving rejects to file a.rej
    abort: patch failed to apply
    [255]"""
sh % "hg import --no-commit -v fuzzy-tip.patch" == r"""
    applying fuzzy-tip.patch
    patching file a
    Hunk #1 succeeded at 2 with fuzz 1 (offset 0 lines).
    applied to working directory"""
sh % "hg revert -a" == "reverting a"


# import with --no-commit should have written .hg/last-message.txt

sh % "cat .hg/last-message.txt" == "change (no-eol)"


# test fuzziness with eol=auto

sh % "hg --config 'patch.eol=auto' import --no-commit -v fuzzy-tip.patch" == r"""
    applying fuzzy-tip.patch
    patching file a
    Hunk #1 succeeded at 2 with fuzz 1 (offset 0 lines).
    applied to working directory"""
sh % "cd .."


# Test hunk touching empty files (issue906)

sh % "hg init empty"
sh % "cd empty"
sh % "touch a"
sh % "touch b1"
sh % "touch c1"
sh % "echo d" > "d"
sh % "hg ci -Am init" == r"""
    adding a
    adding b1
    adding c1
    adding d"""
sh % "echo a" > "a"
sh % "echo b" > "b1"
sh % "hg mv b1 b2"
sh % "echo c" > "c1"
sh % "hg copy c1 c2"
sh % "rm d"
sh % "touch d"
sh % "hg diff --git" == r"""
    diff --git a/a b/a
    --- a/a
    +++ b/a
    @@ -0,0 +1,1 @@
    +a
    diff --git a/b1 b/b2
    rename from b1
    rename to b2
    --- a/b1
    +++ b/b2
    @@ -0,0 +1,1 @@
    +b
    diff --git a/c1 b/c1
    --- a/c1
    +++ b/c1
    @@ -0,0 +1,1 @@
    +c
    diff --git a/c1 b/c2
    copy from c1
    copy to c2
    --- a/c1
    +++ b/c2
    @@ -0,0 +1,1 @@
    +c
    diff --git a/d b/d
    --- a/d
    +++ b/d
    @@ -1,1 +0,0 @@
    -d"""
sh % "hg ci -m empty"
sh % "hg export --git tip" > "empty.diff"
sh % "hg up -C 0" == "4 files updated, 0 files merged, 2 files removed, 0 files unresolved"
sh % "hg import empty.diff" == "applying empty.diff"
sh % "for name in a b1 b2 c1 c2 'd;' do" == r"""
    >   echo % $name file
    >   test -f $name && cat $name
    >   done
    % a file
    a
    % b1 file
    % b2 file
    b
    % c1 file
    c
    % c2 file
    c
    % d file"""
sh % "cd .."


# Test importing a patch ending with a binary file removal

sh % "hg init binaryremoval"
sh % "cd binaryremoval"
sh % "echo a" > "a"
sh % "'$PYTHON' -c 'file('\\''b'\\'', '\\''wb'\\'').write('\\''a\\x00b'\\'')'"
sh % "hg ci -Am addall" == r"""
    adding a
    adding b"""
sh % "hg rm a"
sh % "hg rm b"
sh % "hg st" == r"""
    R a
    R b"""
sh % "hg ci -m remove"
sh % "hg export --git ." > "remove.diff"
sh % "cat remove.diff" | "grep git" == r"""
    diff --git a/a b/a
    diff --git a/b b/b"""
sh % "hg up -C 0" == "2 files updated, 0 files merged, 0 files removed, 0 files unresolved"
sh % "hg import remove.diff" == "applying remove.diff"
sh % "hg manifest"
sh % "cd .."


# Issue927: test update+rename with common name

sh % "hg init t"
sh % "cd t"
sh % "touch a"
sh % "hg ci -Am t" == "adding a"
sh % "echo a" > "a"

# Here, bfile.startswith(afile)

sh % "hg copy a a2"
sh % "hg ci -m copya"
sh % "hg export --git tip" > "copy.diff"
sh % "hg up -C 0" == "1 files updated, 0 files merged, 1 files removed, 0 files unresolved"
sh % "hg import copy.diff" == "applying copy.diff"

# a should contain an 'a'

sh % "cat a" == "a"

# and a2 should have duplicated it

sh % "cat a2" == "a"
sh % "cd .."


# test -p0

sh % "hg init p0"
sh % "cd p0"
sh % "echo a" > "a"
sh % "hg ci -Am t" == "adding a"
sh % "hg import -p foo" == r"""
    abort: invalid value 'foo' for option -p, expected int
    [255]"""
sh % "hg import -p0 -" << r"""
foobar
--- a	Sat Apr 12 22:43:58 2008 -0400
+++ a	Sat Apr 12 22:44:05 2008 -0400
@@ -1,1 +1,1 @@
-a
+bb
""" == "applying patch from stdin"
sh % "hg status"
sh % "cat a" == "bb"

# test --prefix

sh % "mkdir -p dir/dir2"
sh % "echo b" > "dir/dir2/b"
sh % "hg ci -Am b" == "adding dir/dir2/b"
sh % "hg import -p2 --prefix dir -" << r"""
foobar
--- drop1/drop2/dir2/b
+++ drop1/drop2/dir2/b
@@ -1,1 +1,1 @@
-b
+cc
""" == "applying patch from stdin"
sh % "hg status"
sh % "cat dir/dir2/b" == "cc"
sh % "cd .."


# test paths outside repo root

sh % "mkdir outside"
sh % "touch outside/foo"
sh % "hg init inside"
sh % "cd inside"
sh % "hg import -" << r"""
diff --git a/a b/b
rename from ../outside/foo
rename to bar
""" == r"""
    applying patch from stdin
    abort: path contains illegal component: ../outside/foo
    [255]"""
sh % "cd .."


# test import with similarity and git and strip (issue295 et al.)

sh % "hg init sim"
sh % "cd sim"
sh % "echo 'this is a test'" > "a"
sh % "hg ci -Ama" == "adding a"
sh % "cat" << r"""
diff --git a/foo/a b/foo/a
deleted file mode 100644
--- a/foo/a
+++ /dev/null
@@ -1,1 +0,0 @@
-this is a test
diff --git a/foo/b b/foo/b
new file mode 100644
--- /dev/null
+++ b/foo/b
@@ -0,0 +1,2 @@
+this is a test
+foo
""" > "../rename.diff"
sh % "hg import --no-commit -v -s 1 ../rename.diff -p2" == r"""
    applying ../rename.diff
    patching file a
    patching file b
    adding b
    recording removal of a as rename to b (88% similar)
    applied to working directory"""
sh % "echo 'mod b'" > "b"
sh % "hg st -C" == r"""
    A b
      a
    R a"""
sh % "hg revert -a" == r"""
    undeleting a
    forgetting b"""
sh % "cat b" == "mod b"
sh % "rm b"
sh % "hg import --no-commit -v -s 100 ../rename.diff -p2" == r"""
    applying ../rename.diff
    patching file a
    patching file b
    adding b
    applied to working directory"""
sh % "hg st -C" == r"""
    A b
    R a"""
sh % "cd .."


# Issue1495: add empty file from the end of patch

sh % "hg init addemptyend"
sh % "cd addemptyend"
sh % "touch a"
sh % "hg addremove" == "adding a"
sh % "hg ci -m commit"
sh % "cat" << r"""
add a, b
diff --git a/a b/a
--- a/a
+++ b/a
@@ -0,0 +1,1 @@
+a
diff --git a/b b/b
new file mode 100644
""" > "a.patch"
sh % "hg import --no-commit a.patch" == "applying a.patch"

# apply a good patch followed by an empty patch (mainly to ensure
# that dirstate is *not* updated when import crashes)
sh % "hg update -q -C ."
sh % "rm b"
sh % "touch empty.patch"
sh % "hg import a.patch empty.patch" == r"""
    applying a.patch
    applying empty.patch
    transaction abort!
    rollback completed
    abort: empty.patch: no diffs found
    [255]"""
sh % "hg tip --template '{rev}  {desc|firstline}\\n'" == "0  commit"
sh % "hg -q status" == "M a"
sh % "cd .."

# create file when source is not /dev/null

sh % "cat" << r"""
diff -Naur proj-orig/foo proj-new/foo
--- proj-orig/foo       1969-12-31 16:00:00.000000000 -0800
+++ proj-new/foo        2009-07-17 16:50:45.801368000 -0700
@@ -0,0 +1,1 @@
+a
""" > "create.patch"

# some people have patches like the following too

sh % "cat" << r"""
diff -Naur proj-orig/foo proj-new/foo
--- proj-orig/foo.orig  1969-12-31 16:00:00.000000000 -0800
+++ proj-new/foo        2009-07-17 16:50:45.801368000 -0700
@@ -0,0 +1,1 @@
+a
""" > "create2.patch"
sh % "hg init oddcreate"
sh % "cd oddcreate"
sh % "hg import --no-commit ../create.patch" == "applying ../create.patch"
sh % "cat foo" == "a"
sh % "rm foo"
sh % "hg revert foo"
sh % "hg import --no-commit ../create2.patch" == "applying ../create2.patch"
sh % "cat foo" == "a"

sh % "cd .."

# Issue1859: first line mistaken for email headers

sh % "hg init emailconfusion"
sh % "cd emailconfusion"
sh % "cat" << r"""
module: summary

description


diff -r 000000000000 -r 9b4c1e343b55 test.txt
--- /dev/null
+++ b/a
@@ -0,0 +1,1 @@
+a
""" > "a.patch"
sh % "hg import -d '0 0' a.patch" == "applying a.patch"
sh % "hg parents -v" == r"""
    changeset:   0:5a681217c0ad
    tag:         tip
    user:        test
    date:        Thu Jan 01 00:00:00 1970 +0000
    files:       a
    description:
    module: summary

    description"""
sh % "cd .."


# in commit message

sh % "hg init commitconfusion"
sh % "cd commitconfusion"
sh % "cat" << r"""
module: summary

--- description

diff --git a/a b/a
new file mode 100644
--- /dev/null
+++ b/a
@@ -0,0 +1,1 @@
+a
EOF
hg import -d '0 0' a.patch
hg parents -v
cd ..

echo '% tricky header splitting'
cat > trickyheaders.patch <<EOF
From: User A <user@a>
Subject: [PATCH] from: tricky!

# HG changeset patch
# User User B
# Date 1266264441 18000
# Branch stable
# Node ID f2be6a1170ac83bf31cb4ae0bad00d7678115bc0
# Parent  0000000000000000000000000000000000000000
from: tricky!

That is not a header.

diff -r 000000000000 -r f2be6a1170ac foo
--- /dev/null
+++ b/foo
@@ -0,0 +1,1 @@
+foo
""" > "a.patch" == r"""
    applying a.patch
    changeset:   0:f34d9187897d
    tag:         tip
    user:        test
    date:        Thu Jan 01 00:00:00 1970 +0000
    files:       a
    description:
    module: summary


    % tricky header splitting"""

sh % "hg init trickyheaders"
sh % "cd trickyheaders"
sh % "hg import -d '0 0' ../trickyheaders.patch" == "applying ../trickyheaders.patch"
sh % "hg export --git tip" == r"""
    # HG changeset patch
    # User User B
    # Date 0 0
    #      Thu Jan 01 00:00:00 1970 +0000
    # Node ID eb56ab91903632294ac504838508cb370c0901d2
    # Parent  0000000000000000000000000000000000000000
    from: tricky!

    That is not a header.

    diff --git a/foo b/foo
    new file mode 100644
    --- /dev/null
    +++ b/foo
    @@ -0,0 +1,1 @@
    +foo"""
sh % "cd .."


# Issue2102: hg export and hg import speak different languages

sh % "hg init issue2102"
sh % "cd issue2102"
sh % "mkdir -p src/cmd/gc"
sh % "touch src/cmd/gc/mksys.bash"
sh % "hg ci -Am init" == "adding src/cmd/gc/mksys.bash"
sh % "hg import -" << r"""
# HG changeset patch
# User Rob Pike
# Date 1216685449 25200
# Node ID 03aa2b206f499ad6eb50e6e207b9e710d6409c98
# Parent  93d10138ad8df586827ca90b4ddb5033e21a3a84
help management of empty pkg and lib directories in perforce

R=gri
DELTA=4  (4 added, 0 deleted, 0 changed)
OCL=13328
CL=13328

diff --git a/lib/place-holder b/lib/place-holder
new file mode 100644
--- /dev/null
+++ b/lib/place-holder
@@ -0,0 +1,2 @@
+perforce does not maintain empty directories.
+this file helps.
diff --git a/pkg/place-holder b/pkg/place-holder
new file mode 100644
--- /dev/null
+++ b/pkg/place-holder
@@ -0,0 +1,2 @@
+perforce does not maintain empty directories.
+this file helps.
diff --git a/src/cmd/gc/mksys.bash b/src/cmd/gc/mksys.bash
old mode 100644
new mode 100755
""" == "applying patch from stdin"

if feature.check(["execbit"]):

    sh % "hg sum" == r"""
        parent: 1:d59915696727 tip
         help management of empty pkg and lib directories in perforce
        commit: (clean)
        phases: 2 draft"""

    sh % "hg diff --git -c tip" == r"""
        diff --git a/lib/place-holder b/lib/place-holder
        new file mode 100644
        --- /dev/null
        +++ b/lib/place-holder
        @@ -0,0 +1,2 @@
        +perforce does not maintain empty directories.
        +this file helps.
        diff --git a/pkg/place-holder b/pkg/place-holder
        new file mode 100644
        --- /dev/null
        +++ b/pkg/place-holder
        @@ -0,0 +1,2 @@
        +perforce does not maintain empty directories.
        +this file helps.
        diff --git a/src/cmd/gc/mksys.bash b/src/cmd/gc/mksys.bash
        old mode 100644
        new mode 100755"""

else:

    sh % "hg sum" == r"""
        parent: 1:28f089cc9ccc tip
         help management of empty pkg and lib directories in perforce
        branch: default
        commit: (clean)
        update: (current)
        phases: 2 draft"""

    sh % "hg diff --git -c tip" == r"""
        diff --git a/lib/place-holder b/lib/place-holder
        new file mode 100644
        --- /dev/null
        +++ b/lib/place-holder
        @@ -0,0 +1,2 @@
        +perforce does not maintain empty directories.
        +this file helps.
        diff --git a/pkg/place-holder b/pkg/place-holder
        new file mode 100644
        --- /dev/null
        +++ b/pkg/place-holder
        @@ -0,0 +1,2 @@
        +perforce does not maintain empty directories.
        +this file helps."""

    # /* The mode change for mksys.bash is missing here, because on platforms  */
    # /* that don't support execbits, mode changes in patches are ignored when */
    # /* they are imported. This is obviously also the reason for why the hash */
    # /* in the created changeset is different to the one you see above the    */
    # /* #else clause */


sh % "cd .."


# diff lines looking like headers

sh % "hg init difflineslikeheaders"
sh % "cd difflineslikeheaders"
sh % "echo a" > "a"
sh % "echo b" > "b"
sh % "echo c" > "c"
sh % "hg ci -Am1" == r"""
    adding a
    adding b
    adding c"""

sh % "echo 'key: value'" >> "a"
sh % "echo 'key: value'" >> "b"
sh % "echo foo" >> "c"
sh % "hg ci -m2"

sh % "hg up -C 0" == "3 files updated, 0 files merged, 0 files removed, 0 files unresolved"
sh % "hg diff --git -c1" > "want"
sh % "hg diff -c1" | "hg import --no-commit -" == "applying patch from stdin"
sh % "hg diff --git" > "have"
sh % "diff want have"
sh % "cd .."

# import a unified diff with no lines of context (diff -U0)

sh % "hg init diffzero"
sh % "cd diffzero"
sh % "cat" << r"""
c2
c4
c5
""" > "f"
sh % "hg commit -Am0" == "adding f"

sh % "hg import --no-commit -" << r"""
# HG changeset patch
# User test
# Date 0 0
# Node ID f4974ab632f3dee767567b0576c0ec9a4508575c
# Parent  8679a12a975b819fae5f7ad3853a2886d143d794
1
diff -r 8679a12a975b -r f4974ab632f3 f
--- a/f	Thu Jan 01 00:00:00 1970 +0000
+++ b/f	Thu Jan 01 00:00:00 1970 +0000
@@ -0,0 +1,1 @@
+c1
@@ -1,0 +3,1 @@
+c3
@@ -3,1 +4,0 @@
-c5
""" == "applying patch from stdin"

sh % "cat f" == r"""
    c1
    c2
    c3
    c4"""

sh % "cd .."

# commit message that looks like a diff header (issue1879)

sh % "hg init headerlikemsg"
sh % "cd headerlikemsg"
sh % "touch empty"
sh % "echo nonempty" >> "nonempty"
sh % "hg ci -qAl -" << r"""
blah blah
diff blah
blah blah
"""
sh % "hg --config 'diff.git=1' log -pv" == r"""
    changeset:   0:c6ef204ef767
    tag:         tip
    user:        test
    date:        Thu Jan 01 00:00:00 1970 +0000
    files:       empty nonempty
    description:
    blah blah
    diff blah
    blah blah


    diff --git a/empty b/empty
    new file mode 100644
    diff --git a/nonempty b/nonempty
    new file mode 100644
    --- /dev/null
    +++ b/nonempty
    @@ -0,0 +1,1 @@
    +nonempty"""

#  (without --git, empty file is lost, but commit message should be preserved)

sh % "hg init plain"
sh % "hg export 0" | "hg -R plain import -" == "applying patch from stdin"
sh % "hg --config 'diff.git=1' -R plain log -pv" == r"""
    changeset:   0:60a2d231e71f
    tag:         tip
    user:        test
    date:        Thu Jan 01 00:00:00 1970 +0000
    files:       nonempty
    description:
    blah blah
    diff blah
    blah blah


    diff --git a/nonempty b/nonempty
    new file mode 100644
    --- /dev/null
    +++ b/nonempty
    @@ -0,0 +1,1 @@
    +nonempty"""

#  (with --git, patch contents should be fully preserved)

sh % "hg init git"
sh % "hg --config 'diff.git=1' export 0" | "hg -R git import -" == "applying patch from stdin"
sh % "hg --config 'diff.git=1' -R git log -pv" == r"""
    changeset:   0:c6ef204ef767
    tag:         tip
    user:        test
    date:        Thu Jan 01 00:00:00 1970 +0000
    files:       empty nonempty
    description:
    blah blah
    diff blah
    blah blah


    diff --git a/empty b/empty
    new file mode 100644
    diff --git a/nonempty b/nonempty
    new file mode 100644
    --- /dev/null
    +++ b/nonempty
    @@ -0,0 +1,1 @@
    +nonempty"""

sh % "cd .."

# no segfault while importing a unified diff which start line is zero but chunk
# size is non-zero

sh % "hg init startlinezero"
sh % "cd startlinezero"
sh % "echo foo" > "foo"
sh % "hg commit -Amfoo" == "adding foo"

sh % "hg import --no-commit -" << r"""
diff a/foo b/foo
--- a/foo
+++ b/foo
@@ -0,1 +0,1 @@
 foo
""" == "applying patch from stdin"

sh % "cd .."

# Test corner case involving fuzz and skew

sh % "hg init morecornercases"
sh % "cd morecornercases"

sh % "cat" << r"""
diff --git a/a b/a
--- a/a
+++ b/a
@@ -1,0 +1,1 @@
+line
""" > "01-no-context-beginning-of-file.diff"

sh % "cat" << r"""
diff --git a/a b/a
--- a/a
+++ b/a
@@ -1,1 +1,1 @@
-2
+add some skew
@@ -2,0 +2,1 @@
+line
""" > "02-no-context-middle-of-file.diff"

sh % "cat" << r"""
diff --git a/a b/a
--- a/a
+++ b/a
@@ -10,0 +10,1 @@
+line
""" > "03-no-context-end-of-file.diff"

sh % "cat" << r"""
diff --git a/a b/a
--- a/a
+++ b/a
@@ -1,1 +1,1 @@
-2
+add some skew
@@ -2,2 +2,3 @@
 not matching, should fuzz
 ... a bit
+line
""" > "04-middle-of-file-completely-fuzzed.diff"

sh % "cat" << r"""
1
2
3
4
""" > "a"
sh % "hg ci -Am adda a"
sh % "for p in '*.diff;' do" == r"""
    >   hg import -v --no-commit $p
    >   cat a
    >   hg revert -aqC a
    >   # patch -p1 < $p
    >   # cat a
    >   # hg revert -aC a
    > done
    applying 01-no-context-beginning-of-file.diff
    patching file a
    applied to working directory
    1
    line
    2
    3
    4
    applying 02-no-context-middle-of-file.diff
    patching file a
    Hunk #1 succeeded at 2 (offset 1 lines).
    Hunk #2 succeeded at 4 (offset 1 lines).
    applied to working directory
    1
    add some skew
    3
    line
    4
    applying 03-no-context-end-of-file.diff
    patching file a
    Hunk #1 succeeded at 5 (offset -6 lines).
    applied to working directory
    1
    2
    3
    4
    line
    applying 04-middle-of-file-completely-fuzzed.diff
    patching file a
    Hunk #1 succeeded at 2 (offset 1 lines).
    Hunk #2 succeeded at 5 with fuzz 2 (offset 1 lines).
    applied to working directory
    1
    add some skew
    3
    4
    line"""
sh % "cd .."

# Test partial application
# ------------------------

# prepare a stack of patches depending on each other

sh % "hg init partial"
sh % "cd partial"
sh % "cat" << r"""
one
two
three
four
five
six
seven
""" > "a"
sh % "hg add a"
sh % "echo b" > "b"
sh % "hg add b"
sh % "hg commit -m initial -u Babar"
sh % "cat" << r"""
one
two
3
four
five
six
seven
""" > "a"
sh % "hg commit -m three -u Celeste"
sh % "cat" << r"""
one
two
3
4
five
six
seven
""" > "a"
sh % "hg commit -m four -u Rataxes"
sh % "cat" << r"""
one
two
3
4
5
six
seven
""" > "a"
sh % "echo bb" >> "b"
sh % "hg commit -m five -u Arthur"
sh % "echo Babar" > "jungle"
sh % "hg add jungle"
sh % "hg ci -m jungle -u Zephir"
sh % "echo Celeste" >> "jungle"
sh % "hg ci -m 'extended jungle' -u Cornelius"
sh % "hg log -G --template '{desc|firstline} [{author}] {diffstat}\\n'" == r"""
    @  extended jungle [Cornelius] 1: +1/-0
    |
    o  jungle [Zephir] 1: +1/-0
    |
    o  five [Arthur] 2: +2/-1
    |
    o  four [Rataxes] 1: +1/-1
    |
    o  three [Celeste] 1: +1/-1
    |
    o  initial [Babar] 2: +8/-0"""
# Adding those config options should not change the output of diffstat. Bugfix #4755.

sh % "hg log -r . --template '{diffstat}\\n'" == "1: +1/-0"
sh % "hg log -r . --template '{diffstat}\\n' --config 'diff.git=1' --config 'diff.noprefix=1'" == "1: +1/-0"

# Importing with some success and some errors:

sh % "hg update --rev 'desc(initial)'" == "2 files updated, 0 files merged, 1 files removed, 0 files unresolved"
sh % "hg export --rev 'desc(five)'" | "hg import --partial -" == r"""
    applying patch from stdin
    patching file a
    Hunk #1 FAILED at 1
    1 out of 1 hunks FAILED -- saving rejects to file a.rej
    patch applied partially
    (fix the .rej files and run `hg commit --amend`)
    [1]"""

sh % "hg log -G --template '{desc|firstline} [{author}] {diffstat}\\n'" == r"""
    @  five [Arthur] 1: +1/-0
    |
    | o  extended jungle [Cornelius] 1: +1/-0
    | |
    | o  jungle [Zephir] 1: +1/-0
    | |
    | o  five [Arthur] 2: +2/-1
    | |
    | o  four [Rataxes] 1: +1/-1
    | |
    | o  three [Celeste] 1: +1/-1
    |/
    o  initial [Babar] 2: +8/-0"""
sh % "hg export" == r"""
    # HG changeset patch
    # User Arthur
    # Date 0 0
    #      Thu Jan 01 00:00:00 1970 +0000
    # Node ID 26e6446bb2526e2be1037935f5fca2b2706f1509
    # Parent  8e4f0351909eae6b9cf68c2c076cb54c42b54b2e
    five

    diff -r 8e4f0351909e -r 26e6446bb252 b
    --- a/b	Thu Jan 01 00:00:00 1970 +0000
    +++ b/b	Thu Jan 01 00:00:00 1970 +0000
    @@ -1,1 +1,2 @@
     b
    +bb"""
sh % "hg status -c ." == r"""
    C a
    C b"""
sh % "ls" == r"""
    a
    a.rej
    b"""

# Importing with zero success:

sh % "hg update --rev 'desc(initial)'" == "1 files updated, 0 files merged, 0 files removed, 0 files unresolved"
sh % "hg export --rev 'desc(four)'" | "hg import --partial -" == r"""
    applying patch from stdin
    patching file a
    Hunk #1 FAILED at 0
    1 out of 1 hunks FAILED -- saving rejects to file a.rej
    patch applied partially
    (fix the .rej files and run `hg commit --amend`)
    [1]"""

sh % "hg log -G --template '{desc|firstline} [{author}] {diffstat}\\n'" == r"""
    @  four [Rataxes] 0: +0/-0
    |
    | o  five [Arthur] 1: +1/-0
    |/
    | o  extended jungle [Cornelius] 1: +1/-0
    | |
    | o  jungle [Zephir] 1: +1/-0
    | |
    | o  five [Arthur] 2: +2/-1
    | |
    | o  four [Rataxes] 1: +1/-1
    | |
    | o  three [Celeste] 1: +1/-1
    |/
    o  initial [Babar] 2: +8/-0"""
sh % "hg export" == r"""
    # HG changeset patch
    # User Rataxes
    # Date 0 0
    #      Thu Jan 01 00:00:00 1970 +0000
    # Node ID cb9b1847a74d9ad52e93becaf14b98dbcc274e1e
    # Parent  8e4f0351909eae6b9cf68c2c076cb54c42b54b2e
    four"""
sh % "hg status -c ." == r"""
    C a
    C b"""
sh % "ls" == r"""
    a
    a.rej
    b"""

# Importing with unknown file:

sh % "hg update --rev 'desc(initial)'" == "0 files updated, 0 files merged, 0 files removed, 0 files unresolved"
sh % "hg export --rev 'desc(\"extended jungle\")'" | "hg import --partial -" == r"""
    applying patch from stdin
    unable to find 'jungle' for patching
    (use '--prefix' to apply patch relative to the current directory)
    1 out of 1 hunks FAILED -- saving rejects to file jungle.rej
    patch applied partially
    (fix the .rej files and run `hg commit --amend`)
    [1]"""

sh % "hg log -G --template '{desc|firstline} [{author}] {diffstat}\\n'" == r"""
    @  extended jungle [Cornelius] 0: +0/-0
    |
    | o  four [Rataxes] 0: +0/-0
    |/
    | o  five [Arthur] 1: +1/-0
    |/
    | o  extended jungle [Cornelius] 1: +1/-0
    | |
    | o  jungle [Zephir] 1: +1/-0
    | |
    | o  five [Arthur] 2: +2/-1
    | |
    | o  four [Rataxes] 1: +1/-1
    | |
    | o  three [Celeste] 1: +1/-1
    |/
    o  initial [Babar] 2: +8/-0"""
sh % "hg export" == r"""
    # HG changeset patch
    # User Cornelius
    # Date 0 0
    #      Thu Jan 01 00:00:00 1970 +0000
    # Node ID 1fb1f86bef43c5a75918178f8d23c29fb0a7398d
    # Parent  8e4f0351909eae6b9cf68c2c076cb54c42b54b2e
    extended jungle"""
sh % "hg status -c ." == r"""
    C a
    C b"""
sh % "ls" == r"""
    a
    a.rej
    b
    jungle.rej"""

# Importing multiple failing patches:

sh % "hg update --rev 'desc(initial)'" == "0 files updated, 0 files merged, 0 files removed, 0 files unresolved"
sh % "echo B" > "b"
sh % "hg commit -m 'a new base'"
sh % 'hg export --rev \'desc("four") + desc("extended jungle")\'' | "hg import --partial -" == r"""
    applying patch from stdin
    patching file a
    Hunk #1 FAILED at 0
    1 out of 1 hunks FAILED -- saving rejects to file a.rej
    patch applied partially
    (fix the .rej files and run `hg commit --amend`)
    [1]"""
sh % "hg log -G --template '{desc|firstline} [{author}] {diffstat}\\n'" == r"""
    @  four [Rataxes] 0: +0/-0
    |
    o  a new base [test] 1: +1/-1
    |
    | o  extended jungle [Cornelius] 0: +0/-0
    |/
    | o  four [Rataxes] 0: +0/-0
    |/
    | o  five [Arthur] 1: +1/-0
    |/
    | o  extended jungle [Cornelius] 1: +1/-0
    | |
    | o  jungle [Zephir] 1: +1/-0
    | |
    | o  five [Arthur] 2: +2/-1
    | |
    | o  four [Rataxes] 1: +1/-1
    | |
    | o  three [Celeste] 1: +1/-1
    |/
    o  initial [Babar] 2: +8/-0"""
sh % "hg export" == r"""
    # HG changeset patch
    # User Rataxes
    # Date 0 0
    #      Thu Jan 01 00:00:00 1970 +0000
    # Node ID a9d7b6d0ffbb4eb12b7d5939250fcd42e8930a1d
    # Parent  f59f8d2e95a8ca5b1b4ca64320140da85f3b44fd
    four"""
sh % "hg status -c ." == r"""
    C a
    C b"""

# Importing some extra header
# ===========================

sh % "cat" << r"""
import edenscm.mercurial.patch
import edenscm.mercurial.cmdutil

def processfoo(repo, data, extra, opts):
    if 'foo' in data:
        extra['foo'] = data['foo']
def postimport(ctx):
    if 'foo' in ctx.extra():
        ctx.repo().ui.write('imported-foo: %s\n' % ctx.extra()['foo'])

edenscm.mercurial.patch.patchheadermap.append(('Foo', 'foo'))
edenscm.mercurial.cmdutil.extrapreimport.append('foo')
edenscm.mercurial.cmdutil.extrapreimportmap['foo'] = processfoo
edenscm.mercurial.cmdutil.extrapostimport.append('foo')
edenscm.mercurial.cmdutil.extrapostimportmap['foo'] = postimport
""" > "$TESTTMP/parseextra.py"
sh % "cat" << r"""
[extensions]
parseextra=$TESTTMP/parseextra.py
""" >> "$HGRCPATH"
sh % "hg up -C tip" == "0 files updated, 0 files merged, 0 files removed, 0 files unresolved"
sh % "cat" << r"""
# HG changeset patch
# User Rataxes
# Date 0 0
#      Thu Jan 01 00:00:00 1970 +0000
# Foo bar
height

--- a/a	Thu Jan 01 00:00:00 1970 +0000
+++ b/a	Wed Oct 07 09:17:44 2015 +0000
@@ -5,3 +5,4 @@
 five
 six
 seven
+heigt
""" > "$TESTTMP/foo.patch"
sh % "hg import '$TESTTMP/foo.patch'" == r"""
    applying $TESTTMP/foo.patch
    imported-foo: bar"""
sh % "hg log --debug -r ." | "grep extra" == r"""
    extra:       branch=default
    extra:       foo=bar"""

# Warn the user that paths are relative to the root of
# repository when file not found for patching

sh % "mkdir filedir"
sh % "echo file1" >> "filedir/file1"
sh % "hg add filedir/file1"
sh % "hg commit -m file1"
sh % "cd filedir"
sh % "hg import -p 2 -" << r"""
# HG changeset patch
# User test
# Date 0 0
file2

diff --git a/filedir/file1 b/filedir/file1
--- a/filedir/file1
+++ b/filedir/file1
@@ -1,1 +1,2 @@
 file1
+file2
""" == r"""
    applying patch from stdin
    unable to find 'file1' for patching
    (use '--prefix' to apply patch relative to the current directory)
    1 out of 1 hunks FAILED -- saving rejects to file file1.rej
    abort: patch failed to apply
    [255]"""

# test import crash (issue5375)
sh % "cd .."
sh % "hg init repo"
sh % "cd repo"
sh % "printf 'diff --git a/a b/b\\nrename from a\\nrename to b'" | "hg import -" == r"""
    applying patch from stdin
    a not tracked!
    abort: source file 'a' does not exist
    [255]"""
