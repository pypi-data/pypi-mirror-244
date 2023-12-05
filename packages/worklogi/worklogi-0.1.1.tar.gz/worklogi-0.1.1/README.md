# How to install:

Just run `pip install worklogi`.

# How to use:

You can combine this with [m](https://github.com/jmlopez-rod/m) and git hooks to 
automatically log your work.

You can create the following hooks:

## `post-checkout`


```bash
#!/bin/fish

echo checkout | worklogi add-entry (m git branch) > /dev/null
```

## `post-commit`


```bash
#!/bin/fish

git log -1 --oneline --format=%s | sed 's/^.*: //' | worklogi add-entry (m git branch)
```

## How to browse:

Just run `worklogi browse`
