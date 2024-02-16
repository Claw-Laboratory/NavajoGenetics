import pandas as pd
import re
from collections import Counter, defaultdict
pd.set_option('future.no_silent_downcasting', True) # FutureWarning: Downcasting behavior in `replace` is deprecated and will be removed in a future version. To retain the old behavior, explicitly call `result.infer_objects(copy=False)`. To opt-in to the future behavior, set `pd.set_option('future.no_silent_downcasting', True)`
######################
# METHOD DECLARATION #
######################
def add_to_dataframe(df1):
    columns = ["Num", "Title", "CodesApplied", "LinkedMemos", "ExcerptRange", "ExcerptText"]
    df2 = pd.DataFrame(columns=columns)
    tempCodes1 = ''
    tempCodes2 = ''
    tempCodes3 = ''
    tempMemos1 = ''
    tempMemos2 = ''
    tempMemos3 = '' 
    tempRange1 = ''
    tempRange2 =''
    tempRange3 = ''
    tempExcerpt1 = ''
    tempExcerpt2 =''
    for index, row in df1.iterrows():
        textSnippet = row['Text']  #df1[index] #row['Text']
        if textSnippet is None:
            print("Empty row ignored")
            continue  # Skip if textSnippet is None
        match1 = re.search('(ID .*?final.doc)', str(textSnippet))
        data_dict = {
            "Num": index,
            "Title": match1.group() if match1 else '',
            "CodesApplied": '',#re.search('(Codes Applied:.*?\n)', str(textSnippet)).group() if re.search('(Codes Applied:.*?\n)', str(textSnippet)) else '',
            "LinkedMemos": '',# if re.search('(Linked Memos:.*?\n)', str(textSnippet)) else '',
            "ExcerptRange": '',
            "ExcerptText": ''
        }
        lines = textSnippet.split('\n')
        combined_text = '\n'.join(lines[4:])
        pattern = re.compile(r'(.*)(?=\Z)', re.DOTALL)
        match4 = pattern.search(combined_text)
        if match4:
            tempExcerpt1 = match4.group(1)
            excerpt_exists = df2['ExcerptText'].isin([tempExcerpt1]).any()         # Check if 'tempExcerpt1' exists in the 'ExcerptText' column of df2
            if not (tempExcerpt1==''): # #look if this excerpt already exists in df
          #      print("????, ",tempExcerpt1[20:40])
  #          else:
                if excerpt_exists:
         #           print("!!! ",tempExcerpt1,"\talready in df")
                    excerpt_index = df2[df2['ExcerptText'] == tempExcerpt1].index
                    if not excerpt_index.empty:
                    #   print("test!")
                        tempMemos2= df2.loc[excerpt_index[0],"LinkedMemos"]  #
                        tempRange2= df2.loc[excerpt_index[0],"ExcerptRange"]#
                        tempCodes2 = df2.loc[excerpt_index[0],"CodesApplied"]
                        match7 = re.search("Excerpt Range:(.*?)\n", str(textSnippet))
                        if match7:
                            tempRange1 = match7.group(1)
            #              print("~~~~~~~~~~~~~~~~~~>",tempRange1,"\t",tempRange2)
                            if (tempRange1!=tempRange2): 
                            #        df2.loc[excerpt_index[0],"ExcerptRange"] = tempRange1
                            #   else:
                                cList_tempRanges = ([tempRange1]+[tempRange2])
                #                print("~~~~~~~~~ ++++ ~~~~~~~~~>",tempRange1,"\t",tempRange2,"\t",cList_tempRanges)
                                fList_tempRanges = [item for tempRange in cList_tempRanges for item in tempRange]
                                uList_tempRanges = list(set(fList_tempRanges)) #set should only keep unique items in the list
                                tempRange3 = '\t'.join(uList_tempRanges)
                                print("\nRANGES 3: ",tempRange3,"\t1: ",tempRange1,"\t2: ",tempRange2)
                                df2.loc[excerpt_index[0],"ExcerptRange"] = tempRange3
                            else:
                                df2.loc[excerpt_index[0],"ExcerptRange"] = tempRange1
                            
                            match8 = re.search('Linked Memos:(.*?)\n', str(textSnippet))
                            if match8:
                                tempMemos1 = match8.group(1)
                                if (tempMemos1==tempMemos2):
                                    pass
                                        #data_dict["LinkedMemos"]=tempMemos1
                                else:
                                    tempMemos3 = max(tempMemos1,tempMemos2)
                                    df2.loc[excerpt_index[0],"LinkedMemos"] = tempMemos3
                                    
                                    uList_codes = list(set(this_codeList2))
                                    tempCode_str = '\t'.join(uList_codes)
                                    data_dict["CodesApplied"] = tempCode_str
                            else:
                                continue

                            pattern2 = r'(Codes Applied:(.*?))\n'
                            match3 = re.search(pattern2, str(textSnippet))
                            if match3:
                                theseCodes = match3.group(2)
                                this_codeList = theseCodes.split('\t') #break up string by \t, gives list of codes:  -->  [' ', 'Data Sharing', 'Appropriate research']
                                if (this_codeList==''):
                                    pass
                                else:
                                    tempCodes1 = this_codeList
                                    tempCodes2 = tempCodes2.split('\t')
                                    combined_list = ([tempCodes1]+[tempCodes2])#concat(tempCodes1,tempCodes2)
                                    flattened_list = [item for tempCodes in combined_list for item in tempCodes]    # Flatten the combined list if there are nested lists
                                    unique_list = list(set(flattened_list))            # Remove duplicate codes by converting the list to a set and then back to a list
                                    tempCodes3 = '\t'.join(unique_list)
                                    df2.loc[excerpt_index[0],"CodesApplied"] = tempCodes3
                            else:
                                continue
                        else:
                            print("Mismatched Excerpt to what's in DF already")
                            pass   
                    else:
                        pass

                    tempRange1 ='' #reset temp variables
                    tempRange2 =''
                    tempRange3 = ''
                    tempMemos1 =''
                    tempMemos2 =''
                    tempMemos3 =''
                    tempCodes1 = ''
                    tempCodes2 = ''
                    tempCodes3 = ''
                else:  #excerpt not in df yet
                    data_dict["ExcerptText"] = tempExcerpt1
                    pattern2 = r'(Codes Applied:(.*?))\n'
                    match9 = re.search(pattern2, str(textSnippet))
                    if match9:
                        theseCodes2 = match9.group(2)
                        this_codeList2 = theseCodes2.split('\t') #break up string by \t, gives list of codes:  -->  [' ', 'Data Sharing', 'Appropriate research']
                        if (this_codeList2==''):
                            print("codes not found with RegEx ",this_codeList2)
                        else:
                            uList_codes = list(set(this_codeList2))
                            tempCode_str = '\t'.join(uList_codes)
                            data_dict["CodesApplied"] = tempCode_str
                    match5=re.search('Linked Memos:(.*?)\n', str(textSnippet))
                    if match5:
                        data_dict["LinkedMemos"] = match5.group(1)
                    else:
                        pass

                    match6 =re.search("Excerpt Range:(.*?)\n", str(textSnippet))
                    if match6:
                        data_dict["ExcerptRange"] = match6.group(1)
                    else:
                        pass
            else:
                print("\n",textSnippet)
                pass
        else:
            data_dict["ExcerptText"] = "NotMatched"
        df2 = df2._append(data_dict, ignore_index=True)
    return df2

