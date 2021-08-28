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

def commit_and_pushtoGithub(gitURL, file, username, userpass):
    curTime = time.localtime()    
    cur_time = time.strftime('%Y %b %H:%M:%S', curTime)
    commit_message = 'auto committed on ..' + cur_time
    
    print('Trying to push..')

    subprocess.call(['git', 'add' , file])
    subprocess.call(['git', 'commit' , '-m', commit_message])
    pushURL = 'https://{}:{}{}'.format(username, userpass, gitURL)
    # print(pushURL)
    subprocess.call(['git', 'push'])#, pushURL])

    
    # path = os.getcwd()
    # # print(path)
    # repo = git.Repo(path)
    # username = username
    # password = userpass
    
    
    # repo.index.add(file)    
    
    
    # origin = repo.remote('origin')
    # origin.push()
    print("Successful..")


CSRF_Token = readToken()

USERNAME = 'xianglaniunan'

while True:
    # submissionList = getSubmission(USERNAME=USERNAME, CSRF_Token=CSRF_Token)
    # writeToFile(submissionList)
    remoteURL = '@github.com/feiteng-gcp/submissionHistory.git'
    username = 'feiteng-gcp'
    # userpass = ''
    userpass = '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'

    commit_and_pushtoGithub(remoteURL, 'submission_result.md',username, userpass)
    break
    # sleep for 60 minutes
    # time.sleep(60 * 60)

