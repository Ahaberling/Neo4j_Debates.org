from neo4j import GraphDatabase
import json
import numpy as np
from datetime import datetime

#import collections

######################
### Initialization ###
######################

f = open('D:/Universitaet Mannheim/MMDS 6. Semester/Individual Project/users.json', "r")
g = open('D:/Universitaet Mannheim/MMDS 6. Semester/Individual Project/debates.json', "r")

users_data = json.load(f)
debates_data = json.load(g)

driver = GraphDatabase.driver("neo4j://localhost:7687", auth=("neo4j", "abc"))


user_bool = True
debate_bool = False
comment_bool = False
argument_bool = False
votemap_bool = False
opinion_bool = False
poll_bool = False
issues_bool = True

friends_with_bool = False
debates_in_bool = False
gives_comment_bool = False
gives_argument_bool = False
gives_votemap_bool = False
gives_opinion_bool = False
gives_pollvote_bool = False
gives_issues_bool = True
user_timeline_bool = False

has_comment_bool = False
has_votemap_bool = False
has_argument_bool = False
debate_timeline_bool = False

comment_timeline_bool = False

refers_to_bool = False



sample = 100

#####################################
### Functions: Write Transactions ###
#####################################

### Nodes ###

def add_user(tx, userName, userBirth, userDescr, userEduc, userElo, userEmail, userEthni, userSex, userInterest, userInc,
                    userJoin, userOn, userUpd, userLook, userParty, userPoli, userPresi, userRels, userReli,
                    userURL, userWinR):
    tx.run("MERGE (a:User {userID: $userName, birthday: $userBirth, description: $userDescr, education: $userEduc, elo_ranking: $userElo," +
                    "email: $userEmail, ethnicity: $userEthni, gender: $userSex, interested: $userInterest,income: $userInc, joined: $userJoin, last_online: $userOn," +
                    "last_updated: $userUpd, looking: $userLook, party: $userParty, political_ideology: $userPoli, president: $userPresi, relationship: $userRels," +
                    "religious_ideology: $userReli, url: $userURL, win_ratio: $userWinR})",
                    userName=userName, userBirth=userBirth, userDescr=userDescr, userEduc=userEduc, userElo=userElo, userEmail=userEmail,
                    userEthni=userEthni, userSex=userSex, userInterest=userInterest, userInc=userInc, userJoin=userJoin, userOn=userOn, userUpd=userUpd, userLook=userLook,
                    userParty=userParty, userPoli=userPoli, userPresi=userPresi, userRels=userRels, userReli=userReli, userURL=userURL,
                    userWinR=userWinR)
    # 'all_debates' excluded due to redundancy

def add_debate(tx, debateName, debateUrl, debateCategory, debateTitle, start_date):
    tx.run("MERGE (a:Debate {debateID: $debateName, url: $debateUrl, category: $debateCategory, title: $debateTitle, start: $start_date})",
           debateName=debateName, debateUrl=debateUrl, debateCategory=debateCategory, debateTitle=debateTitle, start_date=start_date)

def add_comment(tx, commentID, commentTime, commentContent):
    tx.run("MERGE (a:Comment {commentID: $commentID, commentTime: $commentTime, content: $commentContent})", commentID=commentID, commentTime=commentTime, commentContent=commentContent)

def add_argument(tx, argumentID, argumentContent):
    tx.run("MERGE (a:Argument {argumentID: $argumentID, argumentContent: $argumentContent})", argumentID=argumentID, argumentContent=argumentContent)

def add_voteMap_extended(tx, votemapID, beforeDebate, afterDebate, betterConduct, betterSpellingGrammar, convincingArguments,
                reliableSources, totalPoints):
    tx.run("MERGE (a:VoteMap {votemapID: $votemapID, beforeDebate: $beforeDebate, afterDebate: $afterDebate, " +
           "betterConduct: $betterConduct, betterSpellingGrammar: $betterSpellingGrammar, convincingArguments: $convincingArguments, " +
           "reliableSources: $reliableSources, totalPoints: $totalPoints})",
           votemapID=votemapID, beforeDebate=beforeDebate, afterDebate=afterDebate, betterConduct=betterConduct,
           betterSpellingGrammar=betterSpellingGrammar, convincingArguments=convincingArguments, reliableSources=reliableSources,
           totalPoints=totalPoints)

def add_voteMap_reduced(tx, votemapID, won):
    tx.run("MERGE (a:VoteMap {votemapID: $votemapID, won: $won})",
           votemapID=votemapID, won=won)

def add_opinion(tx, opinionID, opinionLink):
    tx.run("MERGE (a:Opinion {opinionID: $opinionID, opinionLink: $opinionLink})",
           opinionID=opinionID, opinionLink=opinionLink)


def add_poll(tx, pollID, pollLink):
    tx.run("MERGE (a:Poll {pollID: $pollID, pollLink: $pollLink})",
           pollID=pollID, pollLink=pollLink)

