import pandas as pd
import speech_recognition as sr
import pyttsx3
from datetime import date, timedelta
import re
#FUNCTIONS START
def recognize_audio(engine):
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[0].id)
    # print(voices[0].id)
    engine.setProperty('rate', 150)
    r = sr.Recognizer()
    engine.say("PLEASE ASK ANY OF THE FOLLOWING")
    engine.runAndWait()
    print("SERIAL NUMBER")
    print("BOOK NAME")
    print("AUTHOR")
    print("RETURN BOOK")
    with sr.Microphone()as source:
        engine.say("CHOOSE YOUR OPTION")
        engine.runAndWait()
        choice_audio1 = r.listen(source)
        try:
            choice1 = r.recognize_google(choice_audio1)
            print('YOU SAID:{}'.format(choice1))
        except:
            error(engine)
    x = sr.Recognizer()
    with sr.Microphone()as source:
        engine.say('PLEASE SAY THE CORRECT ' + choice1)
        engine.runAndWait()
        print('PLEASE SAY THE CORRECT ' + choice1)
        choice_audio2 = x.listen(source)
        try:
            choice2 = x.recognize_google(choice_audio2)
            print('YOU SAID:{}'.format(choice2))
        except:
            error(engine)
    return choice1,choice2
def request_a_book(engine,data,index_position):
    position = data.loc[index_position[0], 'position']
    status = data.loc[index_position[0], 'status']
    if status == 1:
        engine.say("BOOK  IS AVAILABLE")
        engine.runAndWait()
        print("BOOK  IS AVAILABLE")
        print('DO YOU WANT THIS BOOK')
        engine.say('DO YOU WANT THIS BOOK')
        engine.runAndWait()
        m = sr.Recognizer()
        with sr.Microphone()as source:
            engine.say('SAY YES OR NO')
            engine.runAndWait()
            print('SAY YES OR NO  ')
            audio2 = m.listen(source)
            try:
                response = m.recognize_google(audio2)
                print('YOU SAID:{}'.format(response))
            except:
                error(engine)
            if (response == 'yes'):
                m = sr.Recognizer()
                with sr.Microphone()as source:
                    engine.say('PLEASE SAY YOUR LIBRARY PASS ID')
                    engine.runAndWait()
                    print('PLEASE SAY YOUR LIBRARY PASS ID')
                    audio4 = m.listen(source)
                    try:
                        student_ID = m.recognize_google(audio4)
                        print('YOU SAID:{}'.format(student_ID))
                        print('THE BOOK IS IN THE ROW '+ position)
                        engine.say('THE BOOK IS IN THE ROW '+ position)
                        print("THE BOOK IS RETURN AFTER 15 DAYS")
                        engine.say("THE BOOK IS RETURN AFTER 15 DAYS")
                    except:
                        error(engine)
        current_date= date.today().isoformat()
        return_date = (date.today() + timedelta(days=15)).isoformat()
        count =data.loc[index_position[0],'count']
        count -= 1
        if count <= 0:
            data.loc[index_position[0], 'count'] = count
            data.loc[index_position[0], 'status'] = 0
        else:
            data.loc[index_position[0], 'count'] = count
        student_IDS = data.loc[index_position[0], 'student_ID']
        #print(type(student_IDS))
        data.loc[index_position[0],'student_ID'] =student_ID+','+str(student_IDS)
        data.loc[index_position[0],'timedate'] = current_date
        data.loc[index_position[0],'retimedate'] =return_date
        engine.say('THE BOOK IS RETURN' + return_date)
        engine.say('THANK YOU')
        print('THE BOOK IS RETURN' +return_date)
        print('THANK YOU')
        engine.runAndWait()
    else:
        engine.say("BOOK  IS NOT AVALIBLE")
        engine.runAndWait()
        print("BOOK  IS  NOT AVALIBLE")
        engine.say("THANK YOU")
        engine.runAndWait()
        print("THANK YOU")
    return data
def write_csv(data):
    data.to_csv('speech_dataset.csv', index=False) #data set save
    return None
def error(engine):
    print('SORRY..I CANT HEAR YOUR VOICE')
    engine.say("SORRY..I CANT HEAR YOUR VOICE")
    engine.runAndWait()
    return recognize_audio(engine)
#FUNCTIONS END

#MAIN STARTS
if __name__ == "__main__":
    engine = pyttsx3.init()
    first_choice,second_choice = recognize_audio(engine)
    #print('second_choice',second_choice)
    #print('first_choice', first_choice)
    s_second_choice = str(second_choice)
    s_first_choice = str(first_choice)
    data = pd.read_csv('speech_dataset.csv')
    if s_first_choice:
        if s_first_choice == "return book":
            index_position = data.index[data["book name"] ==s_second_choice].tolist()
            m = sr.Recognizer()
            if index_position:
                with sr.Microphone()as source:
                    engine.say('PLEASE SAY YOUR LIBRARY PASS ID')
                    engine.runAndWait()
                    print('PLEASE SAY YOUR LIBRARY PASS ID')
                    audio4 = m.listen(source)
                    try:
                        student_ID = m.recognize_google(audio4)
                        print('YOU SAID:{}'.format(student_ID))
                    except:
                        error(engine)
                count = data.loc[index_position[0],'count']
                count += 1
                status = data.loc[index_position[0],'status']
                if status == 0:
                    #print(status)
                    data.loc[index_position[0],'count'] = count
                    data.loc[index_position[0],'status'] = 1
                    write_csv(data)
                else:
                    data.loc[index_position[0], 'count'] = count
                    write_csv(data)

                student_IDS = data.loc[index_position[0], 'student_ID']
                data.loc[index_position[0],'student_ID'] =re.sub(student_ID,' ',student_IDS)
                current_date = date.today().isoformat()
                data.loc[index_position[0],'timedate'] = current_date
                #data.loc[index_position[0], 'retimedate'] = ''
                write_csv(data)
                replace_book_position = data.loc[index_position[0], 'position']
                engine.say('PLEASE RETURN BOOK  IN THE ROW' + replace_book_position)
                engine.say('THANK YOU')
                print('PLEASE RETURN BOOK  IN THE ROW ' + replace_book_position)
                print('THANK YOU')
                engine.runAndWait()
            else:
                print('CHOOSE THE CORRECT OPTION')
                engine.say('CHOOSE THE CORRECT OPTION')
                engine.runAndWait()
                #do code CHOOSE CORRECT
        else:
            if s_first_choice == "serial number":
                index_position = data.index[data[s_first_choice] == int(s_second_choice)].tolist()
                s_second_choice=int(s_second_choice)
                data = request_a_book(engine,data,index_position)
                write_csv(data)
            elif s_first_choice == "book name":
                index_position = data.index[data[s_first_choice] == s_second_choice].tolist()
                data = request_a_book(engine, data, index_position)
                write_csv(data)
            elif s_first_choice == "author":
                index_position = data.index[data[s_first_choice] == s_second_choice].tolist()
                data = request_a_book(engine, data, index_position)
                write_csv(data)
            else:
                print('CHOOSE THE CORRECT OPTION')
                engine.say('CHOOSE THE CORRECT OPTION')
                engine.runAndWait()

    else:
        print('CHOOSE THE CORRECT OPTION')
        engine.say('CHOOSE THE CORRECT OPTION')
        engine.runAndWait()
