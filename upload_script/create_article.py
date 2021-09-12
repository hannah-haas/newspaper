from docx import *
import sys
import gspread
import pandas as pd
from oauth2client.service_account import ServiceAccountCredentials


if len(sys.argv) < 9:
    print("make sure to include arguments: path to article, related article num 1, related article num 2, cover image, image 1, image 2 etc")
    sys.exit()

# define the scope
scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']

# add credentials to the account
creds = ServiceAccountCredentials.from_json_keyfile_name('credentials.json', scope)

# authorize the clientsheet
client = gspread.authorize(creds)

# get the instance of the Spreadsheet
sheet = client.open('Article Tracksheet')

# get the first sheet of the Spreadsheet
sheet_instance = sheet.get_worksheet(1)
records_data = sheet_instance.get_all_records()
print(records_data)


article_path = str(sys.argv[1])
related_article1 = str(sys.argv[2])
related_article2 = str(sys.argv[3])
cover_image = str(sys.argv[4])
article_filename = sys.argv[5]
images = sys.argv[6:]

document = Document('article_to_upload.docx')

paragraphs = document.paragraphs

article_title = paragraphs[0].text
article_genre = paragraphs[1].text

if paragraphs[2].text[0:2] == "By":
    splits = paragraphs[2].text.split(',')
    author = splits[0][3:]
    author_role = splits[1][1:]

elif paragraphs[3].text[0:2] == "By":
    splits = paragraphs[3].text.split(',')
    author = splits[0][3:]
    print(splits)
    author_role = splits[1][1:]

counter = 0
after_published = False
after_prelude = False
for para in paragraphs:
    counter += 1
    # print(para.text)
    text_group = para.text.split()
    if text_group:
        if text_group[0] == "Published":
            date = para.text[10:]
            after_published = True
            continue

    if after_published and not after_prelude:
        if para.text:
            prelude = para.text
            after_prelude = True
            break

print(article_title)
print(article_genre)
print(author)
print(author_role)
print(date)
print(prelude)
print(article_path)
print(cover_image)
print(images)
print(counter)

author_path = author.split()
author_path = author_path[0].lower() + "_" + author_path[1].lower()


genre_split = article_genre.split("|")
print(genre_split[0][:-1])

if genre_split[0][:-1] == "Environment":
    navigating = "../../../"
    if genre_split[1][1:] == "Tundras and Poles":
        navigating = "../../"
else:
    navigating = "../../"

print(navigating)


content = "<!DOCTYPE html>\n<html>\n<head>"

newHTMLFile = open('test_new.html', 'w')
newHTMLFile.write(content)

content = "\n  <title>"+ article_title + "</title>"
newHTMLFile.write(content)

content = '\n  <link href="%shome_style.css" rel="stylesheet" />' % navigating
newHTMLFile.write(content)

content = '\n  <link href="%sindividual_article.css" rel="stylesheet" />' % navigating
newHTMLFile.write(content)

content = "\n  <link href='https://fonts.googleapis.com/css?family=Spectral' rel='stylesheet'>\n  <link href='https://fonts.cdnfonts.com/css/glacial-indifference-2' rel='stylesheet'>\n  <meta name='viewport' content='width=device-width'>\n  <link rel='icon' href='https://the-kingfisher.org/static_images/Withoutbackground.png'>\n  <meta http-equiv='content-type' content='text/html; charset=utf-8' />\n"
newHTMLFile.write(content)

content = '\n  <!-- for facebook -->\n  <link rel="image_src" href="images/%s" />\n' % cover_image
newHTMLFile.write(content)

content = '\n  <!-- for twitter -->\n  <meta name="twitter:card" content="summary_large_image" />\n  <meta name="twitter:title" content="%s" />' % article_title
newHTMLFile.write(content)

content = '\n  <meta name="twitter:description" content="%s" />' % prelude
newHTMLFile.write(content)

