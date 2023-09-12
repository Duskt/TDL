stop-tmux:
	tmux kill-session -t tdl-server;
	tmux kill-session -t tdl-client;

run-tmux:
	tmux new-session -d -s tdl-server 'cd server; python3 app.py';
	tmux new-session -d -s tdl-client 'cd client; yarn dev';


setup:
	./utils/set-ip
	./utils/inherit-workspace
	./utils/export-types

build: setup run-tmux
