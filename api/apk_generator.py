import os
import subprocess

def generate_apk(website_url):
    output_apk = "web_app_converter.apk"
    command = f"apktool b input-folder -o {output_apk}"
    
    result = subprocess.run(command, shell=True, capture_output=True, text=True)

    if result.returncode == 0:
        return output_apk
    else:
        raise Exception(f"APK Generation Failed: {result.stderr}")

def sign_apk(apk_path):
    signed_apk = "signed_app.aab"
    keystore = os.getenv("KEYSTORE_PATH")
    alias = os.getenv("KEYSTORE_ALIAS")
    keystore_pass = os.getenv("KEYSTORE_PASSWORD")
    key_pass = os.getenv("KEY_PASSWORD")

    command = f"jarsigner -verbose -sigalg SHA1withRSA -digestalg SHA1 -keystore {keystore} -storepass {keystore_pass} -keypass {key_pass} {apk_path} {alias}"
    
    result = subprocess.run(command, shell=True, capture_output=True, text=True)

    if result.returncode == 0:
        return signed_apk
    else:
        raise Exception(f"Signing Failed: {result.stderr}")
