# (Paste the script above, save with CTRL+O then CTRL+X)
chmod +x Ξ.invoke_shell.sh
./Ξ.invoke_shell.sh
#!/data/data/com.termux/files/usr/bin/bash

# Make sure all necessary scripts are executable
chmod +x xi_shell.sh reflect_pulse.sh toast_daemon.sh

# Launch background daemons
./reflect_pulse.sh &
./toast_daemon.sh &

# Brief pause for background init
sleep 1

# Invoke main symbolic shell
./xi_shell.sh
