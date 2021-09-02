#!/usr/bin/env bash
# This is the init file for local development of the opennem client library
#
# Steps:
# 1. check if already running in venv and initialized
# 2. if no venv then install deps
# 3. link the venv
# 4. init PYTHONPATH
#
set -eo pipefail

unset _envdir
unset _python_version
unset RED
unset GREEN
unset RESET
unset BOLD

_envdir=".venv"
_python_version=3.9

RED=`tput setaf 1`
GREEN=`tput setaf 2`
RESET=`tput sgr0`
BOLD=$(tput bold)

command_exists() {
	command -v "$@" >/dev/null 2>&1
}

fmt_underline() {
  printf '\033[4m%s\033[24m\n' "$*"
}

fmt_code() {
  # shellcheck disable=SC2016 # backtic in single-quote
  printf '`\033[38;5;247m%s%s`\n' "$*" "$RESET"
}

_logerror() {
  printf '%s[ERROR]: %s%s\n' "$BOLD$RED" "$*" "$RESET" >&2
}

_loggreen() {
  printf '%s[ERROR]: %s%s\n' "$BOLD$GREEN" "$*" "$RESET" >&2
}

_log() {
    printf "%s[INFO ]: %s%s\n" "$BOLD$GREEN" "$*" "$RESET" >&1
}

_check_poetry() {
  local _poetry_path=`which poetry`

  if ! [ -x "$(command -v $_poetry_path)" ]; then
    _logerror "Require poetry"
    exit -1
  else
    _log "Have poetry ... well done."
  fi
}

_activate_env() {
  if ! [ -x "$(command -v poetry)" ]; then
    echo "Error: Poetry not installed. Trying pip." >&2

    if [ -x "$_envdir/bin/activate "]; then
      echo "Sourcing venv."
      source $_envdir/bin/activate
    fi
  fi
}

_check_poetry_env() {
  local _POETRY_ENV_PATH=`poetry env info -p`

  if [ ! $? -eq 0 ]
  then
    echo "No poetry environments listed"
    exit -1
  fi
}

_get_poetry_env() {
  local _poetry_env_path=`poetry env info -p >&2 `
  echo "$_poetry_env_path"
}

_poetry_gen_and_link_venv() {
  # creates the poetry environment if it doesnt exist
  local _poetry_env_path=$(_get_poetry_env)

  if [ -z $_poetry_env_path ]; then
    poetry install >&2
  fi

  _poetry_env_path = $(_get_poetry_env)

  ln -s $_poetry_env_path $_envdir

  _log "Created virtual env at $_envdir"
}


_link_module_path() {
  # links the local folder into python path
  if [ -d "$PWD/.venv/lib/python$_python_version/site-packages"]; then
    if [ ! -f "$PWD/.venv/lib/python$_python_version/site-packages/local.pth" ]; then
      pwd > .venv/lib/python3.9/site-packages/local.pth
      _log "Linked local module to PYTHONPATH using site-packages path"
    fi
  else
    _logerror "Error no local python env"
  fi
}

# welcome
_loggreen "Setting up venv in $_envdir with python version $_python_version"

# 0. Check poetry is installed
_check_poetry

# 1. Check if virtualenv is activated
if [ -z "$VIRTUAL_ENV" ]; then
  _log "Running and setup in $VIRTUAL_ENV"
  python -V
  exit 1
else
  _logerror "Virtual Environment not found ... will initialize"
fi

# 2. check poetry env exists if not install and link
if [ -z $(_get_poetry_env) ]; then
  _log "No poetry env .. initializing"
  _poetry_gen_and_link_venv
else
  _loggreen "Found poetry end at $(_get_poetry_env)"
fi


# 3. Activate the venv if it exists
if [ -f "$PWD/$_envdir/bin/activate"]; then
  _activate_env
fi

# 4. link opennem to python path
_link_module_path