def add_issues(tx, issuesID, abortion, affirmative_a, animal_rights, obama, border, capitalism, civil_unions, death_penalty, drug_legaliz, electoral_college, enviro_prot,
               estate_tax, eu, euthanasia, federal_reserve, flat_tax, free_trade, gay_marriage, global_warming, globalization, gold_standard, gun_rights, homeschooling,
               internet_censor, iran_iraq_war, labor_union, legal_prostit, medicaid_care, medical_marijuana, military_interv, minimum_wage, national_health_care,
               nat_ret_sales_tax, occupy_movement, progressive_tax, racial_profiling, redistribution, smoking_ban, social_programs, social_security, socialism, stimulus_spending,
               term_limits, torture, united_nations, war_afghanistan, war_terror, welfare):
    tx.run("MERGE (a:Issues {issuesID: $issuesID, abortion: $abortion, affirmative_a: $affirmative_a, animal_rights: $animal_rights, obama: $obama, border: $border, capitalism: $capitalism, " +
           "civil_unions: $civil_unions, death_penalty: $death_penalty, drug_legaliz: $drug_legaliz, electoral_college: $electoral_college, enviro_prot: $enviro_prot, estate_tax: $estate_tax, " +
           "eu: $eu, euthanasia: $euthanasia, federal_reserve: $federal_reserve, flat_tax: $flat_tax, free_trade: $free_trade, gay_marriage: $gay_marriage, global_warming: $global_warming, " +
           "globalization: $globalization, gold_standard: $gold_standard, gun_rights: $gun_rights, homeschooling: $homeschooling, internet_censor: $internet_censor, iran_iraq_war: $iran_iraq_war, " +
           "labor_union: $labor_union, legal_prostit: $legal_prostit, medicaid_care: $medicaid_care, medical_marijuana: $medical_marijuana, military_interv: $military_interv, " +
           "minimum_wage: $minimum_wage, national_health_care: $national_health_care, nat_ret_sales_tax: $nat_ret_sales_tax, occupy_movement: $occupy_movement, progressive_tax: $progressive_tax, " +
           "racial_profiling: $racial_profiling, redistribution: $redistribution, smoking_ban: $smoking_ban, social_programs: $social_programs, social_security: $social_security, " +
           "socialism: $socialism, stimulus_spending: $stimulus_spending, term_limits: $term_limits, torture: $torture, united_nations: $united_nations, war_afghanistan: $war_afghanistan, " +
           "war_terror: $war_terror, welfare: $welfare})",
           issuesID=issuesID, abortion=abortion, affirmative_a=affirmative_a, animal_rights=animal_rights, obama=obama, border=border, capitalism=capitalism, civil_unions=civil_unions,
           death_penalty=death_penalty, drug_legaliz=drug_legaliz, electoral_college=electoral_college, enviro_prot=enviro_prot, estate_tax=estate_tax, eu=eu, euthanasia=euthanasia,
           federal_reserve=federal_reserve, flat_tax=flat_tax, free_trade=free_trade, gay_marriage=gay_marriage, global_warming=global_warming, globalization=globalization,
           gold_standard=gold_standard, gun_rights=gun_rights, homeschooling=homeschooling, internet_censor=internet_censor, iran_iraq_war=iran_iraq_war,
           labor_union=labor_union, legal_prostit=legal_prostit, medicaid_care=medicaid_care, medical_marijuana=medical_marijuana, military_interv=military_interv,
           minimum_wage=minimum_wage, national_health_care=national_health_care, nat_ret_sales_tax=nat_ret_sales_tax, occupy_movement=occupy_movement, progressive_tax=progressive_tax,
           racial_profiling=racial_profiling, redistribution=redistribution, smoking_ban=smoking_ban, social_programs=social_programs, social_security=social_security,
           socialism=socialism, stimulus_spending=stimulus_spending, term_limits=term_limits, torture=torture, united_nations=united_nations, war_afghanistan=war_afghanistan,
           war_terror=war_terror, welfare=welfare)

### User Edges ###

def add_friends_with(tx, userName, friendName):
    tx.run("MATCH (a:User {userID: $userName}) \n" +
           "MATCH (b:User {userID: $friendName}) \n" +
           "MERGE (a)-[:FRIENDS_WITH]->(b)", userName=userName, friendName=friendName)

def add_debates_in(tx, userName, debateName, debateForfeit, debateWinning, debatePosition):
    tx.run("MATCH (a:User {userID: $userName}) \n" +
           "MATCH (b:Debate {debateID: $debateName}) \n" +
           "MERGE (a)-[:DEBATES_IN {forfeit: $debateForfeit, winning: $debateWinning, position: $debatePosition }]->(b)",
           userName=userName, debateName=debateName, debateForfeit=debateForfeit, debateWinning=debateWinning, debatePosition=debatePosition)

def add_gives_comment(tx, userName, commentID):
    tx.run("MATCH (a:User {userID: $userName}) \n" +
           "MATCH (b:Comment {commentID: $commentID}) \n" +
           "MERGE (a)-[:GIVES_COMMENT]->(b)", userName=userName, commentID=commentID)

def add_gives_argument(tx, userID, argumentID):
    tx.run("MATCH (a:User {userID: $userID}) \n" +
           "MATCH (b:Argument {argumentID: $argumentID}) \n" +
           "MERGE (a)-[:GIVES_ARGUMENT]->(b)", userID=userID, argumentID=argumentID)

def add_gives_voteMap(tx, userID, votemapID):
    #print('called in write function with: ', userID, votemapID)
    tx.run("MATCH (a:User {userID: $userID}) \n" +
           "MATCH (b:VoteMap {votemapID: $votemapID}) \n" +
           "MERGE (a)-[:GIVES_VOTEMAP]->(b)", userID=userID, votemapID=votemapID)

def add_gives_opinion(tx, userID, opinionID, opinionText):
    tx.run("MATCH (a:User {userID: $userID}) \n" +
           "MATCH (b:Opinion {opinionID: $opinionID}) \n" +
           "MERGE (a)-[rel:GIVES_OPINION {opinionText: $opinionText}]->(b)", userID=userID, opinionID=opinionID, opinionText=opinionText)

