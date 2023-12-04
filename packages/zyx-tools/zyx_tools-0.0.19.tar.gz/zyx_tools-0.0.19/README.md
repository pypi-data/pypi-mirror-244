# usage

# install

```
pip install zyx_tools

```

# logprint

```
from zyx_tools import OtherTool

```

## init logprint

must in main start

```
OtherTool.init_log()
```

## start print log file

```
tail = logprint.Tail(log_name,"build_log")
tail.daemon = True
tail.start()


```

## close print log thread

```
tail.stop()
```