path_to_photo = article_path + "images/" + cover_image
content = '\n  <meta name="twitter:image" content="%s">\n  <meta name="twitter:image:src" content="%s">\n  <meta name="twitter:url" content="encodeURIComponent(document.URL)" />\n' % (path_to_photo, path_to_photo)
newHTMLFile.write(content)

content = "\n  <!-- for linkedin -->\n  <meta property='og:title' content='%s' />" % article_title
newHTMLFile.write(content)

content = '\n  <meta property="og:description" content="%s" />' % prelude
newHTMLFile.write(content)

content = "\n  <meta property='og:image' content='images/%s' />\n  <meta property='image' content='images/%s' />\n  <meta property='og:image:width' content='500' />\n  <meta property='og:image:height' content='200' />" % (cover_image, cover_image)
newHTMLFile.write(content)

content = "\n</head>\n<body>"
newHTMLFile.write(content)

content = '\n  <div class="container">\n    <div class="logo">\n      <a href="%sindex.html"><img src="%sstatic_images/logo.jpg" alt="logo"></a>\n    </div>' % (navigating, navigating)
newHTMLFile.write(content)

content = '\n    <div class="navbar">\n      <div class="icon-bar" onclick="Show()">\n        <i></i>\n        <i></i>\n        <i></i>\n      </div>'
newHTMLFile.write(content)

content = '\n      <ul id="nav-lists">\n        <li class="close"><span onclick="Hide()">×</span></li>'
newHTMLFile.write(content)

content = '\n        <li><a href="%sindex.html">Home</a></li>\n        <li><a href="%ssustainable_cities/sustainable_leaders.html">Sustainable Leaders</a></li>\n        <li><a href="%senvironment/environment.html">Environment</a></li>\n        <li><a href="%speople/people.html">People</a></li>\n        <li><a href="%swrite_for_us.html">Write For Us</a></li>\n        <li><a href="%sour_mission.html">Our Mission</a></li>\n        <li><a href="%sabout_us.html">About Us</a></li>' % (navigating, navigating, navigating, navigating, navigating, navigating, navigating)
newHTMLFile.write(content)

content = '\n        <li>\n          <form class="form_class" action="%ssearch_results.html" method="GET" autocomplete="off">\n            <input class="searchInput" placeholder="Search..." type="search" name="search">\n            <button style="border:none" type="submit" class="searchButton">\n              <img class="material_icons" src="%sstatic_images/search_icon.png" />\n            </button>\n          </form>\n        </li>\n      </ul>\n    </div>\n  </div>' % (navigating, navigating)
newHTMLFile.write(content)

content = '\n  <div id="main">\n    <div class="content_wrap">'
newHTMLFile.write(content)

content = '\n    <div>\n      <div class="parallax" style="background-image: url(%s);">\n        <div class="center_thing">\n          <div class="article_title_info">\n            <div class="meta">\n            <p class="cover_text_test"> %s</p>\n            <p class="tags"> %s </p>\n          </div>\n        </div>\n      </div>\n    </div>\n  </div>' % ('images/' + cover_image, article_title, article_genre)
newHTMLFile.write(content)

content = '\n      <div class="main_article_content">\n        </br>\n        <p class="author_name"> By <strong> <a style="text-decoration: none; color: grey;" href="%sauthor/%s.html"> %s, </a> </strong> %s </p>' % (navigating, author_path,author, author_role)
newHTMLFile.write(content)

content = '\n        <p class="date"> Published %s\n        <div style="height:30px"></div>\n' % date
newHTMLFile.write(content)

content ='\n        <p style="font-weight: bold;">\n          %s\n        </p>\n        </br>' % prelude
newHTMLFile.write(content)

at_references = False


