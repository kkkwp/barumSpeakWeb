#!/usr/bin/env python
# coding: utf-8

# Copyright (c) Microsoft. All rights reserved.
# Licensed under the MIT license. See LICENSE.md file in the project root for full license information.

"""
Speech recognition samples for the Microsoft Cognitive Services Speech SDK
"""
import string
import time
import wave
import os


upload_dir = '/home/ivpl-d04/Web/module/console/'

'''
samples = OrderedDict([
    (speech_sample, [
        speech_sample.pronunciation_assessment_from_microphone,
        speech_sample.pronunciation_assessment_continuous_from_file,
    ])
])
'''


# ---  start SDK  ---
try:
    import azure.cognitiveservices.speech as speechsdk
except ImportError:
    print("""
    Importing the Speech SDK for Python failed.
    Refer to
    https://docs.microsoft.com/azure/cognitive-services/speech-service/quickstart-python for
    installation instructions.
    """)
    import sys
    sys.exit(1)

# Set up the subscription info for the Speech Service:
# Replace with your own subscription key and service region (e.g., "westus").
speech_key, service_region = "d2aaa9e263c14f1ea5d1697f4a8f0d77", "eastus"

# Specify the path to an audio file containing speech (mono WAV / PCM with a sampling rate of 16
# kHz).
# weatherfilename = "whatstheweatherlike.wav"
# weatherfilenamemp3 = "whatstheweatherlike.mp3"

dir = "/var/www/html/barum/module/console/"
# ---  set 'weatherfilename'  ---
def audio():
    audiofiles = os.listdir(upload_dir)
    audiofiles_mp4 = [file for file in audiofiles if file.endswith(".wav")]
    audiofiles_mp4.sort()
    if len(audiofiles_mp4) != 0:
        try:
            weatherfilename = str(audiofiles_mp4[-1])
        except:
            print("Try Except Error")
            pass
    print(weatherfilename)
    return weatherfilename

weatherfilename = dir+audio()
# weatherfilename = "myVoiceIsMyPassportVerifyMe01.wav"

scores = []

# --- call pronunciation_assessment_continuous_from_file() with question_num
def select(question_num):
    '''
    modules = list(samples.keys())
    
    try:
        selected_module = modules[0]
    except EOFError:
        raise
    except Exception as e:
        print(e)
        return

    print('select sample function, {} to abort'.format(eofkey))
    for i, fun in enumerate(samples[selected_module]):
        print("{}: {}\n\t{}".format(i, fun.__name__, fun.__doc__))
    
    try:
        num = 1
        selected_function = samples[selected_module][num]
    except EOFError:
        raise
    except Exception as e:
        print(e)
        return

    # print('You selected: {}'.format(selected_function))
    '''

    try:
        pronunciation_assessment_continuous_from_file(question_num)
    except Exception as e:
        print('Error running sample: {}'.format(e))

    print()

    return scores