def add_gives_pollvote(tx, userID, pollID, pollText, pollExplanation):
    tx.run("MATCH (a:User {userID: $userID}) \n" +
           "MATCH (b:Poll {pollID: $pollID}) \n" +
           "MERGE (a)-[rel:GIVES_POLLVOTE {pollText: $pollText, pollExplanation: $pollExplanation}]->(b)", userID=userID, pollID=pollID, pollText=pollText, pollExplanation=pollExplanation)

def add_gives_issues(tx,):
    tx.run()
    '''insert'''

def add_user_timeline(tx, prevUserID, debateID):
    tx.run("MATCH (a:User {userID: $debateID}) \n" +
           "MATCH (b:User {userID: $prevUserID}) \n" +
           "MERGE (b)-[:BEFORE]->(a)", debateID=debateID, prevUserID=prevUserID)

### Debate Edges ###

def add_has_comment(tx, debateName, commentID):
    tx.run("MATCH (a:Debate {debateID: $debateName}) \n" +
           "MATCH (b:Comment {commentID: $commentID}) \n" +
           "MERGE (a)-[:HAS_COMMENT]->(b)", debateName=debateName, commentID=commentID)

def add_has_voteMap(tx, debateID, votemapID):
    tx.run("MATCH (a:Debate {debateID: $debateID}) \n" +
           "MATCH (b:VoteMap {votemapID: $votemapID}) \n" +
           "MERGE (a)-[:HAS_VOTEMAP]->(b)", debateID=debateID, votemapID=votemapID)

def add_has_argument(tx, debateID, argumentID):
    tx.run("MATCH (a:Debate {debateID: $debateID}) \n" +
           "MATCH (b:Argument {argumentID: $argumentID}) \n" +
           "MERGE (a)-[:HAS_ARGUMENT]->(b)", debateID=debateID, argumentID=argumentID)

def add_debate_timeline(tx, debateID, prevDebateID):
    #print('add_debate_timeline is called with \n')
    #print(debateID, prevDebateID)
    tx.run("MATCH (a:Debate {debateID: $debateID}) \n" +
           "MATCH (b:Debate {debateID: $prevDebateID}) \n" +
           "MERGE (b)-[:BEFORE]->(a)", debateID=debateID, prevDebateID=prevDebateID)


### Comment Edges ###

def add_comment_timeline(tx, prevCommentID, commentID):
    tx.run("MATCH (a:Comment {commentID: $commentID}) \n" +
           "MATCH (b:Comment {commentID: $prevCommentID}) \n" +
           "MERGE (b)-[:BEFORE]->(a)", commentID=commentID, prevCommentID=prevCommentID)

### VoteMap Edges ###

def add_refers_to(tx, votemapID, userID):
    tx.run("MATCH (a:VoteMap {votemapID: $votemapID}) \n" +
           "MATCH (b:User {userID: $userID}) \n" +
           "MERGE (a)-[:REFERS_TO]->(b)", votemapID=votemapID, userID=userID)


### Miscellaneous ###

def delete_all(tx):
    tx.run("MATCH (n) DETACH DELETE n")


####################################
### Functions: Read Transactions ###
####################################

### Nodes ###

def read_user(tx):
    result = tx.run("MATCH (n:User) \n" +
           "RETURN n.userID, n.birthday, n.last_online, n.interested,n.income")
    for record in result:
        print(record["n.userID"])

def read_debate(tx):
    result = tx.run("MATCH (n:Debate) \n" +
           "RETURN n.debateID, n.url, n.category, n.title")
    for record in result:
        print(record["n.debateID"])

def read_argument(tx):
    result = tx.run("MATCH (n:Argument) \n" +
           "RETURN n.argumentID, n.argumentContent")
    for record in result:
        print(record["n.argumentID"], record['n.argumentContent'])

def read_comment(tx):
    result = tx.run("MATCH (n:Comment) \n" +
                    "RETURN n.commentID, n.content")
    for record in result:
        print("{} has content {}".format(record["n.commentID"], record["n.content"]))

def read_voteMap(tx):
    result = tx.run("MATCH (n:VoteMap) \n" +
                    "RETURN n.votemapID, n.beforeDebate, n.afterDebate, n.betterConduct, n.betterSpellingGrammar, n.convincingArguments, \n" +
                    "n.reliableSources, n.totalPoints, n.won")
    for record in result:
        print("{} has agreed before debate: {}, and overall: {} - {}".format(record["n.votemapID"], record["n.beforeDebate"], record["n.totalPoints"], record["n.won"]))

def read_opinion(tx):
    result = tx.run("MATCH (n:Opinion) \n" +
                    "RETURN n.opinionID, n.opinionLink, n.opinionText")
    for record in result:
        print("{} has link {} with text {}".format(record["n.opinionID"], record["n.opinionLink"], record["n.opinionText"]))

def read_poll(tx):
    result = tx.run("MATCH (n:Poll) \n" +
                    "RETURN n.pollID, n.pollLink, n.pollText, n.pollExplanation")
    for record in result:
        print("{} has link {} with text {} and explanation: {}".format(record["n.pollID"], record["n.pollLink"], record["n.pollText"], record["n.pollExplanation"]))

def read_issues(tx):
    result = tx.run("MATCH (n:Issues) \n" +
                    "RETURN n.issuesID, n.abortion, n.affirmative_a, n.animal_rights")
    for record in result:
        print("issuesID: {}, abortion: {}, affirmative_a: {},animal_rights: {}".format(record["n.issuesID"], record["n.abortion"], record["n.affirmative_a"], record["n.animal_rights"]))



### User Edges ###

def read_friends_with(tx):
    result = tx.run("MATCH (a:User)-[:FRIENDS_WITH]->(b:User) RETURN a.userID, b.userID")
    for record in result:
        print("{} nominated {}".format(record["a.userID"], record["b.userID"]))