for para in paragraphs[counter:]:
    text = para.text

    print(text)
    # url = para.url
    # print(url)

    if at_references:
        print("TIME TO DO REFERENCES")
        final = ""
        if len(text.strip()) == 0:
            continue;
        for run in para.runs:
            print(run.text)
            if run.italic:
                final = final + "<i>" + run.text + "</i>"
            elif run.bold:
                final = final + "<strong>" + run.text + "</strong>"
            else:
                print(run.text[0:4])
                if run.text[0:4] == "http":
                    print("LINK!!")
                    final = final + '<a target="_blank" class="reference_link" href="%s">%s</a>' % (run.text, run.text)
                else:
                    final = final + run.text
        content ='\n          <p class="reference_item">\n          %s\n        </p>' % final
        newHTMLFile.write(content)
    elif len(text.strip()) != 0:
        print(text)
        if text[0] == "[": # image
            print("UGHH")
            image_num = text[7]
            print(text)

            if text[9] == "&":
                image_num_2 = text[11]
                content = '\n        <figure>\n          <div style="float:left; width:42.58%; margin-right: 2%; margin-left: 5%">\n            <img style="width:100%" src="images/%s">\n          </div>\n          <div style="float:left; width:45.42%; margin-right: 5%">\n            <img style="width:100%" src="images/%s">\n          </div>\n          <figcaption>\n            %s\n          </figcaption>\n        </figure>' % (images[int(image_num)-1], images[int(image_num_2)-1], text[10:-1])
                newHTMLFile.write(content)
            else:
                content = '\n        <figure>\n          <img class="article_photos" src="images/%s">\n          <figcaption>\n            %s\n      </figcaption>\n    </figure>\n    </br>' % (images[int(image_num)-1], text[10:-1])
                newHTMLFile.write(content)

        elif text[0] == "‘": # highlighted_info_right
            print("highlighted_info_right")
            content = "\n        <p class='highlighted_info_right'>\n          %s\n        </p>\n      </br>" % text
            newHTMLFile.write(content)

        elif text.split()[0] == "References":
            print("REFERENCES")
            at_references = True
            content = '\n        <button type="button" class="collapsible">References</button>\n        <div class="content">'
            newHTMLFile.write(content)
        elif text.split()[0] + " " + text.split()[1] == "Featured Image:":
            print("features images")
            content ='\n        </br>\n          <p>\n          %s\n        </p>\n        </br>' % text
            newHTMLFile.write(content)
        else:

            is_bold = False
            for run in para.runs:
                print(run.text)
                if run.bold:
                    content ='\n        <p style="font-weight: bold;">\n          %s\n        </p>\n        </br>' % text
                    newHTMLFile.write(content)
                    is_bold = True
                    break
            if not is_bold:
                final = ""
                for run in para.runs:
                    print(run)
                    if run.italic:
                        print("ITALIC")
                        final = final + "<i>" + run.text + "</i>"
                    else:
                        final = final + run.text
                content ='\n        <p>\n          %s\n        </p>\n        </br>' % final
                newHTMLFile.write(content)


content ='\n        </div>\n        <hr>'
newHTMLFile.write(content)

content = '\n        <div class="social-container">\n          <a class="share-btn" id="twitter_share" href="https://twitter.com/intent/tweet?" target="_blank" style="font-family: %s" title="Tweet" onclick="window.open(%s + encodeURIComponent(document.title) + %s + encodeURIComponent(document.URL)); return false;">' %  ("'Spectral'", "'https://twitter.com/intent/tweet?text='", "'%20'")
newHTMLFile.write(content)

content = '\n            <img src="%sstatic_images/twitter.png" class="share_image_icon">' % navigating
newHTMLFile.write(content)

content = '\n            <p> Tweet</p>\n          </a>'
newHTMLFile.write(content)

content = '\n          <a class="share-btn" id="facebook_share" href="https://www.facebook.com/sharer/sharer.php?u=&t=" target="_blank" style="font-family: %s" title="Share" onclick="window.open(%s + encodeURIComponent(document.URL) + %s + encodeURIComponent(document.URL)); return false;">' % ("'Spectral'", "'https://www.facebook.com/sharer/sharer.php?u='", "'&t='")
newHTMLFile.write(content)

