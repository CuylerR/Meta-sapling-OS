#!/usr/bin/env python2.7

import os
import random
import sys
import unittest

import silenttestrunner

# Add the repo root to the path so we can find the built ctreemanifest
fullpath = os.path.join(os.getcwd(), __file__)
sys.path.insert(0, os.path.dirname(os.path.dirname(fullpath)))
import ctreemanifest

from mercurial import (
    manifest,
    match as matchmod
)

class FakeStore(object):
    def __init__(self):
        self._data = {}

    def get(self, path, node):
        return self._data[(path, node)]

    def add(self, path, node, deltabase, value):
        self._data[(path, node)] = value

def getvalidflag():
    # t is reserved as a directory entry, so don't go around setting that as the
    # flag.
    while True:
        r = random.randint(0, 255)
        if r != ord('t'):
            return chr(r)

def hashflags(requireflag=False):
    h = ''.join([chr(random.randint(0, 255)) for x in range(20)])
    if random.randint(0, 1) == 0 and requireflag is False:
        f = ''
    else:
        f = getvalidflag()
    return h, f

class ctreemanifesttests(unittest.TestCase):
    def setUp(self):
        random.seed(0)

    def testInitialization(self):
        ctreemanifest.treemanifest(FakeStore())

    def testEmptyFlag(self):
        a = ctreemanifest.treemanifest(FakeStore())
        h, f = hashflags()[0], ''
        a.set("abc", h, f)
        out = a.find("abc")
        self.assertEquals((h, f), out)

    def testNullFlag(self):
        a = ctreemanifest.treemanifest(FakeStore())
        h, f = hashflags()[0], '\0'
        a.set("abc", h, f)
        out = a.find("abc")
        self.assertEquals((h, f), out)

    def testSetGet(self):
        a = ctreemanifest.treemanifest(FakeStore())
        h, f = hashflags()
        a.set("abc", h, f)
        out = a.find("abc")
        self.assertEquals((h, f), out)

    def testUpdate(self):
        a = ctreemanifest.treemanifest(FakeStore())
        h, f = hashflags()
        a.set("abc", h, f)
        out = a.find("abc")
        self.assertEquals((h, f), out)

        h, f = hashflags()
        a.set("abc", h, f)
        out = a.find("abc")
        self.assertEquals((h, f), out)

    def testDirAfterFile(self):
        a = ctreemanifest.treemanifest(FakeStore())
        file_h, file_f = hashflags()
        a.set("abc", file_h, file_f)
        out = a.find("abc")
        self.assertEquals((file_h, file_f), out)

        dir_h, dir_f = hashflags()
        a.set("abc/def", dir_h, dir_f)
        out = a.find("abc/def")
        self.assertEquals((dir_h, dir_f), out)

        out = a.find("abc")
        self.assertEquals((file_h, file_f), out)

    def testFileAfterDir(self):
        a = ctreemanifest.treemanifest(FakeStore())
        dir_h, dir_f = hashflags()
        a.set("abc/def", dir_h, dir_f)
        out = a.find("abc/def")
        self.assertEquals((dir_h, dir_f), out)

        file_h, file_f = hashflags()
        a.set("abc", file_h, file_f)
        out = a.find("abc")
        self.assertEquals((file_h, file_f), out)

        out = a.find("abc/def")
        self.assertEquals((dir_h, dir_f), out)

    def testDeeplyNested(self):
        a = ctreemanifest.treemanifest(FakeStore())
        h, f = hashflags()
        a.set("abc/def/ghi/jkl", h, f)
        out = a.find("abc/def/ghi/jkl")
        self.assertEquals((h, f), out)

        h, f = hashflags()
        a.set("abc/def/ghi/jkl2", h, f)
        out = a.find("abc/def/ghi/jkl2")
        self.assertEquals((h, f), out)

    def testDeeplyNested(self):
        a = ctreemanifest.treemanifest(FakeStore())
        h, f = hashflags()
        a.set("abc/def/ghi/jkl", h, f)
        out = a.find("abc/def/ghi/jkl")
        self.assertEquals((h, f), out)

        h, f = hashflags()
        a.set("abc/def/ghi/jkl2", h, f)
        out = a.find("abc/def/ghi/jkl2")
        self.assertEquals((h, f), out)

    def testBushyTrees(self):
        a = ctreemanifest.treemanifest(FakeStore())
        nodes = {}
        for ix in range(111):
            h, f = hashflags()
            nodes["abc/def/ghi/jkl%d" % ix] = (h, f)

        for fp, (h, f) in nodes.items():
            a.set(fp, h, f)

        for fp, (h, f) in nodes.items():
            out = a.find(fp)
            self.assertEquals((h, f), out)

    def testFlagChanges(self):
        a = ctreemanifest.treemanifest(FakeStore())

        # go from no flags to with flags, back to no flags.
        h, f = hashflags(requireflag=True)
        self.assertEquals(len(f), 1)

        a.set("abc", h, '')
        out = a.find("abc")
        self.assertEquals(h, out[0])
        self.assertEquals('', out[1])

        a.set("abc", h, f)
        out = a.find("abc")
        self.assertEquals(h, out[0])
        self.assertEquals(f, out[1])

        a.set("abc", h, '')
        out = a.find("abc")
        self.assertEquals(h, out[0])
        self.assertEquals('', out[1])

    def testSetRemove(self):
        a = ctreemanifest.treemanifest(FakeStore())
        h, f = hashflags()
        a.set("abc", h, f)
        out = a.find("abc")
        self.assertEquals((h, f), out)

        a.set("abc", None, None)
        try:
            out = a.find("abc")
            raise RuntimeError("set should've removed file abc")
        except KeyError:
            pass

    def testCleanupAfterRemove(self):
        a = ctreemanifest.treemanifest(FakeStore())
        h, f = hashflags()
        a.set("abc/def/ghi", h, f)
        out = a.find("abc/def/ghi")
        self.assertEquals((h, f), out)

        a.set("abc/def/ghi", None, None)

        h, f = hashflags()
        a.set("abc", h, f)
        out = a.find("abc")
        self.assertEquals((h, f), out)

    def testIterOrder(self):
        a = ctreemanifest.treemanifest(FakeStore())
        h, f = hashflags()
        a.set("abc/def/ghi", h, f)
        a.set("abc/def.ghi", h, f)

        results = [fp for fp in a]
        self.assertEquals(results[0], "abc/def.ghi")
        self.assertEquals(results[1], "abc/def/ghi")

    def testIterOrderSigned(self):
        a = ctreemanifest.treemanifest(FakeStore())
        h, f = hashflags()
        a.set("abc/def/\xe6\xe9", h, f)
        a.set("abc/def/gh", h, f)

        results = [fp for fp in a]
        self.assertEquals(results[0], "abc/def/gh")
        self.assertEquals(results[1], "abc/def/\xe6\xe9")

    def testWrite(self):
        a = ctreemanifest.treemanifest(FakeStore())
        a.set("abc/def/x", *hashflags())
        a.set("abc/def/y", *hashflags())
        a.set("abc/z", *hashflags())

        store = FakeStore()
        anode = a.write(store)

        a2 = ctreemanifest.treemanifest(store, anode)
        self.assertEquals(list(a.iterentries()), list(a2.iterentries()))

        b = a2.copy()
        b.set("lmn/v", *hashflags())
        b.set("abc/z", *hashflags())

        bnode = b.write(store)

        b2 = ctreemanifest.treemanifest(store, bnode)
        self.assertEquals(list(b.iterentries()), list(b2.iterentries()))

    def testWriteReplaceFile(self):
        """Tests writing a manifest which replaces a file with a directory."""
        a = ctreemanifest.treemanifest(FakeStore())
        a.set("abc/a", *hashflags())
        a.set("abc/z", *hashflags())

        store = FakeStore()
        a.write(store)

        b = a.copy()
        b.set("abc/a", None, None)
        b.set("abc/a/foo", *hashflags())

        bnode = b.write(store, a, useDeltas=False)

        b2 = ctreemanifest.treemanifest(store, bnode)
        self.assertEquals(list(b.iterentries()), list(b2.iterentries()))

    def testGet(self):
        a = ctreemanifest.treemanifest(FakeStore())
        zflags = hashflags()
        a.set("abc/z", *zflags)

        self.assertEquals(a.get('abc/z'), zflags[0])
        self.assertEquals(a.get('abc/x'), None)
        self.assertEquals(a.get('abc'), None)

    def testFind(self):
        a = ctreemanifest.treemanifest(FakeStore())
        zflags = hashflags()
        a.set("abc/z", *zflags)

        self.assertEquals(a.find('abc/z'), zflags)
        try:
            a.find('abc/x')
            raise RuntimeError("find for non-existent file should throw")
        except KeyError:
            pass

    def testSetFlag(self):
        a = ctreemanifest.treemanifest(FakeStore())
        zflags = hashflags()
        a.set("abc/z", *zflags)
        a.setflag("abc/z", '')
        self.assertEquals(a.flags('abc/z'), '')

        a.setflag("abc/z", 'd')
        self.assertEquals(a.flags('abc/z'), 'd')

        try:
            a.setflag("foo", 'd')
            raise RuntimeError("setflag should throw")
        except KeyError:
            pass

    def testSetItem(self):
        a = ctreemanifest.treemanifest(FakeStore())
        zflags = hashflags(requireflag=True)
        a.set("abc/z", *zflags)

        fooflags = hashflags()
        a["foo"] = fooflags[0]
        self.assertEquals(a.find('foo'), (fooflags[0], ''))

        newnode = hashflags()[0]
        a["abc/z"] = newnode
        self.assertEquals(a.find('abc/z'), (newnode, zflags[1]))

    def testText(self):
        a = ctreemanifest.treemanifest(FakeStore())
        zflags = hashflags(requireflag=True)
        a.set("abc/z", *zflags)

        treetext = a.text()
        treetextv2 = a.text(usemanifestv2=True)

        b = manifest.manifestdict()
        b["abc/z"] = zflags[0]
        b.setflag("abc/z", zflags[1])
        fulltext = b.text()
        fulltextv2 = b.text(usemanifestv2=True)

        self.assertEquals(treetext, fulltext)
        self.assertEquals(treetextv2, fulltextv2)

    def testDiff(self):
        a = ctreemanifest.treemanifest(FakeStore())
        zflags = hashflags()
        mflags = hashflags()
        a.set("abc/z", *zflags)
        a.set("xyz/m", *mflags)

        b = ctreemanifest.treemanifest(FakeStore())
        b.set("abc/z", *zflags)
        b.set("xyz/m", *mflags)

        # Diff matching trees
        # - uncommitted trees
        diff = a.diff(b)
        self.assertEquals(diff, {})

        # - committed trees
        store = FakeStore()
        a.write(store)
        b.write(store)
        diff = a.diff(b)
        self.assertEquals(diff, {})

        # Diff with modifications
        newfileflags = hashflags()
        newzflags = hashflags()
        b.set("newfile", *newfileflags)
        b.set("abc/z", *newzflags)

        # - uncommitted trees
        diff = a.diff(b)
        self.assertEquals(diff, {
            "newfile": ((None, ''), newfileflags),
            "abc/z": (zflags, newzflags)
        })

        # - committed trees
        a.write(store)
        b.write(store)

        diff = a.diff(b)
        self.assertEquals(diff, {
            "newfile": ((None, ''), newfileflags),
            "abc/z": (zflags, newzflags)
        })

        # Diff with clean
        diff = a.diff(b, clean=True)
        self.assertEquals(diff, {
            "newfile": ((None, ''), newfileflags),
            "abc/z": (zflags, newzflags),
            "xyz/m": None
        })

    def testHasDir(self):
        a = ctreemanifest.treemanifest(FakeStore())
        zflags = hashflags()
        a.set("abc/z", *zflags)

        self.assertFalse(a.hasdir('abc/z'))
        self.assertTrue(a.hasdir('abc'))
        self.assertFalse(a.hasdir('xyz'))

    def testContains(self):
        a = ctreemanifest.treemanifest(FakeStore())
        zflags = hashflags()
        a.set("abc/z", *zflags)

        self.assertTrue("abc/z" in a)
        self.assertFalse("abc" in a)
        self.assertFalse(None in a)

    def testDirs(self):
        a = ctreemanifest.treemanifest(FakeStore())
        zflags = hashflags()
        a.set("abc/z", *zflags)

        dirs = a.dirs()
        self.assertTrue("abc" in dirs)
        self.assertFalse("abc/z" in dirs)

    def testNonZero(self):
        a = ctreemanifest.treemanifest(FakeStore())
        self.assertFalse(bool(a))
        zflags = hashflags()
        a.set("abc/z", *zflags)
        self.assertTrue(bool(a))

    def testFlags(self):
        a = ctreemanifest.treemanifest(FakeStore())
        zflags = hashflags(requireflag=True)
        a.set("abc/z", *zflags)

        self.assertEquals(a.flags('x'), '')
        self.assertEquals(a.flags('x', default='z'), 'z')
        self.assertEquals(a.flags('abc/z'), zflags[1])

    def testMatches(self):
        a = ctreemanifest.treemanifest(FakeStore())
        zflags = hashflags()
        a.set("abc/z", *zflags)
        a.set("foo", *hashflags())

        match = matchmod.match('/', '/', ['abc/z'])

        result = a.matches(match)
        self.assertEquals(list(result.iterentries()),
                          [('abc/z', zflags[0], zflags[1])])

        match = matchmod.match('/', '/', ['x'])
        result = a.matches(match)
        self.assertEquals(list(result.iterentries()), [])

    def testKeys(self):
        a = ctreemanifest.treemanifest(FakeStore())
        self.assertEquals(a.keys(), [])

        zflags = hashflags()
        a.set("abc/z", *zflags)
        a.set("foo", *hashflags())

        self.assertEquals(a.keys(), ["abc/z", "foo"])

    def testIterItems(self):
        a = ctreemanifest.treemanifest(FakeStore())
        self.assertEquals(list(a.iteritems()), [])

        zflags = hashflags()
        fooflags = hashflags()
        a.set("abc/z", *zflags)
        a.set("foo", *fooflags)

        self.assertEquals(list(a.iteritems()), [("abc/z", zflags[0]),
                                                ("foo", fooflags[0])])

if __name__ == '__main__':
    silenttestrunner.main(__name__)
