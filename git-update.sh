#!/bin/bash

paths="$@"

git_current_branch () {
  local ref=$(git symbolic-ref --quiet HEAD 2> /dev/null)
  local ret=$?
  if [[ $ret != 0 ]]; then
    [[ $ret == 128 ]] && return
    ref=$(git rev-parse --short HEAD 2> /dev/null) || return
  fi
  echo ${ref#refs/heads/}
}

update () {
  cd "$1"

  local diffs=$(git diff --shortstat)

  printf "\033[94;1m%s\033[0m " "$1"

  if [ -z "$diffs" ]; then

    git fetch --all --prune --jobs=10 > /dev/null

    diffs=$(git diff --shortstat origin/"$(git_current_branch)")

    if [ -z "$diffs" ]; then
      printf "%s\n" up-to-date
    else
      git reset --hard origin/"$(git_current_branch)" > /dev/null
      printf "\033[92m%s\033[0m\n" updated
    fi

  else
    printf "\033[91m%s\033[0m\n" has-diffs
  fi
}

if [ -z "$paths" ]; then
  paths=$(ghq list -p)
fi

for path in ${paths[@]}; do
  update "$path"
done