def read_debates_in(tx):
    result = tx.run("MATCH (a:User)-[rel:DEBATES_IN]->(b:Debate) RETURN a.userID, b.debateID, rel.forfeit ,rel.winning, rel.position")
    for record in result:
        print("{} debated in {} and has ff-value {}".format(record["a.userID"], record["b.debateID"], record["rel.forfeit"]))

def read_gives_comment(tx):
    result = tx.run("MATCH (a:User)-[rel:GIVES_COMMENT]->(b:Comment) RETURN a.userID, b.commentID, b.content")
    for record in result:
        print("{} gives comment {} with content {}".format(record["a.userID"], record["b.commentID"], record["b.content"]))
        #print(record)

def read_gives_argument(tx):
    result = tx.run("MATCH (a:User)-[:GIVES_ARGUMENT]->(b:Argument) RETURN a.userID, b.argumentID, b.argumentContent")
    for record in result:
        print("{} has argued in {} with content {}".format(record["a.userID"], record["b.argumentID"], record["b.argumentContent"]))
        #print("called in read")
        #print(record)

def read_gives_voteMap(tx):
    result = tx.run("MATCH (a:User)-[:GIVES_VOTEMAP]->(b:VoteMap) RETURN a.userID, b.votemapID")
    for record in result:
        #print('called in read function: ')
        #print(record)
        print("{} gives votemap {}".format(record["a.userID"], record["b.votemapID"]))


def read_gives_opinion(tx):
    result = tx.run("MATCH (a:User)-[rel:GIVES_OPINION]->(b:Opinion) RETURN a.userID, b.opinionID, rel.opinionText")
    for record in result:
        print("{} gives opinion {} with value {}".format(record["a.userID"], record["b.opinionID"], record["rel.opinionText"]))


def read_gives_pollvote(tx):
    result = tx.run("MATCH (a:User)-[rel:GIVES_POLLVOTE]->(b:Poll) RETURN a.userID, b.pollID, rel.pollText, rel.pollExplanation")
    for record in result:
        print("{} gives pollvote {} with value {} and explanation {} ".format(record["a.userID"], record["b.pollID"], record["rel.pollText"], record["rel.pollExplanation"]))

def read_gives_issues(tx):
    result = tx.run("MATCH (a:User)-[rel:GIVES_ISSUES]->(b:Issues) RETURN a.userID, b.issuesID, b.abortion")
    for record in result:
        print("{} gives Issues {} with abortion value {} ".format(record["a.userID"], record["b.issuesID"], record["rel.abortion"]))

def read_user_timeline(tx):
    result = tx.run("MATCH (a:User)-[:BEFORE]->(b:User) RETURN a.userID, a.joined , b.userID, b.joined")
    for record in result:
        print("User {} joined on {} before User {} joined on {}".format(record["a.userID"], record["a.joined"], record["b.userID"], record["b.joined"]))


### Debate Edges ###

def read_has_comment(tx):
    result = tx.run("MATCH (a:Debate)-[rel:HAS_COMMENT]->(b:Comment) RETURN a.debateID, b.commentID, b.content")
    for record in result:
        print("{} has comment {} with content {}".format(record["a.debateID"], record["b.commentID"], record["b.content"]))

def read_has_voteMap(tx):
    result = tx.run("MATCH (a:Debate)-[rel:HAS_VOTEMAP]->(b:VoteMap) RETURN a.debateID, b.votemapID, b.totalPoints")
    for record in result:
        print("{} has votemap: {} with points: {}".format(record["a.debateID"], record["b.votemapID"], record["b.totalPoints"]))

def read_has_argument(tx):
    result = tx.run("MATCH (a:Debate)-[:HAS_ARGUMENT]->(b:Argument) RETURN a.debateID, b.argumentID, b.argumentContent")
    for record in result:
        print("{} has argument {} with content {}".format(record["a.debateID"], record["b.argumentID"], record["b.argumentContent"]))

def read_debate_timeline(tx):
    result = tx.run("MATCH (a:Debate)-[:BEFORE]->(b:Debate) RETURN a.debateID, a.start , b.debateID, b.start")
    #print('read_debate_timeline is called')
    for record in result:
        print("{} with {} took place before {} with {}".format(record["a.debateID"], record["a.start"], record["b.debateID"], record["b.start"]))


### Comment Edges ###

def read_comment_timeline(tx):
    result = tx.run("MATCH (a:Comment)-[:BEFORE]->(b:Comment) RETURN a.commentID, a.commentTime , b.commentID, b.commentTime")
    for record in result:
        print("Comment {} with date {} was created before comment {} with date {}".format(record["a.commentID"], record["a.commentTime"], record["b.commentID"], record["b.commentTime"]))


### VoteMap Edges ###

def read_refers_to(tx):
    result = tx.run("MATCH (a:VoteMap)-[:REFERS_TO]->(b:User) RETURN a.votemapID, b.userID")
    for record in result:
        print("{} refers to {}".format(record["a.votemapID"], record["b.userID"]))


### Miscellaneous ###

def read_all(tx):
    tx.run("MATCH (n) RETURN n")


########################
### Sessions - write ###
########################

