start:
	podman build -t mailtracker .;
	podman run --name mailtracker -v app:/app -p 8050:8050 mailtracker
	
stop:
	podman stop mailtracker;

clean:
	podman rm mailtracker;
	podman rmi mailtracker

restart: stop clean start

copy:
	 podman cp mailtracker:demo_file.xlsx path/to/zielverzeichnis
