# ClearZip
Use it to clear your project and create backup archives

To build .exe call "python setup.py py2exe". To do it you need a py2exe package. 
Edit .bat file and use it to manage clearzip.py.
But if you want you can call python script directly:

python clearzip.py -t trash_list_file.lst -m archive_mode dir_to_backup

Available arcive modes are: zip, tar, bztar, gztar, 7z (if you have 7zip installed)
To use 7zip archivator change path to 7z.exe in clearzip.py

Example of trash file you can see in xeTrash.lst