with driver.session() as session:

    ###---------------###
    ### Miscellaneous ###
    ###---------------###

    ### Cleaning ###

    session.write_transaction(delete_all)


    ###-------###
    ### Nodes ###
    ###-------###

    ### User Node ###
    if user_bool == True:

        userList = []
        c = 0
        for i in users_data:
            c = c + 1
            userList.append(i)
            session.write_transaction(add_user, i, users_data[i]['birthday'], users_data[i]['description'], users_data[i]['education'],
                                      users_data[i]['elo_ranking'], users_data[i]['email'], users_data[i]['ethnicity'], users_data[i]['gender'],
                                      users_data[i]['interested'], users_data[i]['income'], users_data[i]['joined'], users_data[i]['last_online'], users_data[i]['last_updated'],
                                      users_data[i]['looking'], users_data[i]['party'], users_data[i]['political_ideology'], users_data[i]['president'],
                                      users_data[i]['relationship'], users_data[i]['religious_ideology'], users_data[i]['url'], users_data[i]['win_ratio'])
            if c % 100 == 0:
                print(c)
            if c >= sample:
                break
        print("-- user nodes done --")


    ### Debate Node ###
    if debate_bool == True:

        c = 0
        for i in debates_data:
            c = c + 1
            session.write_transaction(add_debate, i, debates_data[i]['url'], debates_data[i]['category'], debates_data[i]['title'], debates_data[i]['start_date'])
            if c % 100 == 0:
                print(c)
            if c >= sample:
                break
        print("-- debate nodes done --")

    ### Comment Nodes ###
    if comment_bool == True:

        c = 0
        for i in debates_data:
            c = c + 1
            c2 = 0
            for k in debates_data[i]['comments']:
                c2 = c2 + 1
                commentID = str(str(i) + '_Comment_' + str(c2))
                session.write_transaction(add_comment, commentID, k['time'], k['comment_text'])
            if c % 100 == 0:
                print(c)
            if c >= sample:
                break
        print("-- comment nodes done --")


    ### Argument Nodes ###
    if argument_bool == True:

        c = 0
        for i in debates_data:
            c = c + 1
            c2 = 0
            for k in debates_data[i]['rounds']:
                c2 = c2 + 1
                for p in k:
                    argumentID = str(str(i) + "_round_" + str(c2) + "_"+ str(p['side']))
                    session.write_transaction(add_argument, argumentID, p['text'])
            if c % 100 == 0:
                print(c)
            if c >= sample:
                break
        print("-- argument nodes done --")


    ### VoteMap Nodes ###
    if votemap_bool == True:

        c = 0
        for i in debates_data:
            c = c + 1
            c2 = 0
            for k in debates_data[i]['votes']:
                c2 = c2 + 1
                c3 = 0
                for p in k['votes_map']:
                    if c3 == 2:                               # VoteMaps consist of 3 parts. Bools of votes given to participant1, to participant2 and a redundant part 3 called tied with the same variables that are simply the first two variables connected with an logic AND
                        break
                    votemapID = str(str(i) + '_' + str(k['user_name']) + '_' + str(p))
                    if 'Agreed with before the debate' in k['votes_map'][p]:
                        session.write_transaction(add_voteMap_extended, votemapID, k['votes_map'][p]['Agreed with before the debate'], k['votes_map'][p]['Agreed with after the debate'],
                                              k['votes_map'][p]['Who had better conduct'],k['votes_map'][p]['Had better spelling and grammar'],k['votes_map'][p]['Made more convincing arguments'],
                                              k['votes_map'][p]['Used the most reliable sources'],k['votes_map'][p]['Total points awarded']) # "Total points awarded" kinda redundant
                    else:
                        session.write_transaction(add_voteMap_reduced, votemapID, k['votes_map'][p]['Who won the debate'])
                    c3 = c3 + 1
            if c % 100 == 0:
                print(c)
            if c >= sample:
                break
        print("-- voteMap nodes done --")

    ### Opinion Nodes ###
    if opinion_bool == True:

        c = 0
        for i in users_data:
            c = c + 1
            for k in users_data[i]['opinion_arguments']:
                session.write_transaction(add_opinion, k['opinion title'], k['opinion link'])
            if c % 100 == 0:
                print(c)
            if c >= sample:
                break
        print("-- opinion nodes done --")

    ### Poll Nodes ###
    if poll_bool == True:

        c = 0
        for i in users_data:
            c = c + 1
            for k in users_data[i]['poll_votes']:
                session.write_transaction(add_poll, k['vote title'], k['vote link'])
            if c % 100 == 0:
                print(c)
            if c >= sample:
                break
        print("-- poll nodes done --")

    ### Issues Nodes ###
    if issues_bool == True:

        c = 0
        for i in users_data:
            c = c + 1
            issuesID = i + '_issues'
            k = users_data[i]['big_issues_dict']
            #print(issuesID, k['Abortion'])
            session.write_transaction(add_issues, issuesID, k['Abortion'], k['Affirmative Action'], k['Animal Rights'], k['Barack Obama'], k['Border Fence'], k['Capitalism'], k['Civil Unions'],
                                      k['Death Penalty'], k['Drug Legalization'], k['Electoral College'], k['Environmental Protection'], k['Estate Tax'], k['European Union'], k['Euthanasia'],
                                      k['Federal Reserve'], k['Flat Tax'], k['Free Trade'], k['Gay Marriage'], k['Global Warming Exists'], k['Globalization'], k['Gold Standard'], k['Gun Rights'],
                                      k['Homeschooling'], k['Internet Censorship'], k['Iran-Iraq War'], k['Labor Union'], k['Legalized Prostitution'], k['Medicaid & Medicare'], k['Medical Marijuana'],
                                      k['Military Intervention'], k['Minimum Wage'], k['National Health Care'], k['National Retail Sales Tax'], k['Occupy Movement'], k['Progressive Tax'],
                                      k['Racial Profiling'], k['Redistribution'], k['Smoking Ban'], k['Social Programs'], k['Social Security'], k['Socialism'], k['Stimulus Spending'], k['Term Limits'],
                                      k['Torture'], k['United Nations'], k['War in Afghanistan'], k['War on Terror'], k['Welfare'])
            if c % 100 == 0:
                print(c)
            if c >= sample:
                break
        print("-- issues nodes done --")

    print("-- Nodes done --")


    ###------------###
    ### User Edges ###
    ###------------###

    ### User Edge - friends_with ###
    if friends_with_bool == True:

        c = 0
        for i in users_data:
            c = c + 1
            if (users_data[i]['friends'] != []):
                if (users_data[i]['friends'] != "private"):                         #todo represent them in the database as node feature friendship: private
                    for k in users_data[i]['friends']:
                        if k in userList:
                            session.write_transaction(add_friends_with, i, k)
            if c % 100 == 0:
                print(c)
            if c >= sample:
                break
        print("-- user edges - friends_with done --")


    ### User Edges - debates_in ###
    if debates_in_bool == True:

        c = 0
        for i in debates_data:
            c = c + 1
            forfeit_bool1 = False
            winning_bool1 = False
            forfeit_bool2 = False
            winning_bool2 = False

            if debates_data[i]['participant_1_name'] in userList:
                if debates_data[i]['forfeit_side'] == debates_data[i]['participant_1_name']:
                    forfeit_bool1 = True
                if debates_data[i]['participant_1_status'] == "Winning":
                    winning_bool1 = True
                session.write_transaction(add_debates_in, debates_data[i]['participant_1_name'], i, forfeit_bool1, winning_bool1, debates_data[i]['participant_1_position'])     #todo check if there is inconsistency in participants and user.json

            if debates_data[i]['participant_2_name'] in userList:
                if debates_data[i]['forfeit_side'] == debates_data[i]['participant_2_name']:
                    forfeit_bool2 = True
                if debates_data[i]['participant_2_status'] == "Winning":
                    winning_bool2 = True
                session.write_transaction(add_debates_in, debates_data[i]['participant_2_name'], i, forfeit_bool2, winning_bool2, debates_data[i]['participant_2_position'])     #todo check if there is inconsistency in participants and user.json

            if c % 100 == 0:
                print(c)
            if c >= sample:
                break
        print("-- user edges - debates_in done --")


    ### User Edge - gives_comment ###
    if gives_comment_bool == True:

        c = 0
        for i in debates_data:
            c = c + 1
            c2 = 0
            for k in debates_data[i]['comments']:
                c2 = c2 + 1
                commentID = str(str(i) + '_Comment_' + str(c2))
                session.write_transaction(add_gives_comment, k['user_name'], commentID)
            if c % 100 == 0:
                print(c)
            if c >= sample:
                break
        print("-- user edge - gives_comment done --")


    ### User Edge - gives_argument ###
    if gives_argument_bool == True:

        c = 0
        for i in debates_data:
            c = c + 1
            c2 = 0
            for k in debates_data[i]['rounds']:
                c2 = c2 + 1
                for p in k:
                    argumentID = str(str(i) + "_round_" + str(c2) + "_" + str(p['side']))
                    if p['side'] == "Pro":
                        UserID = debates_data[i]['participant_1_name']  # participant_1_position is always "Pro"
                    else:
                        UserID = debates_data[i]['participant_2_name']
                    session.write_transaction(add_gives_argument, UserID, argumentID)
            if c % 100 == 0:
                print(c)
            if c >= sample:
                break
        print("-- user edge - gives_argument done --")


    ### User Edge - gives_voteMap ###
    if gives_votemap_bool == True:

        c = 0
        for i in debates_data:
            c = c + 1
            c2 = 0
            for k in debates_data[i]['votes']:
                c2 = c2 + 1
                c3 = 0
                for p in k['votes_map']:
                    if c3 == 2:  # VoteMaps consist of 3 parts. Bools of votes given to participant1, to participant2 and a redundant part 3 called tied with the same variables that are simply the first two variables connected with an logic AND
                        break
                    votemapID = str(str(i) + '_' + str(k['user_name']) + '_' + str(p))
                    #print('called in extraction: ', k['user_name'], votemapID)
                    session.write_transaction(add_gives_voteMap, k['user_name'], votemapID)
                    c3 = c3 + 1
            if c % 100 == 0:
                print(c)
            if c >= sample:
                break
        print("-- User Edge - gives_voteMap done --")

    ### User Edge - gives_opinion ###
    if gives_opinion_bool == True:

        c = 0
        for i in users_data:
            c = c + 1
            for k in users_data[i]['opinion_arguments']:
                session.write_transaction(add_gives_opinion, i, k['opinion title'], k['opinion text'])
            if c % 100 == 0:
                print(c)
            if c >= sample:
                break
        print("-- User Edge - gives_opinion done --")


    ### User Edge - gives_pollvote ###
    if gives_pollvote_bool == True:

        c = 0
        for i in users_data:
            c = c + 1
            for k in users_data[i]['poll_votes']:
                session.write_transaction(add_gives_pollvote, i, k['vote title'], k['vote text'], k['vote explanation'])
            if c % 100 == 0:
                print(c)
            if c >= sample:
                break
        print("-- User Edge - gives_pollvote done --")


    ### User Edge - gives_issues ###
    if gives_issues_bool == True:
        '''insert'''

    ### User Edge - user_timeline ###
    if user_timeline_bool == True:
        c = 0

        joined_array = np.array([])
        userID_array = np.array([])

        for i in users_data:
            c = c + 1

            #print(users_data[i]['joined'])

            if 'Years'      in users_data[i]['joined'] or 'Year'    in users_data[i]['joined']:
                if users_data[i]['joined'][1] != ' ':
                    joined_days = int(users_data[i]['joined'][0:2]) * 365
                    #print('yes')
                    #print(int(users_data[i]['joined'][0:2]))
                else:
                    joined_days = int(users_data[i]['joined'][0]) * 365
                    #print('no')

            elif 'Months'   in users_data[i]['joined'] or 'Month'   in users_data[i]['joined']:
                if users_data[i]['joined'][1] != ' ':
                    joined_days = int(users_data[i]['joined'][0:2]) * 30
                else:
                    joined_days = int(users_data[i]['joined'][0]) * 30

            elif 'Weeks'    in users_data[i]['joined'] or 'Week'    in users_data[i]['joined']:
                if users_data[i]['joined'][1] != ' ':
                    joined_days = int(users_data[i]['joined'][0:2]) * 7
                else:
                    joined_days = int(users_data[i]['joined'][0]) * 7

            elif 'Days'     in users_data[i]['joined'] or 'Day'     in users_data[i]['joined']:
                if users_data[i]['joined'][1] != ' ':
                    joined_days = int(users_data[i]['joined'][0:2])
                else:
                    joined_days = int(users_data[i]['joined'][0])

            else:
                joined_days = 'unidentified joined period'

            #print(joined_days)

            userID_array = np.append(userID_array, i)
            joined_array = np.append(joined_array, joined_days)

            if c % 100 == 0:
                print(c)
            if c >= sample:
                break


        sort_joined_array_index = np.argsort(joined_array)

        sort_joined_array = joined_array[sort_joined_array_index]
        sort_userID_array = userID_array[sort_joined_array_index]

        sort_joined_array_unique = np.unique(sort_joined_array)

        for i in range(len(sort_joined_array_unique)-1):

            focal_date = sort_joined_array_unique[i]
            next_date = sort_joined_array_unique[i+1]

            focal_date_index = np.where(sort_joined_array == sort_joined_array_unique[i])
            next_date_index = np.where(sort_joined_array == sort_joined_array_unique[i+1])

            for userID in sort_userID_array[focal_date_index]:
                for prevuserID in sort_userID_array[next_date_index]:
                    #print('focal: ', sorted_day_array[focal_date_index], 'next: ', sorted_day_array[next_date_index])
                    session.write_transaction(add_user_timeline, prevuserID, userID)  # -[Before]->

    ###--------------###
    ### Debate Edges ###
    ###--------------###

    ### Debate Edge - has_comment ###
    if has_comment_bool == True:

        c = 0
        for i in debates_data:
            c = c + 1
            c2 = 0
            for k in debates_data[i]['comments']:
                c2 = c2 + 1
                commentID = str(str(i) + '_Comment_' + str(c2))
                session.write_transaction(add_has_comment, i, commentID)
            if c % 100 == 0:
                print(c)
            if c >= sample:
                break
        print("-- debate edge - has_comment done --")


    ### Debate Edge - has_votemap ###
    if has_votemap_bool == True:

        c = 0
        for i in debates_data:
            c = c + 1
            c2 = 0
            for k in debates_data[i]['votes']:
                c2 = c2 + 1
                c3 = 0
                for p in k['votes_map']:
                    if c3 == 2:  # VoteMaps consist of 3 parts. Bools of votes given to participant1, to participant2 and a redundant part 3 called tied with the same variables that are simply the first two variables connected with an logic AND
                        break
                    votemapID = str(str(i) + '_' + str(k['user_name']) + '_' + str(p))
                    print(i, votemapID)
                    session.write_transaction(add_has_voteMap, i, votemapID)

                    c3 = c3 + 1
            if c % 100 == 0:
                print(c)
            if c >= sample:
                break
        print("-- Debate Edge - has_votemap done --")


    ### Debate Edge - has_argument ###
    if has_argument_bool == True:

        c = 0
        for i in debates_data:
            c = c + 1
            c2 = 0
            for k in debates_data[i]['rounds']:
                c2 = c2 + 1
                for p in k:
                    UserID = ""
                    argumentID = str(str(i) + "_round_" + str(c2) + "_" + str(p['side']))
                    session.write_transaction(add_has_argument, i, argumentID)
            if c % 100 == 0:
                print(c)
            if c >= sample:
                break
        print("-- debate edge - has_argument done --")


    ### Debate Edge - debate_timeline ###
    if debate_timeline_bool == True:
        c = 0
        #debate_timeline_array = np.array([[], []])
        debate_day_array = np.array([], dtype='datetime64')
        debate_title_array = np.array([])

        for i in debates_data:
            c = c + 1

            debate_day = datetime.strptime((debates_data[i]['start_date']), '%m/%d/%Y').date()
            debate_day_array = np.append(debate_day_array, debate_day)
            debate_title_array = np.append(debate_title_array, [i])
            sort_order_array = np.argsort(debate_day_array)


            if c % 100 == 0:
                print(c)
            if c >= sample:
                break

        sort_order_array = np.argsort(debate_day_array)

        sorted_title_array = debate_title_array[sort_order_array]
        sorted_day_array = debate_day_array[sort_order_array]
        sorted_day_array_unique = np.unique(debate_day_array[sort_order_array])
        #print(sorted_day_array_unique)
        #print(sorted_day_array_unique[0])

        for i in range(len(sorted_day_array_unique)-1):

            focal_date = sorted_day_array_unique[i]
            next_date = sorted_day_array_unique[i+1]

            focal_date_index = np.where(sorted_day_array == sorted_day_array_unique[i])
            next_date_index = np.where(sorted_day_array == sorted_day_array_unique[i+1])

            #print(i)
            #print(focal_date_index)

            #print(sorted_day_array[focal_date_index])
            #print(sorted_title_array[focal_date_index])

            for debateID in sorted_title_array[focal_date_index]:
                for prevdebateID in sorted_title_array[next_date_index]:
                    #print('focal: ', sorted_day_array[focal_date_index], 'next: ', sorted_day_array[next_date_index])
                    session.write_transaction(add_debate_timeline, prevdebateID, debateID)  # -[Before]->




    ###---------------###
    ### Comment Edges ###
    ###---------------###

    ### Comment Edge - comment_timeline ###
    if comment_timeline_bool == True:

        c = 0
        created_array = np.array([])
        commentID_array = np.array([])

        for i in debates_data:
            c = c + 1
            c2 = 0
            for k in debates_data[i]['comments']:
                c2 = c2 + 1
                commentID = str(str(i) + '_Comment_' + str(c2))

                print(k['time'])

                if 'years'      in k['time'] or 'year'    in k['time']:
                    if k['time'][1] != ' ':
                        created_days = int(k['time'][0:2]) * 365
                        #print('yes')
                        #print(int(users_data[i]['joined'][0:2]))
                    else:
                        created_days = int(k['time'][0]) * 365
                        #print('no')

                elif 'months'   in k['time'] or 'month'   in k['time']:
                    if k['time'][1] != ' ':
                        created_days = int(k['time'][0:2]) * 30
                    else:
                        created_days = int(k['time'][0]) * 30

                elif 'weeks'    in k['time'] or 'week'    in k['time']:
                    if k['time'][1] != ' ':
                        created_days = int(k['time'][0:2]) * 7
                    else:
                        created_days = int(k['time'][0]) * 7

                elif 'days'     in k['time'] or 'day'     in k['time']:
                    if k['time'][1] != ' ':
                        created_days = int(k['time'][0:2])
                    else:
                        created_days = int(k['time'][0])

                else:
                    created_days = 'unidentified created period'

                #print(joined_days)

                commentID_array = np.append(commentID_array, commentID)
                created_array = np.append(created_array, created_days)

            if c % 100 == 0:
                print(c)
            if c >= sample:
                break


        sort_created_array_index = np.argsort(created_array)

        sort_created_array = created_array[sort_created_array_index]
        sort_comment_array = commentID_array[sort_created_array_index]

        sort_created_array_unique = np.unique(sort_created_array)

        print(sort_created_array)
        print(sort_comment_array)

        for i in range(len(sort_created_array_unique)-1):

            focal_date = sort_created_array_unique[i]
            next_date = sort_created_array_unique[i+1]

            focal_date_index = np.where(sort_created_array == sort_created_array_unique[i])
            next_date_index = np.where(sort_created_array == sort_created_array_unique[i+1])

            for commentID in sort_comment_array[focal_date_index]:
                for prevcommentID in sort_comment_array[next_date_index]:
                    #print('focal: ', sorted_day_array[focal_date_index], 'next: ', sorted_day_array[next_date_index])
                    session.write_transaction(add_comment_timeline, prevcommentID, commentID)  # -[Before]->
                    print(prevcommentID, commentID)



    ###---------------###
    ### VoteMap Edges ###
    ###---------------###

    ### VoteMap Edge - refers_to ###
    if refers_to_bool == True:

        c = 0
        for i in debates_data:
            c = c + 1
            c2 = 0
            for k in debates_data[i]['votes']:
                c2 = c2 + 1
                c3 = 0
                for p in k['votes_map']:
                    if c3 == 2:                               # VoteMaps consist of 3 parts. Bools of votes given to participant1, to participant2 and a redundant part 3 called tied with the same variables that are simply the first two variables connected with an logic AND
                        break
                    votemapID = str(str(i) + '_' + str(k['user_name']) + '_' + str(p))
                    #print(votemapID, p)
                    session.write_transaction(add_refers_to, votemapID, p)
                    c3 = c3 + 1
            if c % 100 == 0:
                print(c)
            if c >= sample:
                break
        print("-- votemap edge - refers_to done --")



    print("-- write done --")

