#!/usr/bin/python3
#
# Torbert, 18 December 2015
#
# chmod 755 runme.py
#
# ./runme.py
# modmod.py = modified moderator
#
##################################################
#
from random     import choice
#
from subprocess import Popen
from subprocess import PIPE
from subprocess import TimeoutExpired
#
from time       import time
from os         import path
import sys
import re
#
##################################################
#
TIMEOUT = 1.5 # seconds allowed per move
#
startTime = time()
theE = '.'
theX = 'X'
theO = 'O'
#
print ("{} running under\nversion {}".format(path.basename(__file__), sys.version))

fname = path.abspath('BaselineRandom.py')
gname = path.abspath('Smarter2.py')
runCount = 1
if len(sys.argv)>1: runCount = int(2 * float(sys.argv[1]))
if len(sys.argv)>2: gname = path.abspath(sys.argv[2])
if len(sys.argv)>3: fname = path.abspath(sys.argv[3])
preBoard = sys.argv[4].upper() if len(sys.argv)>4 else ""
#
##################################################
#
def st( alist ) :
   #
   return '' . join( alist )
   #
#
##################################################
#
def ib( r , c ) :
   #
   return 0 <= r < 8 and 0 <= c < 8
   #
#
##################################################
#
def wouldBracket( theboard , thepiece , r , c , dr , dc ) :
   #
   theother = theX
   #
   if theother == thepiece : theother = theO
   #
   #
   #
   if ib( r + dr , c + dc ) :
      #
      j = ( r + dr ) * 8 + ( c + dc )
      #
      if theboard[j] == theother :
         #
         r += dr
         c += dc
         #
         while ib( r + dr , c + dc ) :
            #
            j = ( r + dr ) * 8 + ( c + dc )
            #
            if theboard[j] == thepiece : return True
            if theboard[j] == theE     : return False
            #
            r += dr
            c += dc
            #
         #
      #
   #
   return False
   #
#
##################################################
#
def thenBracket( theboard , thepiece , r , c , dr , dc ) :
   #
   theother = theX
   #
   if theother == thepiece : theother = theO
   #
   #
   #
   j = ( r + dr ) * 8 + ( c + dc )
   #
   while theboard[j] != thepiece :
      #
      theboard[j] =  thepiece
      #
      r += dr
      c += dc
      #
      j = ( r + dr ) * 8 + ( c + dc )
      #
   #
#
##################################################
#
def getPossMoves( theboard , thepiece ) :
   #
   alist = []
   #
   j = 0
   #
   while j < 64 :
      #
      if theboard[j] == theE :
         #
         r = j // 8 # row
         c = j %  8 # col
         #
         #          E   NE    N   NW    W   SW   S  SE
         drlist = [ 0 , -1 , -1 , -1 ,  0 ,  1 , 1 , 1 ]
         dclist = [ 1 ,  1 ,  0 , -1 , -1 , -1 , 0 , 1 ]
         #
         drc = zip( drlist , dclist )
         #
         for ( dr , dc ) in drc :
            #
            if wouldBracket( theboard , thepiece , r , c , dr , dc ) :
               #
               alist . append( j )
               #
               break
               #
            #
      #
      j += 1
      #
   #
   return alist
   #
