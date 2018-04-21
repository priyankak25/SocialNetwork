# coding: utf-8

"""
Collecting a political social network

I've taken a list of Twitter accounts of 4
U.S. presedential candidates from the previous election.

The goal is to use the Twitter API to construct a social network of these
accounts. I will then use the [networkx](http://networkx.github.io/) library
to plot these links, as well as print some statistics of the resulting graph.

1. Create an account on [twitter.com](http://twitter.com).
2. Generate authentication tokens by following the instructions [here](https://developer.twitter.com/en/docs/basics/authentication/guides/access-tokens.html).
3. Add your tokens to the key/token variables below. (API Key == Consumer Key)
4. Be sure you've installed the Python modules
[networkx](http://networkx.github.io/) and
[TwitterAPI](https://github.com/geduldig/TwitterAPI). Assuming you've already
installed [pip](http://pip.readthedocs.org/en/latest/installing.html), you can
do this with `pip install networkx TwitterAPI`.

"""

# Imports you'll need.
from collections import Counter
import matplotlib.pyplot as plt
import networkx as nx
import sys
import time
from TwitterAPI import TwitterAPI

consumer_key = 'Owr4FqSkok8VDXRzLEByqVeOG'
consumer_secret = 'T3TvzdM3eSyYGI8TskKHe2Mc43NBzJSGAUB7dAJvnAH32NNm7k'
access_token = '2891901698-F8NxRTBijVcfBjUAgZjyp6NTfNXe2skVgQW8fUb'
access_token_secret = 'szWWXDuB5EWCiFtjBofKLLAbd434nhBVNGohQIOvoy1xT'



def get_twitter():
    """ Construct an instance of TwitterAPI using the tokens you entered above.
    Returns:
      An instance of TwitterAPI.
    """
    return TwitterAPI(consumer_key, consumer_secret, access_token, access_token_secret)


def read_screen_names(filename):
    """
    Read a text file containing Twitter screen_names, one per line.

    Params:
        filename....Name of the file to read.
    Returns:
        A list of strings, one per screen_name, in the order they are listed
        in the file.

    Here's a doctest to confirm your implementation is correct.
    >>> read_screen_names('candidates.txt')
    ['DrJillStein', 'GovGaryJohnson', 'HillaryClinton', 'realDonaldTrump']
    """
    ###TODO
    with open(filename, 'r') as file:
         string = file.read().splitlines()
    return string
    pass   



# below method is to handle Twitter's rate limiting.
# You should call this method whenever you need to access the Twitter API.
def robust_request(twitter, resource, params, max_tries=5):
    """ If a Twitter request fails, sleep for 15 minutes.
    Do this at most max_tries times before quitting.
    Args:
      twitter .... A TwitterAPI object.
      resource ... A resource string to request; e.g., "friends/ids"
      params ..... A parameter dict for the request, e.g., to specify
                   parameters like screen_name or count.
      max_tries .. The maximum number of tries to attempt.
    Returns:
      A TwitterResponse object, or None if failed.
    """
    for i in range(max_tries):
        request = twitter.request(resource, params)
        if request.status_code == 200:
            return request
        else:
            print('Got error %s \nsleeping for 15 minutes.' % request.text)
            sys.stderr.flush()
            time.sleep(61 * 15)


def get_users(twitter, screen_names):
    """Retrieve the Twitter user objects for each screen_name.
    Params:
        twitter........The TwitterAPI object.
        screen_names...A list of strings, one per screen_name
    Returns:
        A list of dicts, one per user, containing all the user information
        (e.g., screen_name, id, location, etc)

    See the API documentation here: https://dev.twitter.com/rest/reference/get/users/lookup


In this example, I test retrieving two users: twitterapi and twitter.

    >>> twitter = get_twitter()
    >>> users = get_users(twitter, ['twitterapi', 'twitter'])
    >>> [u['id'] for u in users]
    [6253282, 783214]
    """
    ###TODO
    user_objects = []
    for scr_name in screen_names:
        response = robust_request(twitter, 'users/lookup', {'screen_name': scr_name}, max_tries=100)
        usr = [u for u in response]
        desc = {'screen_name': usr[0]['screen_name'],
             'id': usr[0]['id'],
             'name': usr[0]['name'],
             'location': usr[0]['location'],
             'description': usr[0]['description']             
             }
                
        user_objects.append(desc)
           
    
    return user_objects
    pass


