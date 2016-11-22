import sys
import config
import random
from TcpServer import TcpServer

class DirectoryServer(TcpServer):
    messages = {config.REQUEST_FILE_DETAILS}
    servers = [config.REP_SERVER + (x * (config.REP_SERVER_COPIES + 1)) for x in range(config.REP_SERVERS)]
    folders = {}

    # override request processing function
    def process_req(self, conn, request, vars):
        # requesting file details from directory
        print vars
        print "var0:" + vars[0]
        print "var1:" +vars[1]
        print "var2:" +vars[2]
        if request == config.REQUEST_FILE_DETAILS:
            #try:
                # add folder to directory listing if writing
                if vars[2] == 'WRITE':
                    # check if folder exists in directory listing
                    if vars[0] not in self.folders:
                        
                        # if not then assign folder to random server
                        random_server_port = random.choice(self.servers)
                        self.folders[vars[1]] = {'id' : self.hash_str(self.ip + str(random_server_port) + vars[1]), 'ip' : self.ip, 'port' : str(random_server_port), 'files' : [vars[0]]}
                
                # return directory id and location
                response = self.folders[vars[1]]
                print "resp is " + str(response)
                
                # check if file in directory
                if vars[0] in response['files']:
                    print "Find"
                    self.send_msg(conn, config.RETURN_FILE_DETAILS.format(response['id'], response['ip'], response['port']))
                    return
                else:
                    print "NOT FIND\n"
                    self.error(conn, "File not found.")
            
            #except KeyError:
                # return file not found if file_id key not in files dict
             #   self.error(conn, "File not found.")
                
def main():
    print "Directory Server started on " + str(config.DIR_SERVER)
    server = DirectoryServer(config.DIR_SERVER)
if __name__ == "__main__": main()
