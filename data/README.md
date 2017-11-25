# Data

Data from MQPA and from the authors go in this directory.

**TODO** add directory mapping/naming expected by the code.

All the data in this directory is gitignore'd because of copyright issues.

## Appendix A

The following filepaths are the subset of articles from the MPQA dataset that
the original paper authors used in their paper and included in the dataset
provided to the replicators.

```
docs/20011024/21.53.09-11428
docs/20011125/21.01.04-6923
docs/20011208/20.31.54-28680
docs/20011210/20.28.15-21486
docs/20020106/20.26.14-23928
docs/20020306/20.49.12-24038
docs/20020318/20.33.16-3417
docs/20020507/17.55.10-20068
docs/20020507/22.11.06-28210
docs/non_fbis/04.22.14-2532
docs/non_fbis/04.51.05-27505
docs/non_fbis/05.20.33-11163
docs/non_fbis/06.10.04-18139
docs/non_fbis/06.12.31-26764
docs/non_fbis/06.28.56-23638
docs/non_fbis/07.05.30-9348
docs/non_fbis/08.21.04-13527
docs/non_fbis/08.36.15-7509
docs/non_fbis/08.39.09-12713
docs/non_fbis/08.40.56-18707
docs/non_fbis/08.47.00-17401
docs/non_fbis/08.54.29-27700
docs/non_fbis/09.53.15-23595
docs/non_fbis/10.03.26-15373
docs/non_fbis/10.12.58-29108
docs/non_fbis/10.24.29-21670
docs/non_fbis/11.04.20-23621
docs/non_fbis/11.05.55-12013
docs/non_fbis/11.21.37-22256
docs/non_fbis/11.35.22-9439
docs/non_fbis/12.15.47-5091
docs/non_fbis/12.21.28-26118
docs/non_fbis/13.08.06-1812
docs/non_fbis/13.21.23-8227
docs/non_fbis/13.24.42-23228
docs/non_fbis/14.06.39-26143
docs/non_fbis/15.26.56-25086
docs/non_fbis/15.36.10-18917
docs/non_fbis/15.59.08-16874
docs/non_fbis/16.01.44-19040
docs/non_fbis/16.03.54-17435
docs/temp_fbis/20.13.06-23605
docs/temp_fbis/20.20.10-3414
docs/temp_fbis/20.42.47-22260
docs/temp_fbis/20.45.06-5529
docs/temp_fbis/20.46.39-9348
docs/temp_fbis/20.46.47-22286
docs/temp_fbis/20.46.58-22510
docs/temp_fbis/20.55.24-19278
docs/temp_fbis/20.57.35-19171
docs/temp_fbis/20.58.47-19000
docs/temp_fbis/21.31.45-20536
docs/temp_fbis/21.37.46-9337
docs/temp_fbis/21.39.02-16166
```

For reference, the filepaths were obtained by invoking
```
$ find data-from-authors/mpqa_data/* | sed 's/.json//' | cut -f 3 -d / | xargs -I % grep % database.mpqa.3.0/doclist | sort | sed 's/^/docs\//'
```