def get_friends(twitter, screen_name):
    """ Return a list of Twitter IDs for users that this person follows, up to 5000.
    See https://dev.twitter.com/rest/reference/get/friends/ids

    Note, because of rate limits, it's best to test this method for one candidate before trying
    on all candidates.

    Args:
        twitter.......The TwitterAPI object
        screen_name... a string of a Twitter screen name
    Returns:
        A list of ints, one per friend ID, sorted in ascending order.

    Note: If a user follows more than 5000 accounts, we will limit ourselves to
    the first 5000 accounts returned.

    In this test case, I return the first 5 accounts that I follow.
    >>> twitter = get_twitter()
    >>> get_friends(twitter, 'aronwc')[:5]
    [695023, 1697081, 8381682, 10204352, 11669522]
    """
    ###TODO
    
    TwitterID = []   #array to store Twitter IDs for users(screen_name)
    response = robust_request(twitter,'friends/ids',{'screen_name' : screen_name, 'count':5000},max_tries=100)
   # print(response)
    for i in response.get_iterator(): #it will get the IDs of given Screen Names
        TwitterID.append(i)

    return sorted(TwitterID)

    pass


def add_all_friends(twitter, users):
    """ Get the list of accounts each user follows.
    I.e., call the get_friends method for all 4 candidates.

    Store the result in each user's dict using a new key called 'friends'.

    Args:
        twitter...The TwitterAPI object.
        users.....The list of user dicts.
    Returns:
        Nothing

    >>> twitter = get_twitter()
    >>> users = [{'screen_name': 'aronwc'}]
    >>> add_all_friends(twitter, users)
    >>> users[0]['friends'][:5]
    [695023, 1697081, 8381682, 10204352, 11669522]
    """
    ###TODO    
    for usr in users:
        usr['friends'] = get_friends(twitter,usr['screen_name'])  #calling get_friends for every Screen_name
    pass


def print_num_friends(users):
    """Print the number of friends per candidate, sorted by candidate name.
    See Log.txt for an example.
    Args:
        users....The list of user dicts.
    Returns:
        Nothing
    """
    ###TODO
    pass
    
    for usr in users:
        print(str(usr['screen_name'])+"  "+str(len(usr['friends'])))


def count_friends(users):
    """ Count how often each friend is followed.
    Args:
        users: a list of user dicts
    Returns:
        a Counter object mapping each friend to the number of candidates who follow them.
        Counter documentation: https://docs.python.org/dev/library/collections.html#collections.Counter

    In this example, friend '2' is followed by three different users.
    >>> c = count_friends([{'friends': [1,2]}, {'friends': [2,3]}, {'friends': [2,3]}])
    >>> c.most_common()
    [(2, 3), (3, 2), (1, 1)]
    """
    ###TODO
    cnt = Counter()
    for usr in users:
        cnt.update(usr['friends']) #Elements are counted from an iterable or added-in from another mapping like counter
    
    return cnt
    pass

def friend_overlap(users):
    """
    Compute the number of shared accounts followed by each pair of users.

    Args:
        users...The list of user dicts.

    Return: A list of tuples containing (user1, user2, N), where N is the
        number of accounts that both user1 and user2 follow.  This list should
        be sorted in descending order of N. Ties are broken first by user1's
        screen_name, then by user2's screen_name (sorted in ascending
        alphabetical order). See Python's builtin sorted method.

    In this example, users 'a' and 'c' follow the same 3 accounts:
    >>> friend_overlap([
    ...     {'screen_name': 'a', 'friends': ['1', '2', '3']},
    ...     {'screen_name': 'b', 'friends': ['2', '3', '4']},
    ...     {'screen_name': 'c', 'friends': ['1', '2', '3']},
    ...     ])
    [('a', 'c', 3), ('a', 'b', 2), ('b', 'c', 2)]
    """
    ###TODO
    pass
    count = 0
    frnd_overlap = []
    overlap = tuple()
    
    for i in range(0, len(users)):
        for j in range(i+1, len(users)):
            for k in range(0, len(users[i]['friends'])):
                for l in range(0, len(users[j]['friends'])):
                    if users[i]['friends'][k] == users[j]['friends'][l]:
                        count += 1
            overlap = (users[i]['screen_name'], users[j]['screen_name'], count)
            frnd_overlap.append(overlap)
            count = 0

    frnd_overlap = sorted(frnd_overlap, key=lambda tup: (-tup[2], tup[0], tup[1]))

    return frnd_overlap   

