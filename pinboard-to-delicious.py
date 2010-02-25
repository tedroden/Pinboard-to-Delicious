import getopt, sys, os
import urllib, urllib2, base64 
from xml.dom import minidom

pinboard_username = None
pinboard_password = None
delicious_username = None
delicious_password = None


class pb2del(object):
    pbu = None
    pbp = None
    du = None
    dp = None
    def __init__(self, pbu, pbp, du, dp):
        self.pbu, self.pbp, self.du, self.dp = pbu, pbp, du, dp

    def get_last_bookmark_time(self):
        try:
            f = open(os.path.expanduser("~/.p2b-last"), "r")
            data = f.read()
            f.close()
            return data
        except Exception, e:
            print e
            return None

    def get_new_pinboard_bookmarks(self):
        url = "https://api.pinboard.in/v1/posts/recent"
        
        last_bookmark_time = self.get_last_bookmark_time()

	request = urllib2.Request(url)
	auth_basic = base64.encodestring(self.pbu + ':' + self.pbp)[:-1]
	request.add_header('Authorization', 'Basic %s' % auth_basic)

	# open the connection
	response = urllib2.urlopen(request)
        data = response.read()

        dom = minidom.parseString(data)

        bookmarks = []
        for node in dom.getElementsByTagName('post'):

            if node.attributes.get('time').value > last_bookmark_time:
                obj = {'url': node.attributes.get('href').value,
                       'dt': node.attributes.get('time').value,
                       'description': node.attributes.get('description').value}
                
                if node.attributes.get('extended'):
                    obj['extended'] = node.attributes.get('extended').value

                if node.attributes.get('tag'):
                    obj['tags'] = node.attributes.get('tag').value


                bookmarks.append(obj)
        return bookmarks
        
    def put_bookmarks_on_delicious(self, bookmarks):
        if not len(bookmarks): 
            return
        for x in bookmarks:
            url = "https://api.del.icio.us/v1/posts/add?"
            url += urllib.urlencode(x)
            # print url
            # exit()
            request = urllib2.Request(url)
            auth_basic = base64.encodestring(self.du + ':' + self.dp)[:-1]
            request.add_header('Authorization', 'Basic %s' % auth_basic)
            
            # open the connection
            response = urllib2.urlopen(request)
            data = response.read()
            
    def run_export(self):
        pb_books = self.get_new_pinboard_bookmarks()
        self.put_bookmarks_on_delicious(pb_books)

        if len(pb_books):
            print "Saved %d new bookmarks" % len(pb_books)
            f = open(os.path.expanduser("~/.p2b-last"), "w")
            f.write(pb_books[0]['dt'])
            f.close()
        else:
            print "Nothing to update."
    
if __name__ == "__main__":
    available_arguments = ["pb_user=", "pb_pass=", "del_user=", "del_pass="]

    try:
        opts, args = getopt.getopt(sys.argv[1:], "", available_arguments)
    except getopt.GetoptError, err:
        # print help information and exit:
        print str(err) # will print something like "option -a not recognized"
        print "HERE"
        sys.exit(2)

    for o, a in opts:
        if o in "--pb_user":
            pinboard_username = a
        elif o in "--pb_pass":
            pinboard_password = a
        elif o in "--del_user":
            delicious_username = a
        elif o in "--del_pass":
            delicious_password = a
        else:
            print "Unabled Option"
            sys.exit(-1)

        
    if not pinboard_username or not pinboard_password or not delicious_username or not delicious_password:
        print "Either set your username/password combinations in the file or supply them:\n"
        print "%s " % sys.argv[0],
        for x in available_arguments:
            print "--%setc " % x,
        print "\n"

        sys.exit(-1)
    else:
        p2d = pb2del(pinboard_username, pinboard_password, delicious_username, delicious_password)
        p2d.run_export()