#######################
### Sessions - read ###
#######################

    #session.read_transaction(read_all)

    #session.read_transaction(read_user)                        # ok
    #session.read_transaction(read_debate)                      # ok
    #session.read_transaction(read_comment)                     # ok
    #session.read_transaction(read_argument)                    # ok
    #session.read_transaction(read_voteMap)                     # ok
    #session.read_transaction(read_opinion)                     # ok
    #session.read_transaction(read_poll)                        # ok
    #session.read_transaction(read_issues)                      # ok

    #session.read_transaction(read_friends_with)                # ok
    #session.read_transaction(read_debates_in)                  # ok
    #session.read_transaction(read_gives_comment)               # ok
    #session.read_transaction(read_gives_argument)              # ok
    #session.read_transaction(read_gives_voteMap)               # ok
    #session.read_transaction(read_gives_opinion)               # ok
    #session.read_transaction(read_gives_pollvote)              # ok
    session.read_transaction(read_gives_issues)                # todo
    #session.read_transaction(read_user_timeline)               # ok

    #session.read_transaction(read_has_comment)                 # ok
    #session.read_transaction(read_has_voteMap)                 # ok
    #session.read_transaction(read_has_argument)                # ok
    #session.read_transaction(read_debate_timeline)             # ok

    #session.read_transaction(read_comment_timeline)            # ok
    #session.read_transaction(read_refers_to)                   # ok

    print("-- read done --")