content = '\n            <img src="%sstatic_images/facebook.png" class="share_image_icon">\n            <p> Share </p>\n          </a>' % navigating
newHTMLFile.write(content)

content = '\n          <a class="share-btn" id="linkedin_share" href="http://www.linkedin.com/shareArticle?mini=true&url=&title=&summary=&source=" target="_blank" style="font-family: %s" title="Post" onclick="window.open(%s + encodeURIComponent(document.URL) + %s + encodeURIComponent(document.title)) ; return false;">' % ("'Spectral'", "'http://www.linkedin.com/shareArticle?mini=true&url='", "'&title='")
newHTMLFile.write(content)

content = '\n            <img src="%sstatic_images/linkedin.png" class="share_image_icon">\n            <p> Post</p>\n          </a>' % navigating
newHTMLFile.write(content)

content = '\n          <a class="share-btn" id="email_share" href=%s target="_blank" style="font-family: %s" title="Email" onclick="window.open(%s + encodeURIComponent(document.title) + %s + encodeURIComponent(document.URL)); return false;">' % ('"mailto:?subject=&body=:%20"', "'Spectral'", "'mailto:?subject='", "'&body='")
newHTMLFile.write(content)

content = '\n            <img src="%sstatic_images/mail.png" class="share_image_icon">\n            <p> Email </p>\n          </a>\n        </div>' % navigating
newHTMLFile.write(content)


content = '\n        <hr class="social_line">\n        <h3 class="related_articles_and_author"> Author </h3>'
newHTMLFile.write(content)

content = '\n        <div class="tested" style="display: flex; width: 100%; margin-top:10px;">\n          <div class="image_group">'
newHTMLFile.write(content)

content = '\n            <a href="%sauthor/%s.html">' % (navigating, author_path)
newHTMLFile.write(content)

content = '\n              <img class="article_author_photo" src="%sstatic_images/%s.jpg">' % (navigating, author_path)
newHTMLFile.write(content)

content = '\n            </a>\n          </div>\n          <div class="article_author_name">'
newHTMLFile.write(content)

content = '\n            <a style="text-decoration: none; color: black;" href="%sauthor/%s.html">'  % (navigating, author_path)
newHTMLFile.write(content)

content = '\n              <b> %s </b>\n            </a>' % author
newHTMLFile.write(content)

content = '\n            <p> %s </p>\n          </div>\n        </div>\n\n        <hr>\n' % author_role
newHTMLFile.write(content)

# RELATED ARTICLES
related_article_1_title = sheet_instance.cell(int(related_article1), 2).value
related_article_1_cover = sheet_instance.cell(int(related_article1), 5).value
related_article_1_path = sheet_instance.cell(int(related_article1), 6).value
related_article_1_genre = sheet_instance.cell(int(related_article1), 3).value + " | " + sheet_instance.cell(int(related_article1), 4).value
related_article_1_html = sheet_instance.cell(int(related_article1), 11).value

related_article_2_title = sheet_instance.cell(int(related_article2), 2).value
related_article_2_cover = sheet_instance.cell(int(related_article2), 5).value
related_article_2_path = sheet_instance.cell(int(related_article2), 6).value
related_article_2_genre = sheet_instance.cell(int(related_article2), 3).value + " | " + sheet_instance.cell(int(related_article2), 4).value
related_article_2_html = sheet_instance.cell(int(related_article2), 11).value



print(related_article_1_title, related_article_1_cover, related_article_1_path, related_article_1_html)
print(related_article_2_title, related_article_2_cover, related_article_2_path, related_article_2_html)

content = '\n        <h3 class="related_articles_and_author"> Related Articles </h3>\n        <div class="related_article_flex_container">'
newHTMLFile.write(content)

content = '\n          <div class="sub_article">\n            <a href="%s%s" style="text-decoration:none;">' % (navigating, related_article_1_path + related_article_1_html)
newHTMLFile.write(content)

content = '\n              <img class="related_article_image" src="%s">' % (navigating + related_article_1_path + "images/" + related_article_1_cover)
newHTMLFile.write(content)

