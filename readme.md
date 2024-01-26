<div align="center">
  <h1>edX Bootcamp Staff Helper</h1>
  <p><b>Teaching Assistant Helper | Time = Efficient</b></p>
  <img src="https://upload.wikimedia.org/wikipedia/commons/thumb/c/cd/EdX_newer_logo.svg/1200px-EdX_newer_logo.png" width="50%">
  <br>
  <br>
</div>
After about 4 cohorts as a TA with the pain of going to each gitlab repo for the class to find student guide links and then finding the link to the google slides and then downloading them. This script does it for you. Scripts = efficiency

This script was made to ease the task of being a TA at the bootcamps. Features:
- **Check Master Cirriculum Repo (via git API)** Check if the hashes match, otherwise pull down
- **Check Classes Cirriculum Repo (via Gitlab API)** Check if the hashes match, otherwise pull down
- **Scrape Links To StudentGuides.md & Lecture Slides** Via the repos, scrape for google presentation links, as well as finding student guides present within the repository tree.
- **Download Lecture Slides** Find google slide links and download the files as a PDF for easy upload to our class's slack

## Features
The main feature of the script is to obtain links to the studentguides hosted on gitlab as well as find the google slide presentation links and download them. 
1. What happens first is checking if the repos (Github/Gitlab) are current, if not pull the latest down.
2. The script will scrape through the class repository (from Gitlab) to parse through the repository tree to find all `StudentGuides.md` to put together the file structure of where the student guides are found generating a valid links in `student_guides.txt` by add the file structure to the base Gitlab link for the repository. For a sanity check to ensure all our student guides are found, the script will count through each the local repository and the origin to ensure none are missed. If so the script will prompt that.
3. The script will then scrape through the master cirriculum repository (the local pulled Github repo) to find all `lessonplan.md`. Once a the file is found, it will scrape within the file to pull out a google presentation file via regex and output it to a file called `slide_links.txt`.  
4. Lastly it will begin downloading each of the PDFs via the Gdown API. There was an issue I encountered when utilizing the package, where sometimes it would crash due to a cookie error, so the fix I found was to clear our cookie cache. (`C:/Users/{username}/.cache/gdown/cookies.txt` | Note. the script does this, but functionality is limited to windows until I cross-platorm the script. ). Gdown will download to a folder called `Slide_Folder` and delete the contents every run (so I recommend only running this section if you are doing a fresh fresh pull, as this will download all the slides for the entire bootcamp, otherwise doing it once will do the charm). Within this section BS4 is being used to be able to pull the title of the file to be able to save the downloaded PDF as that name. Note that gdown has a special formatting to utilize its api which is `https://docs.google.com/uc?id=<DOCUMENT_ID>}` but does lead to the presentation link we are wanting and we can export to our desired format. The PDF downloads to the root of the CWD, but then places it in `Slide_Folder` upon finish. 

## Working OS

 - Windows - ✅
 - Linux - ❌
 - MacOS - ❌

## Installation
```bash
pip install -r requirements.txt
```
### Packages Utilized
 - [Python-Gitlab](https://github.com/python-gitlab/python-gitlab) - Python wrapper for Gitlab API
 - [GitPython](https://github.com/gitpython-developers/GitPython) - Python wrapper for Git API
 - [BS4](https://pypi.org/project/beautifulsoup4/) - A library to scrape webpages for info
 - [Gdown](https://github.com/wkentaro/gdown) - A google drive public file/folder downloader
 - [Python-decouple](https://github.com/HBNetwork/python-decouple) - A better way to organize settings

## Enviromental Variables

    GITLABTOKEN=<Your_Personal_Access_Token>
    PROJECT_ID=<PID>
    MAINREPO=<file_location_for_master_cirriculum_repo>
    GITLAB_REPO=<file_location_for_class_cirriculum_repo>
    SUBDIRECTORY=<file_location_within_main_repo_housing_lesson_plans>

### Help With Enviromental Variables
 - `GITLABTOKEN` - https://docs.gitlab.com/ee/user/profile/personal_access_tokens.html
 - `PROJECT_ID` - Usually found at the bottom of the repo name\
   ![Link To Example](https://i.stack.imgur.com/u0K4w.png)
 - `MAINREPO`- This will just be the file location within your cwd
 - `GITLAB_REPO` - This will just be the file location within your cwd
 - `SUBDIRECTORY` - This will just be the file location within the mainrepo housing our curriculum within your cwd