#
##################################################
#
def getMove( fname , theboard , thepiece , timeForThisMove , debugLevel=0) :
   #
   possMoves = getPossMoves( theboard , thepiece )
   #
   if len( possMoves ) == 0 : return -1 # does happen
   #
   #------------------------ RUN THE PLAYER'S CODE ---#
   #
   strboard = st( theboard )
   timeLeft = "{}".format(timeForThisMove)   # ensure a string
   #
   # If the python executable is named python3.exe then use the first line; If it is python.exe then keep as is
   myargs = [ 'python3' , fname , strboard , thepiece , timeLeft ]
   myargs = [ 'python' , fname , strboard , thepiece, timeLeft ]
   #
   po = Popen( myargs , stdout = PIPE , stderr = PIPE )
   #
   # import io
   # print( 'io' , io.DEFAULT_BUFFER_SIZE ) # 8192
   #
   try :
      # x contains the raw output from the called script; y has any error messages
      x , y = po . communicate( timeout = timeForThisMove )
      if debugLevel > 3:
        # raw feed from the 
        print ("Got process output: {}**\n".format(x))
        print ("Got process errors: {}**\n".format(y))
      #
   except TimeoutExpired :
      #
      po . kill()
      #
      x , y = po . communicate()
      #

      global timeoutCount
      timeoutCount += 1
      if debugLevel > 0:
        print( '*** timeout' )
      #
   #
   z = x . split()
   #
   if len( z ) > 0 :
      #
      if debugLevel > 2: print ("*** strategy input: {}".format(x))
      themove = z[-1] . decode( 'utf-8' ) # last only
      #
      if debugLevel > 1:
        print( '*** themove' , themove )
      #
      # check for a match with zero-indexed moves
      #
#      if debugLevel > 1:
#        print( '*** zero' )
      #
      for move in possMoves :
         #
         if ( '%d' % move ) == themove : return move
         if ('+%d' % move ) == themove : return move
         #

      # Debugging contingency: If the user supplied move is not valid, we need to understand why
      if debugLevel > 2:
        exit()

      #
      # then check for a one-indexed (OBOB) match
      #

      if debugLevel > 1:
        print( '*** obob' )
      #
      for move in possMoves :
         #
         move1 = move + 1
         #
         if ( '%d' % move1 ) == themove : return move
         if ('+%d' % move1 ) == themove : return move
         #
      #
      # then check for a row-column OBOB move too
      #
      if debugLevel > 1:
        print( '*** obob rowcol' )
      #
      for move in possMoves :
         #
         r = move // 8 # row ... zero-indexed
         c = move %  8 # col
         #
         r += 1 # one-indexed = OBOB = off-by-one-bug
         c += 1
         #
         j = r * 8 + c
         #
         if ( '%d' % j ) == themove : return move
         if ('+%d' % j ) == themove : return move
         #
      #
   #
   #------------------------ END ---------------------#
   #
   if debugLevel > 1:
     print( '*** default random' )
   #
   # Debugging contingency: If the user supplied move is not valid, we need to understand why
   if debugLevel > 2:
     print("*** strategy issue: {}".format(y))
     exit()
   return choice( possMoves ) # default = random play
   #
#
##################################################
#
def makeMove( theboard , thepiece , themove ) :
   #
   r = themove // 8 # row
   c = themove %  8 # col
   #
   #          E   NE    N   NW    W   SW   S  SE
   drlist = [ 0 , -1 , -1 , -1 ,  0 ,  1 , 1 , 1 ]
   dclist = [ 1 ,  1 ,  0 , -1 , -1 , -1 , 0 , 1 ]
   #
   drc = zip( drlist , dclist )
   #
   for ( dr , dc ) in drc :
      #
      if wouldBracket( theboard , thepiece , r , c , dr , dc ) :
         #
         thenBracket(  theboard , thepiece , r , c , dr , dc )
         #
      #
   #
   theboard[themove] = thepiece
   #
#
##################################################
#
def pr( x ) :
   #
   print()
   #
   nums = '01234567'
   #
   print( ' ' , end = ' ' )
   print( ' ' , end = ' ' )
   print( ' ' + '_' * ( 2 * len( nums ) + 1 ) + ' ' ) # top _ underscore
   #
   for r in nums :
      #
      print( ' ' , end = ' ' )
      print(  r  , end = ' ' )
      print( '|' , end = ' ' )
      #
      for c in nums :
         #
         j = int(r) * 8 + int(c)
         #
         print( x[j] , end = ' ' )
         #
      #
      print( '|' , end = ' ' )
      print( r )
      #
   #
   print( ' ' , end = ' ' )
   print( ' ' , end = ' ' )
   print( ' ' + '-' * ( 2 * len( nums ) + 1 ) + ' ' ) # bottom - dash
   #
   print( ' ' , end = ' ' )
   print( ' ' , end = ' ' )
   print( ' ' , end = ' ' )
   #
   for c in nums :
      #
      print( c , end = ' ' )
      #
   #
   print()
   print()
   #
