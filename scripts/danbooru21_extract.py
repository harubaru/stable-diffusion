## This script WAS NOT USED on the weights released by ProjectAI Touhou on 8th of september, 2022.
## This script CAN convert tags to human-readable-text BUT IT IS NOT REQUIRED.
import argparse
#Stolen code from https://stackoverflow.com/a/43357954 (troll face)
def str2bool(v):
    if isinstance(v, bool):
        return v
    if v.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif v.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected.')

## In the future someone might want to access this via import. Consider adding support for that
parser = argparse.ArgumentParser()
parser.add_argument('--jsonpath', '-J', type=str, help='Path to JSONL file with the metadata', required = True)
parser.add_argument('--extractpath', '-E', type=str, help='Path to the folder where to extract the images and text files', required = True)
parser.add_argument('--imagespath', '-I', type=str, help='Path to the folder with the images', required = False, default="512px")
parser.add_argument('--convtohuman', '-H', type=str2bool, help='Convert to human-readable-text', required = False, default=True)
args = parser.parse_args()
print("Arguments: " + str(args))

import json
import os
import shutil
if os.path.exists(args.extractpath) == False:
    os.mkdir(args.extractpath)

def writefile(filename, text):
    f = open(filename, "w")
    f.write(text)
    print('Saved the following: ' + text)
    f.close()
#Converts tags to T2I-like prompts (blue_dress, 1girl -> A blue dress, one girl)
def convert_tags_to_humantxt(convtohuman, input):
    tars = input
    if convtohuman == True:
        tars = tars.replace(' ', ', ')
        tars = tars.replace('_', ' ')
        tars = tars.replace('1girl', 'one girl')
        tars = tars.replace('2girls', 'two girls')
        tars = tars.replace('3girls', 'three girls')
        tars = tars.replace('4girls', 'four girls')
        tars = tars.replace('5girls', 'five girls')
        ##Implying it will ever be able to differentiate so many entities
        tars = tars.replace('6girls', 'six girls')

        #Almost forgot about boys tags... I wonder if theres also for other entities?
        tars = tars.replace('1boy', 'one boy')
        tars = tars.replace('2boys', 'two boys')
        tars = tars.replace('3boys', 'three boys')
        tars = tars.replace('4boys', 'four boys')
        tars = tars.replace('5boys', 'five boys')
        tars = tars.replace('6boys', 'six boys')
    elif convtohuman == False:
        print("convert_tags_to_humantxt: convtohuman is false hence not doing anything")
    print("FINAL TARS: " + tars)
    return tars

#Converts ratings to X content
def convert_rating_to_humanrating(convtohuman, input):
    if convtohuman == True:
        if input == "e":
            return "explicit content"
        if input == "g":
            return "general content"
        if input == "q":
            return "questionable content"
        if input == "s":
            return "sensitive content"
            ##This will be the start of everything unethical
    if convtohuman == False:
        if input == "e":
            return "explicit_content"
        if input == "g":
            return "general_content"
        if input == "q":
            return "questionable_content"
        if input == "s":
            return "sensitive_content"

# unrecog_ans = True
# while unrecog_ans:
#     inputans = input("Convert tags to human-readable-text? (smiley_face blue_hair -> smiley face, blue hair) [y/n]")
#     if inputans == "y":
#         convtohuman = True
#         unrecog_ans = False
#     elif inputans == "n":
#         convtohuman = False
#         unrecog_ans = False
#     else:
#         print("unrecognizable input. only y or n.")
#         unrecog_ans = True

convtohuman = args.convtohuman

##Open the file
json_file_path = args.jsonpath ##Name of the JSON file to use, converted into parser arg
with open(json_file_path, 'r', encoding="utf8") as json_file:
    json_list = list(json_file)

##Read line
current_saved_file_count = 0
current_line_count = 0
for json_str in json_list:
    current_line_count = current_line_count + 1
    ##415627 last line of 00.json, ignore
    ##TODO: Add a line counter to print progress accurately
    print("Current Line:" + str(current_line_count) + '/415000 (aprox) | Current saved files count: ' + str(current_saved_file_count) )
    #here, result = line
    result = json.loads(json_str)

    try:
        img_id = str(result['id'])
    except Exception:
        img_id = "nan"
        print("failed to get img_id")
        continue

    try:
        tmp_img_id = img_id[-3:]
        img_id_last3 = tmp_img_id.zfill(3)
    except Exception:
        img_id_last3 = "nan"
        print("failed to get img_id_last3")
        continue
    
    try:
        img_tags = result['tag_string']
    except Exception:
        img_tags = "none"
        print("failed to get img_tags")
        continue

    try:
        img_ext = result['file_ext']
    except Exception:
        print("failed to get img_ext")
        continue

    try:
        img_rating = result['rating']
    except Exception:
        print("failed to get img_rating")
        continue

    file_path =  str(args.imagespath) + "/0" + img_id_last3 + "/" + img_id + "." + img_ext
    if os.path.exists(file_path):
        shutil.copyfile(file_path, args.extractpath + '/' + img_id + "." + img_ext)
        humanoid_tags = convert_tags_to_humantxt(convtohuman, img_tags)
        humanoid_rating = convert_rating_to_humanrating(convtohuman, img_rating)
        if convtohuman == True:
            dan_iden = 'uploaded on danbooru'
            tag_separator = ', '
        elif convtohuman == False:
            dan_iden = 'danbooru'
            tag_separator = ' '
        to_write = humanoid_tags + tag_separator + humanoid_rating + tag_separator + dan_iden
        txt_name = args.extractpath +  "/" + img_id + '.txt'
        writefile(txt_name, to_write)
        current_saved_file_count = current_saved_file_count + 1

print("finished process. Your extracted data should be in " + args.extractpath + " !")
        