content = '\n              <p class="sub_article_text"> %s </p>' % related_article_1_title
newHTMLFile.write(content)

content = '\n              <p class="sub_article_text2"> %s </p>' % related_article_1_genre
newHTMLFile.write(content)

content = '\n            </a>\n          </div>\n          <div class="sub_article">'
newHTMLFile.write(content)

content = '\n            <a href="%s%s" style="text-decoration:none;">' % (navigating, related_article_2_path + related_article_2_html)
newHTMLFile.write(content)

content = '\n              <img class="related_article_image" src="%s">' % (navigating + related_article_2_path + "images/" + related_article_2_cover)
newHTMLFile.write(content)

content = '\n              <p class="sub_article_text"> %s </p>' % related_article_2_title
newHTMLFile.write(content)

content = '\n              <p class="sub_article_text2"> %s </p>' % related_article_2_genre
newHTMLFile.write(content)

content = '\n            </a>\n          </div>'
newHTMLFile.write(content)

content = '\n          </div>\n          </div>\n          </div>'
newHTMLFile.write(content)

# bottom nav bar

content = '\n      <div id="bottomBar">\n        <div id="explore"> EXPLORE </div>'
newHTMLFile.write(content)

content = '\n        <a href="%sconnect.html" id="connect"> CONNECT </a>\n        <a href="%slegal.html" id="legal"> LEGAL </a>' % (navigating, navigating)
newHTMLFile.write(content)

content = '\n        <div id="empty2"> </div>\n        <div id="follow_us">\n          <p id="ugh"> FOLLOW US: </p>'
newHTMLFile.write(content)

content = '\n          <a href="https://www.facebook.com/theKingfisher.newspaper" target="_blank"><img class="social_media_icon" id="three" src="%sstatic_images/facebook_white.png"></a>' % navigating
newHTMLFile.write(content)

content ='\n          <a href="https://www.instagram.com/thekingfisher.newspaper/" target="_blank"><img class="social_media_icon" id="four" src="%sstatic_images/instagram_white.png"></a>' % navigating
newHTMLFile.write(content)

content ='\n          <a href="https://www.linkedin.com/company/the-kingfisher-newspaper/" target="_blank"><img class="social_media_icon" id="five" src="%sstatic_images/linkedin_white.png"></a>' % navigating
newHTMLFile.write(content)

content ='\n          <a href="https://twitter.com/kingfisher_news" target="_blank"><img class="social_media_icon" id="six" src="%sstatic_images/twitter_new.png"></a>' % navigating
newHTMLFile.write(content)

content = '\n        </div>\n      </div>\n    </div>\n  </div>\n</body>\n</html>'
newHTMLFile.write(content)



#script stuff!
content ='\n<script>\n  var coll = document.getElementsByClassName("collapsible");\n  var i;\n  for (i = 0; i < coll.length; i++) {\n    coll[i].addEventListener("click", function() {\n      this.classList.toggle("active");\n      var content = this.nextElementSibling;\n      if (content.style.maxHeight) {\n        content.style.maxHeight = null;\n      } else {\n        content.style.maxHeight = content.scrollHeight + "px";\n      }\n    });\n  }'
newHTMLFile.write(content)


content = '\n   var navList = document.getElementById("nav-lists");\n\n   function Show() {\n     navList.classList.add("_Menus-show");\n   }'
newHTMLFile.write(content)

content = '\n\n   function Hide() {\n     navList.classList.remove("_Menus-show");\n   }\n </script>'
newHTMLFile.write(content)

content = '\n<script type="text/javascript" src="%sexplore_function.js"></script>' % navigating
newHTMLFile.write(content)

newHTMLFile.close()

# FOR UPDATING AUTHOR PAGE
author_html = "../author/" + author_path + ".html"
relative_path_to_article = "../" + article_path[27:] + article_filename
relative_path_to_image =  "../" + article_path[27:] + "images/" + cover_image
subtitle = article_genre + ", " + date
a_file = open(author_html, "r")
list_of_lines = a_file.readlines()
print("line 56", list_of_lines[56])
print(len(list_of_lines))

