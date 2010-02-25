
# Pinboard.in To Delicious Shover

http://github.com/tedroden

I have always used delicious, but delicious is getting worse and worse. So I recently started using http://pinboard.in as well. I've configured pinboard to automatically import the bookmarks from delicious but recently decided that I wanted to go the other way. I want to use pinboard as my main bookmarking service and push them to delicious as a backup. 

This is a script to do that. (Take your pinboard.in bookmarks and shove them into delicious).

## Running it

This script uses fairly standard Python, so it should run on most anything. To run it:

`python pinboard-to-delicious.py --pb_user=pinboard-username --pb_pass=pinboard-password --del_user=etc --del_pass=etc`

If you don't want to supply the password on the command line, simply open up the file and set the variables at the top.

## Things to know.

 - This will add a file called `.p2b-last` into your home directory to keep track of the last bookrmarks the script as seen.
 - This will probably break and stinks really bad
 - Anything else?
 
## Running automatically

If you modify the script, you can easily run it from cron by adding something like this to your crontab:

`*/10 * * * * /path/to/pinboard-to-delicious.py`

## License

Do whatever you want with this... It's not my fault if it kills you or makes you millions. If you want, let me know if you use it. I'm nosy.

## Thanks!

&copy; 2010 [Ted Roden](http://tedroden.com) [@tedroden](http://twitter.com/tedroden) [On github](http://github.com/tedroden)