#
##################################################

def playGame(aCompetitors, timePerMove, debugLevel=0):
  # returns tuple: (competitor1 score, competitor2 score)
  theboard = [ theE ] * 64
  theboard[27] = theX
  theboard[36] = theX
  theboard[28] = theO
  theboard[35] = theO
  if preBoard: theboard = [preBoard[pos] for pos in range(len(preBoard))]
  aTimeLeft = [0.0, 0.0]

  if debugLevel>2:
    pr( theboard )

  theother = theO
  thepiece = theX # first move

  passCt = 0

  aMoves = []
  while passCt < 2:
    fname = aCompetitors[0]
    if debugLevel > 2:
      print( '*' * 50 )

    tic = time()
    num = getMove( fname , theboard , thepiece, aTimeLeft[0] + timePerMove, debugLevel )
    toc = time()
   #
    aMoves.append(num)
    if num != -1 :
      if debugLevel > 2:
        print ("{} as {} moves to index {} (row,col: {},{}) in {} seconds".format(
            re.sub("^.*[/\\\\]", '' , fname), thepiece, num, num // 8, num % 8, toc - tic))

      
      aTimeLeft[0] = max(aTimeLeft[0] + timePerMove - (toc - tic), 0.0)
      makeMove( theboard , thepiece , num )

      if debugLevel > 2:
        pr( theboard )

      if debugLevel > 2:
        print ("Resulting score: {}: {} and {}: {}".format(theX, theboard.count(theX), theO, theboard.count(theO)))
      passCt = 0
      #
    else :
      if debugLevel > 2:
        print ("***************  {} Passes  ***********************".format(thepiece))
      passCt += 1

    thepiece , theother = theother , thepiece
    aCompetitors = aCompetitors[::-1]
    aTimeLeft = aTimeLeft[::-1]
  if debugLevel > 0:
    print ("Time left: {}".format(aTimeLeft))
  return (theboard.count(theX), theboard.count(theO), aMoves)


timeoutCount = 0
aComp = [fname, gname]               # The competitors
aScore = [0, 0]                      # Number of wins each one has
aTotal = [0, 0]                      # Total number of tokens this strategy got
for gameNum in range(runCount):      # Play a series of games, alternating who goes first
  # Next line plays the game
  xScore, oScore, aMoves = playGame(aComp[::1-2*(gameNum % 2)], TIMEOUT, 1+2*(runCount<2))
  # Next line summarizes the game
  print ("Game {} score is {}: {} to {}: {}".format(gameNum, re.sub("^.*[/\\\\]", '' , aComp[gameNum % 2]), xScore,
                                                               re.sub("^.*[/\\\\]", '' , aComp[1-(gameNum % 2)]), oScore))
  if (xScore==oScore) or (xScore>oScore)==((gameNum % 2) == 0):
    aMoves = [str(aMoves[i]) for i in range(len(aMoves))]
    print (" ".join(aMoves[:-2]))
  # Update the scores
  aTotal = [aTotal[0]+oScore, aTotal[1]+xScore] if gameNum % 2 else [aTotal[0]+xScore, aTotal[1]+oScore]
  aScore = [aScore[0]+(oScore>xScore), aScore[1]+(xScore>oScore)] if gameNum % 2 \
      else [aScore[0]+(xScore>oScore), aScore[1]+(oScore>xScore)]
  print (" ")

# Print overall results
print ("After playing {} games, the score is\n{}: {} games ({} total tokens) vs {}: {} games ({} total tokens)".format(
           runCount, re.sub("^.*[/\\\\]", '' , fname), aScore[0], aTotal[0],
                     re.sub("^.*[/\\\\]", '' , gname), aScore[1], aTotal[1]))
print ("Total time: {}s;  Timeout count: {}".format(time() - startTime, timeoutCount))


##################################################
#
# end of file
#
##################################################
