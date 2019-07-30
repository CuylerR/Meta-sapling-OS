# Copyright (c) Facebook, Inc. and its affiliates.
#
# This software may be used and distributed according to the terms of the
# GNU General Public License version 2 or any later version.

from __future__ import absolute_import

from testutil.dott import feature, sh, testtmp  # noqa: F401


sh % "newrepo"
sh % "hg d" == ""

sh % "hg d --config alias.do=root" == r"""
    hg: command 'd' is ambiguous:
     diff
     do
    [255]"""

sh % "hg debugf" == r"""
    hg: command 'debugf' is ambiguous:
    	debugfilerevision
    	debugfileset
    	debugformat
    	debugfsinfo
    [255]"""
