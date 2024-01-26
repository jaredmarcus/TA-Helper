from decouple import config
from bs4 import BeautifulSoup
from sys import platform
import glob, os
import gdown
import shutil
import os
import os.path
import re
import time
import requests
import git
import gitlab
import base64

GITLAB_TOKEN = str(config('GITLAB_TOKEN'))
GITLAB_PROJECT = int(config('PROJECT_ID'))
GITHUB_REPO = str(config('MAIN_REPO'))
GITLAB_REPO = str(config('GITLAB_REPO'))
SUBDIRECTORY = str(config('SUBDIRECTORY'))

def gitrepo(directory):
    directory = git.Repo(directory)
    current = directory.head.commit
    directory.remotes.origin.pull()
    print(f"\nGithub Repo Latest Commit Hash: {directory.head.commit.hexsha}")
    if current != directory.head.commit:
        print("Github Repo is Outdated! | ❌")
        g = git.cmd.Git(directory)
        g.pull()
        print("Github Repo Updated!")
        directory = git.Repo(directory)
        current = directory.head.commit
        print(f"Github Local Repo Hash: {current.hexsha}")
    else:
        print(f"Github Local Repo is Current! ✅ | Hash: {current.hexsha}")

def gitlrepo(directory):
    gl = gitlab.Gitlab(url='https://git.bootcampcontent.com', private_token=GITLAB_TOKEN)
    gl.auth()
    project = gl.projects.get(GITLAB_PROJECT)
    most_recent_commit = project.commits.list(get_all=True)
    repo_commit_hash = most_recent_commit[0].id
    print(f"\nGitlab Repo Latest Commit Hash: {most_recent_commit[0].id}")

    repo_directory = directory
    repo_directory = git.Repo(repo_directory)
    current = repo_directory.head.commit
    repo_directory.remotes.origin.pull()
    local_commit_hash = repo_directory.head.commit.hexsha
    if current.hexsha != local_commit_hash:
        print("Gitlab Repo is Outdated! | ❌")
        project.mirror_pull
        print("Gitlab Updated!")
    else:
        print(f"Gitlab Local Repo is Current! ✅ | Hash: {current.hexsha}\n")

    ## FIND STUDENT GUIDES
    # METHOD 1
    # with open("student_guides.txt", 'w') as o:
    #     for root, dirs, files in os.walk(directory):
    #         for file in files:
    #             if file.endswith('.md') and "studentguide" in file.lower():
    #                 file_path = os.path.join(root, file)
    #                 print(file_path)
    #                 file_path = file_path.split("/")
    #                 file_path = (file_path[2])
    #                 file_path = file_path.replace('\\', '/')
    #                 base_gitlab_url = "BOOTCAMP_BASE_URL"
    #                 new_url = f"{base_gitlab_url}{file_path}"
    #                 o.write(str(new_url))
    #                 o.write("\n")
        
    ## METHOD 2
    branch = project.branches.list()[0].name
    local = 0
    remote = 0
    with open("student_guides.txt", 'w') as o:
        for root, dirs, files in os.walk(directory):
            for file in files:
                if file.endswith('.md') and "studentguide" in file.lower():
                    file_path = os.path.join(root, file)
                    # print(file_path)
                    file_path = file_path.split("/")
                    file_path = (file_path[2])
                    file_path = file_path.replace('\\', '/')
                    local+=1
                    try:
                        f = project.files.get(file_path=file_path, ref=branch)
                        repo_base_url = str(f.manager._parent.http_url_to_repo)
                        repo_base_url = repo_base_url.removesuffix(".git")
                        repo_base_url = f"{repo_base_url}/-/blob/main/"
                        new_url = f"{repo_base_url}{f.file_path}"
                        remote+=1
                        o.write(str(new_url))
                        o.write("\n")

                        ## IF YOU WANT TO PRINT CONTENT OF A FILE
                        # file_content = base64.b64decode(f.content).decode("utf-8")
                        # print(file_content.replace('\\n', '\n'))
                    except:
                        "Error"
    print(f"SGs In Local Gitlab Repo: {local}")


    ## SEARCH THROUGH DIRECTORIES ON THE GITLAB REPO & COUNT STUDENT GUIDES
    main_dir = project.repository_tree()
    for item in main_dir:
        sub_dir = project.repository_tree(path=item['path'])
        for item_1 in sub_dir:
            sub_subdir = project.repository_tree(path=item_1['path'])
            for item_2 in sub_subdir:
                if(str(item_2['name']).lower() ==  "studentguide"):
                    remote+=1
    print(f"SGs In Master Gitlab Repo: {remote}\n")

    if local == remote:
        print("LOCAL AMOUNT MATCHES REMOTE AMOUNT OF STUDENT GUIDES! ✅")
    else:
        print("LOCAL AMOUNT DOES NOT MATCH REMOTE AMOUNT OF STUDENT GUIDES! ❌\n")
                    