def removeDupExcerpts(orig_df):
    orig_df = orig_df.replace({"Õ":"'", "Ô": " ", "É":" ", "Ð":"",}, regex=True)
    orig_df['middlePortion'] = orig_df["ExcerptText"].str.slice(30, 60)  # Extract the middle portion of the ExcerptText
    unique_df = orig_df.drop_duplicates(subset='middlePortion', keep='first')
    print(unique_df.head(10))
    return unique_df


def writeOutputFile(output_file, orig_dfData, uniq_dfData):
    with open(output_file, 'a', encoding='UTF-8') as f:
        for i, row in uniq_dfData.iterrows():
            if(row["ExcerptText"]==''):
                pass
            else:
                f.write("\nTitle: ")
                f.write(row["Title"])
                f.write("\nCodes Applied:\t")
                f.write(row["CodesApplied"])
                f.write("\nLinked Memos:\t")
                f.write(row["LinkedMemos"])
                f.write("\nExcerpt Range:\t")
                f.write(row["ExcerptRange"])
                f.write("\n")
                f.write(row["ExcerptText"])
                f.write("\n\n")
    print(f"Successfully generated output file: '{output_file}', containing {uniq_dfData.shape[0]} excerpts, after removing {len(orig_dfData)-len(uniq_dfData)} number of duplicates from the original {len(orig_dfData)} excerpts.")

########
# MAIN #
########
def main(input_file, output_file):
    df = pd.DataFrame()
    with open(input_file, 'r',encoding='latin-1') as file: #,encoding='ISO-8859-1'
        content = file.read()
        sections = content.split("Title: ") # Split the content by "Title: "
        df = df._append(pd.DataFrame(sections,columns=["Text"]))
    df_fileData2 = add_to_dataframe(df)
    print(f"length of original data set was ")
    df_uniqExcerpts = removeDupExcerpts(df_fileData2)
    writeOutputFile(output_file,df,df_uniqExcerpts)

if __name__ == "__main__":
    input_fileName = "Inappropriate Research_2023_12_8.txt"
    output_suffix = "_dupsRemoved02162024crm.txt"
    output_fileName = input_fileName.replace(".txt", output_suffix)
    main(input_fileName, output_fileName)