# ---  assessment with question_num ---
def pronunciation_assessment_continuous_from_file(question_num):
    """performs continuous speech recognition asynchronously with input from an audio file"""

    import difflib
    import json

    # Creates an instance of a speech config with specified subscription key and service region.
    # Replace with your own subscription key and service region (e.g., "westus").
    # Note: The pronunciation assessment feature is currently only available on en-US language.
    speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region)
    audio_config = speechsdk.audio.AudioConfig(filename=weatherfilename)

    if question_num == 1:
        reference_text = "I have a fox."
    elif question_num == 2:
        reference_text = "I have a box."
    elif question_num == 3:
        reference_text = "I have a vase."
    else:
        reference_text = "My voice is my passport verify me."
            
    # create pronunciation assessment config, set grading system, granularity and if enable miscue based on your requirement.
    enable_miscue = True
    pronunciation_config = speechsdk.PronunciationAssessmentConfig(reference_text=reference_text,
                                                                   grading_system=speechsdk.PronunciationAssessmentGradingSystem.HundredMark,
                                                                   granularity=speechsdk.PronunciationAssessmentGranularity.Phoneme,
                                                                   enable_miscue=enable_miscue)

    # Creates a speech recognizer using a file as audio input.
    # The default language is "en-us".
    speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)
    # apply pronunciation assessment config to speech recognizer
    pronunciation_config.apply_to(speech_recognizer)

    done = False
    recognized_words = []
    accuracy_scores = []
    fluency_scores = []
    durations = []

    def stop_cb(evt):
        """callback that signals to stop continuous recognition upon receiving an event `evt`"""
        #print('CLOSING on {}'.format(evt))
        nonlocal done
        done = True


    def recognized(evt):
        print('pronunciation assessment for: {}'.format(evt.result.text))
        pronunciation_result = speechsdk.PronunciationAssessmentResult(evt.result)
        print('    Accuracy score: {}, pronunciation score: {}, completeness score : {}, fluency score: {}'.format(
            pronunciation_result.accuracy_score, pronunciation_result.pronunciation_score,
            pronunciation_result.completeness_score, pronunciation_result.fluency_score
        ))
        scores.append(pronunciation_result.accuracy_score)
        scores.append(pronunciation_result.pronunciation_score)
        scores.append(pronunciation_result.completeness_score)
        scores.append(pronunciation_result.fluency_score)
        nonlocal recognized_words, accuracy_scores, fluency_scores, durations
        recognized_words += pronunciation_result.words
        accuracy_scores.append(pronunciation_result.accuracy_score)
        fluency_scores.append(pronunciation_result.fluency_score)
        json_result = evt.result.properties.get(speechsdk.PropertyId.SpeechServiceResponse_JsonResult)
        jo = json.loads(json_result)
        nb = jo['NBest'][0]
        durations.append(sum([int(w['Duration']) for w in nb['Words']]))

    # Connect callbacks to the events fired by the speech recognizer
    speech_recognizer.recognized.connect(recognized)
    #speech_recognizer.session_started.connect(lambda evt: print('SESSION STARTED: {}'.format(evt)))
    #speech_recognizer.session_stopped.connect(lambda evt: print('SESSION STOPPED {}'.format(evt)))
    #speech_recognizer.canceled.connect(lambda evt: print('CANCELED {}'.format(evt)))
    # stop continuous recognition on either session stopped or canceled events
    speech_recognizer.session_stopped.connect(stop_cb)
    speech_recognizer.canceled.connect(stop_cb)

    # Start continuous pronunciation assessment
    speech_recognizer.start_continuous_recognition()
    while not done:
        time.sleep(.5)

    speech_recognizer.stop_continuous_recognition()

    # We can calculate whole accuracy and fluency scores by duration weighted averaging
    accuracy_score = sum(i[0] * i[1] for i in zip(accuracy_scores, durations)) / sum(durations)
    fluency_score = sum(i[0] * i[1] for i in zip(fluency_scores, durations)) / sum(durations)

    # we need to convert the reference text to lower case, and split to words, then remove the punctuations.
    reference_words = [w.strip(string.punctuation) for w in reference_text.lower().split()]

    # For continuous pronunciation assessment mode, the service won't return the words with `Insertion` or `Omission`
    # even if miscue is enabled.
    # We need to compare with the reference text after received all recognized words to get these error words.
    if enable_miscue:
        diff = difflib.SequenceMatcher(None, reference_words, [x.word for x in recognized_words])
        final_words = []
        for tag, i1, i2, j1, j2 in diff.get_opcodes():
            if tag == 'insert':
                for word in recognized_words[j1:j2]:
                    if word.error_type == 'None':
                        word._error_type = 'Insertion'
                    final_words.append(word)
            elif tag == 'delete':
                for word_text in reference_words[i1:i2]:
                    word = speechsdk.PronunciationAssessmentWordResult({
                        'Word': word_text,
                        'PronunciationAssessment': {
                            'ErrorType': 'Omission',
                        }
                    })
                    final_words.append(word)
            else:
                final_words += recognized_words[j1:j2]
    else:
        final_words = recognized_words

    # Calculate whole completeness score
    completeness_score = len([w for w in final_words if w.error_type == 'None']) / len(reference_words) * 100

    print('    Paragraph accuracy score: {}, completeness score: {}, fluency score: {}'.format(
        accuracy_score, completeness_score, fluency_score
    ))



    for idx, word in enumerate(final_words):
        print('    {}: word: {}\taccuracy score: {}\terror type: {};'.format(
            idx + 1, word.word, word.accuracy_score, word.error_type
        ))
