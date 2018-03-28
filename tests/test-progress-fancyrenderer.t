  $ cat >> $HGRCPATH <<EOF
  > [extensions]
  > color=
  > progress=
  > progresstest=$TESTDIR/progresstest.py
  > [progress]
  > delay = 0
  > changedelay = 2
  > refresh = 1
  > renderer = fancy
  > assume-tty = true
  > width = 60
  > [ui]
  > color = debug
  > EOF

simple test
  $ hg progresstest 4 4
  \r (no-eol) (esc)
  [progress.fancy.bar.normal progress.fancy.topic| progress test:][progress.fancy.bar.background progress.fancy.topic| ][progress.fancy.bar.background progress.fancy.item|loop 1                            ][progress.fancy.bar.background progress.fancy.count|  1/4 04s ]\r (no-eol) (esc)
  [progress.fancy.bar.normal progress.fancy.topic| progress test: ][progress.fancy.bar.normal progress.fancy.item|loop 2        ][progress.fancy.bar.background progress.fancy.item|                    ][progress.fancy.bar.background progress.fancy.count|  2/4 03s ]\r (no-eol) (esc)
  [progress.fancy.bar.normal progress.fancy.topic| progress test: ][progress.fancy.bar.normal progress.fancy.item|loop 3                       ][progress.fancy.bar.background progress.fancy.item|     ][progress.fancy.bar.background progress.fancy.count|  3/4 02s ]\r (no-eol) (esc)
  [progress.fancy.bar.normal progress.fancy.topic| progress test: ][progress.fancy.bar.normal progress.fancy.item|loop 4                            ][progress.fancy.bar.normal progress.fancy.count|  4/4 01s ]\r (no-eol) (esc)
                                                              \r (no-eol) (esc)

no progress with --quiet
  $ hg progresstest --quiet 4 4

