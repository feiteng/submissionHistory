import requests, json, time, collections, git, os, subprocess


def getSubmission(USERNAME, CSRF_Token):
    print('Getting submission..')
    COOKIE = 'csrftoken=' + CSRF_Token
    X_CSRFTOKEN = CSRF_Token
    url = 'https://leetcode.com/graphql'
    headers = {
            'referer': 'https://leetcode.com/accounts/login/',
            'cookie' : COOKIE,
            'x-csrftoken' : X_CSRFTOKEN
        }
    data = {
        "operationName":"getRecentSubmissionList",
        "variables":'{"username":"' + USERNAME + '"}',
        "query":"query getRecentSubmissionList($username: String!, $limit: Int) {\n  recentSubmissionList(username: $username, limit: $limit) {\n    title\n    titleSlug\n    timestamp\n    statusDisplay\n    lang\n    __typename\n  }\n  languageList {\n    id\n    name\n    verboseName\n    __typename\n  }\n}\n"
    }

    resptext = json.loads(requests.post(url, headers = headers, data = data).text)
    submissionList = resptext['data']['recentSubmissionList']
    successful_submission_result = collections.defaultdict(dict)
    for each_submission in submissionList:
        questionTitle = each_submission['title']
        submissionStatus = each_submission['statusDisplay']
        if not submissionStatus == 'Accepted': continue
        timeStamp = each_submission['timestamp']
        ctime = time.ctime((int)(timeStamp))
        successful_submission_result[USERNAME][questionTitle] = ctime
    print('Successfully crawled submission..')
    return successful_submission_result

def readToken():
    with open('CSRF_TOKEN', 'r') as f:
        return f.readline()

def writeToFile(subsmission):
    banner = '|User Handle|Question|Last Successful Submission|\n|-|-|-|\n'
    f = open('submission_result.md', 'w')
    f.write(banner)
    for name in subsmission:
        for question in subsmission[name]:
            timestamp = subsmission[name][question]
            f.write(name + '|' + question + '|' + timestamp + '\n')
    f.close()

def commit_and_pushtoGithub(gitURL, file)
    curTime = time.localtime()    
    cur_time = time.strftime('%Y %b %H:%M %p %z', curTime)
    commit_message = 'auto committed on ..' + cur_time
    
    print('Trying to push..')

    push_successful = True
    try:
        subprocess.call(['git', 'add' , file])
        subprocess.call(['git', 'commit' , '-m', commit_message])
        subprocess.call(['git', 'push'])
    except Error:
        push_successful = False
        print(Error)
        pass
    
    if push_successful:
        print("Successful..")


CSRF_Token = readToken()

USERNAME = 'xianglaniunan'

while True:
    # submissionList = getSubmission(USERNAME=USERNAME, CSRF_Token=CSRF_Token)
    # writeToFile(submissionList)
    commit_and_pushtoGithub(remoteURL, 'submission_result.md')
    break
    # sleep for 60 minutes
    # time.sleep(60 * 60)

