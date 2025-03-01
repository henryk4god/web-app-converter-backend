import os
import subprocess
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def generate_apk(website_url):
    """
    Generate an APK from a website URL using apktool.
    
    Args:
        website_url (str): The URL of the website to convert to an APK.
    
    Returns:
        str: The path to the generated APK file.
    
    Raises:
        Exception: If APK generation fails.
    """
    output_apk = "web_app_converter.apk"
    command = f"apktool b input-folder -o {output_apk}"
    
    try:
        # Run the apktool command
        logging.info(f"Generating APK for website: {website_url}")
        result = subprocess.run(command, shell=True, capture_output=True, text=True)

        if result.returncode == 0:
            logging.info(f"APK generated successfully: {output_apk}")
            return output_apk
        else:
            # Log the error and raise an exception
            logging.error(f"APK generation failed: {result.stderr}")
            raise Exception(f"APK Generation Failed: {result.stderr}")
    except Exception as e:
        logging.error(f"Error during APK generation: {e}")
        raise Exception(f"APK Generation Failed: {e}")

def sign_apk(apk_path):
    """
    Sign an APK using jarsigner.
    
    Args:
        apk_path (str): The path to the APK file to sign.
    
    Returns:
        str: The path to the signed APK file.
    
    Raises:
        Exception: If signing fails or required environment variables are missing.
    """
    # Check if required environment variables are set
    keystore = os.getenv("KEYSTORE_PATH")
    alias = os.getenv("KEYSTORE_ALIAS")
    keystore_pass = os.getenv("KEYSTORE_PASSWORD")
    key_pass = os.getenv("KEY_PASSWORD")

    if not all([keystore, alias, keystore_pass, key_pass]):
        error_msg = "Missing required environment variables for signing. Ensure KEYSTORE_PATH, KEYSTORE_ALIAS, KEYSTORE_PASSWORD, and KEY_PASSWORD are set."
        logging.error(error_msg)
        raise Exception(error_msg)

    signed_apk = "signed_app.aab"
    command = (
        f"jarsigner -verbose -sigalg SHA1withRSA -digestalg SHA1 "
        f"-keystore {keystore} -storepass {keystore_pass} "
        f"-keypass {key_pass} {apk_path} {alias}"
    )

    try:
        # Run the jarsigner command
        logging.info(f"Signing APK: {apk_path}")
        result = subprocess.run(command, shell=True, capture_output=True, text=True)

        if result.returncode == 0:
            logging.info(f"APK signed successfully: {signed_apk}")
            return signed_apk
        else:
            # Log the error and raise an exception
            logging.error(f"APK signing failed: {result.stderr}")
            raise Exception(f"Signing Failed: {result.stderr}")
    except Exception as e:
        logging.error(f"Error during APK signing: {e}")
        raise Exception(f"Signing Failed: {e}")