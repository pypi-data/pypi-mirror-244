# decide-analysis

This project is a python package for analyzing data from the [decide operant control system ](https://github.com/melizalab/decide) stored on [django-decide-host](https://github.com/melizalab/django-decide-host).

This is a work in progress. The only functionality in place right now is a
script to retrieve trials from the host and save them in csv format.

Example:

``` shell
decide-get-trials -r http://pholia.lab:4000/decide/api/ \
        --fields subject,time,trial,result,correct,response,stimulus,correction \
        --from-date 2022-03-01 --to-date 2022-03-09 -k experiment=2ac-config-segmented10 C14
```

