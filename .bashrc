# 1. Create the lockers
mkdir -p ~/Tools ~/Evidence ~/Logs ~/Scripts

# 2. Move the main tools
mv Storm-Breaker PhoneSploit-Pro X-osint android-sdk proot-distro ~/Tools/ 2>/dev/null

# 3. Move the legal and research data
mv dorks google_Dorks.txt title47_dorks.sh travis_ryle_dorks.txt travis trtext.txt ~/Evidence/ 2>/dev/null
mv ffnox_filings.html fidelity_filings.html fidelity_reports.html fidelity_rules.txt fidelity_trust.txt evidence_portal ~/Evidence/ 2>/dev/null

# 4. Move the coding scripts
mv app.py bot.py convert.py harvester.py optimize.sh scanner.py ~/Scripts/ 2>/dev/null

# 5. Move the logs and temp files
mv *.log *.json audit_log.txt yagooglesearch.py.log tunnel.log ~/Logs/ 2>/dev/null

# 6. Delete the "ghost" files and accidental downloads
rm -f "C.docx" "'tall nmap'" test.pdf downloads.pdf downloads.txt "jj.txt" "filetype:pdf" "cd \$HOME"
# --- [ Lawfully-Illegal Command Center ] ---

# Power Tools Aliases
alias harvest='python ~/harvester.py'
alias dork-audit='python3 ~/dorks/pagodo/pagodo.py -d lawfully-illegal.art -g ~/dorks/pagodo/dorks.txt -s -o -i 120 -x 300'
alias xos='cd ~/X-osint && python3 xosint.py'

# Interactive Dashboard (Requires tmux and btop)
alias center='tmux new-session -d -s CC "btop"; \
              tmux split-window -h "tail -f ~/dorks/pagodo/pagodo.py.log"; \
              tmux split-window -v "echo Welcome Travis. Ready for OSINT.; bash"; \
              tmux attach-session -t CC'

# Emergency Fixes
alias fix-node='unset PREFIX; source ~/.bashrc; export PREFIX=/data/data/com.termux/files/usr'
alias refresh='source ~/.bashrc'

# --- [ Environment & Fixes ] ---

# NVM Peacekeeper (Stops the PREFIX conflict)
export NVM_DIR="$HOME/.nvm"
alias nvm='unalias nvm; [ -s "$NVM_DIR/nvm.sh" ] && . "$NVM_DIR/nvm.sh"; nvm "$@"'

# Prompt Customization (Makes it look like a pro terminal)
PS1='\[\e[1;32m\][Travis@Termux] \[\e[1;34m\]\w \$ \[\e[0m\]'

# Fix for common Termux library paths
export LD_LIBRARY_PATH="$PREFIX/lib:$LD_LIBRARY_PATH"
[ -s "$NVM_DIR/bash_completion" ] && \. "$NVM_DIR/bash_completion"  # This loads nvm bash_completion
# Travis's Custom Shortcuts
alias storm='cd ~/Storm-Breaker && python3 st.py'
alias xosint='cd ~/X-osint && bash xosint.sh'
alias phone='cd ~/PhoneSploit-Pro && python3 main.py'
alias droid='cd ~/lawfullyillegal-droid'
alias cls='clear'
alias home='cd ~'
export GPG_TTY=$(tty)
alias gethosts='python ~/Scripts/host_parser.py'