def followed_by_hillary_and_donald(users, twitter):
    """
    Find and return the screen_name of the one Twitter user followed by both Hillary
    Clinton and Donald Trump. You will need to use the TwitterAPI to convert
    the Twitter ID to a screen_name. See:
    https://dev.twitter.com/rest/reference/get/users/lookup

    Params:
        users.....The list of user dicts
        twitter...The Twitter API object
    Returns:
        A string containing the single Twitter screen_name of the user
        that is followed by both Hillary Clinton and Donald Trump.
    """
    ###TODO
    user_hillary=next((u for u in users if u['screen_name'] == 'HillaryClinton'),None) #return HillaryClinton whole data
    user_trump=next((u for u in users if u['screen_name'] == 'realDonaldTrump'),None) #return realDonaldTrump whole data
    
    friends_hillary=Counter(user_hillary['friends'])
    friends_trump=Counter(user_trump['friends'])
    
    followed_by_HT = set(friends_hillary).intersection(friends_trump) #this will give friend id followed by Hillary and Trump
    
    response=robust_request(twitter,'users/lookup', {'user_id':followed_by_HT})
    common_id=[r for r in response]   #retrived the whole data of followed_by_both id
    
    return common_id[0]['screen_name']
    pass  


def create_graph(users, friend_counts):
    """ Create a networkx undirected Graph, adding each candidate and friend
        as a node.  Note: while all candidates should be added to the graph,
        only add friends to the graph if they are followed by more than one
        candidate. (This is to reduce clutter.)

        Each candidate in the Graph will be represented by their screen_name,
        while each friend will be represented by their user id.

    Args:
      users...........The list of user dicts.
      friend_counts...The Counter dict mapping each friend to the number of candidates that follow them.
    Returns:
      A networkx Graph
    """
    ###TODO
    graph = nx.Graph()
    frn_ids = [i for i in friend_counts if friend_counts[i]>1]
    for u in frn_ids:
        graph.add_node(u)
    for u in users:
        graph.add_node(u['screen_name'])
        friend_list = set(u['friends']) & set(frn_ids)
        for friend in friend_list:
            graph.add_node(friend)
            graph.add_edge(friend, u['screen_name'])
   
    return graph
    
    pass


def draw_network(graph, users, filename):
    """
    Draw the network to a file. Only label the candidate nodes; the friend
    nodes should have no labels (to reduce clutter).

    Methods you'll need include networkx.draw_networkx, plt.figure, and plt.savefig.

    Your figure does not have to look exactly the same as mine, but try to
    make it look presentable.
    """
    ###TODO
    
    user= {}
    for u in users:
        user[u['screen_name']] = u['screen_name']
    
    plt.figure(figsize=(15, 15))
    plt.axis('off')
    nx.draw_networkx(graph, labels=user, alpha=.8, node_size=150, width=0.3)
    
    plt.savefig(filename)
    
    pass


def main():
    """ Main method. You should not modify this. """
    twitter = get_twitter()
    screen_names = read_screen_names('candidates.txt')
    print('Established Twitter connection.')
    print('Read screen names: %s' % screen_names)
    users = sorted(get_users(twitter, screen_names), key=lambda x: x['screen_name'])
    print('found %d users with screen_names %s' %
         (len(users), str([u['screen_name'] for u in users])))
    add_all_friends(twitter, users)
    print('Friends per candidate:')
    print_num_friends(users)
    friend_counts = count_friends(users)
    print('Most common friends:\n%s' % str(friend_counts.most_common(5)))
    print('Friend Overlap:\n%s' % str(friend_overlap(users)))
    print('User followed by Hillary and Donald: %s' % followed_by_hillary_and_donald(users, twitter))
    graph = create_graph(users, friend_counts)
    print('graph has %s nodes and %s edges' % (len(graph.nodes()), len(graph.edges())))
    draw_network(graph, users, 'network.png')
    print('network drawn to network.png')


if __name__ == '__main__':
    main()

