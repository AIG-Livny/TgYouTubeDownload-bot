import pytube
import requests
import telebot
import sys
import xml.etree.ElementTree as ET
from telebot import types,util

# Check existance
def url_check(url):
    get = requests.get(url)
    if get.status_code == 200:
        return True
    else:
        return False

# YouTube subscripts "timedtext3" format to .srt converter
def timedtext3_to_srt(xmlfilepath:str, outfilepath:str):
    def formatSrtTime(milliseconds):
        sec, milli = divmod(milliseconds, 1000)
        m, s = divmod(int(sec), 60)
        h, m = divmod(m, 60)
        return "{:02}:{:02}:{:02},{}".format(h,m,s,milli)

    i = 1
    fout = open(outfilepath, "w+", encoding='utf-8')
    for p in ET.ElementTree(file=xmlfilepath).getroot().find("body").findall('p'):
        if ('t' in p.attrib.keys()) and ('d' in p.attrib.keys()):
            time = int(p.attrib['t'])
            duration = int(p.attrib['d'])
            line = ''
            if p.text:
                line += p.text
            else:
                for s in p.findall('s'):
                    line += s.text
            if line:
                srtline = f"{i}\n{formatSrtTime(time)} --> {formatSrtTime(time + duration)}\n{line}\n\n"
                i+=1
                fout.write(srtline)
    fout.close()

bot = telebot.TeleBot(sys.argv[2])
ytsavedir = sys.argv[1]

@bot.message_handler(content_types=["text"])
def handle_text(mes : telebot.types.Message):
    def download_video(video):
        bot.send_chat_action(mes.chat.id, 'typing')
        streams = video.streams.order_by('resolution').filter(file_extension='mp4',only_video=False)
        for stream in reversed(streams):
            acod = 'none'
            vcod = stream.codecs[0]
            try:
                acod = stream.codecs[1]
            except:
                acod = 'none'

            # Only resolution 720p and lower!
            if stream.resolution in ['720p','480p','360p','240p','144p']:
                if acod != 'none':
                    vid = video.streams.get_by_itag(stream.itag)
                    bot.send_message(mes.chat.id, f"Started {stream.default_filename}\nResolution: {stream.resolution}")
                    vid.download(ytsavedir)
                    def write_caption(code = 'en'):
                        if code in video.captions.keys():
                           nam = ytsavedir + stream.default_filename
                           namo = nam+f"{code}.xml"
                           namn = nam+f"{code}.srt"
                           f = open(namo,"w+",encoding="utf-8")
                           f.write(video.captions[code].xml_captions)
                           f.close()
                           timedtext3_to_srt(namo,namn)

                           return True
                        else:
                           return False
                    # Here you can add any other languages
                    # a.en - mean automatic created.
                    if not write_caption('en'):
                        write_caption('a.en')
                    
                    
                    bot.send_message(mes.chat.id, f"Done {stream.default_filename}")
                    break

    if url_check(mes.text):
       if 'playlist' in mes.text:
           for video in pytube.Playlist(mes.text).videos:
               download_video(video)
           bot.send_message(mes.chat.id, f"List done")
       else:
           download_video(pytube.YouTube(mes.text))

def main():
    bot.infinity_polling(allowed_updates=util.update_types)
    
if __name__ == "__main__":
    main()