import re

def spaceline():
    textfile = "aaa.srt"                    #你要修改的字幕文件
    old_str = "\n"                          #被替换的换行符
    new_str = ""                            #将换行符取消
    new_data = ""

    input_name = textfile.split('.')                                    #以.作为分隔符，将文件名分隔开
    new_textfile = input_name[0] + ".srt"                               #读取要修改的字幕
    sec_textfile = input_name[0] + "_new.srt"                           #定义新的字幕文件名

    with open(new_textfile, "r", encoding="utf-8") as f:                #将字幕文件内的所有换行符都取消
        for line in f:
            line = line.replace(old_str,new_str)
        
            if re.search('[0-9][0-9]:[0-9][0-9]:[0-9][0-9],[0-9][0-9][0-9] --> [0-9][0-9]:[0-9][0-9]:[0-9][0-9],[0-9][0-9][0-9]', line):            #正则表达式匹配文件里的时间戳   
                line = '\n' + line                                      #在时间戳前加入换行符
                line = line + '\n'                                      #在时间戳后加入换行符
            elif re.search('^[0-9]+$', line):                           #正则表达式匹配纯数字行
                line = '\n\n' + line                                    #在纯数字行前加入两个换行符
            new_data += line
        #print(new_data)
    with open(sec_textfile,"w", encoding="utf-8") as f:                 #将修改过后的内容写入新的定义新的字幕文件内
        f.write(new_data)                               

if __name__ == '__main__':
    spaceline()
