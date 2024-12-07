# Welcome to Fizer
Fizer is a script that allows you to transfer files between two devices or between a server and your device without needing an FTP or HTTP server. 
It also logs all server activities.



# Setup
```bash
pip install -r requirements.txt
```

# Usage

1.Start the Server:
  Open a terminal and navigate to your project directory. Run the server script:
  ```bash
  python .\server.py
 
  Enter EXIT if you want to shut down the server.
  Server is listening on port 9999...
  ```

 

2.Using the Client:
  Open another terminal and navigate to your project directory. Run the client script:
  ```bash
  python .\client.py
    Enter command (UPLOAD <filename> / DOWNLOAD <filename> / EXIT): UPLOAD client.py
    Uploading... 
    File client.py uploaded successfully.
    Enter command (UPLOAD <filename> / DOWNLOAD <filename> / EXIT): DOWNLOAD server.py
    Downloading... 
    File server.py downloaded successfully.
    Enter command (UPLOAD <filename> / DOWNLOAD <filename> / EXIT): exit
    Exiting...

```


# Example Session


```bash
> ls





Mode                 LastWriteTime         Length Name
----                 -------------         ------ ----
d-----         5/25/2024   9:37 PM                homework
-a----         5/26/2024  12:13 AM           2591 client.py
-a----         5/26/2024  12:20 AM              0 docs.md
-a----         5/26/2024  12:23 AM           3997 downloaded_server.py
-a----         5/26/2024  12:16 AM             17 requirements.txt
-a----         5/26/2024  12:13 AM           3997 server.py
-a----         5/26/2024  12:23 AM            132 server_log.txt

```

# Requirements
```bash
pip install -r requirements.txt

colorama==0.4.4

```
This ensures that all necessary libraries are installed for the scripts to run smoothly.