def extract_google_drive_link(text):
    pattern = r'\[(.*?)\]\((https://docs\.google\.com/presentation/d/[A-Za-z0-9_-]+)'
    match = re.search(pattern, text)
    
    if match:
        return match.group(2)
    else:
        return None
    
def extract_links_from_directory(directory):
    links = []
    ## RECREATE FILE (CLEAR CONTENTS)
    open("slide_links.txt", "w").close()
    
    with open("slide_links.txt", 'w') as o:
        for root, dirs, files in os.walk(directory):
            for file in files:
                if file.endswith('.md') and "lessonplan" in file.lower():
                    file_path = os.path.join(root, file)
                    
                    with open(file_path, 'r', encoding="mbcs") as f:
                        text = f.read()
                        link = extract_google_drive_link(text)
                        
                        if link:
                            links.append(link)
                            o.write(str(link))
                            o.write("\n")
        
def url_to_id(url):
    x = url.split("/")
    return x[5]

def namesplit(page_title):
    x = page_title.split(" - ")
    return x[0]

def downloader():
    ## CLEAR COOKIES PRIOR TO DOWNLOAD
    if platform == "win32": ## WINDOWS
        username = os.getenv('username')
        Cookie_path = f"C:/Users/{username}/.cache/gdown/cookies.txt"
        check_file = os.path.isfile(Cookie_path)
        if check_file == True:
            ## RECREATE FILE (CLEAR CONTENTS)
            open(Cookie_path, "w").close()
            ## WRITE TO FILE WITH NEW CONTENT
            with open(Cookie_path, "w") as c:
                c.write("# Netscape HTTP Cookie File\n")
                c.write("# http://curl.haxx.se/rfc/cookie_spec.html\n")
                c.write("# This is a generated file!  Do not edit.\n")

    ## NEED TO WORK ON THIS SECTION ###
    #elif platform == "darwin": ##MAC OS
    
    #elif platform == "linux": ##LINUX


    with open("slide_links.txt", 'r') as o:
        Lines = o.readlines()
        count = 0
        num = 1

        ## Clear Contents of Folder
        folder = "./Slide_Folder"
        if not os.path.exists(folder):
            os.mkdir(folder) 
        for filename in os.listdir(folder):
            file_path = os.path.join(folder, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                print('Failed to delete %s. Reason: %s' % (file_path, e))


        for line in Lines:
            ## DOWNLOAD FILES TO ROOT
            count+= 1
            if count <= len(Lines):
                print(f"\nDownloading File {count}/{len(Lines)}")
                url = line.rstrip('\n')

                ## OBTAIN OG NAME FOR FILE
                reqs = requests.get(url)
                soup = BeautifulSoup(reqs.text, 'html.parser')
                
                for title in soup.find_all('title'):
                    scraped_title = str(title.get_text())
                    scraped_title = scraped_title.replace(':', '')
                    clean_title = namesplit(scraped_title)

                clean_url = f"https://docs.google.com/uc?id={url_to_id(url)}"
                gdown.download(clean_url, quiet=False, format="pdf", output=f"{clean_title}.pdf")
                time.sleep(3)
            
                ## MOVE FILES TO PROPER FOLDER
                source_dir = './'
                dest_dir = './Slide_Folder/'

                for fname in os.listdir(source_dir):
                    if fname.lower().endswith('.pdf'):
                        print(f"{num}. {fname}")
                        num+=1
                        shutil.move(os.path.join(source_dir, fname), dest_dir)

if __name__ == '__main__':
    mainrepo = f"./{GITHUB_REPO}/"
    gitlabrepo = f"./{GITLAB_REPO}/"
    sub_directory = f"./{GITHUB_REPO}/{SUBDIRECTORY}"
    gitrepo(mainrepo)
    gitlrepo(gitlabrepo)
    extract_links_from_directory(sub_directory)
    downloader()