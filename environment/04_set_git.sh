git config --global user.name "Aran"
git config --global user.email "aran4122@126.com"

git config --global alias.co checkout
git config --global alias.br branch
git config --global alias.ci commit
git config --global alias.st status
git config --global alias.last '!git log -1 HEAD | cat'
git config --global alias.lg "log --color --graph --pretty=format:'%Cred%h%Creset -%C(yellow)%d%Creset %s %Cgreen(%cr) %C(bold blue)<%an>%Creset' --abbrev-commit --"

git config --add oh-my-zsh.hide-dirty 1
git config --add oh-my-zsh.hide-status 1
