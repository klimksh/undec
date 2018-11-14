#!/usr/bin/env python
import getch as g
from pymongo import MongoClient

import pprint 
import requests
from jira import JIRA
import sys


def wait():
    g.getch()


def load_all_decisions(db):
	jira = JIRA("https://issues.apache.org/jira")
	issues_in_proj = jira.search_issues("project=SPARK", maxResults=1, json_result=True)
	total = issues_in_proj["total"]
	print(total)
	counter = 0
	while total > 0:
		if total <50:
    			issues_in_proj = jira.search_issues("project=SPARK", startAt=counter, maxResults=50+total, json_result=True)
		else:
    			issues_in_proj = jira.search_issues("project=SPARK", startAt=counter, maxResults=50, json_result=True)
		total -= 50
		
		db.decisions.insert_many(issues_in_proj["issues"])
		print("Processed %d"%counter);
		print("left %d"%total);
		counter += 50

def update_decisions(db):
	jira = JIRA("https://issues.apache.org/jira")		
	for d in get_decisions(db):
		db.decisions.find_one_and_update(
					{'id':d['id'] }, 
					{ '$set':{
								# 'description':jira.issue(d['issueId']).fields.description, 
								'jira_type':jira.issue(d['key']).fields.issuetype.name 
							} 
					},
					upsert=True)

def update_issue_with_comment(db):
    jira = JIRA("https://issues.apache.org/jira")
    for d in get_decisions_range(db, 3098, 7206):
        try:
            print(d['key'])
            db.decisions.find_one_and_update(
            {'id':d['id'] }, 
            { '$set':{
                    # 'description':jira.issue(d['issueId']).fields.description, 
                    'comments':[c.raw for c in jira.issue(d['key']).fields.comment.comments] 
                } 
            },
            upsert=True)
        except Exception as e:
            print(e)
        finally:
            pass


def get_decisions(db):
	return [d for d in db.decisions.find()]

def get_decisions_filtered(db):
	return [d for d in db.decisions.find({'fields.created':{'$gte':"2017-01-01"}})]


def get_decisions_range(db, begin, end):
    decisions = []
    for i in range(begin,end):
        decisions.append(db.decisions.find_one({'key':"SPARK-"+str(i)}))
    return decisions


def annotate_decisions(decisions):
	total_annotated = 0
	for r in decisions:
		for k, v in r.items():
			try:
				if not v['error']:
					total_annotated+=1
					db.decisions.find_one_and_update(
						{'id':k }, 
						{ '$set':{
									'description_annotations':v['data'], 
									'description_numberOfSentences':v['numOfSentences'], 
								} 
						},
						upsert=True)
				else:
					print("Error:%s, data: %s"%(k,v))
			except:
				print("Unexpected error:", sys.exc_info()[0])
	print ("Total number of desicions annotated in db:%d" % (total_annotated))

if __name__ == '__main__':
    db = connect_to_mongo()
    decisions = get_decisions_filtered(db)
    print ("Total number of desicions:%d"%(len(decisions)))
    # for d in decisions:
    # 	print(d['fields']['description'])
    # annotate_decisions([{ d['id'] : requests.post('http://127.0.0.1:5000/api', 
    #   json = {
    #       "text":d['fields']['description'], 
    #       "fields":["begin","end", "lemma", "token", "pos", "tag", "deps", "sentence_index", "ner"], 
    #       "ners":["UNCERTAINTY", "DATE", "ORG", "PRODUCT", "LANGUAGE", "PERCENT", "TIME", "QUANTITY", "ORDINAL"]
    #   }
    #   ).json()} for d in decisions])
    print([d for d in decisions])    
    #load_all_decisions(db)     
    #update_issue_with_comment(db)
    print("END")
    wait()
	
