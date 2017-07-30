from pytube import YouTube
from flask import Flask,redirect, url_for,render_template,request
import requests, random
requests.packages.urllib3.disable_warnings()
import ssl

app=Flask(__name__)

yt= None
rng = None
list = None
video = None

def fetch(url):
    global yt
    try:
        _create_unverified_https_context = ssl._create_unverified_context
    except AttributeError:
        # Legacy Python that doesn't verify HTTPS certificates by default
        pass
    else:
        # Handle target environment that doesn't support HTTPS verification
        ssl._create_default_https_context = _create_unverified_https_context

    try:
        yt = YouTube(url)
    except Exception:
        return -1
    else:
        return yt.get_videos()

@app.route('/')
def renderHomePage():
    return render_template("index.html")



@app.route('/work', methods=['POST','GET'])
def work():
    global list
    global rng
    if request.method == 'POST':
        url_dw = request.form['url']
        y='https://www.youtube.com/watch'
        if y in url_dw:
            list=fetch(url_dw)
            if list==-1:
                return render_template('index.html', eval=1)
            p=len(list)
            rng=[]
            for k in range(p):
                rng.append(k)
            return render_template('download.html', packet=zip(list,rng))
        else:
            return render_template('index.html',eval=1)


@app.route('/success')
def success():
    global video
    render_template('success.html')
    video.download("F:/Pytube downloads/")
    return redirect(url_for('renderHomePage'))


@app.route('/receive', methods=['POST','GET'])
def receive():
    global list
    global video
    global rng
    global yt
    try:
        choice = int(request.form['category'])
    except Exception:
        return render_template('download.html',packet=zip(list,rng),eval=1)
    else:
        video=list[choice]
        try:
            save_at=request.form['save_at']
            if save_at=='':
                return render_template('download.html',packet=zip(list,rng),eval=2)
            video.download(save_at)
        except Exception:
            num=str(random.randrange(1,10))
            nm=video.filename
            name=nm+num
            yt.set_filename(name)
            video.download(save_at)
            return render_template('success.html',vid=video,path=save_at)
        else:
            return render_template('success.html', vid=video,path=save_at)

if __name__== '__main__':
    app.run(debug='true')
