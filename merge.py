import subprocess

def run_transparent():

    transparent_script = 'transparent.py'
    subprocess.Popen(['python', transparent_script])

def run_streamlit_app():

    streamlit_file = "assistant.py"
    command = ["streamlit", "run", streamlit_file]
    subprocess.run(command)

if __name__ == "__main__":

    run_transparent()
    run_streamlit_app()