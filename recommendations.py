from math import sqrt
# A dictionary of movie critics and their ratings of a small
# set of movies
critics={
   'Lisa Rose': 
    {  
           'Lady in the Water': 2.5
        ,  'Snakes on a Plane': 3.5
        ,  'Just My Luck': 3.0
        ,  'Superman Returns': 3.5
        ,  'You, Me and Dupree': 2.5
        ,  'The Night Listener': 3.0
    },
   'Lisa Clone': 
    {  
           'Lady in the Water': 2.5
        ,  'Snakes on a Plane': 3.5
        ,  'Just My Luck': 3.0
        ,  'Superman Returns': 3.5
        ,  'You, Me and Dupree': 2.5
        ,  'The Night Listener': 3.0
    },    
 
   'Gene Seymour': 
    {
           'Lady in the Water': 3.0
        ,  'Snakes on a Plane': 3.5
        ,  'Just My Luck': 1.5
        ,  'Superman Returns': 5.0
        ,  'The Night Listener': 3.0
        ,  'You, Me and Dupree': 3.5
    }, 
 
   'Michael Phillips': 
   {
          'Lady in the Water': 2.5
       ,  'Snakes on a Plane': 3.0
       ,  'Superman Returns': 3.5
       ,  'The Night Listener': 4.0
   },
 
   'Claudia Puig': 
    {
    
          'Snakes on a Plane': 3.5
       ,  'Just My Luck': 3.0
       ,  'The Night Listener': 4.5
       ,  'Superman Returns': 4.0
       ,  'You, Me and Dupree': 2.5
    },
 
   'Mick LaSalle': 
   {
          'Lady in the Water': 3.0
       ,  'Snakes on a Plane': 4.0
       ,  'Just My Luck': 2.0
       ,  'Superman Returns': 3.0
       ,  'The Night Listener': 3.0,
          'You, Me and Dupree': 2.0
    }, 
 
    'Jack Matthews': 
    {
           'Lady in the Water': 3.0
        ,  'Snakes on a Plane': 4.0
        ,  'The Night Listener': 3.0
        ,  'Superman Returns': 5.0
        ,  'You, Me and Dupree': 3.5
    },
 
    'Toby': 
    {
          'Snakes on a Plane':4.5
        , 'You, Me and Dupree':1.0
        , 'Superman Returns':4.0
    },
    
    'Kenji':
    {
         'Batman Begins':4.5
    }
}

def sim_distance(prefs, person1, person2):
    similar_items = {}
    
    for item in prefs[person1]:
        if item in prefs[person2]:
            similar_items[item]=1
    
    #no ratings in common
    if len(similar_items)==0: return 0;
    
    # (a1 - b1)**2 + (a2 - b2)**2 + .. + (an - bn)**2
    sum_of_squares = sum( [ pow( prefs[person1][item] - prefs[person2][item], 2 )  for item in similar_items ] )
    
    return 1 /(1 + sqrt(sum_of_squares))
    
    
def sim_pearson(prefs, p1, p2):    
    similar_items = {}
    
    for item in prefs[p1]:
        if item in prefs[p2]:
            similar_items[item]=1
    
    
    n = len(similar_items)
    
    if n==0: return 0
    
    # adding all the ratings for similar items for p1
    sum1 = sum( [ prefs[p1][it] for it in similar_items ] )
    
    # adding all the ratings for similar items for p2
    sum2 = sum( [ prefs[p2][it] for it in similar_items ] )    
    
    sum1Sq = sum( [ pow( prefs[p1][it], 2 ) for it in similar_items ] )
    sum2Sq = sum( [ pow( prefs[p2][it], 2 ) for it in similar_items ] )    
    
    pSum=sum( [ prefs[p1][it]*prefs[p2][it] for it in similar_items ] )

    num = pSum - ( sum1 * sum2 / n )
    den = sqrt( (sum1Sq - pow(sum1, 2) / n ) * ( sum2Sq - pow(sum2, 2) / n ) )
    
    if den==0: return 0

    r=num/den

    return r
    
def topMatches(prefs, person, n=5, similarity=sim_pearson):    
    scores = [ (similarity(prefs, person, other), other) for other in prefs if other != person ]     
    scores.sort()
    scores.reverse()
    return scores[0:n]
    
    
def getRecommendations(prefs, person, similarity=sim_pearson):    
    totals={}
    simSums={}
    
    for other in prefs:
        if other==person: continue
        
        sim=similarity(prefs, person, other)
    
        if sim<=0: continue
            
        for item in prefs[other]:        
            
            if item not in prefs[person] or prefs[person][item]==0:
                #similarity*score
                totals.setdefault(item, 0)
                totals[item] += prefs[other][item]*sim
                
                simSums.setdefault(item, 0)
                simSums[item]+=sim
                
    print totals.items()
        
    rankings = [ (total/simSums[item], item) for item,total in totals.items() ]        
    rankings.sort()
    rankings.reverse()
    return rankings    
            
def transformPrefs(prefs):    
    result={}
    
    for person in prefs:
        for item in prefs[person]:
            result.setdefault(item, {})
            result[item][person] = prefs[person][item]
            
            
    return result;

def all_options(prefs):
    all_movies = []
    for person in prefs:
        for item in prefs[person]:
            all_movies.append(item) 
            
    return set(all_movies)
            
def sim_tanimoto(prefs, person, other):
    #get all options
    #for each person, mark 1 if he/she has seen it

    all_movies = all_options(prefs)
    matrix = {}
    
    # tan_score = m11 / (m01 + m10 + m11)
    similar_to_both = [ movie for movie in all_movies if (movie in prefs[person] and movie in prefs[other]) ]
    only_a = [ movie for movie in all_movies if (movie in prefs[person] and movie not in prefs[other]) ]
    only_b = [ movie for movie in all_movies if (movie not in prefs[person] and movie in prefs[other]) ]
    
    print 'similar to both:' + str(len(similar_to_both))
    print 'only A:' + str(len(only_a))
    print 'only B:' + str(len(only_b))
    
    simi = float(len(similar_to_both))
    a =  float(len(only_a))
    b = float(len(only_b))
    
    tan_score = simi / ( a + b + simi) 
    
    return tan_score
    

    
    