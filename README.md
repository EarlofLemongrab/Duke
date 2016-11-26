An implementation of the smart thread pooling TCP server for distributed file storage.

Uses Directory Server, Lock Server, and Replication Servers (Masters) each with multiple redundant Replication Slaves.
An effort was made to ensure complete modularity of TcpServer.py, allowing for additional server types to be added with ease.


## Start all file servers in background
    >sh start.sh

## Begin client proxy (in separate ssh session)
    >python new_client.py