test nested short-lived topics (which shouldn't display with changedelay)
  $ hg progresstest --nested 4 4
  \r (no-eol) (esc)
  [progress.fancy.bar.background progress.fancy.topic| progress test: ][progress.fancy.bar.background progress.fancy.item|loop 0                               ][progress.fancy.bar.background progress.fancy.count|  0/4  ]\r (no-eol) (esc)
  [progress.fancy.bar.background progress.fancy.topic| progress test: ][progress.fancy.bar.background progress.fancy.item|loop 0                               ][progress.fancy.bar.background progress.fancy.count|  0/4  ]\r (no-eol) (esc)
  [progress.fancy.bar.background progress.fancy.topic| progress test: ][progress.fancy.bar.background progress.fancy.item|loop 0                               ][progress.fancy.bar.background progress.fancy.count|  0/4  ]\r (no-eol) (esc)
  [progress.fancy.bar.normal progress.fancy.topic| progress test:][progress.fancy.bar.background progress.fancy.topic| ][progress.fancy.bar.background progress.fancy.item|loop 1                            ][progress.fancy.bar.background progress.fancy.count|  1/4 13s ]\r (no-eol) (esc)
  [progress.fancy.bar.normal progress.fancy.topic| progress test:][progress.fancy.bar.background progress.fancy.topic| ][progress.fancy.bar.background progress.fancy.item|loop 1                            ][progress.fancy.bar.background progress.fancy.count|  1/4 16s ]\r (no-eol) (esc)
  [progress.fancy.bar.normal progress.fancy.topic| progress test:][progress.fancy.bar.background progress.fancy.topic| ][progress.fancy.bar.background progress.fancy.item|loop 1                            ][progress.fancy.bar.background progress.fancy.count|  1/4 19s ]\r (no-eol) (esc)
  [progress.fancy.bar.normal progress.fancy.topic| progress test:][progress.fancy.bar.background progress.fancy.topic| ][progress.fancy.bar.background progress.fancy.item|loop 1                            ][progress.fancy.bar.background progress.fancy.count|  1/4 22s ]\r (no-eol) (esc)
  [progress.fancy.bar.normal progress.fancy.topic| progress test: ][progress.fancy.bar.normal progress.fancy.item|loop 2        ][progress.fancy.bar.background progress.fancy.item|                    ][progress.fancy.bar.background progress.fancy.count|  2/4 09s ]\r (no-eol) (esc)
  [progress.fancy.bar.normal progress.fancy.topic| progress test: ][progress.fancy.bar.normal progress.fancy.item|loop 2        ][progress.fancy.bar.background progress.fancy.item|                    ][progress.fancy.bar.background progress.fancy.count|  2/4 10s ]\r (no-eol) (esc)
  [progress.fancy.bar.normal progress.fancy.topic| progress test: ][progress.fancy.bar.normal progress.fancy.item|loop 2        ][progress.fancy.bar.background progress.fancy.item|                    ][progress.fancy.bar.background progress.fancy.count|  2/4 11s ]\r (no-eol) (esc)
  [progress.fancy.bar.normal progress.fancy.topic| progress test: ][progress.fancy.bar.normal progress.fancy.item|loop 2        ][progress.fancy.bar.background progress.fancy.item|                    ][progress.fancy.bar.background progress.fancy.count|  2/4 12s ]\r (no-eol) (esc)
  [progress.fancy.bar.normal progress.fancy.topic| progress test: ][progress.fancy.bar.normal progress.fancy.item|loop 3                       ][progress.fancy.bar.background progress.fancy.item|     ][progress.fancy.bar.background progress.fancy.count|  3/4 05s ]\r (no-eol) (esc)
  [progress.fancy.bar.normal progress.fancy.topic| progress test: ][progress.fancy.bar.normal progress.fancy.item|loop 3                       ][progress.fancy.bar.background progress.fancy.item|     ][progress.fancy.bar.background progress.fancy.count|  3/4 05s ]\r (no-eol) (esc)
  [progress.fancy.bar.normal progress.fancy.topic| progress test: ][progress.fancy.bar.normal progress.fancy.item|loop 3                       ][progress.fancy.bar.background progress.fancy.item|     ][progress.fancy.bar.background progress.fancy.count|  3/4 05s ]\r (no-eol) (esc)
  [progress.fancy.bar.normal progress.fancy.topic| progress test: ][progress.fancy.bar.normal progress.fancy.item|loop 3                       ][progress.fancy.bar.background progress.fancy.item|     ][progress.fancy.bar.background progress.fancy.count|  3/4 06s ]\r (no-eol) (esc)
  [progress.fancy.bar.normal progress.fancy.topic| progress test: ][progress.fancy.bar.normal progress.fancy.item|loop 4                            ][progress.fancy.bar.normal progress.fancy.count|  4/4 01s ]\r (no-eol) (esc)
  [progress.fancy.bar.normal progress.fancy.topic| progress test: ][progress.fancy.bar.normal progress.fancy.item|loop 4                            ][progress.fancy.bar.normal progress.fancy.count|  4/4 01s ]\r (no-eol) (esc)
  [progress.fancy.bar.normal progress.fancy.topic| progress test: ][progress.fancy.bar.normal progress.fancy.item|loop 4                            ][progress.fancy.bar.normal progress.fancy.count|  4/4 01s ]\r (no-eol) (esc)
  [progress.fancy.bar.normal progress.fancy.topic| progress test: ][progress.fancy.bar.normal progress.fancy.item|loop 4                            ][progress.fancy.bar.normal progress.fancy.count|  4/4 01s ]\r (no-eol) (esc)
                                                              \r (no-eol) (esc)

test nested long-lived topics
  $ hg progresstest --nested 8 8
  \r (no-eol) (esc)
  [progress.fancy.bar.background progress.fancy.topic| progress test: ][progress.fancy.bar.background progress.fancy.item|loop 0                               ][progress.fancy.bar.background progress.fancy.count|  0/8  ]\r (no-eol) (esc)
  [progress.fancy.bar.background progress.fancy.topic| progress test: ][progress.fancy.bar.background progress.fancy.item|loop 0                               ][progress.fancy.bar.background progress.fancy.count|  0/8  ]\r (no-eol) (esc)
  [progress.fancy.bar.background progress.fancy.topic| progress test: ][progress.fancy.bar.background progress.fancy.item|loop 0                               ][progress.fancy.bar.background progress.fancy.count|  0/8  ]\r (no-eol) (esc)
  [progress.fancy.bar.normal progress.fancy.topic| progre][progress.fancy.bar.background progress.fancy.topic|ss test: ][progress.fancy.bar.background progress.fancy.item|loop 1                            ][progress.fancy.bar.background progress.fancy.count|  1/8 29s ]\r (no-eol) (esc)
  [progress.fancy.bar.normal progress.fancy.topic| progre][progress.fancy.bar.background progress.fancy.topic|ss test: ][progress.fancy.bar.background progress.fancy.item|loop 1                            ][progress.fancy.bar.background progress.fancy.count|  1/8 36s ]\r (no-eol) (esc)
  [progress.fancy.bar.normal progress.fancy.topic| progre][progress.fancy.bar.background progress.fancy.topic|ss test: ][progress.fancy.bar.background progress.fancy.item|loop 1                            ][progress.fancy.bar.background progress.fancy.count|  1/8 43s ]\r (no-eol) (esc)
  [progress.fancy.bar.normal progress.fancy.topic| progre][progress.fancy.bar.background progress.fancy.topic|ss test: ][progress.fancy.bar.background progress.fancy.item|loop 1                            ][progress.fancy.bar.background progress.fancy.count|  1/8 50s ]\r (no-eol) (esc)
  [progress.fancy.bar.normal progress.fancy.topic| progress test:][progress.fancy.bar.background progress.fancy.topic| ][progress.fancy.bar.background progress.fancy.item|loop 2                            ][progress.fancy.bar.background progress.fancy.count|  2/8 25s ]\r (no-eol) (esc)
  [progress.fancy.bar.normal progress.fancy.topic| progress test:][progress.fancy.bar.background progress.fancy.topic| ][progress.fancy.bar.background progress.fancy.item|loop 2                            ][progress.fancy.bar.background progress.fancy.count|  2/8 28s ]\r (no-eol) (esc)
  [progress.fancy.bar.normal progress.fancy.topic| progress test:][progress.fancy.bar.background progress.fancy.topic| ][progress.fancy.bar.background progress.fancy.item|loop 2                            ][progress.fancy.bar.background progress.fancy.count|  2/8 31s ]\r (no-eol) (esc)
  [progress.fancy.bar.normal progress.fancy.topic| progress test:][progress.fancy.bar.background progress.fancy.topic| ][progress.fancy.bar.background progress.fancy.item|loop 2                            ][progress.fancy.bar.background progress.fancy.count|  2/8 34s ]\r (no-eol) (esc)
  [progress.fancy.bar.normal progress.fancy.topic| progress test: ][progress.fancy.bar.normal progress.fancy.item|loop 3][progress.fancy.bar.background progress.fancy.item|                            ][progress.fancy.bar.background progress.fancy.count|  3/8 21s ]\r (no-eol) (esc)
  [progress.fancy.bar.normal progress.fancy.topic| progress test: ][progress.fancy.bar.normal progress.fancy.item|loop 3][progress.fancy.bar.background progress.fancy.item|                            ][progress.fancy.bar.background progress.fancy.count|  3/8 22s ]\r (no-eol) (esc)
  [progress.fancy.bar.normal progress.fancy.topic| progress test: ][progress.fancy.bar.normal progress.fancy.item|loop 3][progress.fancy.bar.background progress.fancy.item|                            ][progress.fancy.bar.background progress.fancy.count|  3/8 24s ]\r (no-eol) (esc)
  [progress.fancy.bar.normal progress.fancy.topic| progress test: ][progress.fancy.bar.normal progress.fancy.item|loop 3][progress.fancy.bar.background progress.fancy.item|                            ][progress.fancy.bar.background progress.fancy.count|  3/8 26s ]\r (no-eol) (esc)
  [progress.fancy.bar.normal progress.fancy.topic| progress test: ][progress.fancy.bar.normal progress.fancy.item|loop 4        ][progress.fancy.bar.background progress.fancy.item|                    ][progress.fancy.bar.background progress.fancy.count|  4/8 17s ]\r (no-eol) (esc)
  [progress.fancy.bar.normal progress.fancy.topic| progress test: ][progress.fancy.bar.normal progress.fancy.item|loop 4        ][progress.fancy.bar.background progress.fancy.item|                    ][progress.fancy.bar.background progress.fancy.count|  4/8 18s ]\r (no-eol) (esc)
  [progress.fancy.bar.normal progress.fancy.topic| progress test: ][progress.fancy.bar.normal progress.fancy.item|loop 4        ][progress.fancy.bar.background progress.fancy.item|                    ][progress.fancy.bar.background progress.fancy.count|  4/8 19s ]\r (no-eol) (esc)
  [progress.fancy.bar.normal progress.fancy.topic| progress test: ][progress.fancy.bar.normal progress.fancy.item|loop 4        ][progress.fancy.bar.background progress.fancy.item|                    ][progress.fancy.bar.background progress.fancy.count|  4/8 20s ]\r (no-eol) (esc)
  [progress.fancy.bar.normal progress.fancy.topic| progress test: ][progress.fancy.bar.normal progress.fancy.item|loop 5               ][progress.fancy.bar.background progress.fancy.item|             ][progress.fancy.bar.background progress.fancy.count|  5/8 12s ]\r (no-eol) (esc)
  [progress.fancy.bar.normal progress.fancy.topic| progress test: ][progress.fancy.bar.normal progress.fancy.item|loop 5               ][progress.fancy.bar.background progress.fancy.item|             ][progress.fancy.bar.background progress.fancy.count|  5/8 12s ]\r (no-eol) (esc)
  [progress.fancy.bar.normal progress.fancy.topic| progress test: ][progress.fancy.bar.normal progress.fancy.item|loop 5               ][progress.fancy.bar.background progress.fancy.item|             ][progress.fancy.bar.background progress.fancy.count|  5/8 12s ]\r (no-eol) (esc)
  [progress.fancy.bar.normal progress.fancy.topic| progress test: ][progress.fancy.bar.normal progress.fancy.item|loop 5               ][progress.fancy.bar.background progress.fancy.item|             ][progress.fancy.bar.background progress.fancy.count|  5/8 15s ]\r (no-eol) (esc)
  [progress.fancy.bar.normal progress.fancy.topic| nested progress: ][progress.fancy.bar.normal progress.fancy.item|nest 3            ][progress.fancy.bar.background progress.fancy.item|              ][progress.fancy.bar.background progress.fancy.count|  3/5 03s ]\r (no-eol) (esc)
  [progress.fancy.bar.normal progress.fancy.topic| nested progress: ][progress.fancy.bar.normal progress.fancy.item|nest 4                        ][progress.fancy.bar.background progress.fancy.item|  ][progress.fancy.bar.background progress.fancy.count|  4/5 02s ]\r (no-eol) (esc)
  [progress.fancy.bar.normal progress.fancy.topic| nested progress: ][progress.fancy.bar.normal progress.fancy.item|nest 5                          ][progress.fancy.bar.normal progress.fancy.count|  5/5 01s ]\r (no-eol) (esc)
                                                              \r (no-eol) (esc)
  \r (no-eol) (esc)
  [progress.fancy.bar.normal progress.fancy.topic| progress test: ][progress.fancy.bar.normal progress.fancy.item|loop 6                       ][progress.fancy.bar.background progress.fancy.item|     ][progress.fancy.bar.background progress.fancy.count|  6/8 10s ]\r (no-eol) (esc)
  [progress.fancy.bar.normal progress.fancy.topic| progress test: ][progress.fancy.bar.normal progress.fancy.item|loop 6                       ][progress.fancy.bar.background progress.fancy.item|     ][progress.fancy.bar.background progress.fancy.count|  6/8 10s ]\r (no-eol) (esc)
  [progress.fancy.bar.normal progress.fancy.topic| progress test: ][progress.fancy.bar.normal progress.fancy.item|loop 6                       ][progress.fancy.bar.background progress.fancy.item|     ][progress.fancy.bar.background progress.fancy.count|  6/8 10s ]\r (no-eol) (esc)
  [progress.fancy.bar.normal progress.fancy.topic| progress test: ][progress.fancy.bar.normal progress.fancy.item|loop 6                       ][progress.fancy.bar.background progress.fancy.item|     ][progress.fancy.bar.background progress.fancy.count|  6/8 10s ]\r (no-eol) (esc)
  [progress.fancy.bar.normal progress.fancy.topic| progress test: ][progress.fancy.bar.normal progress.fancy.item|loop 7                            ][progress.fancy.bar.normal progress.fancy.count|  ][progress.fancy.bar.background progress.fancy.count|7/8 05s ]\r (no-eol) (esc)
  [progress.fancy.bar.normal progress.fancy.topic| progress test: ][progress.fancy.bar.normal progress.fancy.item|loop 7                            ][progress.fancy.bar.normal progress.fancy.count|  ][progress.fancy.bar.background progress.fancy.count|7/8 05s ]\r (no-eol) (esc)
  [progress.fancy.bar.normal progress.fancy.topic| progress test: ][progress.fancy.bar.normal progress.fancy.item|loop 7                            ][progress.fancy.bar.normal progress.fancy.count|  ][progress.fancy.bar.background progress.fancy.count|7/8 05s ]\r (no-eol) (esc)
  [progress.fancy.bar.normal progress.fancy.topic| progress test: ][progress.fancy.bar.normal progress.fancy.item|loop 7                            ][progress.fancy.bar.normal progress.fancy.count|  ][progress.fancy.bar.background progress.fancy.count|7/8 05s ]\r (no-eol) (esc)
  [progress.fancy.bar.normal progress.fancy.topic| progress test: ][progress.fancy.bar.normal progress.fancy.item|loop 8                            ][progress.fancy.bar.normal progress.fancy.count|  8/8 01s ]\r (no-eol) (esc)
  [progress.fancy.bar.normal progress.fancy.topic| progress test: ][progress.fancy.bar.normal progress.fancy.item|loop 8                            ][progress.fancy.bar.normal progress.fancy.count|  8/8 01s ]\r (no-eol) (esc)
  [progress.fancy.bar.normal progress.fancy.topic| progress test: ][progress.fancy.bar.normal progress.fancy.item|loop 8                            ][progress.fancy.bar.normal progress.fancy.count|  8/8 01s ]\r (no-eol) (esc)
  [progress.fancy.bar.normal progress.fancy.topic| progress test: ][progress.fancy.bar.normal progress.fancy.item|loop 8                            ][progress.fancy.bar.normal progress.fancy.count|  8/8 01s ]\r (no-eol) (esc)
                                                              \r (no-eol) (esc)

test nested shortlived topics without changedelay
  $ hg progresstest --nested --config progress.changedelay=0 8 8
  \r (no-eol) (esc)
  [progress.fancy.bar.background progress.fancy.topic| progress test: ][progress.fancy.bar.background progress.fancy.item|loop 0                               ][progress.fancy.bar.background progress.fancy.count|  0/8  ]\r (no-eol) (esc)
  [progress.fancy.bar.normal progress.fancy.topic| nested progress: ][progress.fancy.bar.normal progress.fancy.item|nest 1      ][progress.fancy.bar.background progress.fancy.item|                    ][progress.fancy.bar.background progress.fancy.count|  1/2 02s ]\r (no-eol) (esc)
  [progress.fancy.bar.normal progress.fancy.topic| nested progress: ][progress.fancy.bar.normal progress.fancy.item|nest 2                          ][progress.fancy.bar.normal progress.fancy.count|  2/2 01s ]\r (no-eol) (esc)
                                                              \r (no-eol) (esc)
  \r (no-eol) (esc)
  [progress.fancy.bar.normal progress.fancy.topic| progre][progress.fancy.bar.background progress.fancy.topic|ss test: ][progress.fancy.bar.background progress.fancy.item|loop 1                            ][progress.fancy.bar.background progress.fancy.count|  1/8 29s ]\r (no-eol) (esc)
  [progress.fancy.bar.normal progress.fancy.topic| progre][progress.fancy.bar.background progress.fancy.topic|ss test: ][progress.fancy.bar.background progress.fancy.item|loop 1                            ][progress.fancy.bar.background progress.fancy.count|  1/8 36s ]\r (no-eol) (esc)
  [progress.fancy.bar.normal progress.fancy.topic| nested progress: ][progress.fancy.bar.normal progress.fancy.item|nest 1      ][progress.fancy.bar.background progress.fancy.item|                    ][progress.fancy.bar.background progress.fancy.count|  1/2 02s ]\r (no-eol) (esc)
  [progress.fancy.bar.normal progress.fancy.topic| nested progress: ][progress.fancy.bar.normal progress.fancy.item|nest 2                          ][progress.fancy.bar.normal progress.fancy.count|  2/2 01s ]\r (no-eol) (esc)
                                                              \r (no-eol) (esc)
  \r (no-eol) (esc)
  [progress.fancy.bar.normal progress.fancy.topic| progress test:][progress.fancy.bar.background progress.fancy.topic| ][progress.fancy.bar.background progress.fancy.item|loop 2                            ][progress.fancy.bar.background progress.fancy.count|  2/8 25s ]\r (no-eol) (esc)
  [progress.fancy.bar.normal progress.fancy.topic| progress test:][progress.fancy.bar.background progress.fancy.topic| ][progress.fancy.bar.background progress.fancy.item|loop 2                            ][progress.fancy.bar.background progress.fancy.count|  2/8 28s ]\r (no-eol) (esc)
  [progress.fancy.bar.normal progress.fancy.topic| nested progress: ][progress.fancy.bar.normal progress.fancy.item|nest 1      ][progress.fancy.bar.background progress.fancy.item|                    ][progress.fancy.bar.background progress.fancy.count|  1/2 02s ]\r (no-eol) (esc)
  [progress.fancy.bar.normal progress.fancy.topic| nested progress: ][progress.fancy.bar.normal progress.fancy.item|nest 2                          ][progress.fancy.bar.normal progress.fancy.count|  2/2 01s ]\r (no-eol) (esc)
                                                              \r (no-eol) (esc)
  \r (no-eol) (esc)
  [progress.fancy.bar.normal progress.fancy.topic| progress test: ][progress.fancy.bar.normal progress.fancy.item|loop 3][progress.fancy.bar.background progress.fancy.item|                            ][progress.fancy.bar.background progress.fancy.count|  3/8 21s ]\r (no-eol) (esc)
  [progress.fancy.bar.normal progress.fancy.topic| progress test: ][progress.fancy.bar.normal progress.fancy.item|loop 3][progress.fancy.bar.background progress.fancy.item|                            ][progress.fancy.bar.background progress.fancy.count|  3/8 22s ]\r (no-eol) (esc)
  [progress.fancy.bar.normal progress.fancy.topic| nested progress: ][progress.fancy.bar.normal progress.fancy.item|nest 1      ][progress.fancy.bar.background progress.fancy.item|                    ][progress.fancy.bar.background progress.fancy.count|  1/2 02s ]\r (no-eol) (esc)
  [progress.fancy.bar.normal progress.fancy.topic| nested progress: ][progress.fancy.bar.normal progress.fancy.item|nest 2                          ][progress.fancy.bar.normal progress.fancy.count|  2/2 01s ]\r (no-eol) (esc)
                                                              \r (no-eol) (esc)
  \r (no-eol) (esc)
  [progress.fancy.bar.normal progress.fancy.topic| progress test: ][progress.fancy.bar.normal progress.fancy.item|loop 4        ][progress.fancy.bar.background progress.fancy.item|                    ][progress.fancy.bar.background progress.fancy.count|  4/8 17s ]\r (no-eol) (esc)
  [progress.fancy.bar.normal progress.fancy.topic| progress test: ][progress.fancy.bar.normal progress.fancy.item|loop 4        ][progress.fancy.bar.background progress.fancy.item|                    ][progress.fancy.bar.background progress.fancy.count|  4/8 18s ]\r (no-eol) (esc)
  [progress.fancy.bar.normal progress.fancy.topic| nested progress: ][progress.fancy.bar.normal progress.fancy.item|nest 1      ][progress.fancy.bar.background progress.fancy.item|                    ][progress.fancy.bar.background progress.fancy.count|  1/2 02s ]\r (no-eol) (esc)
  [progress.fancy.bar.normal progress.fancy.topic| nested progress: ][progress.fancy.bar.normal progress.fancy.item|nest 2                          ][progress.fancy.bar.normal progress.fancy.count|  2/2 01s ]\r (no-eol) (esc)
                                                              \r (no-eol) (esc)
  \r (no-eol) (esc)
  [progress.fancy.bar.normal progress.fancy.topic| progress test: ][progress.fancy.bar.normal progress.fancy.item|loop 5               ][progress.fancy.bar.background progress.fancy.item|             ][progress.fancy.bar.background progress.fancy.count|  5/8 12s ]\r (no-eol) (esc)
  [progress.fancy.bar.normal progress.fancy.topic| progress test: ][progress.fancy.bar.normal progress.fancy.item|loop 5               ][progress.fancy.bar.background progress.fancy.item|             ][progress.fancy.bar.background progress.fancy.count|  5/8 12s ]\r (no-eol) (esc)
  [progress.fancy.bar.normal progress.fancy.topic| nested prog][progress.fancy.bar.background progress.fancy.topic|ress: ][progress.fancy.bar.background progress.fancy.item|nest 1                          ][progress.fancy.bar.background progress.fancy.count|  1/5 05s ]\r (no-eol) (esc)
  [progress.fancy.bar.normal progress.fancy.topic| nested progress: ][progress.fancy.bar.normal progress.fancy.item|nest 2][progress.fancy.bar.background progress.fancy.item|                          ][progress.fancy.bar.background progress.fancy.count|  2/5 04s ]\r (no-eol) (esc)
  [progress.fancy.bar.normal progress.fancy.topic| nested progress: ][progress.fancy.bar.normal progress.fancy.item|nest 3            ][progress.fancy.bar.background progress.fancy.item|              ][progress.fancy.bar.background progress.fancy.count|  3/5 03s ]\r (no-eol) (esc)
  [progress.fancy.bar.normal progress.fancy.topic| nested progress: ][progress.fancy.bar.normal progress.fancy.item|nest 4                        ][progress.fancy.bar.background progress.fancy.item|  ][progress.fancy.bar.background progress.fancy.count|  4/5 02s ]\r (no-eol) (esc)
  [progress.fancy.bar.normal progress.fancy.topic| nested progress: ][progress.fancy.bar.normal progress.fancy.item|nest 5                          ][progress.fancy.bar.normal progress.fancy.count|  5/5 01s ]\r (no-eol) (esc)
                                                              \r (no-eol) (esc)
  \r (no-eol) (esc)
  [progress.fancy.bar.normal progress.fancy.topic| progress test: ][progress.fancy.bar.normal progress.fancy.item|loop 6                       ][progress.fancy.bar.background progress.fancy.item|     ][progress.fancy.bar.background progress.fancy.count|  6/8 10s ]\r (no-eol) (esc)
  [progress.fancy.bar.normal progress.fancy.topic| progress test: ][progress.fancy.bar.normal progress.fancy.item|loop 6                       ][progress.fancy.bar.background progress.fancy.item|     ][progress.fancy.bar.background progress.fancy.count|  6/8 10s ]\r (no-eol) (esc)
  [progress.fancy.bar.normal progress.fancy.topic| nested progress: ][progress.fancy.bar.normal progress.fancy.item|nest 1      ][progress.fancy.bar.background progress.fancy.item|                    ][progress.fancy.bar.background progress.fancy.count|  1/2 02s ]\r (no-eol) (esc)
  [progress.fancy.bar.normal progress.fancy.topic| nested progress: ][progress.fancy.bar.normal progress.fancy.item|nest 2                          ][progress.fancy.bar.normal progress.fancy.count|  2/2 01s ]\r (no-eol) (esc)
                                                              \r (no-eol) (esc)
  \r (no-eol) (esc)
  [progress.fancy.bar.normal progress.fancy.topic| progress test: ][progress.fancy.bar.normal progress.fancy.item|loop 7                            ][progress.fancy.bar.normal progress.fancy.count|  ][progress.fancy.bar.background progress.fancy.count|7/8 05s ]\r (no-eol) (esc)
  [progress.fancy.bar.normal progress.fancy.topic| progress test: ][progress.fancy.bar.normal progress.fancy.item|loop 7                            ][progress.fancy.bar.normal progress.fancy.count|  ][progress.fancy.bar.background progress.fancy.count|7/8 05s ]\r (no-eol) (esc)
  [progress.fancy.bar.normal progress.fancy.topic| nested progress: ][progress.fancy.bar.normal progress.fancy.item|nest 1      ][progress.fancy.bar.background progress.fancy.item|                    ][progress.fancy.bar.background progress.fancy.count|  1/2 02s ]\r (no-eol) (esc)
  [progress.fancy.bar.normal progress.fancy.topic| nested progress: ][progress.fancy.bar.normal progress.fancy.item|nest 2                          ][progress.fancy.bar.normal progress.fancy.count|  2/2 01s ]\r (no-eol) (esc)
                                                              \r (no-eol) (esc)
  \r (no-eol) (esc)
  [progress.fancy.bar.normal progress.fancy.topic| progress test: ][progress.fancy.bar.normal progress.fancy.item|loop 8                            ][progress.fancy.bar.normal progress.fancy.count|  8/8 01s ]\r (no-eol) (esc)
  [progress.fancy.bar.normal progress.fancy.topic| progress test: ][progress.fancy.bar.normal progress.fancy.item|loop 8                            ][progress.fancy.bar.normal progress.fancy.count|  8/8 01s ]\r (no-eol) (esc)
  [progress.fancy.bar.normal progress.fancy.topic| nested progress: ][progress.fancy.bar.normal progress.fancy.item|nest 1      ][progress.fancy.bar.background progress.fancy.item|                    ][progress.fancy.bar.background progress.fancy.count|  1/2 02s ]\r (no-eol) (esc)
  [progress.fancy.bar.normal progress.fancy.topic| nested progress: ][progress.fancy.bar.normal progress.fancy.item|nest 2                          ][progress.fancy.bar.normal progress.fancy.count|  2/2 01s ]\r (no-eol) (esc)
                                                              \r (no-eol) (esc)
  \r (no-eol) (esc)
                                                              \r (no-eol) (esc)

test format options
  $ hg progresstest --config progress.format='number item-3 bar' 4 4
  \r (no-eol) (esc)
  [progress.fancy.bar.normal progress.fancy.topic| progress test:][progress.fancy.bar.background progress.fancy.topic| ][progress.fancy.bar.background progress.fancy.item|loop 1                            ][progress.fancy.bar.background progress.fancy.count|  1/4 04s ]\r (no-eol) (esc)
  [progress.fancy.bar.normal progress.fancy.topic| progress test: ][progress.fancy.bar.normal progress.fancy.item|loop 2        ][progress.fancy.bar.background progress.fancy.item|                    ][progress.fancy.bar.background progress.fancy.count|  2/4 03s ]\r (no-eol) (esc)
  [progress.fancy.bar.normal progress.fancy.topic| progress test: ][progress.fancy.bar.normal progress.fancy.item|loop 3                       ][progress.fancy.bar.background progress.fancy.item|     ][progress.fancy.bar.background progress.fancy.count|  3/4 02s ]\r (no-eol) (esc)
  [progress.fancy.bar.normal progress.fancy.topic| progress test: ][progress.fancy.bar.normal progress.fancy.item|loop 4                            ][progress.fancy.bar.normal progress.fancy.count|  4/4 01s ]\r (no-eol) (esc)
                                                              \r (no-eol) (esc)

test format options and indeterminate progress
  $ hg progresstest --config progress.format='number item bar' -- 4 -1
  \r (no-eol) (esc)
  [progress.fancy.bar.background progress.fancy.topic| progress test: ][progress.fancy.bar.background progress.fancy.item|loop][progress.fancy.bar.indeterminate progress.fancy.item| 1        ][progress.fancy.bar.background progress.fancy.item|                          ][progress.fancy.bar.background progress.fancy.count|  1 ]\r (no-eol) (esc)
  [progress.fancy.bar.background progress.fancy.topic| progress test: ][progress.fancy.bar.background progress.fancy.item|loop 2                  ][progress.fancy.bar.indeterminate progress.fancy.item|          ][progress.fancy.bar.background progress.fancy.item|      ][progress.fancy.bar.background progress.fancy.count|  2 ]\r (no-eol) (esc)
  [progress.fancy.bar.background progress.fancy.topic| progress test: ][progress.fancy.bar.background progress.fancy.item|loop 3                  ][progress.fancy.bar.indeterminate progress.fancy.item|          ][progress.fancy.bar.background progress.fancy.item|      ][progress.fancy.bar.background progress.fancy.count|  3 ]\r (no-eol) (esc)
  [progress.fancy.bar.background progress.fancy.topic| progress test: ][progress.fancy.bar.background progress.fancy.item|loop][progress.fancy.bar.indeterminate progress.fancy.item| 4        ][progress.fancy.bar.background progress.fancy.item|                          ][progress.fancy.bar.background progress.fancy.count|  4 ]\r (no-eol) (esc)
                                                              \r (no-eol) (esc)

test count over total
  $ hg progresstest 6 4
  \r (no-eol) (esc)
  [progress.fancy.bar.normal progress.fancy.topic| progress test:][progress.fancy.bar.background progress.fancy.topic| ][progress.fancy.bar.background progress.fancy.item|loop 1                            ][progress.fancy.bar.background progress.fancy.count|  1/4 04s ]\r (no-eol) (esc)
  [progress.fancy.bar.normal progress.fancy.topic| progress test: ][progress.fancy.bar.normal progress.fancy.item|loop 2        ][progress.fancy.bar.background progress.fancy.item|                    ][progress.fancy.bar.background progress.fancy.count|  2/4 03s ]\r (no-eol) (esc)
  [progress.fancy.bar.normal progress.fancy.topic| progress test: ][progress.fancy.bar.normal progress.fancy.item|loop 3                       ][progress.fancy.bar.background progress.fancy.item|     ][progress.fancy.bar.background progress.fancy.count|  3/4 02s ]\r (no-eol) (esc)
  [progress.fancy.bar.normal progress.fancy.topic| progress test: ][progress.fancy.bar.normal progress.fancy.item|loop 4                            ][progress.fancy.bar.normal progress.fancy.count|  4/4 01s ]\r (no-eol) (esc)
  [progress.fancy.bar.normal progress.fancy.topic| progress test: ][progress.fancy.bar.normal progress.fancy.item|loop 5                               ][progress.fancy.bar.normal progress.fancy.count|  5/4  ]\r (no-eol) (esc)
  [progress.fancy.bar.normal progress.fancy.topic| progress test: ][progress.fancy.bar.normal progress.fancy.item|loop 6                               ][progress.fancy.bar.normal progress.fancy.count|  6/4  ]\r (no-eol) (esc)
                                                              \r (no-eol) (esc)

test rendering with bytes
  $ hg bytesprogresstest
  \r (no-eol) (esc)
  [progress.fancy.bar.background progress.fancy.topic| bytes progress test: ][progress.fancy.bar.background progress.fancy.item|10 bytes     ][progress.fancy.bar.background progress.fancy.count|  10 bytes/1.03 GB 3y28w ]\r (no-eol) (esc)
  [progress.fancy.bar.background progress.fancy.topic| bytes progress test: ][progress.fancy.bar.background progress.fancy.item|250 bytes  ][progress.fancy.bar.background progress.fancy.count|  250 bytes/1.03 GB 14w05d ]\r (no-eol) (esc)
  [progress.fancy.bar.background progress.fancy.topic| bytes progress test: ][progress.fancy.bar.background progress.fancy.item|999 bytes   ][progress.fancy.bar.background progress.fancy.count|  999 bytes/1.03 GB 5w04d ]\r (no-eol) (esc)
  [progress.fancy.bar.background progress.fancy.topic| bytes progress test: ][progress.fancy.bar.background progress.fancy.item|1000 bytes ][progress.fancy.bar.background progress.fancy.count|  1000 bytes/1.03 GB 7w03d ]\r (no-eol) (esc)
  [progress.fancy.bar.background progress.fancy.topic| bytes progress test: ][progress.fancy.bar.background progress.fancy.item|1024 bytes    ][progress.fancy.bar.background progress.fancy.count|  1.00 KB/1.03 GB 9w00d ]\r (no-eol) (esc)
  [progress.fancy.bar.background progress.fancy.topic| bytes progress test: ][progress.fancy.bar.background progress.fancy.item|22000 bytes   ][progress.fancy.bar.background progress.fancy.count|  21.5 KB/1.03 GB 3d13h ]\r (no-eol) (esc)
  [progress.fancy.bar.background progress.fancy.topic| bytes progress test: ][progress.fancy.bar.background progress.fancy.item|1048576 bytes ][progress.fancy.bar.background progress.fancy.count|  1.00 MB/1.03 GB 2h04m ]\r (no-eol) (esc)
  [progress.fancy.bar.background progress.fancy.topic| bytes progress test: ][progress.fancy.bar.background progress.fancy.item|1474560 bytes ][progress.fancy.bar.background progress.fancy.count|  1.41 MB/1.03 GB 1h41m ]\r (no-eol) (esc)
  [progress.fancy.bar.normal progress.fancy.topic| bytes][progress.fancy.bar.background progress.fancy.topic| progress test: ][progress.fancy.bar.background progress.fancy.item|123456789 byte][progress.fancy.bar.background progress.fancy.count|   118 MB/1.03 GB 1m13s ]\r (no-eol) (esc)
  [progress.fancy.bar.normal progress.fancy.topic| bytes progress test: ][progress.fancy.bar.normal progress.fancy.item|5555555][progress.fancy.bar.background progress.fancy.item|55 bytes ][progress.fancy.bar.background progress.fancy.count|   530 MB/1.03 GB 11s ]\r (no-eol) (esc)
  [progress.fancy.bar.normal progress.fancy.topic| bytes progress test: ][progress.fancy.bar.normal progress.fancy.item|1000000000 bytes][progress.fancy.bar.normal progress.fancy.count|   954 MB/1.03 G][progress.fancy.bar.background progress.fancy.count|B 02s ]\r (no-eol) (esc)
  [progress.fancy.bar.normal progress.fancy.topic| bytes progress test: ][progress.fancy.bar.normal progress.fancy.item|1111111111 bytes][progress.fancy.bar.normal progress.fancy.count|  1.03 GB/1.03 GB 01s ]\r (no-eol) (esc)
                                                              \r (no-eol) (esc)
test immediate completion
  $ hg progresstest 0 0

test unicode topic
  $ hg --encoding utf-8 progresstest 4 4 --unicode --config progress.format='topic number'
  \r (no-eol) (esc)
  [progress.fancy.bar.normal progress.fancy.topic| \xe3\x81\x82\xe3\x81\x84\xe3\x81\x86\xe3\x81\x88: ][progress.fancy.bar.normal progress.fancy.item|\xe3\x81\x82\xe3\x81\x84][progress.fancy.bar.background progress.fancy.item|\xe3\x81\x86                                 ][progress.fancy.bar.background progress.fancy.count|  1/4 04s ]\r (no-eol) (esc)
  [progress.fancy.bar.normal progress.fancy.topic| \xe3\x81\x82\xe3\x81\x84\xe3\x81\x86\xe3\x81\x88: ][progress.fancy.bar.normal progress.fancy.item|\xe3\x81\x82\xe3\x81\x84\xe3\x81\x86\xe3\x81\x88           ][progress.fancy.bar.background progress.fancy.item|                    ][progress.fancy.bar.background progress.fancy.count|  2/4 03s ]\r (no-eol) (esc)
  [progress.fancy.bar.normal progress.fancy.topic| \xe3\x81\x82\xe3\x81\x84\xe3\x81\x86\xe3\x81\x88: ][progress.fancy.bar.normal progress.fancy.item|\xe3\x81\x82\xe3\x81\x84                              ][progress.fancy.bar.background progress.fancy.item|     ][progress.fancy.bar.background progress.fancy.count|  3/4 02s ]\r (no-eol) (esc)
  [progress.fancy.bar.normal progress.fancy.topic| \xe3\x81\x82\xe3\x81\x84\xe3\x81\x86\xe3\x81\x88: ][progress.fancy.bar.normal progress.fancy.item|\xe3\x81\x82\xe3\x81\x84\xe3\x81\x86                                 ][progress.fancy.bar.normal progress.fancy.count|  4/4 01s ]\r (no-eol) (esc)
                                                              \r (no-eol) (esc)

test line trimming when progress topic contains multi-byte characters
  $ hg --encoding utf-8 progresstest 12 12 --unicode --config progress.width=12 --config progress.format='topic number'
  \r (no-eol) (esc)
  [progress.fancy.bar.normal progress.fancy.topic| ][progress.fancy.bar.background progress.fancy.topic|\xe3\x81\x82\xe3\x81\x84\xe3\x81\x86\xe3\x81\x88: ][progress.fancy.bar.background progress.fancy.count| ]\r (no-eol) (esc)
  [progress.fancy.bar.normal progress.fancy.topic| ][progress.fancy.bar.background progress.fancy.topic|\xe3\x81\x82\xe3\x81\x84\xe3\x81\x86\xe3\x81\x88: ][progress.fancy.bar.background progress.fancy.count| ]\r (no-eol) (esc)
  [progress.fancy.bar.normal progress.fancy.topic| \xe3\x81\x82][progress.fancy.bar.background progress.fancy.topic|\xe3\x81\x84\xe3\x81\x86\xe3\x81\x88: ][progress.fancy.bar.background progress.fancy.count| ]\r (no-eol) (esc)
  [progress.fancy.bar.normal progress.fancy.topic| \xe3\x81\x82][progress.fancy.bar.background progress.fancy.topic|\xe3\x81\x84\xe3\x81\x86\xe3\x81\x88: ][progress.fancy.bar.background progress.fancy.count| ]\r (no-eol) (esc)
  [progress.fancy.bar.normal progress.fancy.topic| \xe3\x81\x82\xe3\x81\x84][progress.fancy.bar.background progress.fancy.topic|\xe3\x81\x86\xe3\x81\x88: ][progress.fancy.bar.background progress.fancy.count| ]\r (no-eol) (esc)
  [progress.fancy.bar.normal progress.fancy.topic| \xe3\x81\x82\xe3\x81\x84][progress.fancy.bar.background progress.fancy.topic|\xe3\x81\x86\xe3\x81\x88: ][progress.fancy.bar.background progress.fancy.count| ]\r (no-eol) (esc)
  [progress.fancy.bar.normal progress.fancy.topic| \xe3\x81\x82\xe3\x81\x84\xe3\x81\x86][progress.fancy.bar.background progress.fancy.topic|\xe3\x81\x88: ][progress.fancy.bar.background progress.fancy.count| ]\r (no-eol) (esc)
  [progress.fancy.bar.normal progress.fancy.topic| \xe3\x81\x82\xe3\x81\x84\xe3\x81\x86][progress.fancy.bar.background progress.fancy.topic|\xe3\x81\x88: ][progress.fancy.bar.background progress.fancy.count| ]\r (no-eol) (esc)
  [progress.fancy.bar.normal progress.fancy.topic| \xe3\x81\x82\xe3\x81\x84\xe3\x81\x86\xe3\x81\x88][progress.fancy.bar.background progress.fancy.topic|: ][progress.fancy.bar.background progress.fancy.count| ]\r (no-eol) (esc)
  [progress.fancy.bar.normal progress.fancy.topic| \xe3\x81\x82\xe3\x81\x84\xe3\x81\x86\xe3\x81\x88:][progress.fancy.bar.background progress.fancy.topic| ][progress.fancy.bar.background progress.fancy.count| ]\r (no-eol) (esc)
  [progress.fancy.bar.normal progress.fancy.topic| \xe3\x81\x82\xe3\x81\x84\xe3\x81\x86\xe3\x81\x88: ][progress.fancy.bar.background progress.fancy.count| ]\r (no-eol) (esc)
  [progress.fancy.bar.normal progress.fancy.topic| \xe3\x81\x82\xe3\x81\x84\xe3\x81\x86\xe3\x81\x88: ][progress.fancy.bar.normal progress.fancy.count| ]\r (no-eol) (esc)
              \r (no-eol) (esc)

test calculation of bar width when progress topic contains multi-byte characters
  $ hg --encoding utf-8 progresstest 4 4 --unicode --config progress.width=21 --config progress.format='topic bar'
  \r (no-eol) (esc)
  [progress.fancy.bar.normal progress.fancy.topic| \xe3\x81\x82\xe3\x81\x84][progress.fancy.bar.background progress.fancy.topic|\xe3\x81\x86\xe3\x81\x88: ][progress.fancy.bar.background progress.fancy.count|  1/4 04s ]\r (no-eol) (esc)
  [progress.fancy.bar.normal progress.fancy.topic| \xe3\x81\x82\xe3\x81\x84\xe3\x81\x86\xe3\x81\x88:][progress.fancy.bar.background progress.fancy.topic| ][progress.fancy.bar.background progress.fancy.count|  2/4 03s ]\r (no-eol) (esc)
  [progress.fancy.bar.normal progress.fancy.topic| \xe3\x81\x82\xe3\x81\x84\xe3\x81\x86\xe3\x81\x88: ][progress.fancy.bar.normal progress.fancy.count|  3/][progress.fancy.bar.background progress.fancy.count|4 02s ]\r (no-eol) (esc)
  [progress.fancy.bar.normal progress.fancy.topic| \xe3\x81\x82\xe3\x81\x84\xe3\x81\x86\xe3\x81\x88: ][progress.fancy.bar.normal progress.fancy.count|  4/4 01s ]\r (no-eol) (esc)
                       \r (no-eol) (esc)

test trimming progress items with they contain multi-byte characters
  $ hg --encoding utf-8 progresstest 4 4 --unicode --config progress.format='item+6'
  \r (no-eol) (esc)
  [progress.fancy.bar.normal progress.fancy.topic| \xe3\x81\x82\xe3\x81\x84\xe3\x81\x86\xe3\x81\x88: ][progress.fancy.bar.normal progress.fancy.item|\xe3\x81\x82\xe3\x81\x84][progress.fancy.bar.background progress.fancy.item|\xe3\x81\x86                                 ][progress.fancy.bar.background progress.fancy.count|  1/4 04s ]\r (no-eol) (esc)
  [progress.fancy.bar.normal progress.fancy.topic| \xe3\x81\x82\xe3\x81\x84\xe3\x81\x86\xe3\x81\x88: ][progress.fancy.bar.normal progress.fancy.item|\xe3\x81\x82\xe3\x81\x84\xe3\x81\x86\xe3\x81\x88           ][progress.fancy.bar.background progress.fancy.item|                    ][progress.fancy.bar.background progress.fancy.count|  2/4 03s ]\r (no-eol) (esc)
  [progress.fancy.bar.normal progress.fancy.topic| \xe3\x81\x82\xe3\x81\x84\xe3\x81\x86\xe3\x81\x88: ][progress.fancy.bar.normal progress.fancy.item|\xe3\x81\x82\xe3\x81\x84                              ][progress.fancy.bar.background progress.fancy.item|     ][progress.fancy.bar.background progress.fancy.count|  3/4 02s ]\r (no-eol) (esc)
  [progress.fancy.bar.normal progress.fancy.topic| \xe3\x81\x82\xe3\x81\x84\xe3\x81\x86\xe3\x81\x88: ][progress.fancy.bar.normal progress.fancy.item|\xe3\x81\x82\xe3\x81\x84\xe3\x81\x86                                 ][progress.fancy.bar.normal progress.fancy.count|  4/4 01s ]\r (no-eol) (esc)
                                                              \r (no-eol) (esc)
  $ hg --encoding utf-8 progresstest 4 4 --unicode --config progress.format='item-6'
  \r (no-eol) (esc)
  [progress.fancy.bar.normal progress.fancy.topic| \xe3\x81\x82\xe3\x81\x84\xe3\x81\x86\xe3\x81\x88: ][progress.fancy.bar.normal progress.fancy.item|\xe3\x81\x82\xe3\x81\x84][progress.fancy.bar.background progress.fancy.item|\xe3\x81\x86                                 ][progress.fancy.bar.background progress.fancy.count|  1/4 04s ]\r (no-eol) (esc)
  [progress.fancy.bar.normal progress.fancy.topic| \xe3\x81\x82\xe3\x81\x84\xe3\x81\x86\xe3\x81\x88: ][progress.fancy.bar.normal progress.fancy.item|\xe3\x81\x82\xe3\x81\x84\xe3\x81\x86\xe3\x81\x88           ][progress.fancy.bar.background progress.fancy.item|                    ][progress.fancy.bar.background progress.fancy.count|  2/4 03s ]\r (no-eol) (esc)
  [progress.fancy.bar.normal progress.fancy.topic| \xe3\x81\x82\xe3\x81\x84\xe3\x81\x86\xe3\x81\x88: ][progress.fancy.bar.normal progress.fancy.item|\xe3\x81\x82\xe3\x81\x84                              ][progress.fancy.bar.background progress.fancy.item|     ][progress.fancy.bar.background progress.fancy.count|  3/4 02s ]\r (no-eol) (esc)
  [progress.fancy.bar.normal progress.fancy.topic| \xe3\x81\x82\xe3\x81\x84\xe3\x81\x86\xe3\x81\x88: ][progress.fancy.bar.normal progress.fancy.item|\xe3\x81\x82\xe3\x81\x84\xe3\x81\x86                                 ][progress.fancy.bar.normal progress.fancy.count|  4/4 01s ]\r (no-eol) (esc)
                                                              \r (no-eol) (esc)
