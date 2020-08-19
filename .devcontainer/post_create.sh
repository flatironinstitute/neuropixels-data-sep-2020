# #!/bin/bash

# set -ex

mkdir -p /data/kachery-storage
mkdir -p /data/kachery-p2p-config

pip install -e .

cat <<EOT >> ~/.bashrc
export PATH=/home/vscode/.local/bin:$PATH

alias gs="git status"
alias gpl="git pull"
alias gps="git push"
alias gpst="git push && git push --tags"
alias gc="git commit"
alias ga="git add -u"
EOT
