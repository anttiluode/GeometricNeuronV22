# Mohan CNG calibration

Cell 1125 exists both as an author-used ASC file in `ido4848/FCI` and as a NeuroMorpho standardized CNG SWC. This gives a label-free recovery check.

```text
                              author copy       CNG copy
nodes                         209               213
leaves                        110               110
bifurcations                   94               102
length                      20633.0035        20624.7748
area                        86647.7316        86844.3418
max root-tip path            1230.5875         1229.8191
G1                              .9487561           .9487681
G2                              .5958832           .5956722
G3                             1.3004203          1.3001073
```

The standardized file is not topologically identical, but the frozen primary quantities are very stable: area differs by about 0.23%, path by 0.06%, and each operator feature by less than 0.00032 absolute.

Recovery policy: for Mohan cells missing an exact author copy, the NeuroMorpho CNG representation is acceptable for the primary B2+G panel with explicit provenance. Do not treat its bifurcation count as necessarily identical to the author's original NeuroM count.

This compatibility decision was made before mapping FCI labels.