new_article_text = "\n        <div class='individual_article' style='order: 0;'>\n          <div class='article_hover' id='article_pic'>\n            <a href=%s>\n              <img class='individualPhoto' src=%s>\n            </a>\n          </div>\n          <div class='div_for_aligning'>\n            <a style='text-decoration: none; color: rgb(56, 86, 35);' href=%s>\n              <p class='article_title_left' style='margin-top:1.5vw;'> %s</p>\n            </a>\n            <p class='article_sub_title_left'> %s</p>\n            <p class='about_article_text_left'>\n %s \n            </p>\n          </div>\n        </div>\n\n" % (relative_path_to_article, relative_path_to_image, relative_path_to_article, article_title, subtitle, prelude)

new_article_text_phone = "\n        <div class='sub_article' id='main_article_phone' style=%s>\n          <a href=%s style='text-decoration:none;'>\n            <img class='sub_article_img' src=%s>\n            <p class='sub_article_text'> %s</p>\n            <p class='sub_article_text2'> %s </p>\n          </a>\n        </div>\n" % ('margin-top:0%', relative_path_to_article, relative_path_to_image, article_title, article_genre)

print(list_of_lines)
counter = 0
order_counter = 0

for line in list_of_lines:
    if ' <div class="articles" id="author_results_screen">' in line:
        list_of_lines[counter + 1] = new_article_text
        order_counter += 1
    elif '<div class="individual_article"' in line:
        list_of_lines[counter] = '        <div class="individual_article" style=" order:' + str(order_counter) + '; ">\n'
        if (order_counter % 2) == 0: # even
            print(order_counter)
            offset = 1
            curr_line = list_of_lines[counter + offset]

            while '<div class="article_hover" id="article_pic">' not in curr_line:
                offset += 1
                curr_line = list_of_lines[counter + offset]

            print("OFFSET = ", offset)
            print("CURR LINE", curr_line)
            placeholder_text = list_of_lines[counter + 1: counter + offset]
            print(placeholder_text)

            placeholder_img = list_of_lines[counter + offset: counter + offset + 5]
            print(placeholder_img)

            img_string = ''.join([str(item) for item in placeholder_img])
            print(img_string)
            text_string = ''.join([str(item) for item in placeholder_text])
            print(text_string)

            text_string = text_string.replace("right", "left")

            final_string = img_string + text_string

            num = counter + 5 + offset - counter - 1


            print(final_string)
            print("NUMBER ugh", counter + offset + 6)
            list_of_lines[counter + 1 : counter + offset + 5] = final_string

            # list_of_lines[counter + 1: counter + 5] = img_string
            # list_of_lines[counter + 5: counter + 5 + offset] = text_string

        else: #odd
            placeholder_img = list_of_lines[counter + 1: counter + 6]

            offset = 1
            curr_line = list_of_lines[counter + 5 + offset]

            while '<div class="individual_article"' not in curr_line and '<div id="author_results_phone">' not in curr_line:
                offset += 1
                curr_line = list_of_lines[counter + 5 + offset]

            placeholder_text = list_of_lines[counter + 6: counter + 5 + offset - 2]

            img_string = ''.join([str(item) for item in placeholder_img])
            text_string = ''.join([str(item) for item in placeholder_text])

            text_string = text_string.replace("left", "right")

            final_string = text_string + img_string
            print("final string", final_string)

            num = counter + 5 + offset - 2 - counter - 6
            print(num)
            print(counter)

            list_of_lines[counter + 1 : counter + num + 5 + 1] = final_string


        order_counter += 1
    if '<div id="author_results_phone">' in line:
        print("WAHOOO there")
        list_of_lines[counter + 1] = new_article_text_phone
    counter += 1


a_file = open(author_html, "w")
a_file.writelines(list_of_lines)
a_file.close()
